#!/usr/bin/env node
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { mkdtemp, readFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { existsSync } from 'node:fs';
import { z } from 'zod';

const execFileAsync = promisify(execFile);
const SERVER_DIR = resolve(fileURLToPath(new URL('.', import.meta.url)));
const PACKAGE_ROOT = resolve(SERVER_DIR, '..');
const BUNDLED_PYTHONPATH = join(PACKAGE_ROOT, 'python');
const REPO_PYTHONPATH = join(PACKAGE_ROOT, '..', 'src');
const hasBundledPython = existsSync(join(BUNDLED_PYTHONPATH, 'dayi_core'));
const PYTHON_BIN = process.env.DAYI_PYTHON_BIN ?? 'python3';
const DEFAULT_PYTHONPATH = hasBundledPython ? BUNDLED_PYTHONPATH : REPO_PYTHONPATH;
const DEFAULT_PYTHON_CWD = hasBundledPython ? PACKAGE_ROOT : resolve(PACKAGE_ROOT, '..');
const PYTHON_CWD = process.env.DAYI_PYTHON_CWD ?? DEFAULT_PYTHON_CWD;

const QUERY_TYPES = ['medical', 'disease', 'doctor', 'symptom'] as const;
type QueryType = (typeof QUERY_TYPES)[number];
const EXPOSE_TYPED_TOOLS = process.env.DAYI_EXPOSE_TYPED_TOOLS === '1';

function inferQueryType(input: string): QueryType {
  const text = input.toLowerCase();
  if (/(医生|主任|副主任|主治|医师|出诊|门诊|专家|doctor)/i.test(text)) return 'doctor';
  if (/(症状|疼痛|发热|咳嗽|腹痛|symptom)/i.test(text)) return 'symptom';
  if (/(疾病|癌|炎|综合征|病|disease)/i.test(text)) return 'disease';
  return 'medical';
}

async function runDayiQuery(type: QueryType, keyword: string) {
  const tempDir = await mkdtemp(join(tmpdir(), 'dayi-mcp-'));
  const jsonPath = join(tempDir, 'result.json');

  try {
    const args = [
      '-m',
      'dayi_core.cli.main',
      'query',
      '--type',
      type,
      '--keyword',
      keyword,
      '--json',
      jsonPath,
    ];

    const env = { ...process.env } as NodeJS.ProcessEnv;
    if (process.env.DAYI_PYTHONPATH?.trim()) {
      env.PYTHONPATH = process.env.DAYI_PYTHONPATH;
    } else if (!process.env.PYTHONPATH?.trim()) {
      env.PYTHONPATH = DEFAULT_PYTHONPATH;
    }

    const { stdout, stderr } = await execFileAsync(PYTHON_BIN, args, {
      cwd: PYTHON_CWD,
      env,
      maxBuffer: 1024 * 1024 * 4,
    });

    const raw = await readFile(jsonPath, 'utf-8');
    const result = JSON.parse(raw);
    return {
      result,
      stdout: stdout.trim(),
      stderr: stderr.trim(),
    };
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    throw new Error(`调用 Python Core 失败: ${message}`);
  } finally {
    await rm(tempDir, { recursive: true, force: true });
  }
}

function buildTextSummary(result: any, stdout: string) {
  const title = result?.record?.title ?? result?.search?.selected_name ?? '未知';
  const queryType = result?.query_type ?? 'unknown';
  const detailUrl = result?.detail?.detail_url ?? '';
  const detailApi = result?.detail?.detail_api ?? '';

  return [
    `类型: ${queryType}`,
    `标题: ${title}`,
    detailUrl ? `详情页: ${detailUrl}` : '',
    detailApi ? `详情接口: ${detailApi}` : '',
    stdout ? `摘要:\n${stdout}` : '',
  ]
    .filter(Boolean)
    .join('\n');
}

function flattenEntries(obj: unknown, prefix = ''): Array<{ key: string; value: string }> {
  if (obj == null) return [];
  if (typeof obj !== 'object') return prefix ? [{ key: prefix, value: String(obj) }] : [];
  const out: Array<{ key: string; value: string }> = [];
  for (const [k, v] of Object.entries(obj as Record<string, unknown>)) {
    const nextKey = prefix ? `${prefix}.${k}` : k;
    if (v == null || v === '') continue;
    if (typeof v === 'object' && !Array.isArray(v)) {
      out.push(...flattenEntries(v, nextKey));
    } else if (Array.isArray(v)) {
      if (v.length) out.push({ key: nextKey, value: v.map(String).join(' | ') });
    } else {
      out.push({ key: nextKey, value: String(v) });
    }
  }
  return out;
}

function buildMedicalFullText(result: any, stdout: string) {
  const header = buildTextSummary(result, stdout);
  const record = result?.record ?? {};
  const entries = flattenEntries({
    overview: record?.overview ?? {},
    sections: record?.sections ?? {},
    attributes: record?.attributes ?? {},
  });
  const body = entries.length
    ? entries.map((x) => `${x.key}: ${x.value}`).join('\n')
    : JSON.stringify(result, null, 2);
  return `${header}\n\n完整提取内容:\n${body}`.trim();
}

const server = new McpServer({
  name: 'dayi-mcp-server',
  version: '0.1.0',
});

async function executeQuery(type: QueryType, keyword: string) {
  const { result, stdout } = await runDayiQuery(type, keyword);
  const text = type === 'medical' ? buildMedicalFullText(result, stdout) : buildTextSummary(result, stdout);
  return {
    content: [
      {
        type: 'text' as const,
        text,
      },
    ],
    structuredContent: result,
  };
}

function registerTypedQueryTool(type: QueryType) {
  server.tool(
    `dayi_query_${type}`,
    {
      keyword: z.string().min(1),
    },
    async ({ keyword }) => executeQuery(type, keyword),
  );
}

server.tool(
  'dayi_query',
  {
    type: z.enum(QUERY_TYPES),
    keyword: z.string().min(1),
  },
  async ({ type, keyword }) => executeQuery(type, keyword),
);

server.tool(
  'dayi_query_auto',
  {
    keyword: z.string().min(1),
    type_hint: z.enum(QUERY_TYPES).optional(),
  },
  async ({ keyword, type_hint }) => {
    const decidedType = type_hint ?? inferQueryType(keyword);
    const payload = await executeQuery(decidedType, keyword);
    return {
      ...payload,
      content: [
        {
          type: 'text' as const,
          text: `自动判定类型: ${decidedType}\n${payload.content[0]?.text ?? ''}`.trim(),
        },
      ],
    };
  },
);

if (EXPOSE_TYPED_TOOLS) {
  for (const type of QUERY_TYPES) {
    registerTypedQueryTool(type);
  }
}

const transport = new StdioServerTransport();
await server.connect(transport);
