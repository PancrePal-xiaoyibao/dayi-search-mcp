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

如需指定 Python，可设置：

```bash
DAYI_PYTHON_BIN=/path/to/python3
```

发布前检查：

```bash
cd mcp-server
npm pack --dry-run
```

发布：

```bash
cd mcp-server
npm login
npm publish --access public
```

说明：
- 当前本机 `npm whoami` 返回未登录，需要重新 `npm login`
- 当前包名 `@dayi/mcp-server` 在 npm registry 中还不存在

后续要做：
1. 补充错误码与更细的 tool 描述
2. 如果 `@dayi` scope 不可用，改成你实际可发布的 scope 或包名
