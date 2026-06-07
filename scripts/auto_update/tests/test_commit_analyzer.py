import pytest
import os
import sys
from datetime import datetime, timedelta, timezone
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from commit_analyzer import (
    fetch_commits,
    group_commits_by_repo,
    get_repo_languages,
    format_markdown,
    analyze_recent_commits,
)


@pytest.fixture
def sample_search_response():
    return {
        "total_count": 5,
        "items": [
            {
                "sha": "abc123",
                "commit": {
                    "message": "Fix bug in parser",
                    "author": {"name": "kanitmann", "date": "2026-05-15T10:00:00Z"},
                },
                "repository": {
                    "full_name": "kanitmann01/project-alpha",
                    "language": "Python",
                    "html_url": "https://github.com/kanitmann01/project-alpha",
                },
            },
            {
                "sha": "def456",
                "commit": {
                    "message": "Add new feature",
                    "author": {"name": "kanitmann", "date": "2026-05-20T14:00:00Z"},
                },
                "repository": {
                    "full_name": "kanitmann01/project-alpha",
                    "language": "Python",
                    "html_url": "https://github.com/kanitmann01/project-alpha",
                },
            },
            {
                "sha": "ghi789",
                "commit": {
                    "message": "Update README",
                    "author": {"name": "kanitmann", "date": "2026-05-18T09:00:00Z"},
                },
                "repository": {
                    "full_name": "kanitmann01/project-beta",
                    "language": "JavaScript",
                    "html_url": "https://github.com/kanitmann01/project-beta",
                },
            },
            {
                "sha": "jkl012",
                "commit": {
                    "message": "Refactor utils",
                    "author": {"name": "kanitmann", "date": "2026-05-22T16:00:00Z"},
                },
                "repository": {
                    "full_name": "kanitmann01/project-beta",
                    "language": "JavaScript",
                    "html_url": "https://github.com/kanitmann01/project-beta",
                },
            },
            {
                "sha": "mno345",
                "commit": {
                    "message": "Setup CI pipeline",
                    "author": {"name": "kanitmann", "date": "2026-05-25T11:00:00Z"},
                },
                "repository": {
                    "full_name": "kanitmann01/project-gamma",
                    "language": "TypeScript",
                    "html_url": "https://github.com/kanitmann01/project-gamma",
                },
            },
        ],
    }


@pytest.fixture
def empty_search_response():
    return {"total_count": 0, "items": []}


@pytest.fixture
def mock_rate_limit_response():
    mock_resp = MagicMock()
    mock_resp.status_code = 403
    mock_resp.json.return_value = {
        "message": "API rate limit exceeded",
        "documentation_url": "https://docs.github.com/rest/overview/resources-in-the-rest-api#rate-limiting",
    }
    mock_resp.raise_for_status.side_effect = Exception("403 Client Error: rate limit exceeded")
    return mock_resp


