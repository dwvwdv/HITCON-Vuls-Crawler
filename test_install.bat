@echo off
REM 快速測試安裝腳本 (Windows)

echo 检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python 未安装
    exit /b 1
)
python --version
pip --version >nul 2>&1
if errorlevel 1 (
    echo X pip 未安装
    exit /b 1
)
pip --version

echo.
echo 检查依赖套件...
python -c "import cloudscraper; print('√ cloudscraper')" 2>nul || echo X cloudscraper 未安装
python -c "import textual; print('√ textual')" 2>nul || echo X textual 未安装

echo.
echo 测试模组导入...
python -c "from crawler import HITCONVulsCrawler; print('√ crawler.py')" 2>nul || echo X crawler.py 有问题
python -c "from config_loader import ConfigLoader; print('√ config_loader.py')" 2>nul || echo X config_loader.py 有问题
python -c "from tui_app import HITCONVulsTUI; print('√ tui_app.py')" 2>nul || echo X tui_app.py 有问题

echo.
echo 检查配置档...
if exist config.json (
    python -c "import json; json.load(open('config.json'))" 2>nul && echo √ config.json 格式正确 || echo X config.json 格式错误
) else (
    echo X config.json 不存在
)

echo.
echo 测试完成！
echo.
echo 如果所有项目都显示 √，您可以执行：
echo   python tui_app.py
echo.
pause
