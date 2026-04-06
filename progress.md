# progress

## 2026-04-06
- 已在 `feature/python-core-v1` 分支完成 Python Core 首版骨架。
- 已打通 `medical` 详情页 fixture -> Nuxt 解析 -> provider -> engine -> CLI -> JSON 导出链路。
- 已通过测试：`tests/test_cli.py`、`tests/test_nuxt_state_parser.py`、`tests/test_medical_provider.py`、`tests/test_engine_detail.py`。
- 已完成命令行验收：CLI 可输出标题与概述，并导出标准 JSON。
- 已新增术语文档：`docs/reference/dayi-glossary.md`，用于回看 API / SSR / Nuxt / provider / schema / MCP 等概念。
