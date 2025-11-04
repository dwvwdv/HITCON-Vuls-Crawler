# 故障排除指南

## 安裝問題

### ❌ 錯誤：Failed to build installable wheels for some pyproject.toml based projects

**問題原因：**
`pynput` 套件的依賴 `evdev` 需要編譯，但系統缺少編譯工具或依賴。

**解決方案 1：使用簡化版依賴（推薦）**

TUI 版本不需要 `pynput`，使用簡化版依賴即可：

```bash
# 使用預設的 requirements.txt（已優化）
pip install -r requirements.txt

# 執行 TUI 版本
python tui_app.py
```

**解決方案 2：安裝編譯工具（如果需要使用傳統 CLI 模式）**

<details>
<summary>Ubuntu/Debian 系統</summary>

```bash
# 安裝編譯依賴
sudo apt-get update
sudo apt-get install -y python3-dev build-essential

# 安裝 X11 依賴
sudo apt-get install -y libx11-dev libxtst-dev libxkbcommon-dev

# 安裝完整依賴
pip install -r requirements-full.txt
```
</details>

<details>
<summary>CentOS/RHEL 系統</summary>

```bash
# 安裝編譯依賴
sudo yum groupinstall "Development Tools"
sudo yum install python3-devel

# 安裝 X11 依賴
sudo yum install libX11-devel libXtst-devel

# 安裝完整依賴
pip install -r requirements-full.txt
```
</details>

<details>
<summary>macOS 系統</summary>

```bash
# 安裝 Xcode 命令列工具
xcode-select --install

# 安裝完整依賴
pip install -r requirements-full.txt
```
</details>

<details>
<summary>Windows 系統</summary>

Windows 上通常不會遇到此問題。如果遇到：

```cmd
# 直接安裝完整依賴
pip install -r requirements-full.txt
```
</details>

**解決方案 3：使用虛擬環境隔離安裝**

```bash
# 創建虛擬環境
python3 -m venv venv

# 啟動虛擬環境
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# 安裝依賴
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 執行問題

### ❌ 錯誤：ModuleNotFoundError: No module named 'textual'

**解決方案：**
```bash
pip install textual>=0.47.0
```

### ❌ 錯誤：ModuleNotFoundError: No module named 'cloudscraper'

**解決方案：**
```bash
pip install cloudscraper
```

### ❌ TUI 界面顯示異常或亂碼

**可能原因：**
1. 終端不支援 UTF-8
2. 終端視窗太小
3. 終端不支援 ANSI 顏色

**解決方案：**

```bash
# 1. 檢查終端編碼
echo $LANG
# 應該顯示類似 en_US.UTF-8 或 zh_TW.UTF-8

# 2. 設置 UTF-8 編碼（如果需要）
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# 3. 調整終端視窗大小
# 建議至少 80x24（寬x高）

# 4. 使用推薦的終端
# Linux: gnome-terminal, konsole, alacritty
# macOS: iTerm2, Terminal.app
# Windows: Windows Terminal, ConEmu
```

### ❌ 錯誤：Error fetching page: ...

**可能原因：**
1. 網路連線問題
2. 無法訪問 zeroday.hitcon.org
3. 防火牆或代理問題

**解決方案：**

```bash
# 1. 測試網路連線
curl -I https://zeroday.hitcon.org

# 2. 如果需要代理，設置環境變數
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080

# 3. 執行程式
python tui_app.py
```

---

## 鍵盤輸入問題

### ❌ Vim 鍵位不工作

**檢查步驟：**

1. 確認使用的是 TUI 版本（`python tui_app.py`）
2. 檢查配置檔：

```bash
# 查看預設配置
cat config.json

# 創建自定義配置
cp config.json ~/.hitcon-vuls-crawler-config.json
nano ~/.hitcon-vuls-crawler-config.json
```

3. 測試基本鍵位：
   - `j` 或 `↓` 應該向下移動
   - `k` 或 `↑` 應該向上移動
   - `q` 應該退出

### ❌ 無法輸入中文或特殊字符

**說明：**
這是設計行為。Vim 模式下使用單鍵快捷鍵，不支援中文輸入。

**解決方案：**
需要輸入時（如跳轉頁面），程式會自動彈出輸入對話框。

---

## 配置問題

### ❌ 修改 config.json 後沒有效果

**可能原因：**
1. JSON 格式錯誤
2. 使用了錯誤的鍵名

**解決方案：**

```bash
# 1. 驗證 JSON 格式
python -c "import json; json.load(open('config.json'))"

# 2. 如果格式錯誤，恢復預設配置
git checkout config.json

# 3. 使用用戶配置（不會被覆蓋）
cp config.json ~/.hitcon-vuls-crawler-config.json
nano ~/.hitcon-vuls-crawler-config.json
```

---

## 性能問題

### ⚠️ 載入頁面很慢

**原因：**
首次載入頁面需要從網路抓取資料。

**優化方案：**

1. **使用頁面快取**（已內建）：
   - 已訪問的頁面會自動快取
   - 再次訪問時會更快

2. **手動刷新頁面**：
   - 按 `r` 鍵清除快取並重新載入

---

## 其他問題

### ❓ 如何查看詳細錯誤訊息

```bash
# 啟用除錯模式
python -u tui_app.py 2>&1 | tee debug.log
```

### ❓ 如何回報問題

1. 收集資訊：
   ```bash
   python --version
   pip list | grep -E "textual|cloudscraper"
   echo $TERM
   ```

2. 前往 GitHub Issues：
   https://github.com/dwvwdv/HITCON-Vuls-Crawler/issues

3. 包含以下資訊：
   - 錯誤訊息
   - Python 版本
   - 作業系統
   - 重現步驟

---

## 快速命令參考

```bash
# 重新安裝（乾淨安裝）
pip uninstall -y textual cloudscraper pynput
pip install -r requirements.txt

# 清除快取
rm -rf ~/.cache/pip
rm -rf __pycache__/

# 完整重置
git checkout .
pip install -r requirements.txt --force-reinstall
```

---

## 依賴套件版本選擇

### requirements.txt（推薦）
- 僅包含 TUI 版本需要的套件
- 安裝快速，無編譯問題
- **適合大部分用戶**

### requirements-full.txt（完整版）
- 包含所有功能的套件
- 支援傳統 CLI 模式（main.py）
- 可能需要編譯工具

### requirements-tui.txt（最小版）
- 與 requirements.txt 相同
- 明確標示為 TUI 專用

---

## 還是無法解決？

如果以上方法都無法解決問題：

1. **使用 Docker**（即將推出）
2. **使用在線版本**（未來計劃）
3. **尋求幫助**：
   - GitHub Issues
   - 附上 `debug.log`
   - 詳細描述問題
