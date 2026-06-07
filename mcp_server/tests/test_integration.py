import json
import subprocess
import sys
import time

import pytest


class TestIntegration:
    def test_server_module_imports(self):
        from mcp_server.server import mcp, get_projects, get_skills, get_experience, get_availability
        assert mcp is not None

    def test_all_tools_registered(self):
        from mcp_server.server import mcp
        tool_names = {t.name for t in mcp._tool_manager.list_tools()}
        assert "projects" in tool_names
        assert "skills" in tool_names
        assert "experience" in tool_names
        assert "availability" in tool_names

    def test_tools_return_valid_json(self):
        from mcp_server.server import projects, skills, experience, availability
        for tool_fn in [projects, skills, experience, availability]:
            result = tool_fn()
            parsed = json.loads(result)
            assert parsed is not None

    def test_server_process_starts(self):
        proc = subprocess.Popen(
            [sys.executable, "-m", "mcp_server.server"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
        )
        time.sleep(2)
        assert proc.poll() is None, "Server process exited unexpectedly"
        proc.terminate()
        proc.wait(timeout=5)
