FROM sanicframework/sanic:3.8-latest

COPY . .

RUN pip install -r requirements.txt

EXPOSE 4343

CMD ["python", "server.py"]
