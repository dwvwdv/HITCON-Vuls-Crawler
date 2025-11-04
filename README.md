# HITCON-Vuls
終端下HITCON公開漏洞快速查閱，方便學習各種漏洞與思路

## 功能特色
- 🎨 現代化TUI界面（基於Textual框架）
- ⌨️  Vim風格鍵位支援（完全可自訂）
- 🚀 頁面快取機制，快速瀏覽
- 🎯 支援跳轉到指定頁面
- 🔧 可自訂鍵位綁定和主題

## 使用方式

### 新版TUI界面（推薦）
執行TUI應用程式，享受現代化的終端介面：
```bash
python tui_app.py
```

### 傳統模式
執行main.py，搭配Ctrl+點擊快速打開頁面連結：
```bash
python main.py
```
![image](https://github.com/dwvwdv/github_picture/blob/master/2022-11-07%2016%2014%2004.png)

## 快捷鍵

### TUI模式（Vim風格）
- `j` / `↓` : 向下移動
- `k` / `↑` : 向上移動
- `d` / `Ctrl+f` / `PageDown` : 下一頁
- `u` / `Ctrl+b` / `PageUp` : 上一頁
- `gg` : 跳轉到第一頁
- `G` : 跳轉到最後一頁
- `/` : 跳轉到指定頁面
- `r` : 重新整理當前頁面
- `?` / `F1` : 顯示說明
- `q` / `Esc` : 退出程式

### 傳統模式
- `Page Down` : 下一頁
- `Page Up` : 上一頁
- `/` : 輸入頁碼跳轉
- `F1` : 說明
- `Esc` : 退出

## 自訂鍵位綁定

你可以透過編輯 `config.json` 來自訂鍵位綁定：

```json
{
  "keybindings": {
    "vim_mode": {
      "down": ["j", "down"],
      "up": ["k", "up"],
      "page_down": ["ctrl+f", "pagedown", "d"],
      "page_up": ["ctrl+b", "pageup", "u"],
      ...
    }
  }
}
```

也可以在 `~/.hitcon-vuls-crawler-config.json` 建立個人設定檔來覆蓋預設設定。

## 安裝依賴

```bash
pip install -r requirements.txt
```

## 專案結構

```
HITCON-Vuls-Crawler/
├── tui_app.py          # TUI應用程式（新）
├── crawler.py          # 爬蟲邏輯模組（新）
├── config_loader.py    # 設定載入器（新）
├── config.json         # 預設設定檔（新）
├── main.py             # 傳統CLI應用程式
├── requirements.txt    # Python依賴
└── README.md          # 說明文件
```  