class TestFetchCommits:
    @patch("commit_analyzer.requests.get")
    def test_fetch_commits_success(self, mock_get, sample_search_response):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = sample_search_response
        mock_resp.raise_for_status.return_value = None
        mock_get.return_value = mock_resp

        commits = fetch_commits("kanitmann01", "2026-05-01")

        assert len(commits) == 5
        mock_get.assert_called_once()
        call_kwargs = mock_get.call_args
        params = call_kwargs[1]["params"]
        assert "kanitmann01" in params["q"]

    @patch("commit_analyzer.requests.get")
    def test_fetch_commits_empty(self, mock_get, empty_search_response):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = empty_search_response
        mock_resp.raise_for_status.return_value = None
        mock_get.return_value = mock_resp

        commits = fetch_commits("kanitmann01", "2026-05-01")
        assert len(commits) == 0

    @patch("commit_analyzer.requests.get")
    def test_fetch_commits_rate_limit(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 403
        mock_resp.raise_for_status.side_effect = Exception("403 Client Error")
        mock_get.return_value = mock_resp

        commits = fetch_commits("kanitmann01", "2026-05-01")
        assert commits == []

    @patch("commit_analyzer.requests.get")
    def test_fetch_commits_with_token(self, mock_get, sample_search_response):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = sample_search_response
        mock_resp.raise_for_status.return_value = None
        mock_get.return_value = mock_resp

        fetch_commits("kanitmann01", "2026-05-01", token="test_token")

        call_kwargs = mock_get.call_args
        assert call_kwargs[1]["headers"]["Authorization"] == "token test_token"

    @patch("commit_analyzer.requests.get")
    def test_fetch_commits_includes_date_filter(self, mock_get, sample_search_response):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = sample_search_response
        mock_resp.raise_for_status.return_value = None
        mock_get.return_value = mock_resp

        fetch_commits("kanitmann01", "2026-05-01")

        call_kwargs = mock_get.call_args
        params = call_kwargs[1]["params"]
        assert "2026-05-01" in params["q"]


class TestGroupCommitsByRepo:
    def test_group_commits_basic(self, sample_search_response):
        commits = sample_search_response["items"]
        grouped = group_commits_by_repo(commits)

        assert "kanitmann01/project-alpha" in grouped
        assert "kanitmann01/project-beta" in grouped
        assert "kanitmann01/project-gamma" in grouped

    def test_group_commits_counts(self, sample_search_response):
        commits = sample_search_response["items"]
        grouped = group_commits_by_repo(commits)

        assert grouped["kanitmann01/project-alpha"]["count"] == 2
        assert grouped["kanitmann01/project-beta"]["count"] == 2
        assert grouped["kanitmann01/project-gamma"]["count"] == 1

    def test_group_commits_language(self, sample_search_response):
        commits = sample_search_response["items"]
        grouped = group_commits_by_repo(commits)

        assert grouped["kanitmann01/project-alpha"]["language"] == "Python"
        assert grouped["kanitmann01/project-beta"]["language"] == "JavaScript"

    def test_group_commits_empty(self):
        grouped = group_commits_by_repo([])
        assert grouped == {}

    def test_group_commits_unknown_language(self):
        commits = [
            {
                "sha": "abc",
                "commit": {
                    "message": "test",
                    "author": {"name": "user", "date": "2026-05-15T10:00:00Z"},
                },
                "repository": {
                    "full_name": "user/repo",
                    "language": None,
                    "html_url": "https://github.com/user/repo",
                },
            }
        ]
        grouped = group_commits_by_repo(commits)
        assert grouped["user/repo"]["language"] == "Unknown"


class TestGetRepoLanguages:
    def test_get_languages_from_grouped(self, sample_search_response):
        commits = sample_search_response["items"]
        grouped = group_commits_by_repo(commits)
        languages = get_repo_languages(grouped)

        assert "Python" in languages
        assert "JavaScript" in languages
        assert "TypeScript" in languages

    def test_get_languages_counts(self, sample_search_response):
        commits = sample_search_response["items"]
        grouped = group_commits_by_repo(commits)
        languages = get_repo_languages(grouped)

        assert languages["Python"] == 1
        assert languages["JavaScript"] == 1
        assert languages["TypeScript"] == 1

    def test_get_languages_empty(self):
        languages = get_repo_languages({})
        assert languages == {}

    def test_get_languages_excludes_unknown(self):
        grouped = {
            "user/repo": {"count": 1, "language": "Unknown", "url": "https://github.com/user/repo"}
        }
        languages = get_repo_languages(grouped)
        assert "Unknown" not in languages


class TestFormatMarkdown:
    def test_format_markdown_basic(self):
        repo_data = {
            "kanitmann01/project-alpha": {
                "count": 5,
                "language": "Python",
                "url": "https://github.com/kanitmann01/project-alpha",
            },
            "kanitmann01/project-beta": {
                "count": 3,
                "language": "JavaScript",
                "url": "https://github.com/kanitmann01/project-beta",
            },
        }
        languages = {"Python": 1, "JavaScript": 1}

        md = format_markdown(repo_data, languages, 30)

        assert "🔨 What I've Been Building" in md
        assert "project-alpha" in md
        assert "project-beta" in md
        assert "5 commits" in md
        assert "3 commits" in md
        assert "Python" in md
        assert "JavaScript" in md
        assert "Last 30 days" in md

    def test_format_markdown_empty(self):
        md = format_markdown({}, {}, 30)
        assert "🔨 What I've Been Building" in md
        assert "No recent activity" in md.lower() or "no recent" in md.lower()

    def test_format_markdown_sorted_by_commits(self):
        repo_data = {
            "user/low": {"count": 1, "language": "Python", "url": "https://github.com/user/low"},
            "user/high": {"count": 10, "language": "Go", "url": "https://github.com/user/high"},
        }
        languages = {"Python": 1, "Go": 1}

        md = format_markdown(repo_data, languages, 30)
        high_pos = md.index("user/high")
        low_pos = md.index("user/low")
        assert high_pos < low_pos

    def test_format_markdown_language_summary(self):
        repo_data = {
            "user/repo1": {"count": 3, "language": "Python", "url": "https://github.com/user/repo1"},
            "user/repo2": {"count": 2, "language": "Python", "url": "https://github.com/user/repo2"},
            "user/repo3": {"count": 1, "language": "Rust", "url": "https://github.com/user/repo3"},
        }
        languages = {"Python": 2, "Rust": 1}

        md = format_markdown(repo_data, languages, 30)
        assert "Python" in md
        assert "Rust" in md


class TestAnalyzeRecentCommits:
    @patch("commit_analyzer.fetch_commits")
    def test_analyze_returns_markdown(self, mock_fetch, sample_search_response):
        mock_fetch.return_value = sample_search_response["items"]

        md = analyze_recent_commits("kanitmann01", days=30)

        assert "🔨 What I've Been Building" in md
        assert "project-alpha" in md
        mock_fetch.assert_called_once()

    @patch("commit_analyzer.fetch_commits")
    def test_analyze_empty_data(self, mock_fetch):
        mock_fetch.return_value = []

        md = analyze_recent_commits("kanitmann01", days=30)

        assert "🔨 What I've Been Building" in md

    @patch("commit_analyzer.fetch_commits")
    def test_analyze_respects_days_parameter(self, mock_fetch, sample_search_response):
        mock_fetch.return_value = sample_search_response["items"]

        analyze_recent_commits("kanitmann01", days=7)

        call_args = mock_fetch.call_args
        since_date = call_args[0][1]
        expected_date = (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%d")
        assert since_date == expected_date

    @patch("commit_analyzer.fetch_commits")
    def test_analyze_passes_token(self, mock_fetch, sample_search_response):
        mock_fetch.return_value = sample_search_response["items"]

        with patch.dict(os.environ, {"GITHUB_TOKEN": "test_token"}):
            analyze_recent_commits("kanitmann01", days=30)

        call_kwargs = mock_fetch.call_args
        assert call_kwargs[1].get("token") == "test_token" or (
            len(call_kwargs[0]) > 2 and call_kwargs[0][2] == "test_token"
        )

    @patch("commit_analyzer.fetch_commits")
    def test_analyze_without_token(self, mock_fetch, sample_search_response):
        mock_fetch.return_value = sample_search_response["items"]

        env = os.environ.copy()
        env.pop("GITHUB_TOKEN", None)
        with patch.dict(os.environ, env, clear=True):
            md = analyze_recent_commits("kanitmann01", days=30)

        assert "🔨 What I've Been Building" in md
