import os, json, logging

class DataDisplayer:
    def __init__(self, configurations):
        self.configurations = configurations

    def display(self, profileData):
        self.profileData = profileData
        logging.info('Starting the displaying of data')
        self.displayAll(profileData)
        self.displayGenderStats(profileData)

    def displayAll(self, profileData):
        message = "Total number of profiles: " + str(len(profileData))
        logging.info(message)
        print(message)

        for currentProfile in profileData:
            message = currentProfile.formatted()
            logging.info(message)
            print(message)

    def displayGenderStats(self, profileData):
        countFemale = 0
        countMale = 0
        countUndefined = 0
        for currentProfile in profileData:
            if currentProfile.gender == 'F':
                countFemale += 1
            elif currentProfile.gender == 'M':
                countMale += 1
            else:
                countUndefined += 1
        message = "Total of female: " + str(countFemale) + " males: " + str(countMale) + " and undefined: " + str(countUndefined)
        logging.info(message)
        print(message)

        proportionFemale = str(round(countFemale * 100 / len(profileData), 1))
        proportionMale = str(round(countMale * 100 / len(profileData), 1))
        proportionUndefined = str(round(countUndefined * 100 / len(profileData), 1))

        message = "Proportion of female: " + proportionFemale + " males: " + proportionMale + " and undefined: " + proportionUndefined
        logging.info(message)
        print(message)
