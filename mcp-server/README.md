# dayi MCP server

这是 Dayi MCP 的 Node/TypeScript 实现。

当前状态：
- 已创建 TypeScript 目录结构
- 已注册 `dayi_query` 工具
- 已注册 `dayi_query_medical` / `dayi_query_doctor` / `dayi_query_disease` / `dayi_query_symptom`
- 已桥接本地 Python Core CLI
- 返回 `content + structuredContent`

运行前提：
1. 当前仓库里的 Python Core 可用
2. 本机存在 `python3`
3. 在 `mcp-server/` 下安装 Node 依赖

开发运行：

```bash
cd mcp-server
npm install
npm run dev
```

构建：

```bash
cd mcp-server
npm run build
```

使用 Inspector 调试：

```bash
cd mcp-server
npx @modelcontextprotocol/inspector npx tsx src/index.ts
```

当前工具：
- `dayi_query`
- `dayi_query_medical`
- `dayi_query_doctor`
- `dayi_query_disease`
- `dayi_query_symptom`

默认运行（安装后可直接执行）：

```bash
npm install -g @xiaoyibao_2025/dayi-mcp-server
dayi-mcp
```

这时 MCP server 会走项目路径下的 Python Core；若需要自定义：

```bash
DAYI_PYTHON_BIN=/path/to/python3 dayi-mcp
```

也可以把它注册到 `.mcp.json` 的配置里，使用默认的 stdio transport：

```json
{
  "servers": [
    {
      "name": "dayi-mcp-server",
      "path": "node_modules/@xiaoyibao_2025/dayi-mcp-server/dist/index.js",
      "transport": "stdio"
    }
  ]
}
```

发布前检查：

```bash
cd mcp-server
npm pack --dry-run
```

发布（当前 scope 可用，命令中不再指定 OTP）：

```bash
cd mcp-server
npm login
npm publish --access public
```

说明：
- 当前 `npm whoami` 是 `xiaoyibao_2025`，你拥有这个 scope 的发布权限

后续要做：
1. 补充错误码与更细的 tool 描述
2. （可选）提供精简版 `.mcp.json` 供 Cherry/UV 等客户端直接导入，内容只要保留 server 启动即可，示例参考：

```json
{
  "version": "1.0.0",
  "servers": [
    {
      "name": "dayi-mcp-server",
      "command": "npx -y dayi-mcp-server",
      "cwd": "/Users/qinxiaoqiang/Downloads/dayi/dayi-search-mcp/mcp-server",
      "transport": "stdio"
    }
  ]
}
```

这样客户端会自动通过 `tools/list` 识别 `dayi_query` 等能力，不需要手动配置 `tools` 节点。

按照你给的格式，可以再补一个 `mcpServers` 节点的示例：

```json
{
  "mcpServers": {
    "dayi-mcp-server": {
      "command": "npx -y dayi-mcp-server",
      "cwd": "/Users/qinxiaoqiang/Downloads/dayi/dayi-search-mcp/mcp-server",
      "transport": "stdio"
    }
  }
}
```
