from vk_client import VK_Client
from vk_api.longpoll import VkLongPoll, VkEventType

from keyboard import sql_keyboard, next_keyboard
from sql_client import SQL_Client

class DatingBot:

    def __init__(self, access_token, community_token, db_config):
        self.vk_client = VK_Client(access_token, community_token)
        self.session = self.vk_client.get_session()
        
        self.sql_client = SQL_Client(db_config)
        self.sql_client.connect()

        self.best_photos_count = 3
        self.offset = 0

    def get_sex_from_info(self, info):
        return info[0].get("sex")

    def get_name_from_info(self, info):
        return info[0].get("first_name")

    def get_bdate_from_info(self, info):
        return info[0].get("bdate")
    
    def get_tuple_person(self, offset):
        return self.sql_client.select_user(offset)
    
    def get_person_id(self, tuple_person):
        list_person = []
        for i in tuple_person:
            list_person.append(i)
        return str(list_person[2])

    def get_person_info(self, tuple_person):
        list_person = []
        for i in tuple_person:
            list_person.append(i)
        return f'{list_person[0]} {list_person[1]}, ссылка - {list_person[3]}'

    def listen(self):
        self.longpoll = VkLongPoll(self.session)
        
        for event in VkLongPoll(self.session).listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                user_id = event.user_id
                message = event.text.lower() 

                #self.client.sender(user_id, message)

                '''
                if message == "привет":
                    #name = self.client.name(user_id)
                    text = """Привет! \n Я могу познакомить тебя с кем-нибудь, но мне нужно получить от тебя некоторые разрешения. 
                    Кликни на кнопку 'Разрешить', если хочешь продолжить.""" 
                    self.client.write_message_with_keyboard(user_id, text, request_token_keyboard)
                '''

                if message == 'база':
                    text = 'Нажмите кнопку "Создать базу"'
                    self.offset = 0
                    self.sql_client.dropdb()
                    self.vk_client.write_message_with_keyboard(user_id, text, sql_keyboard)

                elif message == 'создать базу':
                    print('creating db...')

                    count = 10
                    open_count = 0
                    
                    self.sql_client.createdb()
                    
                    search_params = self.vk_client.get_search_params(user_id = user_id, count = count)
                    resp = self.vk_client.find_users(search_params)

                    if resp:
                        list_1 = resp['items']
                        for person_dict in list_1:
                            if person_dict.get('is_closed') == False:
                                open_count += 1
                                first_name = person_dict.get('first_name')
                                last_name = person_dict.get('last_name')
                                vk_id = str(person_dict.get('id'))
                                vk_link = 'https://vk.com/id' + str(person_dict.get('id'))
                                self.sql_client.insert_data_users(first_name, last_name, vk_id, vk_link)
                            else:
                                continue
                        
                        text = "Я нашел для вас {} анкеты c открытой страницей. Нажмите 'Дальше', чтобы посмотреть их.".format(open_count)
                        self.vk_client.write_message_with_keyboard(user_id, text, next_keyboard)

                    else:
                        error = 'Ошибка при запросе поиска подходящих кандидатов'
                        self.vk_client.write_message(user_id, error)

                elif message == 'дальше':
                    tuple_person = self.get_tuple_person(self.offset)
                    if tuple_person is None:
                        print("[Error] person tuple is none type")
                        print('offset: {}'.format(self.offset))
                        text = 'Ошибка при загрузке анкеты'
                        self.vk_client.write_message_with_keyboard(user_id, text, next_keyboard)
                        
                    else:
                        person_info = self.get_person_info(tuple_person)
                        person_id = self.get_person_id(tuple_person)
                    
                        self.vk_client.write_message(user_id, person_info)
                        self.sql_client.insert_data_seen_users(person_id, self.offset)

                        photos = self.vk_client.get_photos(person_id, self.best_photos_count)
                        if not photos:
                            text = 'Фотографии недоступны'
                            self.vk_client.write_message_with_keyboard(user_id, text, next_keyboard)
                        else:
                            self.vk_client.send_photos(user_id, photos, 'Лучшие фото:', next_keyboard)

                        
                    self.offset += 1


                elif message == 'база?':
                    print("Check if 'users' TABLE exist")
                    self.sql_client.is_users_table_exist()

                elif message == 'разрешить':
                    print("Нужно запросить auth token у пользователя")
                
                
                elif message == 'имя':
                    name = self.client.name(user_id)
                    self.vk_client.write_message(user_id, name)

                elif message == 'инфо':
                    info = self.vk_client.get_info(user_id)

                    print(info)

                    sex = self.get_sex_from_info(info)
                    name = self.get_name_from_info(info)
                    bdate = self.get_bdate_from_info(info)

                    text = "Имя: " + name
                    text += ", пол:" + str(sex)
                    text += ", день рождения:" + bdate                   

                    self.vk_client.write_message(user_id, text)
                





