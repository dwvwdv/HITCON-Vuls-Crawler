# 快速開始指南

## 📦 一鍵安裝（推薦）

### Linux/macOS
```bash
git clone https://github.com/dwvwdv/HITCON-Vuls-Crawler.git
cd HITCON-Vuls-Crawler
pip install -r requirements.txt
./test_install.sh
python tui_app.py
```

### Windows
```cmd
git clone https://github.com/dwvwdv/HITCON-Vuls-Crawler.git
cd HITCON-Vuls-Crawler
pip install -r requirements.txt
test_install.bat
python tui_app.py
```

---

## 🎮 基本操作

### 啟動程式
```bash
python tui_app.py
```

### 常用快捷鍵
| 按鍵 | 功能 |
|------|------|
| `j` / `↓` | 向下移動選項 |
| `k` / `↑` | 向上移動選項 |
| `h` | 上一頁 |
| `l` | 下一頁 |
| `b` / `Enter` | 在瀏覽器中打開 |
| `gg` | 第一頁 |
| `G` | 最後一頁 |
| `/` | 跳轉到指定頁 |
| `r` | 重新整理 |
| `?` | 顯示幫助 |
| `q` | 退出 |

---

## ❓ 遇到問題？

### 編譯錯誤
```bash
# 使用簡化版依賴（無需編譯）
pip install -r requirements.txt
```

### 模組找不到
```bash
# 重新安裝
pip install -r requirements.txt --force-reinstall
```

### 顯示異常
```bash
# 檢查終端編碼
echo $LANG  # 應該是 UTF-8

# 設置編碼（如果需要）
export LANG=en_US.UTF-8
```

### 完整故障排除
參閱 **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** 獲取詳細解決方案

---

## 📚 更多資訊

- **詳細安裝**: [INSTALL.md](INSTALL.md)
- **故障排除**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **完整文檔**: [README.md](README.md)

---

## 🎯 快速提示

### 使用虛擬環境（推薦）
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python tui_app.py
```

### 自定義鍵位
```bash
# 複製配置到個人目錄
cp config.json ~/.hitcon-vuls-crawler-config.json

# 編輯配置
nano ~/.hitcon-vuls-crawler-config.json
```

### 傳統CLI模式
```bash
# 需要額外依賴
pip install -r requirements-full.txt
python main.py
```

---

## ✨ 5 秒快速體驗

```bash
git clone https://github.com/dwvwdv/HITCON-Vuls-Crawler.git && \
cd HITCON-Vuls-Crawler && \
pip install -r requirements.txt && \
python tui_app.py
```

**就這麼簡單！** 🚀
