import os
import sys
import logging
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from typing import List, Dict, Optional

import requests
import feedparser

from commit_analyzer import fetch_commits

logger = logging.getLogger(__name__)

GITHUB_API_BASE = "https://api.github.com"
DEFAULT_USERNAME = "kanitmann01"
FEATURED_REPOS = ["kanitmann01/profile-kanitmann", "kanitmann01/capstone"]
MAX_ACTIVITIES = 10
BLOG_RSS_URL = "https://kanit.codes/rss.xml"


def fetch_recent_commits(days: int = 7, username: str = DEFAULT_USERNAME) -> List[Dict]:
    token = os.environ.get("GITHUB_TOKEN")
    since_date = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")

    raw_commits = fetch_commits(username, since_date, token=token)

    activities = []
    for commit in raw_commits:
        commit_data = commit.get("commit", {})
        repo = commit.get("repository", {})
        author_date = commit_data.get("author", {}).get("date", "")

        timestamp = _parse_iso_timestamp(author_date)
        if timestamp is None:
            continue

        message = commit_data.get("message", "").split("\n")[0]
        repo_name = repo.get("full_name", "unknown")
        repo_url = repo.get("html_url", "")
        commit_sha = commit.get("sha", "")[:7]
        commit_url = f"{repo_url}/commit/{commit_sha}" if repo_url and commit_sha else ""

        activities.append({
            "type": "commit",
            "timestamp": timestamp,
            "description": f"Committed to `{repo_name}`: {message}",
            "link": commit_url,
        })

    return activities


def fetch_recent_blog_posts(days: int = 30, url: str = BLOG_RSS_URL) -> List[Dict]:
    activities = []
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as exc:
        logger.warning("Failed to fetch RSS feed: %s", exc)
        return activities

    feed = feedparser.parse(response.content)
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)

    for entry in feed.entries:
        title = entry.get("title", "Untitled")
        link = entry.get("link", "")
        date_str = entry.get("published", "")

        timestamp = _parse_rss_date(date_str)
        if timestamp is None:
            continue

        if timestamp < cutoff:
            continue

        activities.append({
            "type": "blog_post",
            "timestamp": timestamp,
            "description": f"Published blog post: {title}",
            "link": link,
        })

    return activities


def fetch_project_updates(
    days: int = 7,
    repos: Optional[List[str]] = None,
    username: str = DEFAULT_USERNAME,
) -> List[Dict]:
    if repos is None:
        repos = FEATURED_REPOS

    token = os.environ.get("GITHUB_TOKEN")
    since_date = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")
    activities = []

    for repo_full_name in repos:
        owner, repo_name = repo_full_name.split("/")
        commits_url = f"{GITHUB_API_BASE}/repos/{owner}/{repo_name}/commits"

        headers = {"Accept": "application/vnd.github.v3+json"}
        if token:
            headers["Authorization"] = f"token {token}"

        params = {"since": f"{since_date}T00:00:00Z", "per_page": 10}

        try:
            resp = requests.get(commits_url, headers=headers, params=params, timeout=30)
            resp.raise_for_status()
            commits = resp.json()
        except Exception as exc:
            logger.warning("Failed to fetch commits for %s: %s", repo_full_name, exc)
            continue

        for commit in commits:
            commit_data = commit.get("commit", {})
            author_date = commit_data.get("author", {}).get("date", "")
            timestamp = _parse_iso_timestamp(author_date)
            if timestamp is None:
                continue

            message = commit_data.get("message", "").split("\n")[0]
            sha = commit.get("sha", "")[:7]
            html_url = commit.get("html_url", "")
            if not html_url:
                html_url = f"https://github.com/{repo_full_name}/commit/{sha}"

            activities.append({
                "type": "project_update",
                "timestamp": timestamp,
                "description": f"Updated `{repo_full_name}`: {message}",
                "link": html_url,
            })

    return activities


def merge_activities(
    commits: List[Dict],
    posts: List[Dict],
    updates: List[Dict],
    limit: int = MAX_ACTIVITIES,
) -> List[Dict]:
    all_activities = commits + posts + updates
    all_activities.sort(key=lambda a: a.get("timestamp"), reverse=True)
    return all_activities[:limit]


def format_activity_markdown(activities: List[Dict], generated_at: Optional[datetime] = None) -> str:
    if generated_at is None:
        generated_at = datetime.now(timezone.utc)

    lines = []
    lines.append("## ⚡ Recent Activity")
    lines.append("")

    if not activities:
        lines.append("No recent activity to show.")
        lines.append("")
        lines.append(f"*Last updated: {generated_at.strftime('%Y-%m-%d %H:%M UTC')}*")
        return "\n".join(lines)

    type_icons = {
        "commit": "🔨",
        "blog_post": "📝",
        "project_update": "🚀",
    }

    for activity in activities:
        icon = type_icons.get(activity["type"], "📌")
        ts = activity["timestamp"]
        time_str = ts.strftime("%b %d, %Y")
        desc = activity["description"]
        link = activity.get("link", "")

        if link:
            lines.append(f"- {icon} **{time_str}** — [{desc}]({link})")
        else:
            lines.append(f"- {icon} **{time_str}** — {desc}")

    lines.append("")
    lines.append(f"*Last updated: {generated_at.strftime('%Y-%m-%d %H:%M UTC')}*")
    return "\n".join(lines)


def generate_activity_stream(
    username: str = DEFAULT_USERNAME,
    commit_days: int = 7,
    blog_days: int = 30,
    featured_repos: Optional[List[str]] = None,
) -> str:
    commits = _safe_fetch_recent_commits(commit_days, username)
    posts = _safe_fetch_recent_blog_posts(blog_days)
    updates = _safe_fetch_project_updates(commit_days, featured_repos, username)

    merged = merge_activities(commits, posts, updates)
    return format_activity_markdown(merged)


def _safe_fetch_recent_commits(days: int, username: str) -> List[Dict]:
    try:
        return fetch_recent_commits(days=days, username=username)
    except Exception as exc:
        logger.warning("Failed to fetch recent commits: %s", exc)
        return []


def _safe_fetch_recent_blog_posts(days: int) -> List[Dict]:
    try:
        return fetch_recent_blog_posts(days=days)
    except Exception as exc:
        logger.warning("Failed to fetch blog posts: %s", exc)
        return []


def _safe_fetch_project_updates(
    days: int,
    repos: Optional[List[str]],
    username: str,
) -> List[Dict]:
    try:
        return fetch_project_updates(days=days, repos=repos, username=username)
    except Exception as exc:
        logger.warning("Failed to fetch project updates: %s", exc)
        return []


def _parse_iso_timestamp(date_str: str) -> Optional[datetime]:
    if not date_str:
        return None
    try:
        date_str = date_str.replace("Z", "+00:00")
        return datetime.fromisoformat(date_str)
    except (ValueError, TypeError):
        return None


def _parse_rss_date(date_str: str) -> Optional[datetime]:
    if not date_str:
        return None
    try:
        dt = parsedate_to_datetime(date_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        pass
    return None


if __name__ == "__main__":
    username = DEFAULT_USERNAME
    if len(sys.argv) > 1:
        username = sys.argv[1]

    print(f"Generating activity stream for {username}...\n")
    result = generate_activity_stream(username=username)
    print(result)
