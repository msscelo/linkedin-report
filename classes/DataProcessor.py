import logging
from .ProfileDataModel import ProfileDataModel
import requests
import json
import unidecode

class DataProcessor:
    def __init__(self, configurations):
        self.configurations = configurations

    def process(self, profileData):
        logging.info('Starting the processing of data')
        i = 0
        while i < len(profileData):
            profileData[i].gender = self.getGenderViaGenderize(profileData[i])
            i = i + 1

    def getGenderViaGenderize(self, profile):
        urlGenderize = 'https://api.genderize.io'
        name = unidecode.unidecode(profile.name.split(' ', 1)[0])
        params = dict(
            name = name,
            country_id = self.configurations.getConfig('default_country')
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
