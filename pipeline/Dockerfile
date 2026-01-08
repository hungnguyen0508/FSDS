From python:3.11.14-slim

# Go to /app
WORKDIR /app 

# Copy requirement.txt from local
COPY requirements.txt . 

# Install packages needed
RUN pip install --no-cache-dir -r requirements.txt

#Copy ingest.py to current dir 
COPY ingest.py . 

# run the file through command 
CMD ["python", "ingest.py"]