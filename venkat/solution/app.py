from flask import Flask, request
import json

from ip import IpAddress

app = Flask(__name__)

ipObj = IpAddress()
print(ipObj)

STATUS_CODE_SUCCESS = 200

@app.route('/')
def hello_world():
    return 'Welcome to flask app', STATUS_CODE_SUCCESS


@app.route('/addresses',methods = ['GET'])
def get_addresses():
    netwrk_address=request.args.get('addr')
    subnet_mask=request.args.get('mask')

    ip_list = ipObj.validateIpAndSubnet(netwrk_address, subnet_mask)

    if not ip_list:
        return json.dumps({"error": "addr or mask is invalid"}), STATUS_CODE_SUCCESS

    result = ipObj.get_list_of_ips(ip_list)

    if not result:
        return json.dumps([]), STATUS_CODE_SUCCESS

    return json.dumps(result), STATUS_CODE_SUCCESS


@app.route('/report',methods = ['GET'])
def get_report():
    netwrk_address=request.args.get('addr')
    subnet_mask=request.args.get('mask')

    ip_list = ipObj.validateIpAndSubnet(netwrk_address, subnet_mask)

    if not ip_list:
        return """
            <p>
            addr or mask is invalid
            </p>
        """, STATUS_CODE_SUCCESS

    return ipObj.get_ui_table(ip_list), STATUS_CODE_SUCCESS

if __name__ == '__main__':
    app.run("127.0.0.1", 5000)
