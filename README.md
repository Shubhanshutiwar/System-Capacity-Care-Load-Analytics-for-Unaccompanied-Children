Project Overview: System Capacity & Care Load Analytics for Unaccompanied Children
1. High-Level Summary
This project is a data-driven, healthcare-systems analytics initiative designed for the U.S. Department of Health and Human Services (HHS). Its purpose is to monitor, analyze, and forecast the capacity and care load of the federally mandated Unaccompanied Alien Children (UAC) Program. By translating raw, daily operational data into an interactive, real-time command dashboard, the project shifts government decision-making from a reactive crisis-response model to a proactive capacity-management model.

2. Background & Problem Statement
When unaccompanied children are apprehended at the border, they enter a dynamic "care pipeline." They are first taken into U.S. Customs and Border Protection (CBP) custody, then transferred to HHS care facilities for medical screening and sheltering, and finally discharged to vetted sponsors.

The Problem: HHS collects daily counts of these movements, but previously lacked a centralized analytical framework to measure the stress on this pipeline. Without understanding the balance between inflows (intakes) and outflows (discharges), stakeholders cannot anticipate capacity strain, leading to the risk of overcrowded facilities, delayed healthcare routing, and systemic bottlenecks.

3. Core Objectives
Pipeline Visibility: Quantify the daily and cumulative care load across both CBP and HHS facilities.

Bottleneck Detection: Identify exactly where pressure is building up (e.g., are CBP intakes surging, or are HHS discharges stalling?).

Predictive Awareness: Use rolling averages and backlog indicators to flag prolonged strain windows before facilities reach critical capacity.

Policy Support: Deliver a live Streamlit dashboard and executive reporting to support staffing, shelter planning, and humanitarian response evaluation.

4. Technical Methodology
The project was built entirely in Python, designed to run in cloud environments (like Google Colab or Kaggle), and follows a strict data engineering pipeline:

Data Ingestion & Cleaning: Processing the official HHS_Unaccompanied_Alien_Children_Program.csv dataset. This involves dynamic column mapping to clean messy government data formats (handling typos, commas in numeric strings, and date conversions) to ensure automated pipeline resilience.

Time-Series Structuring: Enforcing strict chronological ordering and ensuring a complete daily index to prevent gaps in temporal analysis.

Interactive Visualization: Utilizing Plotly to create fluid, interactive area charts and pressure lines.

Web App Deployment: Wrapping the analytics engine in Streamlit to create a user-friendly, deployable web application that non-technical policymakers can filter by date and metric.

5. Key Metrics Engineered (The "Brain" of the Project)
Rather than just showing raw counts, the project engineered specialized healthcare-capacity KPIs to measure systemic stress:

Total System Load: (CBP Custody + HHS Care) — The total humanitarian footprint on any given day.

Net Daily Intake: (Transferred into HHS - Discharged from HHS) — Measures if the system is taking on more children than it is successfully placing with sponsors.

Backlog Accumulation: A 7-day rolling sum of Net Daily Intake. A sustained positive number triggers a "capacity warning."

Discharge Offset Ratio: (HHS Discharges / CBP Transfers) — A ratio measuring the system's ability to relieve load. A ratio below 1.0 means the system is bottlenecking.

6. Final Deliverables
Automated ETL Pipeline: Python scripts that instantly clean, map, and transform the raw HHS data.

Live Streamlit Command Center: A localtunnel-hosted interactive web application featuring KPI summary cards, Care Load comparison charts, and System Pressure trendlines.

Actionable Insights / Research Paper: The underlying analytical framework required to brief government stakeholders (Unified Mentor / HHS) on historical strain periods and recommend data-driven thresholds for triggering emergency staffing protocols.

Impact: This project directly empowers policymakers to ensure the humane, efficient, and sustainable delivery of federally mandated child care services during dynamic migration events.
