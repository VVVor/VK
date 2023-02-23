import datetime

class ParserException(Exception):
    pass

class VK_Client_Parser:

    def get_opposite_sex(self, resp):
        if not len(resp):
            raise ParserException({'message':'Response length is 0, but should be list with at least one element'})

        sex = resp[0].get('sex')
        if sex == 1:
            return 2
        else:
            return 1
        
    def get_current_age(self, resp):
        date = resp[0].get('bdate')
        date_list = date.split('.')
        if len(date_list) == 3:
            year = int(date_list[2])
            year_now = int(datetime.date.today().year)
            return year_now - year
        else:
            return False
        
    def get_age_low(self, resp):
        if not len(resp):
            raise ParserException({'message':'Response length is 0, but should be list with at least one element'})

        return self.get_current_age(resp)

    def get_age_high(self, resp):
        if not len(resp):
            raise ParserException({'message':'Response length is 0, but should be list with at least one element'})

        return self.get_current_age(resp)
    
    def get_city_id(self, resp):
        if not len(resp):
            raise ParserException({'message':'Response length is 0, but should be list with at least one element'})
        
        city = resp[0].get('city')
        city_id = city.get('id')
        return city_id
        
