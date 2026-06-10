FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir aiogram==3.4.1 aiosqlite==0.19.0 python-dotenv==1.0.0

COPY . .

CMD ["python", "bot.py"]
