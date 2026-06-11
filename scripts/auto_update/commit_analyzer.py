import os
import sys
from datetime import datetime, timedelta, timezone

import requests


GITHUB_API_BASE = "https://api.github.com"
SEARCH_COMMITS_URL = f"{GITHUB_API_BASE}/search/commits"

KNOWN_REPOS = [
    "kanitmann01/kanitmann01",
    "kanitmann01/profile-kanitmann",
    "kanitmann01/capstone",
]


def fetch_commits(username, since_date, token=None):
    headers = {
        "Accept": "application/vnd.github.cloak-preview+json",
    }
    if token:
        headers["Authorization"] = f"token {token}"

    query = f"author:{username} committer-date:>={since_date}"
    params = {"q": query, "per_page": 100, "sort": "committer-date", "order": "desc"}

    try:
        resp = requests.get(SEARCH_COMMITS_URL, headers=headers, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data.get("items", [])
    except Exception:
        return []


def fetch_commits_from_repos(username, since_date, token=None):
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    all_commits = []
    for repo in KNOWN_REPOS:
        url = f"{GITHUB_API_BASE}/repos/{repo}/commits"
        params = {
            "author": username,
            "since": f"{since_date}T00:00:00Z",
            "per_page": 100,
        }
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=30)
            resp.raise_for_status()
            commits = resp.json()
            for commit in commits:
                commit["repository"] = {
                    "full_name": repo,
                    "html_url": f"https://github.com/{repo}",
                    "language": None,
                }
            all_commits.extend(commits)
        except Exception:
            continue

    return all_commits


def group_commits_by_repo(commits):
    grouped = {}
    for commit in commits:
        repo = commit.get("repository", {})
        full_name = repo.get("full_name", "unknown")
        language = repo.get("language") or "Unknown"
        url = repo.get("html_url", "")

        if full_name not in grouped:
            grouped[full_name] = {"count": 0, "language": language, "url": url}
        grouped[full_name]["count"] += 1

    return grouped


def get_repo_languages(grouped):
    languages = {}
    for info in grouped.values():
        lang = info["language"]
        if lang and lang != "Unknown":
            languages[lang] = languages.get(lang, 0) + 1
    return languages


def format_markdown(repo_data, languages, days):
    lines = []
    lines.append("## 🔨 What I've Been Building")
    lines.append("")
    lines.append(f"*Last {days} days*")
    lines.append("")

    if not repo_data:
        lines.append("No recent activity to show. Working on something cool behind the scenes!")
        lines.append("")
        return "\n".join(lines)

    sorted_repos = sorted(repo_data.items(), key=lambda x: x[1]["count"], reverse=True)

    lines.append("### Active Repositories")
    lines.append("")
    for repo_name, info in sorted_repos:
        short_name = repo_name.split("/")[-1] if "/" in repo_name else repo_name
        count = info["count"]
        lang = info["language"]
        url = info["url"]
        commit_word = "commit" if count == 1 else "commits"
        lang_str = f" `{lang}`" if lang != "Unknown" else ""
        lines.append(f"- [{repo_name}]({url}) — {count} {commit_word}{lang_str}")

    lines.append("")

    if languages:
        lines.append("### Languages")
        lines.append("")
        sorted_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)
        lang_list = ", ".join(f"**{lang}**" for lang, _ in sorted_langs)
        lines.append(f"Working with: {lang_list}")
        lines.append("")

    return "\n".join(lines)


def analyze_recent_commits(username, days=30):
    token = os.environ.get("GITHUB_TOKEN")
    since_date = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")

    search_commits = fetch_commits(username, since_date, token=token)
    repo_commits = fetch_commits_from_repos(username, since_date, token=token)

    seen_shas = set()
    all_commits = []
    for commit in search_commits + repo_commits:
        sha = commit.get("sha")
        if sha and sha not in seen_shas:
            seen_shas.add(sha)
            all_commits.append(commit)

    grouped = group_commits_by_repo(all_commits)
    languages = get_repo_languages(grouped)
    markdown = format_markdown(grouped, languages, days)

    return markdown


if __name__ == "__main__":
    username = "kanitmann01"
    if len(sys.argv) > 1:
        username = sys.argv[1]

    days = 30
    if len(sys.argv) > 2:
        try:
            days = int(sys.argv[2])
        except ValueError:
            pass

    print(f"Analyzing commits for {username} (last {days} days)...\n")
    result = analyze_recent_commits(username, days=days)
    print(result)
