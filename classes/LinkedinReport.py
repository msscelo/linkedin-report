import logging
from .Configurations import Configurations
from .DataGatherer import DataGatherer
from .DataDisplayer import DataDisplayer
from .DataProcessor import DataProcessor

class LinkedinReport:
    def __init__(self, executionPath):
        self.executionPath = executionPath
        logging.basicConfig(
            level=logging.INFO,
            filename=self.executionPath + '\\LinkedinReport.log',
            filemode='w',
            format='%(asctime)s %(levelname)s %(module)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
        )
        logging.info('Starting LinkedinReport execution at: ' + executionPath)
        self.configurations = Configurations(executionPath)
        self.dataGatherer = DataGatherer(self.configurations)
        self.dataProcessor = DataProcessor(self.configurations)
        self.dataDisplayer = DataDisplayer(self.configurations)

    def start(self):
        self.GatherData()
        self.ProcessData()
        self.DisplayData()

    def GatherData(self):
        logging.info('Gathering data')
        self.dataGatherer.gather()
        # self.dataGatherer.fillTestData()

    def ProcessData(self):
        logging.info('Processing data')
        self.dataProcessor.process(self.dataGatherer.profileData)

    def DisplayData(self):
        logging.info('Displaying data')
        self.dataDisplayer.display(self.dataGatherer.profileData)
