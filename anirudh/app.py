from flask import Flask, request, render_template
import ipaddress
import csv


app = Flask(__name__)

_file_name="inventory.csv"

def fetch_filtered_from_csv(_addr, _mask):
    """
    This method check addr and mask validity and checks if it present in csv.
    
    _addr: Ip address  
    _mask: Mask or subnet

    Returns:
    data: filtered json data
    """
    fetched_data = list()
    try:
        net = ipaddress.ip_network(_addr + '/'+_mask, strict=False)
    except ValueError as e:
        fetched_data.append({"Error": "invalid addr or mask provided"})
        return fetched_data
    with open(_file_name, 'r') as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            if row:
                if row[2] == net.network_address.__str__():
                    d=dict()
                    d['id'] = row[0]
                    d['object_name'] = row[1]
                    d['address'] = row[2]
                    d['owner'] = row[5]
                    fetched_data.append(d)
    return fetched_data


#Sample endpoint for address
#http://localhost:5000/addresses?addr=10.5.77.1&mask=32
@app.route('/addresses', methods=['GET'])
def get_addresses():
    """
    This endpoint is used to fetch details for given addr and mask as json
    It calls fetch_filtered_from_csv to fetch data.
  
    Returns:
    data: fetched json data
    """
    args = request.args
    _addr = str(args.get("addr",None))
    _mask = str(args.get("mask",None))
    data = fetch_filtered_from_csv(_addr,_mask)
    return data
   

#Sample endpoint for report
#http://localhost:5000/report?addr=10.5.77.1&mask=255.255.255.255
@app.route('/report', methods=['GET'])
def get_report():
    """
    This endpoint is used to fetch details for given addr and return html 
    with data and No Record found if fetched data is empty.
    It calls fetch_filtered_from_csv to fetch data.
  
    Returns:
    data: ender html with data
    """
    args = request.args
    _addr = str(args.get("addr",None))
    _mask = str(args.get("mask",None))
    data = fetch_filtered_from_csv(_addr,_mask)
    return render_template('report.html', data=data)


if __name__ == "__main__":
  app.run()