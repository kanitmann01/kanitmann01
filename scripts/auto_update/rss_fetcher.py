import requests
import feedparser
from datetime import datetime
from typing import List, Dict


def parse_rss_feed(content: bytes) -> List[Dict]:
    feed = feedparser.parse(content)
    entries = []
    
    for entry in feed.entries:
        entry_data = {
            'title': entry.get('title', ''),
            'link': entry.get('link', ''),
            'date': entry.get('published', ''),
        }
        
        if entry_data['date']:
            try:
                parsed_date = feedparser._parse_date(entry_data['date'])
                if parsed_date:
                    entry_data['date'] = datetime(*parsed_date[:6]).strftime('%Y-%m-%d')
            except:
                pass
        
        entries.append(entry_data)
    
    entries.sort(key=lambda x: x.get('date', ''), reverse=True)
    
    return entries


def format_markdown(entries: List[Dict]) -> str:
    markdown = "## 📝 Latest Blog Posts\n\n"
    
    if not entries:
        markdown += "No recent posts available.\n"
        return markdown
    
    for entry in entries:
        title = entry.get('title', 'Untitled')
        link = entry.get('link', '#')
        date = entry.get('date', '')
        
        if date:
            markdown += f"- [{title}]({link}) ({date})\n"
        else:
            markdown += f"- [{title}]({link})\n"
    
    return markdown


def fetch_latest_posts(url: str = "https://kanit.codes/rss.xml", max_posts: int = 3) -> str:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        entries = parse_rss_feed(response.content)
        top_entries = entries[:max_posts]
        
        return format_markdown(top_entries)
    
    except requests.exceptions.Timeout:
        return format_markdown([])
    except requests.exceptions.ConnectionError:
        return format_markdown([])
    except requests.exceptions.HTTPError:
        return format_markdown([])
    except Exception:
        return format_markdown([])


if __name__ == "__main__":
    markdown = fetch_latest_posts()
    print(markdown)
