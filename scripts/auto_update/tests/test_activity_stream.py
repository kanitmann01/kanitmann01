import sys
import os
import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch, MagicMock, Mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from activity_stream import (
    fetch_recent_commits,
    fetch_recent_blog_posts,
    fetch_project_updates,
    merge_activities,
    format_activity_markdown,
    generate_activity_stream,
    _parse_iso_timestamp,
    _parse_rss_date,
    MAX_ACTIVITIES,
)


@pytest.fixture
def sample_github_commits():
    return [
        {
            "sha": "abc1234567890",
            "commit": {
                "message": "Fix bug in parser",
                "author": {"name": "kanitmann", "date": "2026-06-01T10:00:00Z"},
            },
            "repository": {
                "full_name": "kanitmann01/project-alpha",
                "language": "Python",
                "html_url": "https://github.com/kanitmann01/project-alpha",
            },
        },
        {
            "sha": "def4567890123",
            "commit": {
                "message": "Add new feature",
                "author": {"name": "kanitmann", "date": "2026-06-03T14:00:00Z"},
            },
            "repository": {
                "full_name": "kanitmann01/project-alpha",
                "language": "Python",
                "html_url": "https://github.com/kanitmann01/project-alpha",
            },
        },
    ]


@pytest.fixture
def sample_activities():
    return [
        {
            "type": "commit",
            "timestamp": datetime(2026, 6, 3, 14, 0, tzinfo=timezone.utc),
            "description": "Committed to `kanitmann01/project-alpha`: Add new feature",
            "link": "https://github.com/kanitmann01/project-alpha/commit/abc1234",
        },
        {
            "type": "blog_post",
            "timestamp": datetime(2026, 6, 2, 12, 0, tzinfo=timezone.utc),
            "description": "Published blog post: My Latest Post",
            "link": "https://kanit.codes/my-latest-post",
        },
        {
            "type": "project_update",
            "timestamp": datetime(2026, 6, 1, 10, 0, tzinfo=timezone.utc),
            "description": "Updated `kanitmann01/capstone`: Initial setup",
            "link": "https://github.com/kanitmann01/capstone/commit/def5678",
        },
    ]


@pytest.fixture
def sample_rss_content():
    return b"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Test Blog</title>
    <item>
      <title>Recent Post</title>
      <link>https://kanit.codes/recent-post</link>
      <pubDate>Wed, 04 Jun 2026 12:00:00 GMT</pubDate>
    </item>
    <item>
      <title>Old Post</title>
      <link>https://kanit.codes/old-post</link>
      <pubDate>Mon, 01 Jan 2024 12:00:00 GMT</pubDate>
    </item>
  </channel>
</rss>"""


class TestParseIsoTimestamp:
    def test_valid_iso_with_z(self):
        result = _parse_iso_timestamp("2026-06-01T10:00:00Z")
        assert result is not None
        assert result.year == 2026
        assert result.month == 6
        assert result.day == 1

    def test_valid_iso_with_offset(self):
        result = _parse_iso_timestamp("2026-06-01T10:00:00+00:00")
        assert result is not None

    def test_empty_string(self):
        assert _parse_iso_timestamp("") is None

    def test_none(self):
        assert _parse_iso_timestamp(None) is None

    def test_invalid_format(self):
        assert _parse_iso_timestamp("not-a-date") is None


class TestParseRssDate:
    def test_valid_rss_date(self):
        result = _parse_rss_date("Wed, 04 Jun 2026 12:00:00 GMT")
        assert result is not None
        assert result.year == 2026

    def test_empty_string(self):
        assert _parse_rss_date("") is None

    def test_none(self):
        assert _parse_rss_date(None) is None

    def test_invalid_format(self):
        assert _parse_rss_date("not-a-date") is None


class TestFetchRecentCommits:
    @patch("activity_stream.fetch_commits")
    def test_returns_activity_list(self, mock_fetch, sample_github_commits):
        mock_fetch.return_value = sample_github_commits

        activities = fetch_recent_commits(days=7, username="kanitmann01")

        assert len(activities) == 2
        assert all(a["type"] == "commit" for a in activities)
        assert all("kanitmann01/project-alpha" in a["description"] for a in activities)

    @patch("activity_stream.fetch_commits")
    def test_commit_has_link(self, mock_fetch, sample_github_commits):
        mock_fetch.return_value = sample_github_commits

        activities = fetch_recent_commits(days=7)

        assert activities[0]["link"].startswith("https://github.com/")
        assert "/commit/" in activities[0]["link"]

    @patch("activity_stream.fetch_commits")
    def test_empty_commits(self, mock_fetch):
        mock_fetch.return_value = []

        activities = fetch_recent_commits(days=7)
        assert activities == []

    @patch("activity_stream.fetch_commits")
    def test_skips_invalid_dates(self, mock_fetch):
        mock_fetch.return_value = [
            {
                "sha": "abc123",
                "commit": {
                    "message": "test",
                    "author": {"name": "user", "date": ""},
                },
                "repository": {
                    "full_name": "user/repo",
                    "html_url": "https://github.com/user/repo",
                },
            }
        ]

        activities = fetch_recent_commits(days=7)
        assert len(activities) == 0

    @patch("activity_stream.fetch_commits")
    def test_truncates_multiline_messages(self, mock_fetch):
        mock_fetch.return_value = [
            {
                "sha": "abc1234567890",
                "commit": {
                    "message": "First line\nSecond line\nThird line",
                    "author": {"name": "user", "date": "2026-06-01T10:00:00Z"},
                },
                "repository": {
                    "full_name": "user/repo",
                    "html_url": "https://github.com/user/repo",
                },
            }
        ]

        activities = fetch_recent_commits(days=7)
        assert len(activities) == 1
        assert "First line" in activities[0]["description"]
        assert "Second line" not in activities[0]["description"]


class TestFetchRecentBlogPosts:
    @patch("activity_stream.requests.get")
    def test_returns_recent_posts(self, mock_get, sample_rss_content):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = sample_rss_content
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        activities = fetch_recent_blog_posts(days=30)

        assert len(activities) == 1
        assert activities[0]["type"] == "blog_post"
        assert "Recent Post" in activities[0]["description"]

    @patch("activity_stream.requests.get")
    def test_filters_old_posts(self, mock_get, sample_rss_content):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = sample_rss_content
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        activities = fetch_recent_blog_posts(days=30)

        assert all("Old Post" not in a["description"] for a in activities)

    @patch("activity_stream.requests.get")
    def test_handles_request_failure(self, mock_get):
        mock_get.side_effect = Exception("Connection failed")

        activities = fetch_recent_blog_posts(days=30)
        assert activities == []

    @patch("activity_stream.requests.get")
    def test_empty_feed(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel><title>Empty</title></channel></rss>"""
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        activities = fetch_recent_blog_posts(days=30)
        assert activities == []


