import os, json, logging

class Configurations:
    configs = {}

    def __init__(self, executionPath):
        self.executionPath = executionPath
        self.configJsonPath = os.path.join(self.executionPath, 'configs.json')
        logging.info('Config file in use: ' + self.configJsonPath)
        self.reloadConfig()

    def reloadConfig(self):
        if not os.path.exists(self.configJsonPath):
            open(self.configJsonPath, 'w+')
            f.write('{}')
            f.close()

        with open(self.configJsonPath, 'r') as f:
            self.configs = json.load(f)

    def getConfig(self, configName):
        if configName in self.configs:
            return self.configs[configName]

        return ''
