From python:3.11.14-slim

# go to /app 
workdir /app

# Copy all files into /app
copy . .

# install packages needed
run pip install --no-cache-dir -r requirements.txt 

# port
Expose 8501 

CMD ["streamlit", "run", "Frontend.py", "--server.port = 8501", "--server.address = 0.0.0.0"]