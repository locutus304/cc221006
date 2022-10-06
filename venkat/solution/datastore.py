import csv


class datastore:

    def __init__(self):
        self.FILE_NAME = "datastore/inventory.csv"

    """
        Funtion to read the CSV file and return the list of matched row details
        Params: total_ips List
        return: List
    """
    def readAndFilterData(self, total_ips):
        output_list = []
        try:
            with open(self.FILE_NAME, 'r') as file: #read CSV
                csvreader = csv.DictReader(file)
                #iterate over each row and check if ip is matching with the given network address and subnet mask
                for row in csvreader:
                    if row['address'] in total_ips:
                        current_row_data = {}
                        current_row_data["id"] = row["id"]
                        current_row_data["object_name"] = row["object_name"]
                        current_row_data["address"] = row["address"]
                        current_row_data["owner"] = row["owner"]
                        output_list.append(current_row_data)
                return output_list
        except:
            print("error occered wile reading the csv file")
            raise Exception

        return None
