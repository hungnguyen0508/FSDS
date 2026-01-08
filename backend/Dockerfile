From python:3.11.14-slim

# go to /app 
workdir /app

# Copy all files into /app
copy . .

# install packages needed
run pip install --no-cache-dir -r requirements.txt 

# Port for fastAPI 
Expose 8080

CMD ["python", "main.py"]