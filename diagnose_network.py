#!/usr/bin/env python3
"""
網絡診斷工具 - 檢查是否能訪問 HITCON 網站
"""

import sys
import os
import requests
import cloudscraper

def test_basic_connectivity():
    """測試基本網絡連接"""
    print("=" * 60)
    print("1. 測試基本網絡連接...")
    print("=" * 60)

    try:
        response = requests.get("https://google.com", timeout=5)
        print(f"✅ Google 可訪問 (狀態碼: {response.status_code})")
        return True
    except Exception as e:
        print(f"❌ 無網絡連接: {e}")
        return False


def test_hitcon_access():
    """測試 HITCON 網站訪問"""
    print("\n" + "=" * 60)
    print("2. 測試 HITCON 網站訪問...")
    print("=" * 60)

    url = "https://zeroday.hitcon.org/vulnerability/disclosed/page/1"

    # 測試 1: 使用 requests
    print("\n[測試 1] 使用 requests...")
    try:
        response = requests.get(url, timeout=10)
        print(f"狀態碼: {response.status_code}")
        if response.status_code == 200:
            print(f"✅ 成功！HTML 長度: {len(response.text)}")
            return True, response.text
        elif response.status_code == 403:
            print(f"❌ 403 Access Denied")
            print(f"響應內容: {response.text[:100]}")
        else:
            print(f"⚠️  非預期狀態碼")
    except Exception as e:
        print(f"❌ 請求失敗: {type(e).__name__}: {str(e)[:100]}")

    # 測試 2: 使用 cloudscraper
    print("\n[測試 2] 使用 cloudscraper (Chrome)...")
    try:
        scraper = cloudscraper.create_scraper(browser='chrome')
        response = scraper.get(url, timeout=10)
        print(f"狀態碼: {response.status_code}")
        if response.status_code == 200:
            print(f"✅ 成功！HTML 長度: {len(response.text)}")
            return True, response.text
        elif response.status_code == 403:
            print(f"❌ 403 Access Denied")
        else:
            print(f"⚠️  非預期狀態碼")
    except Exception as e:
        print(f"❌ 請求失敗: {type(e).__name__}: {str(e)[:100]}")

    # 測試 3: 嘗試繞過代理
    print("\n[測試 3] 嘗試繞過代理...")
    try:
        session = requests.Session()
        session.trust_env = False
        session.proxies = {'http': None, 'https': None}
        response = session.get(url, timeout=10)
        print(f"狀態碼: {response.status_code}")
        if response.status_code == 200:
            print(f"✅ 成功！HTML 長度: {len(response.text)}")
            return True, response.text
        elif response.status_code == 403:
            print(f"❌ 403 Access Denied")
        else:
            print(f"⚠️  非預期狀態碼")
    except Exception as e:
        print(f"❌ 請求失敗: {type(e).__name__}: {str(e)[:100]}")

    return False, None


def check_proxy_settings():
    """檢查代理設置"""
    print("\n" + "=" * 60)
    print("3. 檢查代理設置...")
    print("=" * 60)

    proxy_vars = ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY', 'no_proxy', 'NO_PROXY']

    has_proxy = False
    for var in proxy_vars:
        value = os.environ.get(var)
        if value:
            has_proxy = True
            print(f"{var} = {value[:80]}...")

    if not has_proxy:
        print("✅ 未檢測到代理設置")
    else:
        print("\n⚠️  檢測到代理設置")
        print("提示: 代理可能封鎖了 HITCON 網站")

    return has_proxy


def test_html_parsing(html):
    """測試 HTML 解析"""
    print("\n" + "=" * 60)
    print("4. 測試 HTML 解析...")
    print("=" * 60)

    import re
    pattern = re.compile(r'title tx-overflow-ellipsis"><a href="(.*?)">(.*?)</a>')
    matches = pattern.findall(html)

    if matches:
        print(f"✅ 找到 {len(matches)} 個漏洞")
        for i, (url, title) in enumerate(matches[:3], 1):
            print(f"\n漏洞 {i}:")
            print(f"  URL: {url}")
            print(f"  標題: {title[:60]}...")
        return True
    else:
        print("❌ 未找到漏洞數據")
        print("HTML 內容:")
        print(html[:500])
        return False


def main():
    """主函數"""
    print("\n" + "=" * 60)
    print("HITCON Vuls Crawler - 網絡診斷工具")
    print("=" * 60 + "\n")

    # 測試 1: 基本連接
    if not test_basic_connectivity():
        print("\n❌ 網絡連接失敗，請檢查網絡設置")
        return 1

    # 測試 2: 檢查代理
    has_proxy = check_proxy_settings()

    # 測試 3: HITCON 訪問
    success, html = test_hitcon_access()

    # 測試 4: HTML 解析
    if success and html:
        test_html_parsing(html)

    # 總結
    print("\n" + "=" * 60)
    print("診斷總結")
    print("=" * 60)

    if success:
        print("✅ HITCON 網站可訪問")
        print("✅ 爬蟲應該能正常工作")
        print("\n建議: 運行 'python tui_app.py' 查看真實數據")
    else:
        print("❌ HITCON 網站無法訪問")
        if has_proxy:
            print("\n可能原因: 代理封鎖了該網站")
            print("解決方案:")
            print("  1. 在本地環境（無代理）運行程式")
            print("  2. 配置代理白名單允許訪問 zeroday.hitcon.org")
            print("  3. 使用 VPN 繞過限制")
        else:
            print("\n可能原因: 網絡防火牆、地理位置限制、或網站封鎖")
            print("解決方案:")
            print("  1. 檢查防火牆設置")
            print("  2. 嘗試使用 VPN")
            print("  3. 聯繫網絡管理員")

        print("\n當前狀態: 程式會自動使用演示模式")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
