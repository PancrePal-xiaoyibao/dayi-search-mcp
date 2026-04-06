# Dayi 项目术语备忘

更新时间：2026-04-06

## 1. API
API 是网站专门给程序调用的数据接口。

在这个项目里：
- 搜索页最终确认使用的接口是：`https://server.dayi.org.cn/api/search`
- 这个接口返回 JSON，适合程序直接处理

可理解为：
- HTML 是给人看的页面
- API 是给程序看的数据出口

---

## 2. HTML 抓取
HTML 抓取就是直接下载网页源码，再从源码里提取信息。

在这个项目里：
- 详情页可以先抓 HTML
- 再从 HTML 里提取结构化数据

---

## 3. SSR
SSR = 服务器端渲染。

意思是页面内容在服务器端已经拼好，浏览器一打开就能看到。

在这个项目里：
- 搜索页的 SSR HTML 没有直接带结果列表
- 详情页 HTML 则带了大量内容

---

## 4. `window.__NUXT__`
这是 Nuxt 前端框架注入到页面里的初始化数据对象。

在这个项目里：
- 详情页里存在 `window.__NUXT__`
- 其中包含 `detailApi`、`response.data/detail`、`dictionary` 等结构化信息

它可以理解成：
- 页面里隐藏的一份结构化数据包

---

## 5. JSON
JSON 是一种结构化文本格式，适合程序处理。

示例：
```json
{
  "title": "替吉奥",
  "type": "medical",
  "id": 1156140
}
```

---

## 6. bundle / 前端 bundle
bundle 是网站前端打包后的 JS 文件。

在这个项目里：
- 我们通过分析前端 bundle，找到搜索逻辑实际调用了 `$axios.$get(...)`
- 并最终定位到真实搜索接口

---

## 7. fixture
fixture 是开发和测试用的固定样本数据。

在这个项目里：
- 详情页 HTML fixture
- 搜索接口 JSON fixture

作用：
- 不用每次联网也能稳定测试

---

## 8. provider
provider 是某一类内容的专用解析器。

在这个项目里：
- `medical` provider：解析药品详情
- `disease` provider：解析疾病详情
- `doctor` provider：解析医生详情
- `symptom` provider：解析症状详情

---

## 9. CLI
CLI = 命令行工具。

在这个项目里：
- `dayi detail ...`
- `dayi query ...`

这是首个用户可直接使用的入口。

---

## 10. MCP
MCP 可以理解为：
- 把项目能力封装成 AI 可以直接调用的工具接口

在这个项目里：
- 后续会把搜索与提取能力暴露给 AI/Agent 调用

---

## 11. schema
schema 是统一的数据结构规范。

在这个项目里：
- 不同类型最终都会落到统一顶层结构
- 便于 CLI、MCP、skill、LLM 共用

---

## 12. 兜底
兜底就是主方案失败时的备用方案。

在这个项目里：
- 搜索优先走 API
- 详情优先走 `window.__NUXT__`
- 必要时再退回 HTML/DOM 解析

---

## 当前项目推荐抓取策略
- search：优先 API
- detail：优先 `window.__NUXT__`
- DOM scraping：仅作为兜底