class TestFetchProjectUpdates:
    @patch("activity_stream.requests.get")
    def test_returns_project_updates(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = [
            {
                "sha": "abc1234567890",
                "commit": {
                    "message": "Update README",
                    "author": {"name": "user", "date": "2026-06-05T10:00:00Z"},
                },
                "html_url": "https://github.com/kanitmann01/profile-kanitmann/commit/abc1234",
            }
        ]
        mock_get.return_value = mock_response

        activities = fetch_project_updates(
            days=7, repos=["kanitmann01/profile-kanitmann"]
        )

        assert len(activities) == 1
        assert activities[0]["type"] == "project_update"
        assert "profile-kanitmann" in activities[0]["description"]

    @patch("activity_stream.requests.get")
    def test_handles_api_failure(self, mock_get):
        mock_get.side_effect = Exception("API error")

        activities = fetch_project_updates(
            days=7, repos=["kanitmann01/profile-kanitmann"]
        )
        assert activities == []

    @patch("activity_stream.requests.get")
    def test_multiple_repos(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = [
            {
                "sha": "abc1234567890",
                "commit": {
                    "message": "test commit",
                    "author": {"name": "user", "date": "2026-06-05T10:00:00Z"},
                },
                "html_url": "https://github.com/user/repo/commit/abc1234",
            }
        ]
        mock_get.return_value = mock_response

        activities = fetch_project_updates(
            days=7, repos=["user/repo1", "user/repo2"]
        )

        assert len(activities) == 2
        assert mock_get.call_count == 2

    @patch("activity_stream.requests.get")
    def test_generates_fallback_link(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = [
            {
                "sha": "abc1234567890",
                "commit": {
                    "message": "test",
                    "author": {"name": "user", "date": "2026-06-05T10:00:00Z"},
                },
            }
        ]
        mock_get.return_value = mock_response

        activities = fetch_project_updates(days=7, repos=["user/repo"])

        assert "github.com/user/repo/commit/abc1234" in activities[0]["link"]


class TestMergeActivities:
    def test_sorts_by_timestamp_descending(self, sample_activities):
        commits = [sample_activities[0]]
        posts = [sample_activities[1]]
        updates = [sample_activities[2]]

        merged = merge_activities(commits, posts, updates)

        assert merged[0]["timestamp"] >= merged[1]["timestamp"]
        assert merged[1]["timestamp"] >= merged[2]["timestamp"]

    def test_limits_to_max(self):
        activities = [
            {
                "type": "commit",
                "timestamp": datetime(2026, 6, i + 1, tzinfo=timezone.utc),
                "description": f"Commit {i}",
                "link": "",
            }
            for i in range(20)
        ]

        merged = merge_activities(activities, [], [])
        assert len(merged) == MAX_ACTIVITIES

    def test_custom_limit(self):
        activities = [
            {
                "type": "commit",
                "timestamp": datetime(2026, 6, i + 1, tzinfo=timezone.utc),
                "description": f"Commit {i}",
                "link": "",
            }
            for i in range(5)
        ]

        merged = merge_activities(activities, [], [], limit=3)
        assert len(merged) == 3

    def test_empty_inputs(self):
        merged = merge_activities([], [], [])
        assert merged == []

    def test_mixed_types(self, sample_activities):
        merged = merge_activities(
            [sample_activities[0]],
            [sample_activities[1]],
            [sample_activities[2]],
        )
        types = [a["type"] for a in merged]
        assert "commit" in types
        assert "blog_post" in types
        assert "project_update" in types


class TestFormatActivityMarkdown:
    def test_header_present(self, sample_activities):
        md = format_activity_markdown(sample_activities)
        assert "## ⚡ Recent Activity" in md

    def test_shows_all_activities(self, sample_activities):
        md = format_activity_markdown(sample_activities)
        assert "project-alpha" in md
        assert "My Latest Post" in md
        assert "capstone" in md

    def test_type_icons(self, sample_activities):
        md = format_activity_markdown(sample_activities)
        assert "🔨" in md
        assert "📝" in md
        assert "🚀" in md

    def test_timestamps_formatted(self, sample_activities):
        md = format_activity_markdown(sample_activities)
        assert "Jun 03, 2026" in md
        assert "Jun 02, 2026" in md
        assert "Jun 01, 2026" in md

    def test_links_included(self, sample_activities):
        md = format_activity_markdown(sample_activities)
        assert "https://github.com/kanitmann01/project-alpha/commit/abc1234" in md
        assert "https://kanit.codes/my-latest-post" in md

    def test_last_updated_timestamp(self, sample_activities):
        generated_at = datetime(2026, 6, 5, 12, 30, tzinfo=timezone.utc)
        md = format_activity_markdown(sample_activities, generated_at=generated_at)
        assert "Last updated: 2026-06-05 12:30 UTC" in md

    def test_empty_activities(self):
        md = format_activity_markdown([])
        assert "## ⚡ Recent Activity" in md
        assert "No recent activity" in md
        assert "Last updated:" in md

    def test_activity_without_link(self):
        activities = [
            {
                "type": "commit",
                "timestamp": datetime(2026, 6, 1, tzinfo=timezone.utc),
                "description": "Some commit",
                "link": "",
            }
        ]
        md = format_activity_markdown(activities)
        assert "Some commit" in md

    def test_sorted_newest_first(self, sample_activities):
        md = format_activity_markdown(sample_activities)
        lines = md.split("\n")
        activity_lines = [l for l in lines if l.startswith("- ")]
        assert "Jun 03, 2026" in activity_lines[0]
        assert "Jun 01, 2026" in activity_lines[-1]


class TestGenerateActivityStream:
    @patch("activity_stream.fetch_project_updates")
    @patch("activity_stream.fetch_recent_blog_posts")
    @patch("activity_stream.fetch_recent_commits")
    def test_returns_markdown_string(
        self, mock_commits, mock_posts, mock_updates, sample_activities
    ):
        mock_commits.return_value = [sample_activities[0]]
        mock_posts.return_value = [sample_activities[1]]
        mock_updates.return_value = [sample_activities[2]]

        result = generate_activity_stream()

        assert "## ⚡ Recent Activity" in result
        assert "Last updated:" in result

    @patch("activity_stream.fetch_project_updates")
    @patch("activity_stream.fetch_recent_blog_posts")
    @patch("activity_stream.fetch_recent_commits")
    def test_handles_all_failures(self, mock_commits, mock_posts, mock_updates):
        mock_commits.return_value = []
        mock_posts.return_value = []
        mock_updates.return_value = []

        result = generate_activity_stream()

        assert "## ⚡ Recent Activity" in result
        assert "No recent activity" in result

    @patch("activity_stream.fetch_project_updates")
    @patch("activity_stream.fetch_recent_blog_posts")
    @patch("activity_stream.fetch_recent_commits")
    def test_passes_username(self, mock_commits, mock_posts, mock_updates):
        mock_commits.return_value = []
        mock_posts.return_value = []
        mock_updates.return_value = []

        generate_activity_stream(username="testuser")

        mock_commits.assert_called_once_with(days=7, username="testuser")

    @patch("activity_stream.fetch_project_updates")
    @patch("activity_stream.fetch_recent_blog_posts")
    @patch("activity_stream.fetch_recent_commits")
    def test_passes_custom_days(self, mock_commits, mock_posts, mock_updates):
        mock_commits.return_value = []
        mock_posts.return_value = []
        mock_updates.return_value = []

        generate_activity_stream(commit_days=14, blog_days=60)

        mock_commits.assert_called_once_with(days=14, username="kanitmann01")
        mock_posts.assert_called_once_with(days=60)
        mock_updates.assert_called_once_with(days=14, repos=None, username="kanitmann01")
