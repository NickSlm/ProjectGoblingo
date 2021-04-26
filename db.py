import sqlite3
from collections import defaultdict
from blizzardAPI import Blizzard
import time
import datetime

connection = sqlite3.connect(r"D:\DATABASE\ape.db",check_same_thread=False)
cursor = connection.cursor()


def find_realm_id(realm_name):
    if cursor.execute(f"SELECT id FROM connected_realm WHERE name LIKE '%{realm_name}%'"):
        a = cursor.fetchone()
        return a[0]

def server_names():
    server_list = []
    cursor.execute("SELECT name FROM connected_realm")
    a = cursor.fetchall()
    for name in a:
        server_list.append(name[0])
    return server_list

def find_item_id(item_name):
    connections = sqlite3.connect(r'D:\DATABASE\ape.db')
    cursor = connections.cursor()
    cursor.execute(f"SELECT id, name, media_url FROM item_db WHERE name LIKE ? ", ('%'+item_name+'%',))
    obj = cursor.fetchall()
    return obj


def get_items_by_type(item_type, auction_data):
    item_dict = defaultdict(list)
    for filter in item_type:
        cursor.execute(f"SELECT id, name, media_url FROM item_db WHERE item_class = ? ", (filter,))
        item_type_list = cursor.fetchall()
        for obj in item_type_list:
            found_item_id, found_name, icon = obj
            for item in auction_data['auctions']:
                if item['item']['id'] == int(found_item_id):
                    try:
                        item_dict[found_name].append((item['unit_price'] / 10000, item['quantity'], icon))
                    except KeyError:
                        item_dict[found_name].append((item['buyout'] / 10000, item['quantity'], icon))
    return item_dict


def get_items(item_name, auction_data):
    item_dict = defaultdict(list)
    for obj in find_item_id(item_name):
        found_item_id, found_name, icon = obj
        for item in auction_data['auctions']:
            if item['item']['id'] == int(found_item_id):
                try:
                    item_dict[found_name].append((item['unit_price'] / 10000, item['quantity'], icon))
                except KeyError:
                    item_dict[found_name].append((item['buyout'] / 10000, item['quantity'], icon))
    return item_dict


def get_total_quantity(dict):
    average_dict = {}
    for key in dict.keys():
        sum = 0
        min_price = dict[key][0][0]
        for val in dict[key]:
            sum += val[1]
            if val[0] < min_price:
                min_price = val[0]
        average_dict.update({key: [min_price, sum, dict[key][0][2]]})
    return average_dict


def get_total_mounts():
    cursor.execute("SELECT id FROM mounts_db")
    mounts_data = cursor.fetchall()
    available_mounts = list(set(mounts_data))
    return len(available_mounts)


def get_mount_list_info(profile_token):
    mounts = []
    conn = Blizzard()
    total_mounts = get_total_mounts()
    mount_list = conn.get_mounts_list(profile_token)
    for mount in mount_list:
        cursor.execute("SELECT name, media FROM mounts_db WHERE id = ?", (mount['mount']['id'],))
        mount_info_list = cursor.fetchall()
        mounts.append({mount_info_list[0][0]: {'media': mount_info_list[0][1]}})
    return mounts, total_mounts
 
# UPDATE ITEM DB
# cursor.execute('SELECT id FROM item_db WHERE name is null')
# print("Connected to SQLite")
# a = cursor.fetchall()
# conn = Blizzard()
# end = len(a)
# start = 0
# start_time = datetime.datetime.utcnow()
# for id in a:
#     start += 1
#     item_data = conn.get_item_data(id[0])
#     sql_update_query = f"""UPDATE item_db set name = ?, media_url = ?, item_class = ?, Item_subclass = ?, inventory_type = ? WHERE id = {id[0]}"""
#     data = (item_data[0],item_data[1],item_data[2],item_data[3],item_data[4])
#     cursor.execute(sql_update_query, data)
#     cursor.connection.commit()
#     print(f"{start} out of {end}: UPDATED {id[0]} name {item_data[0]}", end='\r')

# end_time = datetime.datetime.utcnow()
# print(f"Finished after {end_time - start_time}")

