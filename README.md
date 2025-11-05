# HITCON-Vuls
終端下HITCON公開漏洞快速查閱，方便學習各種漏洞與思路

## 快速開始

```bash
# 1. 克隆專案
git clone https://github.com/dwvwdv/HITCON-Vuls-Crawler.git
cd HITCON-Vuls-Crawler

# 2. 安裝依賴
pip install -r requirements.txt

# 3. 網絡診斷（可選，檢查是否能訪問網站）
python diagnose_network.py

# 4. 執行TUI程式
python tui_app.py
```

**詳細建置說明請參閱 [INSTALL.md](INSTALL.md)**
**遇到問題？請參閱 [TROUBLESHOOTING.md](TROUBLESHOOTING.md)**
**數據為演示模式？請參閱 [ENVIRONMENT_README.md](ENVIRONMENT_README.md)**

## 功能特色
- 現代化TUI界面（基於Textual框架）
- Vim風格鍵位支援（完全可自訂）
- 頁面快取機制，快速瀏覽
- 支援跳轉到指定頁面
- 可自訂鍵位綁定和主題

## 使用方式

### 新版TUI界面（推薦）
執行TUI應用程式，享受現代化的終端介面：
```bash
python app.py
```

![image](https://github.com/dwvwdv/github_picture/blob/master/螢幕擷取畫面%202025-11-05%20200626.png)


## 快捷鍵

### TUI模式（Vim風格）
- `j` / `↓` : 向下移動選項
- `k` / `↑` : 向上移動選項
- `h` / `Ctrl+b` / `PageUp` : 上一頁
- `l` / `Ctrl+f` / `PageDown` : 下一頁
- `b` / `Enter` : 在瀏覽器中打開選中的漏洞
- `gg` : 跳轉到第一頁
- `G` : 跳轉到最後一頁
- `/` : 跳轉到指定頁面
- `r` : 重新整理當前頁面
- `?` / `F1` : 顯示說明
- `q` / `Esc` : 退出程式

## 自訂鍵位綁定

你可以透過編輯 `config.json` 來自訂鍵位綁定：

```json
{
  "keybindings": {
    "vim_mode": {
      "down": ["j", "down"],
      "up": ["k", "up"],
      "page_down": ["l", "ctrl+f", "pagedown"],
      "page_up": ["h", "ctrl+b", "pageup"],
      "open_browser": ["b", "enter"],
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
├── app.py          # TUI應用程式
├── crawler.py          # 爬蟲邏輯模組
├── config_loader.py    # 設定載入器
├── config.json         # 預設設定檔
├── main.py             # CLI應用程式
├── requirements.txt    # Python依賴
└── README.md          # 說明文件
```  
