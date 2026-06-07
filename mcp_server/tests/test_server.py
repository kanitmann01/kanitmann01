import pytest
from mcp_server.server import get_projects, get_skills, get_experience


class TestGetProjects:
    def test_returns_list(self):
        result = get_projects()
        assert isinstance(result, list)

    def test_contains_brand_guard(self):
        result = get_projects()
        names = [p["name"] for p in result]
        assert "Brand Guard" in names

    def test_contains_kanit_codes(self):
        result = get_projects()
        names = [p["name"] for p in result]
        assert "kanit.codes" in names

    def test_each_project_has_required_fields(self):
        result = get_projects()
        required = {"name", "description", "tech_stack", "url"}
        for project in result:
            assert required.issubset(project.keys())

    def test_tech_stack_is_list(self):
        result = get_projects()
        for project in result:
            assert isinstance(project["tech_stack"], list)
            assert len(project["tech_stack"]) > 0

    def test_brand_guard_details(self):
        result = get_projects()
        bg = next(p for p in result if p["name"] == "Brand Guard")
        assert "FastAPI" in bg["tech_stack"]
        assert "Python" in bg["tech_stack"]
        assert "fake brand login detection" in bg["description"].lower() or "ml" in bg["description"].lower()

    def test_kanit_codes_details(self):
        result = get_projects()
        kc = next(p for p in result if p["name"] == "kanit.codes")
        assert "React" in kc["tech_stack"]
        assert "JavaScript" in kc["tech_stack"]

    def test_returns_two_projects(self):
        result = get_projects()
        assert len(result) == 2


class TestGetSkills:
    def test_returns_dict(self):
        result = get_skills()
        assert isinstance(result, dict)

    def test_has_required_categories(self):
        result = get_skills()
        required = {"Languages", "ML & Data Science", "Data Platforms & Cloud", "Visualization & BI", "Techniques"}
        assert required.issubset(result.keys())

    def test_each_category_is_list(self):
        result = get_skills()
        for category, skills in result.items():
            assert isinstance(skills, list), f"{category} should be a list"
            assert len(skills) > 0, f"{category} should not be empty"

    def test_languages_contains_python(self):
        result = get_skills()
        assert "Python" in result["Languages"]

    def test_ml_contains_pytorch(self):
        result = get_skills()
        assert "PyTorch" in result["ML & Data Science"]

    def test_cloud_contains_gcp(self):
        result = get_skills()
        assert "GCP" in result["Data Platforms & Cloud"]

    def test_visualization_contains_tableau(self):
        result = get_skills()
        assert "Tableau" in result["Visualization & BI"]

    def test_techniques_contains_etl(self):
        result = get_skills()
        has_etl = any("ETL" in s for s in result["Techniques"])
        assert has_etl


class TestGetExperience:
    def test_returns_list(self):
        result = get_experience()
        assert isinstance(result, list)

    def test_contains_netstar(self):
        result = get_experience()
        companies = [e["company"] for e in result]
        assert "NetSTAR" in companies

    def test_contains_ericsson(self):
        result = get_experience()
        companies = [e["company"] for e in result]
        assert "Ericsson" in companies

    def test_each_experience_has_required_fields(self):
        result = get_experience()
        required = {"company", "role", "dates", "description", "achievements"}
        for exp in result:
            assert required.issubset(exp.keys())

    def test_achievements_are_lists(self):
        result = get_experience()
        for exp in result:
            assert isinstance(exp["achievements"], list)
            assert len(exp["achievements"]) > 0

    def test_netstar_details(self):
        result = get_experience()
        ns = next(e for e in result if e["company"] == "NetSTAR")
        assert "ML Engineer" in ns["role"] or "ML" in ns["role"]
        assert len(ns["achievements"]) >= 2

    def test_ericsson_details(self):
        result = get_experience()
        er = next(e for e in result if e["company"] == "Ericsson")
        assert "Cloud" in er["role"] or "Infra" in er["role"]
        assert len(er["achievements"]) >= 2

    def test_returns_two_experiences(self):
        result = get_experience()
        assert len(result) == 2
