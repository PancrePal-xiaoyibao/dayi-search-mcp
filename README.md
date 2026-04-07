# dayi-search-mcp

基于中国医药信息查询平台（Dayi）的检索与提取项目。  
当前已形成首个正式可用版本：**`@xiaoyibao_2025/dayi-mcp-server@0.1.7`**。

## 项目组成

1. **Python Core**（`src/dayi_core`）
   - 负责检索、详情提取、结构化输出
   - 支持类型：`medical` / `disease` / `doctor` / `symptom`
2. **MCP Server**（`mcp-server`）
   - Node/TypeScript 实现
   - 已打包内置 Python Core（发布包内 `python/dayi_core`）

## Python Core 快速使用

```bash
PYTHONPATH=src python3 -m dayi_core.cli.main query --type medical --keyword 替吉奥 --json /tmp/替吉奥.json
```

## MCP 工具能力（0.1.7）

- `dayi_query`：指定 type + keyword 查询
- `dayi_query_auto`：自动判定类型
- medical 输出增强：
  - `record.sections.药品详情`：成分/性状/适应症/用法用量/规格/贮藏方法/有效期/执行标准
  - `record.sections.注意事项`：不良反应/禁忌/药物相互作用/注意事项
- 返回 `structuredContent.raw` 原始证据：
  - `detail_html` / `nuxt_script` / `search_payload`
- 支持落盘：
  - `save_path` 可选
  - 不传时默认落盘 `/tmp/标题_YYYYMMDD.json`
  - 返回 `structuredContent.saved_path`

## 客户端接入指引

### 1) Cherry Studio

使用 `mcpServers` 配置（推荐锁版本）：

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

### 2) FastGPT

在 MCP/工具接入里新增 stdio server，命令填：

```bash
npx -y @xiaoyibao_2025/dayi-mcp-server@0.1.7
```

transport 选 `stdio`，工具自动通过 `tools/list` 发现。

### 3) OpenClaw

在插件或运行时的 MCP 配置中添加一个 stdio server：

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

### 4) Claude Code

在项目的 MCP 配置文件中注册：

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

### 5) Codex / Codex CLI

使用同样的 stdio MCP 配置方式，命令保持一致：

```bash
npx -y @xiaoyibao_2025/dayi-mcp-server@0.1.7
```

## 开发与测试

```bash
# Python tests
pytest tests -q

# MCP build
cd mcp-server
npm install
npm run sync:python
npm run build
```

## Skills

已新增项目内技能：

- `skills/dayi-mcp-query/SKILL.md`

用途：在支持 Skill 机制的客户端中，自动触发 Dayi MCP 查询流程（药品/疾病/医生/症状、落盘 JSON、RAG 入库预处理）。
