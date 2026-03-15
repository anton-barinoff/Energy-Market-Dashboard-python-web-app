# Energy Market Dashboard

This project demonstrates a full-stack web application for visualizing and managing electricity market data from European and Asian parts of Russia. The backend is built with [FastAPI](https://fastapi.tiangolo.com/) and the frontend with [Streamlit](https://www.streamlit.io/).

## Project Structure

- `backend/`: FastAPI backend server
	- `main.py`: FastAPI application with CRUD endpoints
	- `data.csv`: data file
- `frontend/`: FastAPI server
	- `app.py`: Streamlit UI with tables and charts
- `requirements.txt`: package requirements files


## Files Description

- **backend/main.py** - FastAPI server implementation with three endpoints:
    - `GET /records` - retrieve all records
    - `POST /records` - add new record (with Pydantic validation)
    - `DELETE /records/{id}` - delete record by id
    - Data persistence in CSV file

- **backend/data.csv** - Initial dataset with columns:
    - `timestep` - datetime
    - `consumption_eur` - consumption in European part (MW)
    - `consumption_sib` - consumption in Siberian part (MW)
    - `price_eur` - price in European part (RUB/MWh)
    - `price_sib` - price in Siberian part (RUB/MWh)

- **frontend/app.py** - Streamlit dashboard with:
  - Data table view
  - Interactive Plotly charts (consumption and prices)
  - Form for adding new records
  - Delete functionality by ID
  - Auto-refresh after changes

- **requirements.txt** - All Python dependencies:
  - FastAPI, Uvicorn (backend)
  - Streamlit, Plotly (frontend)
  - Pandas, Pydantic (data processing)
  - Requests (API communication)

## API Endpoints
Method	               Endpoint Description	  Status Codes
GET	/records	       Get all records	      200 OK, 500 Error
POST /records	       Add new record	      201 Created, 500 Error
DELETE /records/{id}   Delete record by ID	  200 OK, 404 Not Found, 500 Error
GET	/health	           Server health check	  200 OK

## Data Validation

All numeric fields must be non-negative. Backend validates:
- consumption_eur ≥ 0
- consumption_sib ≥ 0
- price_eur ≥ 0
- price_sib ≥ 0

## Configuration

Before running the application, configure the API URL in frontend/app.py:
```python
# For local development:
# API_URL = "http://localhost:8000"
# For deployment (Render):
API_URL = "https://your-app.onrender.com"```

Local development: uncomment the first line, comment the second

Deployment: make sure to replace your-app.onrender.com with your actual Render backend URL when deploying

## Run Locally

1. Clone the repository:
```bash
git clone <repository-url>
cd task_04_service```

2. Create and activate virtual environment:
```python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate```

3. Install dependencies:
```pip install -r requirements.txt```

4. Start Backend Server
```cd backend
uvicorn main:app --reload --port 8000```

Backend API will be available at: http://localhost:8000
Swagger documentation: http://localhost:8000/docs

5. Start Frontend Application (new terminal)
```# From project root with activated venv
cd frontend
streamlit run app.py```

Frontend dashboard will open at: http://localhost:8501

## Deployment

### Backend (Render)

1. Push code to GitHub repository
   Make sure it's in a public folder and that you have a `requirements.txt` file.
   
2. Sign up at render.com (use GitHub account)

3. Click "New +" -> "Web Service"

4. Connect your repository

5. Configure:
   Name: energy-market-api
   Root Directory: backend
   Build Command: pip install -r ../requirements.txt
   Start Command: uvicorn main:app --host 0.0.0.0 --port 10000
   
6. Choose Free plan

7. Click "Create Web Service"

### Frontend (Streamlit Cloud)

1. Update API_URL in frontend/app.py with your Render backend URL:
```API_URL = "https://your-api.onrender.com"  # Replace with your actual backend URL```

2. Push changes to GitHub:
```git add frontend/app.py
git commit -m "Update API URL for production"
git push```

3. Go to share.streamlit.io

4. Sign in with GitHub

5. Click "New app"

6. Fill in your repository, branch main, and file path frontend/app.py

7. Click "Deploy"