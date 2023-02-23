
import vk_api
import requests

from vk_client_parser import VK_Client_Parser

class VK_Client:

    def __init__(self, access_token, community_token):
        self.domain = "https://api.vk.com/method/"
        self.access_token = access_token
        self.session = vk_api.VkApi(token=community_token)

        self.parser = VK_Client_Parser()

    def get_session(self):
        return self.session

    def write_message(self, user_id, message):
        self.session.method("messages.send", {
            "user_id": user_id,
            "message": message,
            "random_id" : 0
        })
        
    def write_message_with_keyboard(self, user_id, message, keyboard):
        self.session.method("messages.send", {
            "user_id": user_id,
            "message": message,
            "random_id" : 0,
            "keyboard" : keyboard
        })

    def get_params(self, add_params: dict = None):
        params = {
            'access_token': self.access_token,
            'v': '5.131'
        }
        if add_params:
            params.update(add_params)
            pass
        return params

    '''
    def sender (self, user_id, text):
        self.session.method('messages.send', {'user_id': user_id,
                                    'message': text,
                                    'random_id': 0,
                                    'keyboard': keyboard})
    '''

    def get_user_token(self, user_id):
        request = 'https://oauth.vk.com/authorize'         

    def name(self, user_id):
        request = self.domain + 'users.get'
        response = requests.get(
            request,
            self.get_params({'user_ids': user_id})
        )
        try:
            for user_info in response.json()['response']:
                first_name = user_info['first_name']
                last_name = user_info['last_name']
                return first_name + " " + last_name
        except:
            print(f"Не удалось получить имя пользователя для {user_id}: {response.json()['error']['error_msg']}")
            self.write_message(user_id, 'Ошибка с нашей стороны. Попробуйте позже.')
            return False

    def get_info(self, user_id):
        request = self.domain + 'users.get'
        response = requests.get(
            request,
            self.get_params({'user_ids': user_id,
                             'fields': 'bdate,sex,city'}))
        resp = response.json()['response']
        return resp    
    
    def get_search_params(self, user_id, count):
        request = self.domain + 'users.get'
        response = requests.get(
            request,
            self.get_params({'user_ids': user_id,
                             'fields': 'bdate,sex,city'}))
        resp = response.json()['response']

        sex = self.parser.get_opposite_sex(resp)
        age_low = self.parser.get_age_low(resp)
        age_to = self.parser.get_age_high(resp)
        city = self.parser.get_city_id(resp)
        
        search_params = {
            'sex': sex,
            'age_from': age_low,
            'age_to': age_to,
            'city': city,
            'fields': 'is_closed, id, first_name, last_name',
            'status': '1' or '6',
            'count': count,
            'v': '5.131',
            'access_token': self.access_token
        }

        print ('[INFO] make search params with {} values'.format(search_params))
        
        return search_params 
    
    def find_users(self, search_params):
        url = f'https://api.vk.com/method/users.search'

        try:
            resp = requests.get(url, params=search_params)
            print ('[INFO] request users.search method')
        
            return resp.json()['response']
        
        except KeyError:
            print ('[ERROR] users.search method has wrong response')
            return False
        
    def get_photos(self, owner_id):
        url = 'https://api.vk.com/method/photos.getAll'
        params = {'access_token': self.access_token,
                  'type': 'album',
                  'owner_id': owner_id,
                  'extended': 1,
                  'count': 25,
                  'v': '5.131'}
        resp = requests.get(url, params=params).json()
        dict_photos = {}

        try:
            popular_pics = sorted(
                resp['response']['items'],
                key=lambda k: k['likes']['count'] + k['comments']['count'],
                reverse=True
            )[0:3]
            for pic in popular_pics:
                if 'owner_id' not in dict_photos.keys():
                    dict_photos['owner_id'] = pic['owner_id']
                    dict_photos['pics_ids'] = []
                dict_photos['pics_ids'].append(pic['id'])
            return dict_photos

        except KeyError:
            print ('[ERROR] photos.getAll method has wrong response')
            return False

