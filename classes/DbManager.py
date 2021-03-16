import os, json, logging, datetime, sqlite3
from sqlite3 import Error
from .ProfileDataModel import ProfileDataModel

class DbManager:
    db_connection = None
    def __init__(self, configurations):
        self.configurations = configurations
        self.db_path = 'linkedinreportdata.sqlite3'
        self.db_connection = sqlite3.connect(self.db_path)
        self.db_cursor = self.db_connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.db_connection.commit()
        if self.db_cursor != None:
            self.db_cursor.close()
        if self.db_connection != None:
            self.db_connection.close()

    def create_database(self):
        self.db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS profiles (
                id INTEGER PRIMARY KEY,
                creation_date TEXT NOT NULL,

                name TEXT NULL,
                employment TEXT NULL,
                city TEXT NULL,

                name_gender_search TEXT NULL,
                gender TEXT NULL
            )
            ''')

        self.db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS name_gender (
                id INTEGER PRIMARY KEY,
                creation_date TEXT NOT NULL,

                name_gender_search TEXT NULL,
                gender TEXT NULL
            )
            ''')

    def insert_profile(self, profile_data):
        existant_gender = self.get_gender(profile_data.name_gender_search)
        if existant_gender != '':
            profile_data.gender = existant_gender
        elif profile_data.gender != '':
            self.insert_gender(profile_data.name_gender_search, profile_data.gender)

        if self.profile_exists(profile_data):
            return
        result = self.db_cursor.execute('INSERT INTO profiles (creation_date, name, employment, city, name_gender_search, gender) VALUES (?,?,?,?,?,?)', [profile_data.creation_date, profile_data.name, profile_data.employment, profile_data.city, profile_data.name_gender_search, profile_data.gender])
        pass

    def profile_exists(self, profile_data):
        self.db_cursor.execute('SELECT id FROM profiles WHERE name=? AND employment=?', [profile_data.name, profile_data.employment])
        exists = self.db_cursor.fetchone()

        return exists != None

    def get_profiles(self):
        profiles = []
        for row in self.db_cursor.execute('SELECT * FROM profiles ORDER BY id'):
            profiles.append(ProfileDataModel(id=row[0], creation_date=row[1], name=row[2], employment=row[3], city=row[4], name_gender_search=row[5], gender=row[6]))

        return profiles

    def get_gender(self, name_gender_search):
        self.db_cursor.execute('SELECT gender FROM name_gender WHERE name_gender_search=?', [name_gender_search])
        gender_data = self.db_cursor.fetchone()
        if gender_data == None:
            return ''

        return gender_data[0]

    def insert_gender(self, name_gender_search, gender):
        creation_date = str(datetime.datetime.now())
        self.db_cursor.execute('INSERT INTO name_gender (creation_date, name_gender_search, gender) VALUES (?,?,?)', [creation_date, name_gender_search, gender])

    def update_gender(self, profile_data):
        self.db_cursor.execute('UPDATE profiles SET gender=? WHERE id=?', [profile_data.gender, str(profile_data.id)])

    def get_gender_totals(self):
        totals = {}
        self.db_cursor.execute("SELECT count(1) as female FROM profiles WHERE gender='F'")
        data = self.db_cursor.fetchone()
        totals['female'] = data[0]

        self.db_cursor.execute("SELECT count(1) as male FROM profiles WHERE gender='M'")
        data = self.db_cursor.fetchone()
        totals['male'] = data[0]

        self.db_cursor.execute("SELECT count(1) as undefined FROM profiles WHERE gender='X'")
        data = self.db_cursor.fetchone()
        totals['undefined'] = data[0]

        self.db_cursor.execute("SELECT count(1) as undefined FROM profiles")
        data = self.db_cursor.fetchone()
        totals['total'] = data[0]

        return totals
