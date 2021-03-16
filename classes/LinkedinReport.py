import logging
from .Configurations import Configurations
from .DataGatherer import DataGatherer
from .DataDisplayer import DataDisplayer
from .DataProcessor import DataProcessor
from .DbManager import DbManager

class LinkedinReport:
    def __init__(self, execution_path):
        self.execution_path = execution_path
        logging.basicConfig(
            level=logging.INFO,
            filename=self.execution_path + '\\LinkedinReport.log',
            filemode='w',
            format='%(asctime)s %(levelname)s %(module)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
        )
        logging.info('Starting LinkedinReport execution at: ' + execution_path)
        self.configurations = Configurations(execution_path)
        with DbManager(self.configurations) as db_manager:
            profiles = db_manager.create_database()

        self.dataGatherer = DataGatherer(self.configurations)
        self.dataProcessor = DataProcessor(self.configurations)
        self.dataDisplayer = DataDisplayer(self.configurations)

    def start(self):
        self.gather_data()
        self.process_data()
        self.display_data()

    def gather_data(self):
        logging.info('Gathering data')
        self.dataGatherer.gather()

    def process_data(self):
        logging.info('Processing data')
        self.dataProcessor.process()

    def display_data(self):
        logging.info('Displaying data')
        self.dataDisplayer.display()
