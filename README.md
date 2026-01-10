# Football Prediction Project

## 1. High-level Architecture Overview

<img width="1546" height="561" alt="Untitled Diagram drawio" src="https://github.com/user-attachments/assets/cd1583da-e6d8-4163-8b61-4acbc46d24a4" />

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
- **Python 3.11.14**: programming language and runtime  
- **pip**: Python package installer  
- **Make**: build automation tool  
- **Docker & Docker Compose**: for containerized services  
- **Git**: version control system  

---

## 3. Tool Introduction

Tools used in this project:

This project uses the following tools:

- **Python**:  
  A high-level, general-purpose programming language widely used for data analysis, machine learning, and backend development. Python provides rich libraries for data manipulation (pandas), machine learning (scikit-learn, XGBoost, etc.), and web development (FastAPI, Flask).  

    + **SQLAlchemy**:  
  A Python Object Relational Mapper (ORM) that allows developers to interact with relational databases using Python classes instead of raw SQL queries. This makes database operations safer, easier to maintain, and integrated with Python objects.  

    + **FastAPI**:  
  A modern Python framework for building APIs. FastAPI is fast, asynchronous, and easy to integrate with Python ML workflows. It exposes endpoints to serve database queries and predictions to users.  

    + **Streamlit**:  
  A Python library for creating interactive web applications with minimal code. Used here as a frontend interface where users can input match data and view predictions in real-time.  

- **PostgreSQL**:  
  An open-source relational database management system (RDBMS) known for reliability, scalability, and strong SQL compliance. Used here to store raw data, transformed tables, and prediction results.  

- **dbt (Data Build Tool)**:  
  A modern data transformation tool that enables analysts and engineers to build modular, tested, and version-controlled SQL models. In this project, dbt implements a **medallion architecture**:  
  - **Bronze**: staging tables for raw data  
  - **Silver**: cleaned and intermediate transformations  
  - **Gold**: final aggregated tables or marts for analytics and ML features  

- **Docker & Docker Compose**:  
  Docker allows packaging applications with all their dependencies into portable containers. Docker Compose is used to orchestrate multiple containers, ensuring that the database, backend, and frontend can run consistently across different machines.  

- **Makefile**:  
  A build automation tool that defines a set of commands (targets) for repetitive tasks. In this project, Make automates: starting containers, running ingestion, executing dbt transformations, and starting backend/frontend services.  

---

## 4. How to Use This Project

1. **Clone the repository**:

```bash
git clone <your-repo-url>
cd <your-repo-folder>
