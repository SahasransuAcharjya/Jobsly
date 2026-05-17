# Job Agent Project Context

## Overview
The goal of this project is to build an automated Job Agent that discovers and aggregates job listings for specific, relevant job titles across multiple job boards. 

## Problem Statement
Job seekers often have to manually search across various platforms to find relevant job openings, which is time-consuming and inefficient. This project aims to solve this by creating an agent that programmatically aggregates jobs from targeted sources into a single, unified dataset for easy tracking and analysis.

## Core Requirements
- **Target Platforms:** 
  - Naukri
  - RemoteOK
  - Wellfound (formerly AngelList)
- **Input:** A specific job title (e.g., "Software Engineer", "Data Scientist").
- **Output:** The extracted job listings must be parsed and stored in a `.csv` file format for easy consumption.
- **Data Points to Extract (Proposed):**
  - Job Title
  - Company Name
  - Location / Remote Status
  - Job URL
  - Description (if feasible)

## Architecture & Tech Stack
- **Language:** Python
- **Data Storage:** `pandas` or built-in `csv` module to generate the final output.
- **Scraping Strategies:**
  - **Naukri:** HTML Scraping (using `BeautifulSoup` or `lxml`).
  - **RemoteOK:** Public API (direct data consumption).
  - **Wellfound:** Firecrawl (AI web scraping API for complex, JS-heavy applications).
