FROM python:3.12-slim

WORKDIR /app

COPY build-requirements.txt .

RUN apt-get update && apt-get install -y build-essential curl software-properties-common git && rm -rf /var/lib/apt/lists/*

RUN pip3 install -r build-requirements.txt

COPY streamlit_app.py .

EXPOSE 8501

HEALTHCHECK --start_period=10s --interval=120s --timeout=3s --retries=3 CMD curl --fail http://localhost/8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "server.address=0.0.0.0"]
