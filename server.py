from typing import List
from sanic.response import HTTPResponse, text
from sanic.request import Request
from sanic import Sanic
from pprint import pprint
import json
import re
import requests

metatrader_address = 'https://fundedmax.org:5001'
add_user_api = '/api/v1/admin/Admin/AddNewUser'
auth_api = '/api/v1/Authentication/Login'
admin_name = 'admin@fundedmax.com'
password = '@1Fundedmaxisthebest'

session = requests.session()
login_token = ''

app =Sanic(__name__)

class UserInfo:
    def __init__(self, email: str, phone: str, name: str, lastname: str, product_line_items: List, date_raw: str) -> None:
        self.email = email
        self.phone = phone
        self.name = name
        self.lastname = lastname
        self.date_raw = date_raw
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
        Name: {self.name}
        LastName: {self.lastname}
        Date: {self.date_raw}
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

def login():
    global login_token
    login_res = session.get(f"{metatrader_address}{auth_api}", params={'login': admin_name, 'password': password})
    login_token = login_res.json()['data']
    if login_token:
        return True


def send_user_to_server(user_info: UserInfo):
    if not login_token:
        login()

    headers = {"Authorization": f"Bearer {login_token}"}
    res = session.post(f"{metatrader_address}{add_user_api}", headers=headers, json= {
        'email': user_info.email,
        'phone': user_info.phone,
        'firstName': user_info.name,
        # TODO: Add last name
        'accountSize': user_info.product_size,
        'accountType': 0 if user_info.product_type == 'Grand' else 1
    })
    print(res.text)
    return res

def test_send_user_to_server():
    send_res = send_user_to_server(test_user_info)


test_user_info = UserInfo(
    email='shrnemati@gmail.com',
    phone='091212345678',
    name='Omid',
    lastname='Yousefi',
    date_raw='2023-09-15T19:58:02',
    product_line_items= [
    {
      "id": 2125,
      "name": "$ 10000 General - no insurance",
      "product_id": 4380,
      "variation_id": 5541,
      "quantity": 1,
      "tax_class": "",
      "subtotal": "4450000",
      "subtotal_tax": "0",
      "total": "4450000",
      "total_tax": "0",
      "taxes": [],
      "meta_data": [
        {
          "id": 14275,
          "key": "pa_ins",
          "value": "no-insurance",
          "display_key": "ins",
          "display_value": "no insurance"
        },
        { "id": 86368, "key": "billing_name", "value": "Omid" },
        { "id": 86368, "key": "billing_lastname", "value": "Yousefi" },
      ],
      "sku": "",
      "price": 4450000,
      "image": {
        "id": 5050,
        "src": "https://fundedmax.com/wp-content/uploads/2023/06/10k.png"
      },
      "parent_name": "$ 10000 General"
    }
  ]
)

# send_res = send_user_to_server(test_user_info)



@app.post("/woocommerce_order")
async def on_order_handler(request: Request) -> HTTPResponse:
    pprint(request.json)
    if request.json['status'] == 'pending':
        print("PENDING")
        return text("Done")
        
    if request.json['status'] == 'processing':
        print("PROCESSING")
        user_name = ''
        user_lastname = ''
        meta_data_field = request.json['meta_data']
        for data in meta_data_field:
            if data['key'] == 'billing_name':
                user_name = data['value']
            if data['key'] == 'billing_lastname':
                user_lastname = data['value']
            if user_name and user_lastname:
                break

        if not user_name:
            print("User doesn't have name")
            return text("No user name")
            
        user_info = UserInfo(
            email=request.json['billing']['email'],
            phone=request.json['billing']['phone'],
            name=user_name,
            lastname=user_lastname,
            date_raw=request.json['date_modified'],
            product_line_items=request.json['line_items']
        );
        pprint(str(user_info))
        print('', flush=True)

        send_user_to_server(user_info)
        
        return text("Done")
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4343)

