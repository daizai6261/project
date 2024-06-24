import configparser
import os


class Configer(configparser.ConfigParser):
    """定义一个读取配置文件的类"""

    def __init__(self, defaults=None):
        configparser.ConfigParser.__init__(self, defaults=defaults)

        root_dir = os.path.dirname(os.path.abspath('.'))
        configpath = os.path.join(root_dir, "project\config\config.ini")
        self.cfg = configparser.RawConfigParser()
        self.cfg.optionxform = str
        self.cfg.read(configpath, encoding='utf-8')

        cfg_orc_error_path = os.path.join(root_dir, "project\config\cfg_orc_error.ini")
        self.cfg_orc_error = configparser.RawConfigParser()
        self.cfg_orc_error.optionxform = str
        self.cfg_orc_error.read(cfg_orc_error_path, encoding='utf-8')

    def optionxform(self, optionstr):
        print("optionxform", optionstr)
        return optionstr

    def get_value(self, table, param):
        value = self.cfg.get(table, param)
        if not value:
            print("config get value failed", table, param)
        return value

    def program_param(self, param):
        value = self.get_value("RUN_PARAM", param)
        return value

    def api_type(self, param):
        value = self.get_value("API_TYPE", param)
        return value

    def word_param(self, param):
        value = self.get_value("WORD", param)
        return value

    def run_param(self, param):
        value = self.get_value("RUN_PARAM", param)
        return value

    def speaker_slience(self, param):
        data = self.get_value("SPEAKER_SILENCE", param)
        value = data.split(',')
        return value

    def orc_error_word(self, param):

        value = self.cfg_orc_error.get("ORC_ERROR_WORD", param)
        if not value:
            print("cfg_orc_error get value failed", table, param)
        return value


configer = Configer()
