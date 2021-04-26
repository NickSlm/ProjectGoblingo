# Imports
import sqlite3
import datetime
import os
import csv
import pandas
# Local Imports
from blizzardAPI import Blizzard


conn = Blizzard()

now = datetime.date.today()



with open(r'D:\ProjectGoblingo\connected_realm_id_list.txt', 'r') as connected_realm_id_list:
    lines = connected_realm_id_list.read().splitlines()
    for c_id in lines:
        auc_data = conn.get_data(c_id)
        if not os.path.exists(r'D:\ProjectGoblingo\\auc_data\{0}'.format(now)):
            os.makedirs(r'D:\ProjectGoblingo\\auc_data\{0}'.format(now))
        else:
            with open(r'D:\ProjectGoblingo\\auc_data\{0}\{1}.csv'.format(now, c_id), 'w', newline='') as csvfile:
                write = csv.DictWriter(csvfile, fieldnames= ['id', 'time_left', 'unit_price', "quantity", 'buyout', 'bid', "item",])
                write.writeheader()
                for data in auc_data['auctions']:
                    write.writerow(data)
    print("FINISHED")
