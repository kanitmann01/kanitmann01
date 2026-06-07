import sys
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from integration import (
    generate_readme,
    write_readme,
    run_pipeline,
    _replace_section,
    BLOG_START,
    BLOG_END,
    COMMITS_START,
    COMMITS_END,
)


SAMPLE_TEMPLATE = f"""# Header

Some static content here.

{BLOG_START}
{BLOG_END}

Middle content.

{COMMITS_START}
{COMMITS_END}

Footer content.
"""


@pytest.fixture
def readme_file(tmp_path):
    readme = tmp_path / "Readme.md"
    readme.write_text(SAMPLE_TEMPLATE, encoding="utf-8")
    return readme


class TestReplaceSection:
    def test_replace_between_markers(self):
        template = f"before\n{BLOG_START}\n{BLOG_END}\nafter"
        result = _replace_section(template, BLOG_START, BLOG_END, "NEW CONTENT")
        assert "NEW CONTENT" in result
        assert "before" in result
        assert "after" in result

    def test_missing_start_marker(self):
        template = f"before\n{BLOG_END}\nafter"
        result = _replace_section(template, BLOG_START, BLOG_END, "CONTENT")
        assert result == template

    def test_missing_end_marker(self):
        template = f"before\n{BLOG_START}\nafter"
        result = _replace_section(template, BLOG_START, BLOG_END, "CONTENT")
        assert result == template

    def test_preserves_surrounding_content(self):
        template = f"TOP\n{BLOG_START}\n{BLOG_END}\nMIDDLE\n{COMMITS_START}\n{COMMITS_END}\nBOTTOM"
        result = _replace_section(template, BLOG_START, BLOG_END, "BLOG")
        result = _replace_section(result, COMMITS_START, COMMITS_END, "COMMITS")
        assert "TOP" in result
        assert "MIDDLE" in result
        assert "BOTTOM" in result
        assert "BLOG" in result
        assert "COMMITS" in result


class TestGenerateReadme:
    def test_inserts_blog_and_commits(self, readme_file):
        content = generate_readme(
            readme_path=readme_file,
            blog_content="## Blog\n- Post 1",
            commits_content="## Commits\n- Repo A",
        )
        assert "## Blog" in content
        assert "- Post 1" in content
        assert "## Commits" in content
        assert "- Repo A" in content

    def test_static_content_preserved(self, readme_file):
        content = generate_readme(
            readme_path=readme_file,
            blog_content="blog",
            commits_content="commits",
        )
        assert "# Header" in content
        assert "Some static content here." in content
        assert "Middle content." in content
        assert "Footer content." in content

    @patch("integration.fetch_latest_posts")
    def test_blog_failure_still_renders_commits(self, mock_blog, readme_file):
        mock_blog.side_effect = Exception("RSS down")
        content = generate_readme(
            readme_path=readme_file,
            commits_content="## Commits\n- Active repo",
        )
        assert "No recent posts available" in content
        assert "## Commits" in content
        assert "- Active repo" in content

    @patch("integration.analyze_recent_commits")
    def test_commits_failure_still_renders_blog(self, mock_commits, readme_file):
        mock_commits.side_effect = Exception("GitHub API down")
        content = generate_readme(
            readme_path=readme_file,
            blog_content="## Blog\n- Post 1",
        )
        assert "## Blog" in content
        assert "- Post 1" in content
        assert "No recent activity" in content

    @patch("integration.analyze_recent_commits")
    @patch("integration.fetch_latest_posts")
    def test_both_failures_still_produces_readme(self, mock_blog, mock_commits, readme_file):
        mock_blog.side_effect = Exception("RSS down")
        mock_commits.side_effect = Exception("GitHub down")
        content = generate_readme(readme_path=readme_file)
        assert "# Header" in content
        assert "Footer content." in content
        assert "No recent posts available" in content
        assert "No recent activity" in content

    @patch("integration.analyze_recent_commits")
    @patch("integration.fetch_latest_posts")
    def test_calls_with_correct_params(self, mock_blog, mock_commits, readme_file):
        mock_blog.return_value = "blog"
        mock_commits.return_value = "commits"
        generate_readme(readme_path=readme_file, username="testuser", days=14)
        mock_commits.assert_called_once_with("testuser", days=14)


class TestWriteReadme:
    def test_writes_content_to_file(self, tmp_path):
        target = tmp_path / "Readme.md"
        write_readme("# Hello", readme_path=target)
        assert target.read_text(encoding="utf-8") == "# Hello"

    def test_returns_path(self, tmp_path):
        target = tmp_path / "Readme.md"
        result = write_readme("content", readme_path=target)
        assert result == target


class TestRunPipeline:
    @patch("integration.analyze_recent_commits")
    @patch("integration.fetch_latest_posts")
    def test_full_pipeline_writes_file(self, mock_blog, mock_commits, readme_file):
        mock_blog.return_value = "## 📝 Latest Blog Posts\n\n- [Post](https://example.com)"
        mock_commits.return_value = "## 🔨 What I've Been Building\n\n- repo: 5 commits"

        result = run_pipeline(readme_path=readme_file)

        assert "## 📝 Latest Blog Posts" in result
        assert "## 🔨 What I've Been Building" in result
        assert "# Header" in result
        assert readme_file.read_text(encoding="utf-8") == result

    @patch("integration.analyze_recent_commits")
    @patch("integration.fetch_latest_posts")
    def test_pipeline_end_to_end(self, mock_blog, mock_commits, readme_file):
        mock_blog.return_value = "## 📝 Latest Blog Posts\n\n- [Article](https://blog.com)"
        mock_commits.return_value = "## 🔨 What I've Been Building\n\n- [user/repo](https://github.com) — 3 commits `Python`"

        content = run_pipeline(readme_path=readme_file, username="kanitmann01", days=30)

        assert "static content here" in content
        assert "[Article](https://blog.com)" in content
        assert "[user/repo]" in content
        assert "3 commits" in content
        assert "Footer content." in content
        assert BLOG_START in content
        assert BLOG_END in content
        assert COMMITS_START in content
        assert COMMITS_END in content
