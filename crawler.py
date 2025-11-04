"""
HITCON Vulnerability Database Crawler
Handles fetching and parsing vulnerability data from zeroday.hitcon.org
"""

import re
import cloudscraper
from typing import List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Vulnerability:
    """Represents a vulnerability entry"""
    url: str
    title: str
    full_url: str

    def __init__(self, url: str, title: str):
        self.url = url
        self.title = title
        self.full_url = f'https://zeroday.hitcon.org{url}'


class HITCONVulsCrawler:
    """Crawler for HITCON vulnerability database"""

    BASE_URL = 'https://zeroday.hitcon.org/vulnerability/disclosed/page/{page}'
    TITLE_PATTERN = re.compile(r'title tx-overflow-ellipsis"><a href="(.*?)">(.*?)</a>')

    def __init__(self):
        """Initialize the crawler with cloudscraper"""
        self.scraper = cloudscraper.create_scraper(
            delay=300,
            browser={'custom': 'ScraperBot/1.0'}
        )
        self._cache = {}

    def fetch_page(self, page_num: int, use_cache: bool = True) -> Optional[str]:
        """
        Fetch a page from the vulnerability database

        Args:
            page_num: The page number to fetch
            use_cache: Whether to use cached results

        Returns:
            HTML content of the page or None if request failed
        """
        if use_cache and page_num in self._cache:
            return self._cache[page_num]

        try:
            url = self.BASE_URL.format(page=page_num)
            response = self.scraper.get(url, timeout=10)

            if response.status_code != 200:
                return None

            html = response.text
            if use_cache:
                self._cache[page_num] = html

            return html

        except Exception as e:
            print(f"Error fetching page {page_num}: {e}")
            return None

    def parse_vulnerabilities(self, html: str) -> List[Vulnerability]:
        """
        Parse vulnerabilities from HTML content

        Args:
            html: HTML content to parse

        Returns:
            List of Vulnerability objects
        """
        matches = self.TITLE_PATTERN.findall(html)
        return [Vulnerability(url=url, title=title) for url, title in matches]

    def get_vulnerabilities(self, page_num: int) -> List[Vulnerability]:
        """
        Get vulnerabilities for a specific page

        Args:
            page_num: The page number to fetch

        Returns:
            List of Vulnerability objects
        """
        html = self.fetch_page(page_num)
        if html is None:
            return []

        return self.parse_vulnerabilities(html)

    def clear_cache(self) -> None:
        """Clear the page cache"""
        self._cache.clear()

    def get_page_count(self) -> Optional[int]:
        """
        Attempt to determine the total number of pages
        (This is a placeholder - actual implementation would need to parse the pagination)

        Returns:
            Estimated page count or None if unknown
        """
        # This would require parsing the pagination elements from the page
        # For now, return None to indicate unknown
        return None


def export_vulnerabilities_to_file(
    vulnerabilities: List[Vulnerability],
    filename: str,
    mode: str = 'w'
) -> bool:
    """
    Export vulnerabilities to a text file

    Args:
        vulnerabilities: List of vulnerabilities to export
        filename: Output filename
        mode: File mode ('w' for write, 'a' for append)

    Returns:
        True if successful, False otherwise
    """
    try:
        with open(filename, mode, encoding='utf-8') as f:
            for vul in vulnerabilities:
                f.write(f'{vul.full_url} {vul.title}\n')
        return True
    except Exception as e:
        print(f"Error exporting to file: {e}")
        return False
