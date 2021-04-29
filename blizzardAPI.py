import requests
import sqlite3
from collections import defaultdict

BLIZZARD_CLIENT_ID = "6eef8ac48dbc417197ed8a34c731e398"
BLIZZARD_CLIENT_SECRET = "mxzBzxKXxQZsYU3ogGjPhoodi9O6VVmQ"

connection = sqlite3.connect(r"D:\DATABASE\ape.db",check_same_thread=False)
cursor = connection.cursor()


def get_mount_info(mount_id):
    cursor.execute("SELECT name, media FROM mounts_db WHERE id = ? ", (mount_id,))
    mount_info = cursor.fetchall()
    return mount_info


class Blizzard:
    def __init__(self, client_id=BLIZZARD_CLIENT_ID, client_secret=BLIZZARD_CLIENT_SECRET, region='eu', **kwargs):
        self.region = region
        self.id = client_id
        self.secret = client_secret
        self.data = {'grant_type': 'client_credentials'}

    def _create_access_token(self):
        data = self.data
        response = requests.post(f'https://{self.region}.battle.net/oauth/token', data=data, auth=(self.id, self.secret))
        return response.json()

    def _get_token(self):
        response = self._create_access_token()
        access_token_id = response['access_token']
        return access_token_id

    def get_data(self, connected_realm):
        auth_token = self._get_token()
        url = f"https://eu.api.blizzard.com/data/wow/connected-realm/{connected_realm}/auctions?namespace=dynamic-eu&locale=en_EU&access_token="
        resp = requests.get(url + auth_token)
        game_data = resp.json()
        return game_data

    def get_item_media(self, item_id):
        auth_token = self._get_token()
        url = f"https://eu.api.blizzard.com/data/wow/media/item/{item_id}?namespace=static-eu&locale=en_US&access_token="
        resp = requests.get(url+ auth_token)
        media_info = resp.json()
        try:
            for obj in media_info['assets']:
                return obj['value']
        except:
            return ''

    def get_item_data(self, item_id):
        auth_token = self._get_token()
        url = f"https://eu.api.blizzard.com/data/wow/item/{item_id}?namespace=static-eu&locale=en_US&access_token="
        resp = requests.get(url + auth_token)
        item_data = resp.json()
        item_icon = self.get_item_media(item_id=item_id)
        try:
            return item_data['name'],item_icon,item_data['item_class']['name'], item_data['item_subclass']['name'], item_data['inventory_type']['type']
        except:
            return '','','','',''
    

    def get_item_type(self, item_id):
        auth_token = self._get_token()
        url = f"https://eu.api.blizzard.com/data/wow/item/{item_id}?namespace=static-eu&locale=en_US&access_token={auth_token}"
        resp = requests.get(url)
        item_type = resp.json()
        return item_type['inventory_type']['type']



    def get_character_media(self,name,realm_slug):
        auth_token = self._get_token()
        url = f"https://eu.api.blizzard.com/profile/wow/character/{realm_slug}/{name.lower()}/character-media?namespace=profile-eu&locale=en_US&access_token={auth_token}"
        resp = requests.get(url)
        media_info = resp.json()
        try:
            for i in media_info['assets']:
                if i['key'] == 'inset':
                    return i['value']
        except KeyError:
            pass

    def get_protected_data(self,realm_id,char_id, profile_token):
        url_protected = f"https://eu.api.blizzard.com/profile/user/wow/protected-character/{realm_id}-{char_id}?namespace=profile-eu&locale=en_US&access_token={profile_token}"
        resp_protected = requests.get(url_protected)
        protected_char_info = resp_protected.json()
        try:
            return (protected_char_info['money'] / 10000)
        except KeyError:
            return 0


    def get_character_list(self, profile_token):
        char_dict = defaultdict(list)
        url = f"https://eu.api.blizzard.com/profile/user/wow?namespace=profile-eu&locale=en_US&access_token={profile_token}"
        resp = requests.get(url)
        profile_char_info = resp.json()
        for obj in profile_char_info['wow_accounts']:
            for char in obj['characters']:
                gold = self.get_protected_data(char['realm']['id'],char['id'], profile_token)
                icon = self.get_character_media(name=char['name'], realm_slug=char['realm']['slug'])
                if char['level'] > 10:
                    char_dict[char['realm']['slug']].append((char['name'],char['faction']['name'],char['playable_class']['name'],char['level'],icon, gold))
        return char_dict


    def get_mounts_list(self, profile_token):
        url = f"https://eu.api.blizzard.com/profile/user/wow/collections/mounts?namespace=profile-eu&locale=en_US&access_token={profile_token}"
        resp =  requests.get(url)
        mount_collection = resp.json()
        return mount_collection['mounts']

    def updatet(self, id):
        auth_token = self._get_token()
        url = f"https://eu.api.blizzard.com/data/wow/mount/{id}?namespace=static-eu&locale=en_US&access_token={auth_token}"
        resp =  requests.get(url)
        mount_collection = resp.json()
        try:
            return mount_collection['source']['name']
        except KeyError:
            return "..."





# class BlizzardData(Blizzard):
#     def __init__(self):
#         super().__init__()
