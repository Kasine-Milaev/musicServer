FROM python:3.13.13-slim

WORKDIR /app

COPY req.txt .

RUN pip install --no-cache-dir -r req.txt

COPY . .

RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]