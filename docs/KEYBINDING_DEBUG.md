# 鍵位調試指南

## 問題診斷

如果您發現 j/k/h/l 等鍵位沒有反應，請使用以下方法診斷：

### 步驟 1：測試按鍵是否被捕獲

運行按鍵測試工具：

```bash
python test_keys.py
```

然後按下以下按鍵，查看是否能被正確識別：
- `j` - 應該顯示 ✅
- `k` - 應該顯示 ✅
- `h` - 應該顯示 ✅
- `l` - 應該顯示 ✅
- `b` - 應該顯示 ✅
- `g` - 應該顯示 ✅
- `G` (Shift+g) - 應該顯示 ✅

**如果這些按鍵能被識別**，說明終端和 Textual 工作正常。

**如果這些按鍵無法識別**，可能是：
1. 終端模擬器問題
2. 終端配置問題
3. 按鍵被其他程式攔截

### 步驟 2：測試主程式

運行主程式：

```bash
python tui_app.py
```

測試以下功能：
- 按 `j` - 向下移動選項
- 按 `k` - 向上移動選項
- 按 `h` - 上一頁
- 按 `l` - 下一頁
- 按 `b` - 打開瀏覽器
- 按 `?` - 顯示幫助

### 步驟 3：啟用調試模式

如果按鍵仍然不工作，啟用調試模式：

編輯 `tui_app.py`，找到這行：

```python
# self.query_one("#status-bar", Static).update(f"[dim]Key pressed: {key}[/dim]")
```

移除 `#` 註釋符號：

```python
self.query_one("#status-bar", Static).update(f"[dim]Key pressed: {key}[/dim]")
```

重新運行程式，狀態欄會顯示您按下的按鍵。

## 常見問題

### Q: 只有方向鍵和 Ctrl+p 能用，其他都不行

**A:** 這通常是 Textual 的按鍵綁定系統問題。最新版本已經改用 `on_key` 事件處理器解決此問題。

**解決方案：**
```bash
# 確保使用最新代碼
git pull origin claude/add-tui-vim-mode-011CUnS6Vsk5ktKQ8KNVkapy

# 重新測試
python tui_app.py
```

### Q: 終端不支援某些按鍵

**A:** 某些終端模擬器可能不支援所有按鍵組合。

**建議的終端：**
- Linux: GNOME Terminal, Konsole, Alacritty, Kitty
- macOS: iTerm2, Alacritty
- Windows: Windows Terminal, Alacritty

**測試終端支援：**
```bash
python test_keys.py
```

### Q: 按鍵被輸入法攔截

**A:** 確保使用英文輸入模式。

**解決方案：**
1. 切換到英文輸入法
2. 在程式內確保沒有中文輸入法激活

### Q: tmux/screen 環境下按鍵不工作

**A:** tmux/screen 可能會影響按鍵傳遞。

**解決方案：**
```bash
# 設置正確的 TERM 變數
export TERM=screen-256color  # 在 tmux/screen 中
# 或
export TERM=xterm-256color   # 在普通終端中

# 重新運行程式
python tui_app.py
```

## 技術細節

### 按鍵處理機制

程式使用 `on_key` 事件處理器來捕獲按鍵：

```python
def on_key(self, event: events.Key) -> None:
    key = event.key

    key_map = {
        "j": self.action_move_down,
        "k": self.action_move_up,
        # ...
    }

    if key in key_map:
        key_map[key]()
        event.prevent_default()
```

### 為什麼不使用 Binding？

Textual 的 `Binding` 系統對單字符按鍵支援不佳。使用 `on_key` 事件處理器可以：
1. 直接捕獲所有按鍵
2. 更可靠的單字符按鍵處理
3. 支援複雜的按鍵組合（如 `gg`）

## 回報問題

如果問題仍然存在，請提供以下資訊：

```bash
# 收集系統資訊
echo "Python: $(python --version)"
echo "Terminal: $TERM"
echo "Shell: $SHELL"
pip show textual | grep Version

# 運行測試
python test_keys.py > key_test_output.txt
# 按下 j, k, h, l, b 等鍵，然後按 Escape

# 附上 key_test_output.txt 和上述資訊
```

## 替代方案

如果鍵位始終無法工作，可以：

1. **使用方向鍵**：
   - `↑/↓` 代替 `j/k`
   - `PageUp/PageDown` 代替 `h/l`

2. **修改鍵位配置**：
   編輯 `config.json`，使用方向鍵：
   ```json
   {
     "keybindings": {
       "vim_mode": {
         "down": ["down"],
         "up": ["up"],
         "page_down": ["pagedown"],
         "page_up": ["pageup"]
       }
     }
   }
   ```

3. **使用傳統模式**：
   ```bash
   python main.py
   ```
