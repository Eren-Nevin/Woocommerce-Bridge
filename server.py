from sanic.response import HTTPResponse, text, json
from sanic.request import Request
from sanic import Sanic
from pprint import pprint

app =Sanic(__name__)

@app.post("/woocommerce")
async def on_order_handler(request: Request) -> HTTPResponse:
    pprint(request)
    pprint(request.headers)
    pprint(request.body.decode())
    return text("Done")
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

