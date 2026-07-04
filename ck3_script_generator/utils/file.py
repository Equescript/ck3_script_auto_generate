import json
def read_json(file_path: str):
    """ 读取json文件并返回字典数据 """
    with open(file_path, 'r') as json_file:
        json_data = json.load(json_file)
        json_file.close()
        return json_data


def write_json(file_path: str, json_data):
    """ 向json文件中写入数据 """
    with open(file_path, 'w') as json_file:
        json_file.write(json.dumps(json_data, ensure_ascii=False, indent=4, separators=(',', ': ')))
        # , ensure_ascii=False, encoding='utf-8'
        json_file.close()

def write_file(file_path: str, data: str):
    with open(file_path, 'w', encoding="utf-8-sig") as file:
        file.write(data)
        file.close()
