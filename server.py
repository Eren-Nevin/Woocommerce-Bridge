from typing import List
from sanic.response import HTTPResponse, text
from sanic.request import Request
from sanic import Sanic
from pprint import pprint
import json
import re

app =Sanic(__name__)

class UserInfo:
    def __init__(self, email: str, phone: str, first_name: str, last_name: str, product_line_items: List) -> None:
        self.email = email
        self.phone = phone
        self.first_name = first_name
        self.last_name = last_name
        self.product_name: str = product_line_items[0]['name'];
        self.product_id: int = product_line_items[0]['product_id'];
        self.product_metadata = product_line_items[0]['meta_data'][0];
        self.product_type = self.get_product_type()
        self.product_size = self.get_product_size()
        self.product_insurance = self.get_product_insurance()


    def __str__(self) -> str:
        return f"""
        Email: {self.email}
        Phone: {self.phone}
        First Name: {self.first_name}
        Last Name: {self.last_name}
        Product Name: {self.product_name}
        Product ID: {self.product_id}
        Product Meta Data: {self.product_metadata}
        Product Type: {self.product_type}
        Product Size: {self.product_size}
        Product Insurance: {self.product_insurance}
        """

    def get_product_type(self) -> str:
        if 'general' in self.product_name.lower():
            return 'General'
        elif 'grand' in self.product_name.lower():
            return 'Grand'
        return 'Unknown'
    
    def get_product_size(self) -> int:
        if size := re.findall(r'\d+', self.product_name):
            return int(size[0]);
    
        return 0
    
    # TODO: Test this
    def get_product_insurance(self) -> bool:
        if 'no insurance' in self.product_name.lower():
            return False
        return True





@app.post("/woocommerce_order")
async def on_order_handler(request: Request) -> HTTPResponse:
    pprint(request.body.decode())
    user_info = UserInfo(
        email=request.json['billing']['email'],
        phone=request.json['billing']['phone'],
        first_name=request.json['billing']['first_name'],
        last_name=request.json['billing']['last_name'],
        product_line_items=request.json['line_items']
    );
    pprint(str(user_info))
    print('', flush=True)
    
    # with open('last.json', 'w+') as f:
    #     json.dump(request.json, f)
    return text("Done")
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4343)

