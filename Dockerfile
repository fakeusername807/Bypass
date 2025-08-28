FROM python:3.12.7

WORKDIR /poster

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "poster.py"]
