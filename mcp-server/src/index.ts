import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { mkdtemp, readFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { z } from 'zod';

const execFileAsync = promisify(execFile);
const SERVER_DIR = resolve(fileURLToPath(new URL('.', import.meta.url)));
const REPO_ROOT = resolve(SERVER_DIR, '..', '..');
const PYTHONPATH = join(REPO_ROOT, 'src');
const PYTHON_BIN = process.env.DAYI_PYTHON_BIN ?? 'python3';

type QueryType = 'medical' | 'disease' | 'doctor' | 'symptom';

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

    const { stdout, stderr } = await execFileAsync(PYTHON_BIN, args, {
      cwd: REPO_ROOT,
      env: {
        ...process.env,
        PYTHONPATH,
      },
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

const server = new McpServer({
  name: 'dayi-mcp-server',
  version: '0.1.0',
});

server.tool(
  'dayi_query',
  {
    type: z.enum(['medical', 'disease', 'doctor', 'symptom']),
    keyword: z.string().min(1),
  },
  async ({ type, keyword }) => {
    const { result, stdout } = await runDayiQuery(type, keyword);
    return {
      content: [
        {
          type: 'text',
          text: buildTextSummary(result, stdout),
        },
      ],
      structuredContent: result,
    };
  },
);

const transport = new StdioServerTransport();
await server.connect(transport);
