FROM sanicframework/sanic:3.8-latest

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "server.py"]
