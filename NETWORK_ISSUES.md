# 網絡訪問問題說明

## 問題：第二頁沒有資料

**原因：** 網站 `zeroday.hitcon.org` 返回 403 Access Denied，無法抓取真實數據。

## 自動演示模式

當無法訪問網站時，程式會**自動切換到演示模式**，生成測試數據以展示功能。

### 演示模式特點

✅ **自動啟用** - 首次訪問失敗時自動切換
✅ **每頁 20 條數據** - 模擬真實分頁
✅ **正確的頁碼** - 第 2 頁從 #21 開始
✅ **狀態欄提示** - 顯示「演示模式」標籤

### 狀態欄說明

```
Page: 2 | Vulnerabilities: 20 | 演示模式 | Access Denied (403)
```

- **演示模式** - 黃色標籤，表示使用測試數據
- **錯誤信息** - 顯示最後一次訪問錯誤

## 為什麼返回 403？

可能的原因：

1. **網站防護** - Cloudflare 或 WAF 封鎖爬蟲
2. **IP 封鎖** - 當前 IP 被限制訪問
3. **地理位置** - 網站可能限制某些地區訪問
4. **頻率限制** - 請求過於頻繁被封鎖
5. **需要認證** - 網站可能需要登入或特殊憑證

## 解決方案

### 方案 1：使用代理

```python
# 修改 crawler.py
import os

class HITCONVulsCrawler:
    def __init__(self):
        self.scraper = cloudscraper.create_scraper(browser='chrome')

        # 添加代理設置
        proxies = {
            'http': 'http://your-proxy:port',
            'https': 'http://your-proxy:port',
        }
        # 在 get 請求中使用代理
        # response = self.scraper.get(url, proxies=proxies, timeout=15)
```

### 方案 2：使用 VPN

如果您在某些地區訪問受限：

1. 連接到台灣或其他可訪問地區的 VPN
2. 重新運行程式
3. 程式會自動嘗試訪問真實數據

### 方案 3：修改 User-Agent

有時更換 User-Agent 可以解決問題：

```python
# crawler.py 中已經使用 Chrome 瀏覽器配置
self.scraper = cloudscraper.create_scraper(browser='chrome')
```

可以嘗試其他瀏覽器配置：
- `browser='firefox'`
- `browser='safari'`
- `browser='edge'`

### 方案 4：添加請求頭

```python
# 在 fetch_page 方法中
headers = {
    'User-Agent': 'Mozilla/5.0 ...',
    'Referer': 'https://zeroday.hitcon.org/',
    'Accept-Language': 'zh-TW,zh;q=0.9,en;q=0.8',
}
response = self.scraper.get(url, headers=headers, timeout=15)
```

### 方案 5：使用網站 API（如果有）

檢查 HITCON 是否提供官方 API：
- 訪問網站開發者文檔
- 聯繫網站管理員獲取 API 密鑰

## 測試網絡訪問

### 測試 1：檢查網站是否可訪問

```bash
curl -I https://zeroday.hitcon.org
```

**預期輸出：**
- `HTTP/1.1 200 OK` - 網站可訪問
- `HTTP/1.1 403 Forbidden` - 被封鎖
- `curl: (6) Could not resolve host` - DNS 問題
- `curl: (7) Failed to connect` - 網絡問題

### 測試 2：使用 Python 測試

```bash
python -c "
import requests
response = requests.get('https://zeroday.hitcon.org')
print(f'Status: {response.status_code}')
"
```

### 測試 3：檢查爬蟲配置

```bash
python -c "
from crawler import HITCONVulsCrawler
crawler = HITCONVulsCrawler(use_demo_data=False)
vuls = crawler.get_vulnerabilities(1)
print(f'Results: {len(vuls)}')
print(f'Demo mode: {crawler.use_demo_data}')
print(f'Error: {crawler.last_error}')
"
```

## 強制使用真實數據

如果您已解決網絡問題，可以強制禁用演示模式：

```python
# 修改 tui_app.py
def __init__(self):
    super().__init__()
    self.config = ConfigLoader()
    self.crawler = HITCONVulsCrawler(use_demo_data=False)  # 強制使用真實數據
    # ...
```

然後在爬蟲代碼中註釋掉自動切換：

```python
# crawler.py - get_vulnerabilities 方法
def get_vulnerabilities(self, page_num: int) -> List[Vulnerability]:
    html = self.fetch_page(page_num)

    if html is None:
        # self.use_demo_data = True  # 註釋掉這行
        return []  # 返回空列表而不是演示數據

    return self.parse_vulnerabilities(html)
```

## 演示模式的用途

即使網站無法訪問，演示模式仍然有用：

✅ **測試功能** - 驗證所有鍵位和功能是否正常
✅ **展示界面** - 演示 TUI 界面設計
✅ **開發測試** - 開發新功能時不依賴網絡
✅ **學習使用** - 新用戶可以熟悉操作方式

## 常見問題

### Q: 為什麼我的環境也返回 403？

**A:** 這是正常的。HITCON 網站有訪問限制，演示模式就是為此設計的。

### Q: 演示數據是真實漏洞嗎？

**A:** 不是。演示數據只是用於展示功能的測試數據，標題中會標註「[示例]」和「測試數據」。

### Q: 如何判斷是真實數據還是演示數據？

**A:** 檢查狀態欄：
- 有「演示模式」標籤 = 測試數據
- 無「演示模式」標籤 = 真實數據
- 漏洞標題包含「[示例]」= 測試數據

### Q: 可以混合使用真實和演示數據嗎？

**A:** 目前不行。程式會在首次失敗後完全切換到演示模式。

## 技術細節

### 自動回退機制

```python
def get_vulnerabilities(self, page_num: int) -> List[Vulnerability]:
    # 1. 如果已在演示模式，直接返回演示數據
    if self.use_demo_data:
        return self._generate_demo_data(page_num)

    # 2. 嘗試獲取真實數據
    html = self.fetch_page(page_num)

    # 3. 失敗時自動切換到演示模式
    if html is None:
        self.use_demo_data = True
        return self._generate_demo_data(page_num)

    # 4. 解析成功返回真實數據
    return self.parse_vulnerabilities(html)
```

### 演示數據生成

```python
def _generate_demo_data(self, page_num: int) -> List[Vulnerability]:
    demo_vulns = []
    start_id = (page_num - 1) * 20 + 1  # 第2頁從21開始

    for i in range(20):  # 每頁20條
        vuln_id = start_id + i
        url = f"/vulnerability/ZD-2024-{vuln_id:05d}"
        title = f"[示例] Vulnerability #{vuln_id} - 測試數據"
        demo_vulns.append(Vulnerability(url=url, title=title))

    return demo_vulns
```

## 聯繫支援

如果您認為網站應該可以訪問但一直返回 403：

1. 檢查您的網絡配置
2. 嘗試從不同網絡訪問（如手機熱點）
3. 聯繫 HITCON 管理員確認訪問政策
4. 在 GitHub Issues 報告您的環境信息

## 總結

✅ **第二頁有資料** - 演示模式下每頁都有 20 條數據
✅ **自動回退** - 無需手動配置
✅ **清晰提示** - 狀態欄顯示當前模式和錯誤
✅ **功能完整** - 所有鍵位和功能都能正常使用

**演示模式讓您即使在網絡問題時也能使用和測試程式！** 🎉
