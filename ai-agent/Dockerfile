FROM python:3.11-slim

WORKDIR /app

COPY app /app

RUN pip install --no-cache-dir \
    browser-use \
    langchain-groq \
    python-dotenv \
    fastapi \
    uvicorn \
    playwright

RUN playwright install

CMD ["python", "main.py"]