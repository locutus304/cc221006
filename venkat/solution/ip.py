from iptools import IpRangeList
from flask_table import Table, Col

from datastore import datastore

class IpAddress():

    def __init__(self):
        self.datastore = datastore()
    """
        Funtion to validate the input params
        Params: ip String
                subnet String
        return: List
    """
    def validateIpAndSubnet(self, ip, subnet):
        list_ip = None
        try:
            #create Iterator obj with the given network address adn subnet
            list_ip = IpRangeList(ip + "/" + subnet)
        except:
            #exception will occer when invalid Ip or subnet is given
            pass

        return list_ip

    """
        Funtion to return matched IP address details
        Params: total_ips List
        return: List
    """
    def get_list_of_ips(self,total_ips):
        try:
            output_list = self.datastore.readAndFilterData(total_ips)

            #retunr empty list, when no rows are matched
            if not output_list:
                return []

            return output_list

        except:
            print("error occered while processing")
            raise Exception


    """
        Funtion to return matched IP address in HTML table form
        Params: total_ips List
        return: HTML
    """
    def get_ui_table(self,total_ips):
        output_list = self.datastore.readAndFilterData(total_ips)

        #retunr "No rows matched." when no rows are matched
        if not output_list:
            return """
                <p>
                 No rows matched.
                </p>
            """

        class ItemTable(Table): #define Html table class
            #define each columns
            id = Col("Id")
            owner = Col("Owner")
            address = Col("Address")
            object_name = Col("Object_name")

        #convert json list into table rows
        table = ItemTable(output_list)

        return table.__html__()
