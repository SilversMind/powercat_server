FROM python:3.9
WORKDIR /Users/bouzdi/Dev/powercat_server
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ src/
EXPOSE 8080
CMD ["python", "-m", "uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]