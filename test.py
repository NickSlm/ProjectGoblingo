import sqlite3
from blizzardAPI import Blizzard
import os
import datetime


# connection = sqlite3.connect(r"D:\DATABASE\ape.db",check_same_thread=False)
# cursor = connection.cursor()
# cursor.execute("SELECT item_class from item_db")
# a = cursor.fetchall()
# with open(r"D:\ProjectGoblingo\item_class.txt", 'w') as filea:
#     for i_type in a:
#         print(i_type[0], file=filea)

# with open(r"D:\ProjectGoblingo\connected_realm_id_list.txt", 'r') as file:
#     lines = file.read().splitlines()
#     for c_id in lines:
#         print(c_id)
#         auc_data = connection.get_data(connected_realm=c_id)
#         with open(r"D:\ProjectGoblingo\item_list\{0}.txt".format(c_id), 'w') as item_file:
#             for item_id in auc_data['auctions']:
#                 print(item_id['item']['id'], file=item_file)

# def check_exists(item_id):
#     cursor.execute("SELECT id from item_db")
#     id_list = cursor.fetchall()
#     if (f'{item_id}',) in id_list:
#         print(f"{item_id} already exists")
#     else:
#         cursor.execute(f"""INSERT INTO item_db (id) VALUES({item_id})""")
#         cursor.connection.commit()
#         print(item_id + '-----' + 'ADDED')


# for filename in os.listdir(r"D:\ProjectGoblingo\item_list"):
#     with open(r"D:\ProjectGoblingo\item_list\{0}".format(filename), 'r') as file:
#         lines = file.read().splitlines()
#         for id in lines:
#             check_exists(item_id=id)
# print("FINISHED")
