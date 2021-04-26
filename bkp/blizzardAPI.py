import requests

BLIZZARD_CLIENT_ID = "6eef8ac48dbc417197ed8a34c731e398"
BLIZZARD_CLIENT_SECRET = "mxzBzxKXxQZsYU3ogGjPhoodi9O6VVmQ"

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
        for obj in media_info['assets']:
            return obj['value']
    
    def get_character_media(self,name,realm_slug):
        auth_token = self._get_token()
        url = f"https://eu.api.blizzard.com/profile/wow/character/{realm_slug}/{name.lower()}/character-media?namespace=profile-eu&locale=en_US&access_token={auth_token}"
        resp = requests.get(url)
        media_info = resp.json()
        try:
            for i in media_info['assets']:
                if i['key'] == 'avatar':
                    print("WORKING", url)
                    return i['value']
        except KeyError as e:
            print(f"ERROR {e}", url)


    def get_character_list(self, profile_token):
        url = f"https://eu.api.blizzard.com/profile/user/wow?namespace=profile-eu&locale=en_US&access_token={profile_token}"
        resp = requests.get(url)
        profile_char_info = resp.json()
        for obj in profile_char_info['wow_accounts']:
            for char in obj['characters']:
                # icon = self.get_character_media(name=char['name'], realm_slug=char['realm']['slug'])
                yield (char['name'],char['realm']['slug'])

