FROM python:3.11-slim

WORKDIR /code

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

# Hugging Face Spaces requires the app to listen on port 7860
ENV PORT=7860

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
