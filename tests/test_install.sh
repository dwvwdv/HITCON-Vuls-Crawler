#!/bin/bash
# 快速測試安裝腳本

echo "🔍 檢查 Python 環境..."
python3 --version || { echo "❌ Python 3 未安裝"; exit 1; }
pip --version || { echo "❌ pip 未安裝"; exit 1; }

echo ""
echo "📦 檢查依賴套件..."
python3 -c "import cloudscraper; print('✅ cloudscraper')" || echo "❌ cloudscraper 未安裝"
python3 -c "import textual; print('✅ textual')" || echo "❌ textual 未安裝"

echo ""
echo "🔧 測試模組導入..."
cd ..
python3 -c "from src.crawler import HITCONVulsCrawler; print('✅ crawler.py')" || echo "❌ crawler.py 有問題"
python3 -c "from src.config_loader import ConfigLoader; print('✅ config_loader.py')" || echo "❌ config_loader.py 有問題"
python3 -c "from src.app import HITCONVulsTUI; print('✅ app.py')" || echo "❌ app.py 有問題"

echo ""
echo "📄 檢查配置檔..."
if [ -f "config.json" ]; then
    python3 -c "import json; json.load(open('config.json'))" && echo "✅ config.json 格式正確" || echo "❌ config.json 格式錯誤"
else
    echo "❌ config.json 不存在"
fi

echo ""
echo "✨ 測試完成！"
echo ""
echo "如果所有項目都顯示 ✅，您可以執行："
echo "  python3 src/app.py"
