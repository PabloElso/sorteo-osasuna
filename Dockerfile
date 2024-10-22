# Dockerfile
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Copy project
COPY . /code/

# Expose port 8000
EXPOSE 8000

# Run the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]