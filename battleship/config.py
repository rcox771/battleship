import yaml
from pathlib import Path


class Configurable(object):
    def __init__(self, *args, file=Path().cwd() / 'config.yaml', **kwargs):
        super().__init__(*args, **kwargs)
        self.file = file

    def get_value(self, *keys):
        config = self.read_config()
        for key in keys:
            config = config[key]
        return config

    def read_config(self):
        with open(self.file) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        return config

    def __getattr__(self, name):
        """called automatically when an attribute does not exist"""
        base, sup = [x.__name__ for x in self.__class__.__mro__[::-1][-2:]]
        return self.get_value(base, sup, name)
