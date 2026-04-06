# dayi-search-mcp

基于中国医药信息查询平台（Dayi）的检索与提取项目。

当前仓库已实现一个 **Python Core**，支持：
- 药品 `medical`
- 疾病 `disease`
- 医生 `doctor`
- 症状 `symptom`

当前能力：
- 真实搜索接口：`https://server.dayi.org.cn/api/search`
- 详情页抓取：`https://m.dayi.org.cn/...`
- 详情解析优先使用：`window.__NUXT__`
- 命令行入口：`detail` / `query`

---

## 安装与开发

建议使用 Python 3.11+。

当前开发态运行方式：

```bash
PYTHONPATH=src python3 -m dayi_core.cli.main query --type medical --keyword 替吉奥
```

也可以运行详情模式：

```bash
PYTHONPATH=src python3 -m dayi_core.cli.main detail --type medical --url https://m.dayi.org.cn/drug/1156140 --keyword 替吉奥
```

---

## 支持的类型

- `medical`
- `disease`
- `doctor`
- `symptom`

---

## 示例

### 1. 药品查询

```bash
PYTHONPATH=src python3 -m dayi_core.cli.main query --type medical --keyword 替吉奥 --json /tmp/medical.json
```

### 2. 医生查询

```bash
PYTHONPATH=src python3 -m dayi_core.cli.main query --type doctor --keyword 傅德良 --json /tmp/doctor.json
```

### 3. 疾病查询

```bash
PYTHONPATH=src python3 -m dayi_core.cli.main query --type disease --keyword 胰腺癌 --json /tmp/disease.json
```

---

## 当前抓取策略

- search：优先 API
- detail：优先 `window.__NUXT__`
- DOM/HTML 标签解析：作为兜底

---

## 测试

```bash
pytest tests/test_cli_query.py tests/test_search_api.py tests/test_multi_providers.py tests/test_cli.py tests/test_nuxt_state_parser.py tests/test_medical_provider.py tests/test_engine_detail.py -q
```

---

## 目录说明

```text
src/dayi_core/
  cli/            # CLI 入口
  core/           # engine / fetcher / models
  parsers/        # Nuxt / HTML 字段解析
  providers/      # medical / disease / doctor / symptom
  exporters/      # 控制台与 JSON 输出

tests/
  fixtures/       # HTML / JSON fixture
```

---

## MCP 规划

当前仓库已初始化 `mcp-server/` 骨架目录，用于后续拆分 Node/TypeScript MCP 服务。

后续 MCP 将负责：
- 暴露 `dayi_query` 等工具
- 通过 bridge 调用 Python Core
- 支持 npm 发布
