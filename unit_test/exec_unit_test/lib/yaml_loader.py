import yaml
import os

class YamlLoader():
    def __init__(self, module_name):
        self.my_yaml = os.path.splitext(module_name)[0] + '.yaml'
        with open(self.my_yaml, 'r', encoding='UTF-8') as f:
            self.my_settings = yaml.safe_load(f)
    def get_yaml_info(self, key1, key2):
        value = self.my_settings[key1][key2]
        index = 0
        while os.path.splitext(value)[1] == '.yaml':
            if index > 4:
                break
            yaml = YamlLoader(value)
            value = yaml.my_settings[key1][key2]
            index += 1
        return value.replace('\\n','\n')
    def get_yaml_dict(self, key1):
        return self.my_settings[key1]
    def get_yaml_all(self):
        return self.my_settings
    def save(self, update_info):
        with open(self.my_yaml, 'r', encoding='UTF-8') as f:
            data_all = f.readlines()
        index_info = self._create_index_info(data_all)
        for key, value in update_info.items():
            posi = index_info.get(key)
            for index in range(posi[0] + 1, posi[1] + 1):
                kind = data_all[index].strip().split(':')[0]
                if (path := update_info[key].get(kind)) != None:
                    data_all[index] = f"  {kind}:  '{path}'\n"
        with open(self.my_yaml, 'w', encoding='UTF-8') as f:
            f.writelines(data_all)
        with open(self.my_yaml, 'r', encoding='UTF-8') as f:
            self.my_settings = yaml.safe_load(f)
    def _create_index_info(self, data_all):
        index_info = {}
        key = ''
        key_posi = end_posi = -1, 
        for index, data in enumerate(data_all):
            if data == '':
                continue
            if data[0] != ' ':
                key = str(data).strip().replace(':', '')
                key_posi = index
                end_posi = index
            else:
                end_posi = index
            index_info[key] = (key_posi, end_posi)
        return index_info
