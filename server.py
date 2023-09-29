from sanic.response import HTTPResponse, text
from sanic.request import Request
from sanic import Sanic
from pprint import pprint
import json

app =Sanic(__name__)

@app.post("/woocommerce_order")
async def on_order_handler(request: Request) -> HTTPResponse:
    pprint(request)
    pprint(request.headers)
    pprint(request.body.decode())
    with open('last.json', 'w+') as f:
        json.dump(request.json, f)
    return text("Done")
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4343)

