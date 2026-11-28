<h1 align="center">Kanit Mann</h1>

<p align="center"><b>Data, ML &amp; AI engineer: models, pipelines, and the dashboards that prove they work</b><br>
Associate Forward Deployed Engineer at Coforge (Aug 2026 – present) · MS in Data Science, University of Arizona, 2026 · New Jersey, US</p>

<p align="center"><a href="https://kanitmann.com">Portfolio</a> · <a href="https://kanitmann.com/Kanit%20Mann%20-%20Resume.pdf">Resume (PDF)</a> · <a href="mailto:mannkanit@gmail.com">Email</a> · <a href="https://www.linkedin.com/in/kanitmann">LinkedIn</a> · <a href="https://github.com/kanitmann01">GitHub</a></p>

---

## 📁 Featured Case Studies

Systems built end to end. The case studies behind most of them are on [kanitmann.com](https://kanitmann.com/projects), each covering the problem, the approach, the measured outcome, and what I would do differently.

### [Zero-Day Phishing Threat Intelligence Platform](https://kanitmann.com/projects/netstar)

*NetSTAR Global · Jan – May 2026 · FastText, XGBoost/LightGBM, Power BI, Docker*

A hybrid detector that combines a FastText text classifier, structured ML models, and distance rules to score brand-spoofing URLs before a client's users reach them. Trained on **1B+** phishing URLs; on a held-out split of 4,409 URLs it reached **96.7% accuracy** and **99.3% precision**, then shipped as an int8 edge model at roughly 5 ms p50 latency.

### [Scale-Out Migration of 2,000+ Servers to GCP](https://kanitmann.com/projects/ericsson)

*Ericsson · Sep 2023 – Dec 2024 · GCP, Citrix, SQL*

Wave-based migration of **2,000+** production servers into a GCP landing zone, with hybrid security hardening and database automation built during the move rather than after it. Infrastructure cost fell an estimated **30%**, tool uptime held at **99.9%**, and maintenance time dropped **40%**.

### [Nexuus Bot: a local-first AI workspace](https://github.com/kanitmann01/agent-desk)

*Active development · Python, React, SQLite, LLM orchestration*

Your workbook, calendar, mail headers, memory, and agents stay on your machine. It adds a sourced memory graph where every fact cites its source, keychain-backed model keys, and a consent-gated plugin marketplace. An evaluation build in active development, not a released product; the commit history is public.

### [Unified Bharat: Cross-Sector Policy Lakehouse](https://kanitmann.com/projects/unified-bharat)

*Completed May 2026 · Spark, Iceberg, Docker*

Five Indian government datasets (CSR spending, groundwater quality, institutions, district codes, population) reconciled on a Spark and Iceberg medallion architecture, then aggregated into a ~300-row state-year panel, a **99.88%** reduction. Random Forest beat OLS and XGBoost at RMSE 0.811, evidence of a non-linear CSR and environment relationship. Code: [unified-bharat](https://github.com/kanitmann01/unified-bharat).

### [Real-Time Twitch Analytics Pipeline](https://kanitmann.com/projects/twitch-analytics-pipeline)

*Jan 2026 · Kafka, Snowflake, dbt, Looker Studio*

A producer polls the Twitch Helix API every 60 seconds for live AoE2 streams, Kafka buffers the events, Snowflake keeps the raw JSON, and dbt models it for [a live Looker Studio dashboard](https://lookerstudio.google.com/s/jyb_uKEUcmo). Code: [twitch_stat_board](https://github.com/kanitmann01/twitch_stat_board).

Four more case studies (IPUMS wage trends, WTO synthetic control, Titanic predictor, VoiceBridge) are on [kanitmann.com/projects](https://kanitmann.com/projects). GitHub-only work: [Brand Guard](https://github.com/kanitmann01/capstone) (five-signal explainable verdicts; 57/59 day-zero catches where both public blocklist lookups scored 0), [TitanTale Analytics](https://github.com/kanitmann01/TitanTale-Analytics), [aoe2-stats](https://github.com/kanitmann01/aoe2-stats).

---

## 🧾 Experience

| Company | Role | Dates | Focus |
|---|---|---|---|
| **Coforge** | Associate Forward Deployed Engineer | Aug 2026 – present | AI orchestration and multi-agent frameworks on the Momentuum Blue team; cost-efficient model deployment |
| **NetSTAR Global** | Machine Learning Engineer | Jan – May 2026 | Zero-day phishing detection: FastText plus a structured ML ensemble, shipped with a Power BI telemetry layer |
| **Ericsson** | Engineer, Cloud and Infra | Sep 2023 – Dec 2024 | Citrix estate migration to GCP, hybrid security, database automation |
| **TATA Power** | Full Stack Intern | Jul – Sep 2021 | Internal employee-transfer portal: schema design and prototype |

Fuller detail for each role is on [kanitmann.com/about](https://kanitmann.com/about) and [LinkedIn](https://www.linkedin.com/in/kanitmann).

---

## ✍️ Writing

- [The Three-Line Skill That Changed Everything](https://kanitmann.com/articles/three-line-skill) (Jun 2026): directing coding agents through structured interviews and PRDs instead of fighting them.
- [Data Visualization Portfolio Reflection](https://kanitmann.com/articles/data-viz-analysis) (Nov 2025): five visuals, and what changed in polish, accessibility, and narrative.
- [CCRB Allegations Analysis](https://kanitmann.com/articles/ccrb-allegations-analysis) (Sep 2025): a multi-week analysis, starting with the baseline report.

Seven articles in total at [kanitmann.com/articles](https://kanitmann.com/articles).

---

## 🧰 Toolbox

**Languages:** Python · SQL · C++ · JavaScript · R  
**Data & ML:** PyTorch · scikit-learn · pandas · PySpark · TensorFlow · dbt  
**Cloud & streaming:** GCP · Docker · Kafka · Snowflake · Looker Studio  
**Methods:** A/B testing · causal inference · ETL/ELT · RAG · LLM evaluation

---

## 📊 GitHub Stats

*975+ commits, 210+ pull requests opened, and 27+ repositories contributed to, across 14 languages. Private work included; the charts refresh daily.*

<p align="center"><img alt="GitHub activity metrics: commits, pull requests, issues, and community stats" src="./github-metrics.svg"><br>
<img alt="Most used languages: Python, JavaScript, TypeScript, HTML, Jupyter Notebook" src="./github-metrics-languages.svg"></p>

<p align="center">
<picture>
<source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/kanitmann01/kanitmann01/output/github-contribution-grid-snake-dark.svg">
<source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/kanitmann01/kanitmann01/output/github-contribution-grid-snake.svg">
<img alt="Contribution grid snake animation" src="https://raw.githubusercontent.com/kanitmann01/kanitmann01/output/github-contribution-grid-snake.svg">
</picture>
</p>

---

<!-- BLOG_POSTS_START -->
## 📝 Latest Blog Posts

No recent posts available.
<!-- BLOG_POSTS_END -->

---

<!-- COMMITS_START -->
## 🔨 What I've Been Building

*Last 30 days*

### Active Repositories

- [kanitmann01/agent-desk](https://github.com/kanitmann01/agent-desk) — 60 commits
<!-- COMMITS_END -->

---

<details>
<summary><b>Last 10 commits</b></summary>

<!-- ACTIVITY_START -->
## ⚡ Recent Activity

- 🔨 **Nov 27, 2026** — [Committed to `kanitmann01/agent-desk`: Merge pull request #372 from kanitmann01/fix/stale-metric-live-label](https://github.com/kanitmann01/agent-desk/commit/c6aeb3d)
- 🔨 **Nov 27, 2026** — [Committed to `kanitmann01/agent-desk`: Merge pull request #370 from kanitmann01/fix/audit-new-p1-search-and-fill-button](https://github.com/kanitmann01/agent-desk/commit/91d34c7)
- 🔨 **Nov 26, 2026** — [Committed to `kanitmann01/agent-desk`: Merge pull request #369 from kanitmann01/fix/audit-3b-inert-tools](https://github.com/kanitmann01/agent-desk/commit/0132531)
- 🔨 **Nov 26, 2026** — [Committed to `kanitmann01/agent-desk`: Merge pull request #371 from kanitmann01/fix/stale-metric-live-label](https://github.com/kanitmann01/agent-desk/commit/3165c55)
- 🔨 **Nov 26, 2026** — [Committed to `kanitmann01/agent-desk`: Merge pull request #367 from kanitmann01/fix/audit-3d-slow-run](https://github.com/kanitmann01/agent-desk/commit/3f099e0)
- 🔨 **Nov 26, 2026** — [Committed to `kanitmann01/agent-desk`: Merge pull request #365 from kanitmann01/merge/bring-core-home](https://github.com/kanitmann01/agent-desk/commit/0f29028)
- 🔨 **Nov 26, 2026** — [Committed to `kanitmann01/agent-desk`: Merge pull request #364 from kanitmann01/docs/spec-032](https://github.com/kanitmann01/agent-desk/commit/b396694)
- 🔨 **Nov 26, 2026** — [Committed to `kanitmann01/agent-desk`: Merge pull request #352 from kanitmann01/feat/audit-face-walk](https://github.com/kanitmann01/agent-desk/commit/e53c591)
- 🔨 **Nov 26, 2026** — [Committed to `kanitmann01/agent-desk`: Merge pull request #348 from kanitmann01/fix/sample-client-name](https://github.com/kanitmann01/agent-desk/commit/68044fc)
- 🔨 **Nov 26, 2026** — [Committed to `kanitmann01/agent-desk`: Merge pull request #349 from kanitmann01/fix/audit-instruments-safe-b](https://github.com/kanitmann01/agent-desk/commit/954a31b)

*Last updated: 2026-11-28 00:06 UTC*
<!-- ACTIVITY_END -->

</details>

---

## 📬 Contact

<p align="center">
<a href="mailto:mannkanit@gmail.com"><img alt="Email" src="https://img.shields.io/badge/Email-EA4335?style=flat-square&logo=gmail&logoColor=white"></a>
<a href="https://www.linkedin.com/in/kanitmann"><img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white"></a>
<a href="https://github.com/kanitmann01"><img alt="GitHub" src="https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white"></a>
<a href="https://kanitmann.com"><img alt="Portfolio" src="https://img.shields.io/badge/kanitmann.com-0B7285?style=flat-square&logo=googlechrome&logoColor=white"></a>
</p>

<p align="center"><i>Resume, case studies, and articles live on kanitmann.com; the blog, commit, and activity sections above update daily from GitHub Actions.</i></p>
