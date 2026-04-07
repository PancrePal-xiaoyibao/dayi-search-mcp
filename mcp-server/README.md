# dayi MCP server

Dayi 的 MCP Server（Node/TypeScript），当前正式版本建议使用：

`@xiaoyibao_2025/dayi-mcp-server@0.1.7`

## 核心能力

- 工具：
  - `dayi_query`
  - `dayi_query_auto`（推荐，自动判定 medical/disease/doctor/symptom）
- medical 输出增强：
  - `record.sections.药品详情`：成分/性状/适应症/用法用量/规格/贮藏方法/有效期/执行标准
  - `record.sections.注意事项`：不良反应/禁忌/药物相互作用/注意事项
- 原始证据：
  - `structuredContent.raw.detail_html`
  - `structuredContent.raw.nuxt_script`
  - `structuredContent.raw.search_payload`
- 落盘：
  - 参数 `save_path` 可选
  - 不传时默认落盘 `/tmp/标题_YYYYMMDD.json`
  - 返回 `structuredContent.saved_path`

## 客户端接入（stdio）

推荐统一命令（锁版本）：

```bash
npx -y @xiaoyibao_2025/dayi-mcp-server@0.1.7
```

### Cherry Studio / OpenClaw / Claude Code / Codex（mcpServers 格式）

```json
{
  "mcpServers": {
    "dayi-mcp-server": {
      "command": "npx",
      "args": ["-y", "@xiaoyibao_2025/dayi-mcp-server@0.1.7"],
      "transport": "stdio"
    }
  }
}
```

### FastGPT

新增 MCP stdio server，命令填写：

```bash
npx -y @xiaoyibao_2025/dayi-mcp-server@0.1.7
```

工具自动通过 `tools/list` 发现。

## 开发

```bash
cd mcp-server
npm install
npm run sync:python
npm run build
```

Inspector 调试：

```bash
npx @modelcontextprotocol/inspector npx tsx src/index.ts
```

## 发布

```bash
cd mcp-server
npm pack --dry-run
npm publish --access public
```
