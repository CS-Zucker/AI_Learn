FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DASHSCOPE_API_KEY=${DASHSCOPE_API_KEY}

EXPOSE 8501

CMD ["streamlit", "run", "ai_partner.py", "--server.port=8501", "--server.address=0.0.0.0"]