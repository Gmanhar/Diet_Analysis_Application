FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir pandas numpy matplotlib seaborn

COPY data_analysis.py .

CMD ["python", "data_analysis.py", "--csv", "/data/All_Diets.csv", "--out", "/outputs"]
