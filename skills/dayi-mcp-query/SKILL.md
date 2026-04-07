---
name: dayi-mcp-query
description: 使用 Dayi MCP Server 进行医药信息检索与结构化提取。只要用户提到药品/疾病/医生/症状查询、药品副作用、不良反应、禁忌、用法用量、医生背景信息，或希望把结果保存为 JSON/用于 RAG，就应优先触发本技能并调用 dayi_query_auto 或 dayi_query。
---

# Dayi MCP Query Skill

## 适用场景

当用户有以下需求时使用本技能：

- 查询药品、医生、疾病、症状相关信息
- 关注药品副作用、不良反应、禁忌、药物相互作用
- 需要将结果结构化输出
- 需要把结果落盘为本地 JSON，后续用于知识库/RAG

## 调用策略

1. 默认优先调用 `dayi_query_auto`
   - 输入：`keyword`
   - 让服务自动判定类型（medical/disease/doctor/symptom）

2. 当用户明确指定类型时调用 `dayi_query`
   - 输入：`type`, `keyword`

3. 当用户要求保存本地文件时，传入 `save_path`
   - 建议传目录路径（如 `/tmp`），服务会按 `标题_YYYYMMDD.json` 落盘
   - 或传绝对文件路径（以 `.json` 结尾）

## 输出处理规范

必须同时关注两层返回：

- `content`：人类可读摘要
- `structuredContent`：机器可消费结构化 JSON（优先用于后续处理）

重点字段：

- `structuredContent.record.sections`
  - 药品详情：成分、性状、适应症、用法用量、规格、贮藏方法、有效期、执行标准
  - 注意事项：不良反应、禁忌、药物相互作用、注意事项
- `structuredContent.raw`
  - `detail_html`
  - `nuxt_script`
  - `search_payload`
- `structuredContent.saved_path`
  - 最终落盘绝对路径

## 推荐回复格式

按以下顺序组织回答：

1. 查询命中（类型、标题）
2. 关键医学信息（按用户问题聚焦）
3. 证据来源（detail_url / 关键字段）
4. 若有落盘：返回 `saved_path`

## 示例

### 示例 1：药品副作用

用户：`检索吉西他滨副作用`  
动作：调用 `dayi_query_auto(keyword='检索吉西他滨副作用')`

### 示例 2：医生背景

用户：`检索傅德良医生背景`  
动作：调用 `dayi_query_auto(keyword='检索傅德良医生背景')`

### 示例 3：指定类型 + 落盘

用户：`查询替吉奥并保存成JSON到/tmp`  
动作：调用 `dayi_query(type='medical', keyword='替吉奥', save_path='/tmp')`

