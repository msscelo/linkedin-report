import os, json, logging
from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from .ProfileDataModel import ProfileDataModel

class DataGatherer:
    profileData = []
    def __init__(self, configurations):
        self.configurations = configurations

        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        self.browser = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
        self.profileData = []

    def gather(self):
        logging.info('Starting the gathering of data')

        #loading the login page
        self.browser.get('https://www.linkedin.com/uas/login')

        # needs to be logged in
        username_input = self.browser.find_element_by_id('username')
        username_input.send_keys(self.configurations.getConfig('linkedin_username'))
        password_input = self.browser.find_element_by_id('password')
        password_input.send_keys(self.configurations.getConfig('linkedin_password'))
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
            self.collect_page_data()
            i = i + 1
        self.browser.quit

    def collect_page_data(self):
        i = 0
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
            currentDataPoint = ProfileDataModel(currentName, currentEmployment, currentCity)
            self.profileData.append(currentDataPoint)
            i = i + 1

    def fillTestData(self):
        self.profileData.append(ProfileDataModel('João da silva', 'teste1', 'cidade1'))
        self.profileData.append(ProfileDataModel('Maria da silva', 'teste2', 'cidade2'))
        self.profileData.append(ProfileDataModel('Hank da silva', 'teste3', 'cidade3'))
        self.profileData.append(ProfileDataModel('Apu da silva', 'teste4', 'cidade4'))
        self.profileData.append(ProfileDataModel('Yoko Ono', 'teste5', 'cidade5'))

