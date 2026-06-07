import pytest
from unittest.mock import patch, Mock
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rss_fetcher import fetch_latest_posts, parse_rss_feed, format_markdown


class TestParseRSSFeed:
    def test_parse_valid_rss_feed(self):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Test Blog</title>
    <item>
      <title>Article 1</title>
      <link>https://example.com/article1</link>
      <pubDate>Mon, 01 Jan 2024 12:00:00 GMT</pubDate>
      <description>Description 1</description>
    </item>
    <item>
      <title>Article 2</title>
      <link>https://example.com/article2</link>
      <pubDate>Tue, 02 Jan 2024 12:00:00 GMT</pubDate>
      <description>Description 2</description>
    </item>
  </channel>
</rss>"""
        
        entries = parse_rss_feed(mock_response.content)
        
        assert len(entries) == 2
        assert entries[0]['title'] == 'Article 2'
        assert entries[0]['link'] == 'https://example.com/article2'
        assert entries[1]['title'] == 'Article 1'
        assert entries[1]['link'] == 'https://example.com/article1'

    def test_parse_empty_rss_feed(self):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Test Blog</title>
  </channel>
</rss>"""
        
        entries = parse_rss_feed(mock_response.content)
        
        assert len(entries) == 0

    def test_parse_malformed_rss_feed(self):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Test Blog</title>
    <item>
      <title>Article 1</title>
      <link>https://example.com/article1</link>
    </item>
  </channel>
</rss>"""
        
        entries = parse_rss_feed(mock_response.content)
        
        assert len(entries) == 1
        assert entries[0]['title'] == 'Article 1'
        assert entries[0]['link'] == 'https://example.com/article1'
        assert 'date' in entries[0] or entries[0].get('date') is None


class TestFormatMarkdown:
    def test_format_empty_entries(self):
        markdown = format_markdown([])
        
        assert "📝 Latest Blog Posts" in markdown
        assert "No recent posts available." in markdown

    def test_format_single_entry(self):
        entries = [
            {
                'title': 'Test Article',
                'link': 'https://example.com/article',
                'date': '2024-01-01'
            }
        ]
        
        markdown = format_markdown(entries)
        
        assert "📝 Latest Blog Posts" in markdown
        assert "[Test Article](https://example.com/article)" in markdown
        assert "2024-01-01" in markdown

    def test_format_multiple_entries(self):
        entries = [
            {
                'title': 'Article 1',
                'link': 'https://example.com/article1',
                'date': '2024-01-01'
            },
            {
                'title': 'Article 2',
                'link': 'https://example.com/article2',
                'date': '2024-01-02'
            }
        ]
        
        markdown = format_markdown(entries)
        
        assert "📝 Latest Blog Posts" in markdown
        assert "[Article 1](https://example.com/article1)" in markdown
        assert "[Article 2](https://example.com/article2)" in markdown
        assert "2024-01-01" in markdown
        assert "2024-01-02" in markdown

    def test_format_entry_without_date(self):
        entries = [
            {
                'title': 'Test Article',
                'link': 'https://example.com/article'
            }
        ]
        
        markdown = format_markdown(entries)
        
        assert "[Test Article](https://example.com/article)" in markdown


class TestFetchLatestPosts:
    @patch('rss_fetcher.requests.get')
    def test_fetch_successful(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Test Blog</title>
    <item>
      <title>Article 1</title>
      <link>https://example.com/article1</link>
      <pubDate>Mon, 01 Jan 2024 12:00:00 GMT</pubDate>
      <description>Description 1</description>
    </item>
    <item>
      <title>Article 2</title>
      <link>https://example.com/article2</link>
      <pubDate>Tue, 02 Jan 2024 12:00:00 GMT</pubDate>
      <description>Description 2</description>
    </item>
    <item>
      <title>Article 3</title>
      <link>https://example.com/article3</link>
      <pubDate>Wed, 03 Jan 2024 12:00:00 GMT</pubDate>
      <description>Description 3</description>
    </item>
    <item>
      <title>Article 4</title>
      <link>https://example.com/article4</link>
      <pubDate>Thu, 04 Jan 2024 12:00:00 GMT</pubDate>
      <description>Description 4</description>
    </item>
  </channel>
</rss>"""
        mock_get.return_value = mock_response
        
        markdown = fetch_latest_posts()
        
        assert "📝 Latest Blog Posts" in markdown
        assert "[Article 4]" in markdown
        assert "[Article 3]" in markdown
        assert "[Article 2]" in markdown
        assert "[Article 1]" not in markdown
        assert mock_get.call_count == 1

    @patch('rss_fetcher.requests.get')
    def test_fetch_timeout_error(self, mock_get):
        import requests
        mock_get.side_effect = requests.exceptions.Timeout()
        
        markdown = fetch_latest_posts()
        
        assert "📝 Latest Blog Posts" in markdown
        assert "No recent posts available" in markdown

    @patch('rss_fetcher.requests.get')
    def test_fetch_connection_error(self, mock_get):
        import requests
        mock_get.side_effect = requests.exceptions.ConnectionError()
        
        markdown = fetch_latest_posts()
        
        assert "📝 Latest Blog Posts" in markdown
        assert "No recent posts available" in markdown

    @patch('rss_fetcher.requests.get')
    def test_fetch_http_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = Exception("404 Not Found")
        mock_get.return_value = mock_response
        
        markdown = fetch_latest_posts()
        
        assert "📝 Latest Blog Posts" in markdown
        assert "No recent posts available" in markdown

    @patch('rss_fetcher.requests.get')
    def test_fetch_selects_top_3(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Test Blog</title>
    <item>
      <title>Article 1</title>
      <link>https://example.com/article1</link>
      <pubDate>Mon, 01 Jan 2024 12:00:00 GMT</pubDate>
    </item>
    <item>
      <title>Article 2</title>
      <link>https://example.com/article2</link>
      <pubDate>Tue, 02 Jan 2024 12:00:00 GMT</pubDate>
    </item>
    <item>
      <title>Article 3</title>
      <link>https://example.com/article3</link>
      <pubDate>Wed, 03 Jan 2024 12:00:00 GMT</pubDate>
    </item>
  </channel>
</rss>"""
        mock_get.return_value = mock_response
        
        markdown = fetch_latest_posts()
        
        lines = markdown.split('\n')
        article_lines = [l for l in lines if l.strip().startswith('-')]
        assert len(article_lines) == 3
