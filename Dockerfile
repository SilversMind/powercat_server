FROM python:3.11
WORKDIR /Users/bouzdi/Dev/powercat_server
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ src/
ENV NODE_OPTIONS="--max-old-space-size=8192"
EXPOSE 3001
CMD ["python", "-m", "uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]