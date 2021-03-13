import logging

class ProfileDataModel:
    # crawled data
    name = ''
    employment = ''
    city = ''

    #processed data
    gender = ''

    def __init__(self, name, employment, city):
        self.name = name
        self.employment = employment
        self.city = city

    def formatted(self):
        return 'Name: ' + self.name + ' | city: ' + self.city + ' | employment: ' + self.employment + ' | gender: ' + self.gender