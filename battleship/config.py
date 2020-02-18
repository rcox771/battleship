import yaml
from pathlib import Path

config_path = Path().cwd() / 'config.yaml'


class Configurable(object):
    def __init__(self, *args, file=config_path, **kwargs):
        super().__init__(*args, **kwargs)
        self.file = file

    def get_value(self, *keys):
        config = self.read_config()
        for key in keys:
            config = config[key]
        return config

    def read_config(self):
        return read_config(self.file)

    def __getattr__(self, name):
        """called automatically when an attribute does not exist"""
        base, sup = [x.__name__ for x in self.__class__.__mro__[::-1][-2:]]
        return self.get_value(base, sup, name)


def read_config(path=config_path):
    with open(path) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config
