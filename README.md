# Football Prediction Project

## 1. High-level Architecture Overview

<img width="1546" height="561" alt="Untitled Diagram drawio" src="https://github.com/user-attachments/assets/cd1583da-e6d8-4163-8b61-4acbc46d24a4" />

This project provides analysis and predicts football match outcomes and is structured with a **medallion data engineering workflow**. It consists of:

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

## 4. Setup and Getting Started Guide

Follow these step-by-step instructions to clone the repository and start using the Football Prediction Project.

### Step 1: Clone the Repository

Open your terminal and clone the repository to your local machine:

```bash
git clone https://github.com/hungnguyen0508/FSDS.git
cd FSDS
```

### Step 2: Create and Activate a Conda Environment

Create a new Conda environment with Python 3.11.14:

```bash
conda create --name football-prediction python=3.11.14
conda activate football-prediction
```

Verify the Python version:

```bash
python --version
```

### Step 3: Install Project Dependencies

Install all required Python packages using pip:

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available, manually install the essential packages:

```bash
pip install pandas sqlalchemy fastapi uvicorn streamlit dbt-postgres python-dotenv scikit-learn
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root directory with your PostgreSQL credentials:

```
DATABASE_URL=postgresql://username:password@localhost:5432/football_prediction
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=your_password
DB_NAME=football_prediction
```

Replace `username`, `password`, and other values with your actual credentials.

### Step 5: Start Docker Services

Use Docker Compose to spin up the PostgreSQL database:

```bash
docker-compose up -d
```

Verify that the database container is running:

```bash
docker-compose ps
```

### Step 6: Run Data Ingestion

Load raw CSV data into the PostgreSQL database. Use the ingestion script:

```bash
python src/ingestion/load_data.py
```

Or use the Makefile command (if available):

```bash
make ingest
```

### Step 7: Run dbt Transformations

Navigate to the dbt project directory and execute transformations:

```bash
cd transformation/football_prediction
dbt run
dbt test
```

This will:
- Create Bronze tables (raw data staging)
- Create Silver tables (cleaned and transformed data)
- Create Gold tables (final aggregated features for ML)

Return to the project root:

```bash
cd ../../
```

### Step 8: Train the Machine Learning Model (Optional)

If you want to train or update the prediction model:

```bash
python src/ml/train_model.py
```

### Step 9: Start the Backend (FastAPI)

In a new terminal window, activate the environment and start the FastAPI backend:

```bash
conda activate football-prediction
python src/backend/main.py
```

Or use uvicorn directly:

```bash
uvicorn src.backend.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`. Access the interactive API documentation at `http://localhost:8000/docs`.

### Step 10: Start the Frontend (Streamlit)

In another new terminal window, activate the environment and start the Streamlit frontend:

```bash
conda activate football-prediction
streamlit run src/frontend/app.py
```

The Streamlit interface will open in your browser at `http://localhost:8501`.

### Step 11: Using the Application

Once the frontend is running, you can:

1. **View Available Matches**: Browse historical football match data
2. **Make Predictions**: Select a match and view the predicted home team win probability
3. **Analyze Data**: Explore statistics and trends in the data
4. **Query via API**: Use the FastAPI endpoints directly via `http://localhost:8000/docs`

---

## 5. Useful Make Commands (Optional)

If a Makefile is available, you can use these shortcuts:

```bash
make setup          # Set up the environment and install dependencies
make ingest         # Run data ingestion
make transform      # Execute dbt transformations
make train          # Train the ML model
make backend        # Start the FastAPI backend
make frontend       # Start the Streamlit frontend
make stop           # Stop all Docker containers
make clean          # Remove containers and clean up
```

---

## 6. Troubleshooting

- **Database Connection Error**: Ensure PostgreSQL container is running with `docker-compose ps` and verify credentials in `.env`.
- **dbt Compilation Error**: Check that profiles.yml is correctly configured in `~/.dbt/`.
- **Port Already in Use**: If ports 5432, 8000, or 8501 are in use, modify the Docker Compose or FastAPI/Streamlit configuration.
- **Missing Dependencies**: Run `pip install -r requirements.txt` again or manually install missing packages.

---

## 7. Stopping the Application

When you're done, stop the services:

```bash
# Stop Streamlit (Ctrl+C in its terminal)
# Stop FastAPI (Ctrl+C in its terminal)
# Stop Docker containers
docker-compose down
```

---

**Enjoy using the Football Prediction Project!** For further questions or issues, please refer to the official documentation of each tool or open an issue on the GitHub repository.


