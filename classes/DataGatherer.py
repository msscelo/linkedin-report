import os, json, logging
from selenium import webdriver
# from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from .ProfileDataModel import ProfileDataModel
from .DbManager import DbManager

class DataGatherer:
    profile_data = []

    def __init__(self, configurations):
        self.configurations = configurations

    def gather(self):
        if self.configurations.get_config('skip_gathering') == True:
            return
        if self.configurations.get_config('debug_mode') == True:
            return self.fill_test_data()

        logging.info('Starting the gathering of data')

        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        self.browser = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)

        #loading the login page
        self.browser.get('https://www.linkedin.com/uas/login')

        # needs to be logged in
        username_input = self.browser.find_element_by_id('username')
        username_input.send_keys(self.configurations.get_config('linkedin_username'))
        password_input = self.browser.find_element_by_id('password')
        password_input.send_keys(self.configurations.get_config('linkedin_password'))
        password_input.submit()

        # checking for a sucessful login
        if not self.browser.current_url == 'https://www.linkedin.com/feed/':
            logging.info('Could not login, instead was sent to: ' + self.browser.current_url)
            return
        i = 1
        urlLinkedinConnections = 'https://www.linkedin.com/search/results/people/?network=%5B%22F%22%5D&origin=MEMBER_PROFILE_CANNED_SEARCH'

        while True:
            pageParam = ''
            if i > 1:
                pageParam = '&page=' + str(i)
            logging.info('Attempting to gather profiles from page ' +str(i))
            self.browser.get(urlLinkedinConnections + pageParam)

            if urlLinkedinConnections not in self.browser.current_url:
                if self.browser.current_url == 'https://www.linkedin.com/in/unavailable/':
                    logging.info('Reached the end at page ' +str(i))
                    break
                else:
                    logging.info('Could not proceed to ' + str(i) + ', was sent to ' + self.browser.current_url)
                    break
            gathered = self.collect_page_data()
            if gathered == 0:
                break
            i = i + 1
        self.browser.quit

    def collect_page_data(self):
        i = 0
        with DbManager(self.configurations) as db_manager:
            while True:
                currentName = ''
                currentEmployment = ''
                currentCity = ''
                try:
                    currentName = self.browser.execute_script("return document.getElementsByClassName('entity-result__title-text')[" + str(i) + "].children[0].children[0].children[0].innerText")
                    currentEmployment = self.browser.execute_script("return document.getElementsByClassName('entity-result__title-text')[" + str(i) + "].parentElement.parentElement.parentElement.parentElement.parentElement.children[1].children[0].innerText")
                    currentCity = self.browser.execute_script("return document.getElementsByClassName('entity-result__title-text')[" + str(i) + "].parentElement.parentElement.parentElement.parentElement.parentElement.children[1].children[1].innerText")
                except:
                    if currentName == '':
                        break
                currentProfile = ProfileDataModel(currentName, currentEmployment, currentCity)
                self.profile_data.append(currentProfile)
                db_manager.insert_profile(currentProfile)
                i = i + 1

        return i

    def fill_test_data(self):
        with DbManager(self.configurations) as db_manager:
            self.profile_data.append(ProfileDataModel('Test', 'test0', 'city'))
            db_manager.insert_profile(self.profile_data[-1])
            # self.profile_data.append(ProfileDataModel('João da silva', 'test1', 'city1'))
            # db_manager.insert_profile(self.profile_data[-1])
            # self.profile_data.append(ProfileDataModel('Maria da silva', 'test2', 'city2'))
            # db_manager.insert_profile(self.profile_data[-1])
            # self.profile_data.append(ProfileDataModel('João Sauro', 'test3', 'city3'))
            # db_manager.insert_profile(self.profile_data[-1])
            # self.profile_data.append(ProfileDataModel('Maria Sauro', 'test4', 'city4'))
            # db_manager.insert_profile(self.profile_data[-1])
