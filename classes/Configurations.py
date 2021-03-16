import os, json, logging
from shutil import copyfile

class Configurations:
    configs = {}

    def __init__(self, execution_path):
        self.execution_path = execution_path
        self.default_config_json_path = os.path.join(self.execution_path, 'configs.json.default')
        self.config_json_path = os.path.join(self.execution_path, 'configs.json')
        self.reload_config()

    def reload_config(self):
        if not os.path.exists(self.config_json_path):
            copyfile(self.default_config_json_path, self.config_json_path)
            open(self.config_json_path, 'w+')
            f.write('{}')
            f.close()

        with open(self.config_json_path, 'r') as f:
            self.configs = json.load(f)

    def get_config(self, config_name):
        if config_name in self.configs:
            return self.configs[config_name]

        return ''
