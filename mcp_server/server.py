"""
MCP Server for Kanit Mann's profile.

Exposes structured data about projects, skills, and experience
for AI assistants to query via the Model Context Protocol.
"""

import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("kanitmann01-profile")


def get_projects() -> list[dict]:
    """
    Returns a list of featured projects with descriptions, tech stacks, and links.

    Each project contains:
      - name (str): Project name
      - description (str): Short description of the project
      - tech_stack (list[str]): Technologies used
      - url (str): Project URL or link

    Returns:
        list[dict]: List of project dictionaries.
    """
    return [
        {
            "name": "Brand Guard",
            "description": (
                "FastAPI capstone for fake brand login detection. "
                "ML-powered system that detects fraudulent login pages "
                "impersonating legitimate brands, built with a FastAPI backend "
                "and ML classification pipeline."
            ),
            "tech_stack": ["FastAPI", "Python", "Scikit-Learn"],
            "url": "https://github.com/kanitmann01",
        },
        {
            "name": "kanit.codes",
            "description": (
                "Personal portfolio with tactile feedback system. "
                "Interactive portfolio website featuring a unique tactile "
                "feedback system for enhanced user engagement and accessibility."
            ),
            "tech_stack": ["React", "JavaScript", "CSS3"],
            "url": "https://kanit.codes",
        },
    ]


def get_skills() -> dict[str, list[str]]:
    """
    Returns categorized tech stack as a dictionary.

    Categories:
      - Languages: Programming languages (Python, SQL, C++, JavaScript, R)
      - ML & Data Science: ML frameworks and data tools (PyTorch, TensorFlow, Scikit-Learn, Pandas, NumPy, PySpark)
      - Data Platforms & Cloud: Cloud and data platforms (GCP, Docker, Snowflake, MongoDB, Git)
      - Visualization & BI: BI and visualization tools (Tableau, Power BI, Looker Studio)
      - Techniques: Methodologies and techniques (A/B Testing, ETL Pipelines, LLMs, Causal Inference)

    Returns:
        dict[str, list[str]]: Dictionary mapping category names to lists of skills.
    """
    return {
        "Languages": ["Python", "SQL", "C++", "JavaScript", "R"],
        "ML & Data Science": [
            "PyTorch",
            "TensorFlow",
            "Scikit-Learn",
            "Pandas",
            "NumPy",
            "PySpark",
        ],
        "Data Platforms & Cloud": ["GCP", "Docker", "Snowflake", "MongoDB", "Git"],
        "Visualization & BI": ["Tableau", "Power BI", "Looker Studio"],
        "Techniques": ["A/B Testing", "ETL Pipelines", "LLMs", "Causal Inference"],
    }


def get_availability() -> dict:
    """
    Returns current availability information for job opportunities.

    Contains:
      - status (str): Current employment-seeking status
      - target_roles (list[str]): Desired role types
      - graduation (str): Expected graduation date
      - contact (dict): Preferred contact methods (email, LinkedIn)

    Returns:
        dict: Availability information dictionary.
    """
    return {
        "status": "Seeking full-time roles",
        "target_roles": [
            "Data Engineering",
            "Analytics",
            "Machine Learning",
        ],
        "graduation": "May 2026",
        "contact": {
            "email": "kanitmann01@gmail.com",
            "linkedin": "linkedin.com/in/kanitmann",
        },
    }


def get_experience() -> list[dict]:
    """
    Returns work history with company, role, dates, description, and achievements.

    Each experience contains:
      - company (str): Company name
      - role (str): Job title / role
      - dates (str): Employment date range
      - description (str): Brief role description
      - achievements (list[str]): Key accomplishments

    Returns:
        list[dict]: List of experience dictionaries.
    """
    return [
        {
            "company": "NetSTAR",
            "role": "ML Engineer",
            "dates": "Threat Intelligence Platform",
            "description": (
                "Built a threat intelligence platform analyzing 1B+ phishing URLs. "
                "Engineered ML pipelines for real-time threat detection and classification. "
                "Developed models to identify malicious domains and brand impersonation."
            ),
            "achievements": [
                "Built a threat intelligence platform analyzing 1B+ phishing URLs",
                "Engineered ML pipelines for real-time threat detection and classification",
                "Developed models to identify malicious domains and brand impersonation",
            ],
        },
        {
            "company": "Ericsson",
            "role": "Cloud/Infra Engineer",
            "dates": "Enterprise Telecom Infrastructure",
            "description": (
                "Led GCP migration for enterprise telecom infrastructure. "
                "Managed 2,000+ servers across hybrid cloud environments. "
                "Automated deployment pipelines and infrastructure provisioning."
            ),
            "achievements": [
                "Led GCP migration for enterprise telecom infrastructure",
                "Managed 2,000+ servers across hybrid cloud environments",
                "Automated deployment pipelines and infrastructure provisioning",
            ],
        },
    ]


@mcp.tool()
def projects() -> str:
    """
    Get featured projects with descriptions, tech stacks, and links.

    Returns structured JSON data about Kanit's featured projects including:
      - Brand Guard: ML-powered fake brand login detection (FastAPI, Python, Scikit-Learn)
      - kanit.codes: Personal portfolio with tactile feedback system (React, JavaScript, CSS3)

    Returns:
        str: JSON string containing a list of project objects.
    """
    return json.dumps(get_projects(), indent=2)


@mcp.tool()
def skills() -> str:
    """
    Get categorized tech stack.

    Returns structured JSON data with skill categories:
      - Languages: Python, SQL, C++, JavaScript, R
      - ML & Data Science: PyTorch, TensorFlow, Scikit-Learn, Pandas, NumPy, PySpark
      - Data Platforms & Cloud: GCP, Docker, Snowflake, MongoDB, Git
      - Visualization & BI: Tableau, Power BI, Looker Studio
      - Techniques: A/B Testing, ETL Pipelines, LLMs, Causal Inference

    Returns:
        str: JSON string containing a dictionary of skill categories.
    """
    return json.dumps(get_skills(), indent=2)


@mcp.tool()
def experience() -> str:
    """
    Get work history with company, role, dates, and achievements.

    Returns structured JSON data about Kanit's work experience:
      - NetSTAR (ML Engineer): Threat intelligence platform, 1B+ phishing URLs analyzed
      - Ericsson (Cloud/Infra Engineer): GCP migration, 2,000+ servers managed

    Returns:
        str: JSON string containing a list of experience objects.
    """
    return json.dumps(get_experience(), indent=2)


@mcp.tool()
def availability() -> str:
    """
    Get current availability and contact information.

    Returns structured JSON data about Kanit's job availability:
      - Status: Seeking full-time roles
      - Target roles: Data Engineering, Analytics, Machine Learning
      - Graduation: May 2026
      - Contact: email (kanitmann01@gmail.com), LinkedIn (linkedin.com/in/kanitmann)

    Returns:
        str: JSON string containing availability information.
    """
    return json.dumps(get_availability(), indent=2)


if __name__ == "__main__":
    mcp.run()
