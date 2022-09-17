import json

from read_srt import *
from default_config import *


def srt_to_json(srt_path="./test_src_files/default_test.srt", json_path="./test_output_files/default_test.json"):
    dict_json = {}
    for key, value in get_config().items():
        if len(value) > 0:
            dict_json[key] = value
    dict_json["caption_list"] = read_srt_file()
    print(json.dumps(dict_json, indent=4, ensure_ascii=False))
    with open(json_path, "w",encoding="utf-8") as json_file:
        json.dump(dict_json, json_file, indent=4, ensure_ascii=False)
