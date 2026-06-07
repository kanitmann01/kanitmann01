import os
import sys
import logging
from pathlib import Path

from rss_fetcher import fetch_latest_posts
from commit_analyzer import analyze_recent_commits
from activity_stream import generate_activity_stream

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
README_PATH = REPO_ROOT / "Readme.md"

BLOG_START = "<!-- BLOG_POSTS_START -->"
BLOG_END = "<!-- BLOG_POSTS_END -->"
COMMITS_START = "<!-- COMMITS_START -->"
COMMITS_END = "<!-- COMMITS_END -->"
ACTIVITY_START = "<!-- ACTIVITY_START -->"
ACTIVITY_END = "<!-- ACTIVITY_END -->"

DEFAULT_USERNAME = "kanitmann01"
DEFAULT_DAYS = 30


def _replace_section(template: str, start_marker: str, end_marker: str, content: str) -> str:
    start_idx = template.find(start_marker)
    end_idx = template.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        logger.warning("Marker pair not found: %s / %s", start_marker, end_marker)
        return template

    replacement = f"{start_marker}\n{content}\n{end_marker}"
    return template[:start_idx] + replacement + template[end_idx + len(end_marker):]


def _safe_fetch_blog() -> str:
    try:
        result = fetch_latest_posts()
        logger.info("Blog posts fetched successfully")
        return result
    except Exception as exc:
        logger.warning("Failed to fetch blog posts: %s", exc)
        return "## 📝 Latest Blog Posts\n\nNo recent posts available.\n"


def _safe_fetch_commits(username: str, days: int) -> str:
    try:
        result = analyze_recent_commits(username, days=days)
        logger.info("Commit analysis completed successfully")
        return result
    except Exception as exc:
        logger.warning("Failed to analyze commits: %s", exc)
        return "## 🔨 What I've Been Building\n\nNo recent activity to show. Working on something cool behind the scenes!\n"


def _safe_fetch_activity(username: str) -> str:
    try:
        result = generate_activity_stream(username=username)
        logger.info("Activity stream generated successfully")
        return result
    except Exception as exc:
        logger.warning("Failed to generate activity stream: %s", exc)
        return "## ⚡ Recent Activity\n\nNo recent activity to show.\n"


def generate_readme(
    readme_path: Path = README_PATH,
    username: str = DEFAULT_USERNAME,
    days: int = DEFAULT_DAYS,
    blog_content: str = None,
    commits_content: str = None,
    activity_content: str = None,
) -> str:
    template = readme_path.read_text(encoding="utf-8")

    if blog_content is None:
        blog_content = _safe_fetch_blog()

    if commits_content is None:
        commits_content = _safe_fetch_commits(username, days)

    if activity_content is None:
        activity_content = _safe_fetch_activity(username)

    updated = _replace_section(template, BLOG_START, BLOG_END, blog_content.strip())
    updated = _replace_section(updated, COMMITS_START, COMMITS_END, commits_content.strip())
    updated = _replace_section(updated, ACTIVITY_START, ACTIVITY_END, activity_content.strip())

    return updated


def write_readme(content: str, readme_path: Path = README_PATH) -> Path:
    readme_path.write_text(content, encoding="utf-8")
    logger.info("README written to %s", readme_path)
    return readme_path


def run_pipeline(
    readme_path: Path = README_PATH,
    username: str = DEFAULT_USERNAME,
    days: int = DEFAULT_DAYS,
) -> str:
    logger.info("Starting README update pipeline")
    content = generate_readme(readme_path=readme_path, username=username, days=days)
    write_readme(content, readme_path=readme_path)
    logger.info("Pipeline complete")
    return content


if __name__ == "__main__":
    username = DEFAULT_USERNAME
    days = DEFAULT_DAYS

    if len(sys.argv) > 1:
        username = sys.argv[1]
    if len(sys.argv) > 2:
        try:
            days = int(sys.argv[2])
        except ValueError:
            pass

    result = run_pipeline(username=username, days=days)
    print(f"\nREADME updated successfully ({len(result)} characters)")
