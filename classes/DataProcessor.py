import logging, requests, json, unidecode
from .ProfileDataModel import ProfileDataModel
from .DbManager import DbManager

class DataProcessor:
    def __init__(self, configurations):
        self.configurations = configurations

    def process(self):
        logging.info('Starting the processing of data')
        i = 0
        with DbManager(self.configurations) as db_manager:
            profiles = db_manager.get_profiles()
            for currentProfile in profiles:
                if currentProfile.gender == '':
                    gender = db_manager.get_gender(currentProfile.name_gender_search)
                    if gender == '':
                        gender = self.getGenderViaGenderize(currentProfile)
                        db_manager.insert_gender(currentProfile.name_gender_search, gender)
                    currentProfile.gender = gender
                    db_manager.update_gender(currentProfile)

    def getGenderViaGenderize(self, profile):
        urlGenderize = 'https://api.genderize.io'
        name = unidecode.unidecode(profile.name_gender_search)
        params = dict(
            name = name,
            country_id = self.configurations.get_config('default_country')
        )
        resp = requests.get(url=urlGenderize, params=params)
        gender = 'X'
        if resp.status_code == 200 and len(resp.content) > 0:
            data = resp.json()
            if data['gender'] == 'male':
                gender = 'M'
            elif data['gender'] == 'female':
                gender = 'F'

        return gender
