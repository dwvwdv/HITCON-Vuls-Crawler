# 建置與執行指南

## 快速開始

### 1. 克隆專案
```bash
git clone https://github.com/dwvwdv/HITCON-Vuls-Crawler.git
cd HITCON-Vuls-Crawler
```

### 2. 安裝依賴

**選項 A：TUI 版本（推薦，無編譯問題）**
```bash
pip install -r requirements.txt
```

**選項 B：完整版本（包含傳統 CLI 模式，可能需要編譯工具）**
```bash
pip install -r requirements-full.txt
```

> ⚠️ **遇到編譯錯誤？** 請參閱 [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

### 3. 執行程式

#### 選項 A：新版TUI界面（推薦）
```bash
python tui_app.py
```

#### 選項 B：傳統CLI模式
```bash
python main.py
```

---

## 詳細建置步驟

### 環境需求
- Python 3.7 或更高版本
- pip（Python 套件管理器）
- 網路連線（用於爬取資料）

### 使用虛擬環境（建議）

#### Linux/macOS
```bash
# 創建虛擬環境
python3 -m venv venv

# 啟動虛擬環境
source venv/bin/activate

# 安裝依賴
pip install -r requirements.txt

# 執行程式
python tui_app.py
```

#### Windows
```cmd
# 創建虛擬環境
python -m venv venv

# 啟動虛擬環境
venv\Scripts\activate

# 安裝依賴
pip install -r requirements.txt

# 執行程式
python tui_app.py
```

---

## 依賴套件說明

### 必需套件
- **cloudscraper** (1.2.71+) - 繞過 Cloudflare 保護的網頁爬蟲
- **textual** (0.47.0+) - 現代化 TUI 框架
- **pynput** (1.8.1+) - 鍵盤輸入處理（傳統模式使用）

### 自動安裝的依賴
執行 `pip install -r requirements.txt` 時會自動安裝：
- requests
- rich（用於終端美化）
- markdown-it-py（用於 Textual）
- 其他相關依賴

---

## 常見問題排解

### 問題 1：找不到模組錯誤
```
ModuleNotFoundError: No module named 'textual'
```

**解決方案：**
```bash
pip install -r requirements.txt --upgrade
```

### 問題 2：權限錯誤（Linux/macOS）
```
Permission denied
```

**解決方案：**
```bash
# 選項 A：使用虛擬環境（推薦）
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 選項 B：使用 --user 參數
pip install -r requirements.txt --user
```

### 問題 3：終端顯示異常
如果 TUI 界面顯示不正常，請確保：
- 使用支援 UTF-8 的終端
- 終端視窗足夠大（建議至少 80x24）
- 終端支援 ANSI 顏色碼

**建議的終端：**
- Linux: GNOME Terminal, Konsole, Alacritty
- macOS: iTerm2, Terminal.app
- Windows: Windows Terminal, ConEmu

### 問題 4：網路連線失敗
```
Error fetching page: ...
```

**解決方案：**
- 檢查網路連線
- 確認可以訪問 https://zeroday.hitcon.org
- 如果在中國大陸，可能需要配置代理

---

## 自定義配置

### 創建個人配置檔
```bash
# 複製預設配置到使用者目錄
cp config.json ~/.hitcon-vuls-crawler-config.json

# 編輯配置
nano ~/.hitcon-vuls-crawler-config.json
```

### 配置範例
```json
{
  "keybindings": {
    "vim_mode": {
      "down": ["j", "down", "ctrl+n"],
      "up": ["k", "up", "ctrl+p"],
      "quit": ["q", "escape", "ctrl+c"]
    }
  },
  "theme": {
    "primary": "green",
    "accent": "cyan"
  }
}
```

---

## 開發模式

### 安裝開發依賴
```bash
pip install -r requirements.txt
pip install pytest black flake8  # 測試和代碼格式化工具
```

### 執行測試
```bash
# 語法檢查
python -m py_compile *.py

# 導入測試
python -c "from tui_app import HITCONVulsTUI; print('✓ Import successful')"
```

---

## 解除安裝

### 移除虛擬環境
```bash
# 停用虛擬環境
deactivate

# 刪除虛擬環境目錄
rm -rf venv/
```

### 移除配置檔
```bash
rm ~/.hitcon-vuls-crawler-config.json
```

---

## 更新專案

```bash
# 拉取最新代碼
git pull origin main

# 更新依賴
pip install -r requirements.txt --upgrade
```

---

## 獲取幫助

- **GitHub Issues**: https://github.com/dwvwdv/HITCON-Vuls-Crawler/issues
- **程式內幫助**: 執行程式後按 `?` 或 `F1`
- **文檔**: 閱讀 README.md

---

## 快速命令參考

```bash
# 一鍵安裝並執行（虛擬環境）
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python tui_app.py

# 一鍵安裝並執行（全局）
pip install -r requirements.txt && python tui_app.py

# 傳統模式
python main.py
```
