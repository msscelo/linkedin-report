import os, json, logging
from .DbManager import DbManager

class DataDisplayer:
    def __init__(self, configurations):
        self.configurations = configurations

    def display(self,):
        logging.info('Starting the displaying of data')
        self.display_all()
        self.display_gender_stats()

    def display_all(self):
        profiles = []
        with DbManager(self.configurations) as db_manager:
            profiles = db_manager.get_profiles()

        message = "Total number of profiles: " + str(len(profiles))
        logging.info(message)
        print(message)

        for current_profile in profiles:
            message = current_profile.formatted()
            logging.info(message)
            print(message)

    def display_gender_stats(self):
        profiles = []
        with DbManager(self.configurations) as db_manager:
            gender_data = db_manager.get_gender_totals()
            message = "Total of females: " + str(gender_data['female']) + " males: " + str(gender_data['male']) + " and undefined: " + str(gender_data['undefined'])
            logging.info(message)
            print(message)

            proportion_female = str(round(gender_data['female'] * 100 / gender_data['total'], 1))
            proportion_male = str(round(gender_data['male'] * 100 / gender_data['total'], 1))
            proportion_undefined = str(round(gender_data['undefined'] * 100 / gender_data['total'], 1))

            message = "Proportion of females: " + proportion_female + " males: " + proportion_male + " and undefined: " + proportion_undefined
            logging.info(message)
            print(message)

            unnacounted = gender_data['female'] + gender_data['male'] + gender_data['undefined'] - gender_data['total']
            if unnacounted != 0:
                message = "There are " + unnacounted + " profiles with an invalid gender"
                logging.info(message)
                print(message)
