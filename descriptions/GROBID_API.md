# GROBID API 文档（实用版）

> Base URL

```
http://localhost:8070/api
```

---

# 1. 服务状态检查

## GET `/isalive`

### 说明

检查 GROBID 服务是否正常运行

### 请求

```
GET /api/isalive
```

### 响应

```
true
```

---

# 2. 解析完整论文（最常用）

## POST `/processFulltextDocument`

### 说明

解析 PDF 全文，返回结构化 TEI XML（推荐使用）

---

### 请求

```
POST /api/processFulltextDocument
Content-Type: multipart/form-data
```

#### 参数

| 参数    | 类型   | 必填 | 说明     |
| ----- | ---- | -- | ------ |
| input | file | ✅  | PDF 文件 |

---

### 示例（curl）

```
curl -X POST "http://localhost:8070/api/processFulltextDocument" \
  -H "accept: application/xml" \
  -H "Content-Type: multipart/form-data" \
  -F "input=@paper.pdf"
```

---

### 响应（示例）

```xml
<TEI>
  <teiHeader>
    <fileDesc>
      <titleStmt>
        <title>Paper Title</title>
      </titleStmt>
    </fileDesc>
  </teiHeader>

  <text>
    <body>
      <div type="section">
        <head>Introduction</head>
        <p>Text content...</p>
      </div>
    </body>
  </text>
</TEI>
```

---

# 3. 仅解析 Header（元信息）

## POST `/processHeaderDocument`

### 说明

提取论文基础信息（标题、作者、期刊等）

---

### 示例

```
curl -X POST "http://localhost:8070/api/processHeaderDocument" \
  -F "input=@paper.pdf"
```

---

### 输出重点

* title
* authors
* affiliations
* abstract（有时）

---

# 4. 解析参考文献

## POST `/processReferences`

### 说明

提取参考文献列表

---

### 示例

```
curl -X POST "http://localhost:8070/api/processReferences" \
  -F "input=@paper.pdf"
```

---

### 输出（示例）

```xml
<listBibl>
  <biblStruct>
    <analytic>
      <title>Referenced Paper</title>
    </analytic>
  </biblStruct>
</listBibl>
```

---

# 5. 解析 citation string

## POST `/processCitation`

### 说明

解析单条引用字符串（用于引用规范化）

---

### 示例

```
curl -X POST "http://localhost:8070/api/processCitation" \
  -F "citations=Smith et al. 2020 Deep Learning"
```

---

# 6. 解析 affiliation（机构）

## POST `/processAffiliations`

### 示例

```
curl -X POST "http://localhost:8070/api/processAffiliations" \
  -F "affiliations=Stanford University"
```

---

# 7. 常用参数（高级）

这些参数可以加在 `processFulltextDocument` 中：

| 参数                   | 说明        |
| -------------------- | --------- |
| consolidateHeader    | 0/1，增强元数据 |
| consolidateCitations | 0/1，增强引用  |
| includeRawCitations  | 1 返回原始引用  |
| segmentSentences     | 1 句子切分    |

---

### 示例（增强模式）

```
curl -X POST "http://localhost:8070/api/processFulltextDocument" \
  -F "input=@paper.pdf" \
  -F "consolidateHeader=1" \
  -F "consolidateCitations=1"
```

---

# 8. 返回格式说明（TEI 核心结构）

## 标题

```xml
<titleStmt>
  <title>...</title>
</titleStmt>
```

---

## 作者

```xml
<author>
  <persName>
    <forename>John</forename>
    <surname>Doe</surname>
  </persName>
</author>
```

---

## 章节

```xml
<div type="section">
  <head>Method</head>
  <p>Text...</p>
</div>
```

---

## 引用

```xml
<ref type="bibr" target="#b1">(Smith et al., 2020)</ref>
```

---

## 参考文献

```xml
<biblStruct xml:id="b1">
  <analytic>
    <title>Paper Title</title>
  </analytic>
</biblStruct>
```

---

# 9. Python 调用示例

```python
import requests

def parse_pdf(path):
    url = "http://localhost:8070/api/processFulltextDocument"

    with open(path, "rb") as f:
        files = {"input": f}
        res = requests.post(url, files=files)

    return res.text
```

---

# 10. 最佳实践（强烈建议）

## 1. 一定开启 consolidate

```
consolidateHeader=1
consolidateCitations=1
```

👉 否则 metadata 很差

---

## 2. 不要直接喂 XML 给 LLM

👉 先转 JSON

---

## 3. 控制 PDF 大小

建议：

* < 20MB
* < 50 页（最佳）

---

## 4. 加缓存

按 PDF hash 缓存结果

---

# 11. 错误处理

| 状态码 | 含义    |
| --- | ----- |
| 200 | 成功    |
| 500 | 解析失败  |
| 503 | 服务不可用 |

---

# 12. 推荐调用流程（你的 skill）

```
PDF
 ↓
processFulltextDocument
 ↓
TEI XML
 ↓
JSON转换（你实现）
 ↓
LLM分析
```

---

# 13. 你真正要用的核心接口（总结）

| 接口                      | 用途    |
| ----------------------- | ----- |
| processFulltextDocument | ⭐ 主接口 |
| processHeaderDocument   | 元信息   |
| processReferences       | 引用    |

---

# END
