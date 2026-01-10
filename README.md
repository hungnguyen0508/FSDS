# Football Prediction Project

## 1. High-level Architecture Overview

This project predicts football match outcomes and is structured with a **medallion data engineering workflow**. It consists of:

- **Database (PostgreSQL)**: stores raw, transformed, and prediction-ready data.  
- **Data Ingestion Script**: loads raw CSV files into the database.  
- **dbt**: transforms data into Bronze, Silver, and Gold tables/views.  
- **Backend (FastAPI)**: serves API endpoints to access data and predictions.  
- **Frontend (Streamlit)**: interactive UI for users to query predictions.  
- **Machine Learning Model**: predicts home team win probabilities using transformed features.  
- **Docker Compose**: containerizes the database, backend, and frontend.  

**Workflow:** Start DB → run ingestion → run dbt transformations → start backend + frontend → users interact via frontend or API.  

---

## 2. Prerequisite

Before you begin, ensure you have the following tools installed:

- **Conda**: package manager and environment management system (Anaconda or Miniconda)  
- **Python 3.11.9**: programming language and runtime  
- **pip**: Python package installer  
- **Make**: build automation tool  
- **Docker & Docker Compose**: for containerized services  
- **Git**: version control system  

---

## 3. Tool Introduction

Tools used in this project:

- **Python**: for ingestion, backend, and ML model scripts  
- **SQLAlchemy**: ORM to interact with PostgreSQL  
- **pandas**: data manipulation  
- **PostgreSQL**: relational database  
- **dbt**: transforms raw data into structured medallion architecture  
- **FastAPI**: backend API service  
- **Streamlit**: frontend UI  
- **Docker & Docker Compose**: containerization for DB, backend, frontend  
- **Makefile**: automates tasks like ingestion, dbt, and container startup  

---

## 4. How to Use This Project

1. **Clone the repository**:

```bash
git clone <your-repo-url>
cd <your-repo-folder>
