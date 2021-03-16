import logging, datetime

class ProfileDataModel:
    id = 0
    creation_date = ''

    # crawled data
    name = ''
    employment = ''
    city = ''

    #processed data
    name_gender_search = ''
    gender = ''

    def __init__(self, name, employment, city, name_gender_search = '', gender = '', id = 0, creation_date = str(datetime.datetime.now())):
        self.name = name
        self.employment = employment
        self.city = city

        if name_gender_search == '':
            name_gender_search = self.name.split(' ', 1)[0]
        self.name_gender_search = name_gender_search
        self.gender = gender
        self.id = id
        self.creation_date = creation_date

    def formatted(self):
        return 'Name: ' + self.name + ' | city: ' + self.city + ' | employment: ' + self.employment + ' | gender: ' + self.gender
