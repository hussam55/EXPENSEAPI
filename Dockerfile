# 1. Use an official, lightweight Python image
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Set environment variables to keep Python behavior predictable
# Prevents Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1 
# Ensures logs are printed directly to the terminal without buffering
ENV PYTHONUNBUFFERED=1

# 4. Copy JUST the requirements first (this is a Docker caching trick)
COPY requirements.txt .

# 5. Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of your application code into the container
COPY . .

# 7. Open the port Uvicorn will run on
EXPOSE 8000

# 8. Start the server! 
# (Update "app.main:app" if your FastAPI instance is located somewhere else)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]