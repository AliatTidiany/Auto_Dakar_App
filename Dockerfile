FROM python:3.11-slim

WORKDIR /app

COPY . /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Créer les dossiers pour éviter les erreurs si absents
RUN mkdir -p /app/data /app/data_web_scraper

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
