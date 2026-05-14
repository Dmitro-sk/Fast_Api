FROM python:3.12-slim
RUN pip install poetry
WORKDIR /app
COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.create false && poetry install --no-root && pip install email-validator
COPY . .

# Додаємо корінь /app до шляхів пошуку модулів
ENV PYTHONPATH=/app

CMD ["python", "src/main.py"]