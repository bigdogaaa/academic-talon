下面给你一套**可直接落地的 Zotero API 入库方案（含附件 PDF）**，适合你做“文献检索 + 自动入库”的 skill。

---

# 🧠 一句话流程

```text
创建文献条目 → 获取 item key → 上传 PDF 附件
```

---

# 🥇 一、准备工作

## 1️⃣ 获取 API Key

在 Zotero 设置中创建：

* 权限：**Read/Write**
* 记下：

  * `ZOTERO_API_KEY`

---

## 2️⃣ 获取用户 ID

打开：

```text
https://api.zotero.org/users/me
```

你会得到：

```json
{
  "userID": 1234567
}
```

---

# 🥈 二、创建文献条目（核心）

## API

```http
POST https://api.zotero.org/users/{userID}/items
```

---

## Python 示例

```python
import requests

ZOTERO_API_KEY = "your_key"
USER_ID = "your_user_id"

def create_item(paper):
    url = f"https://api.zotero.org/users/{USER_ID}/items"

    headers = {
        "Zotero-API-Key": ZOTERO_API_KEY,
        "Content-Type": "application/json"
    }

    item = {
        "itemType": "journalArticle",
        "title": paper["title"],
        "abstractNote": paper.get("abstract"),
        "url": paper.get("url"),
        "DOI": paper.get("doi"),
        "creators": [
            {
                "creatorType": "author",
                "name": a
            } for a in paper.get("authors", [])
        ]
    }

    res = requests.post(url, json=[item], headers=headers)

    return res.json()
```

---

## 返回结果（关键）

```json
[
  {
    "key": "ABCD1234",
    "version": 1
  }
]
```

👉 **这个 `key` 非常重要（后面上传 PDF 要用）**

---

# 🥉 三、上传 PDF 附件（重点）

Zotero 上传附件是 **两步流程（容易踩坑）**

---

## 第一步：获取上传 URL

```python
def get_upload_auth(item_key, filename, filesize):
    url = f"https://api.zotero.org/users/{USER_ID}/items/{item_key}/file"

    headers = {
        "Zotero-API-Key": ZOTERO_API_KEY
    }

    params = {
        "filename": filename,
        "filesize": filesize
    }

    res = requests.post(url, headers=headers, params=params)
    return res.json()
```

---

## 返回示例

```json
{
  "url": "https://storage.zotero.org/...",
  "prefix": "...",
  "suffix": "...",
  "uploadKey": "xxxx"
}
```

---

## 第二步：上传文件

```python
def upload_file(upload_info, file_path):
    with open(file_path, "rb") as f:
        res = requests.put(upload_info["url"], data=f)
    return res.status_code
```

---

## 第三步：确认上传

```python
def register_upload(item_key, upload_key):
    url = f"https://api.zotero.org/users/{USER_ID}/items/{item_key}/file"

    headers = {
        "Zotero-API-Key": ZOTERO_API_KEY
    }

    params = {
        "upload": upload_key
    }

    return requests.post(url, headers=headers, params=params)
```

---

# 🧩 四、完整流程（你可以直接用）

```python
def save_paper_to_zotero(paper, pdf_path):
    # 1. 创建条目
    item_res = create_item(paper)
    item_key = item_res[0]["key"]

    # 2. 获取上传授权
    import os
    size = os.path.getsize(pdf_path)

    upload_info = get_upload_auth(
        item_key,
        "paper.pdf",
        size
    )

    # 3. 上传文件
    upload_file(upload_info, pdf_path)

    # 4. 确认
    register_upload(item_key, upload_info["uploadKey"])

    return item_key
```

---

# 🧠 五、你这个 skill 必加的增强功能

## ✅ 1. 自动识别 itemType

```python
def detect_type(paper):
    if paper.get("is_survey"):
        return "journalArticle"
    return "conferencePaper"
```

---

## ✅ 2. 去重（非常重要）

```python
def is_duplicate(doi):
    url = f"https://api.zotero.org/users/{USER_ID}/items"
    params = {"q": doi}

    res = requests.get(url, params=params)
    return len(res.json()) > 0
```

---

## ✅ 3. 加 collection（推荐）

```python
"collections": ["COLLECTION_KEY"]
```

---

# 📦 六、支持的 itemType（常用）

| 类型   | 值               |
| ---- | --------------- |
| 期刊论文 | journalArticle  |
| 会议论文 | conferencePaper |
| 书    | book            |
| 预印本  | preprint        |

---

# ⚠️ 常见坑（非常重要）

## ❌ 1. 作者格式错

不要：

```json
"name": "John Doe"
```

建议：

```json
"firstName": "John",
"lastName": "Doe"
```

---

## ❌ 2. 上传 PDF 失败

原因：

* 没走 3 步流程
* filesize 不对

---

## ❌ 3. DOI 为空

👉 会影响 Zotero 自动补全

---

# 🚀 七、和你 openclaw skill 的结合

你最终 skill 应该是：

```text
搜索论文
 ↓
LLM筛选
 ↓
用户选择
 ↓
Zotero API入库
```
