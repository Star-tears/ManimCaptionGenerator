import json


def srt_to_json(srt_path="test_src_files/default_test.srt", json_path="test_output_files/default_test.json",
                srt_json_config="test_src_files/default_test.srt"):
    """
    将srt字幕文件转换为json文件
    :param srt_json_config: srt转换成的json基础属性设置
    :param srt_path:srt字幕文件路径
    :param json_path:输出json文件路径
    :return:暂无返回值
    """
    dict_json = {}
    for key, value in get_config(srt_json_config).items():
        if len(value) > 0:
            dict_json[key] = value
    dict_json["caption_list"] = read_srt_file(srt_path)
    # print(json.dumps(dict_json, indent=4, ensure_ascii=False))
    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(dict_json, json_file, indent=4, ensure_ascii=False)


def read_srt_file(srt_path="test_src_files/default_test.srt"):
    """
    读取srt文件
    :param srt_path:srt字幕文件所在路径
    :return: 暂无返回值
    """
    with open(srt_path, "r", encoding="utf-8") as srt_file:
        caption_list = []
        default_caption_list_element = {"start_time": "", "end_time": ""}
        flag = 0
        for element in srt_file.readlines():
            line = element.strip()
            if len(line) == 0:
                flag = 0
                continue
            if flag == 0 and int(line) == len(caption_list) + 1:
                caption_list.append(default_caption_list_element.copy())
                caption_list[len(caption_list) - 1]["caption_group"] = []
                flag = 1
                continue
            if flag == 1:
                time_list = line.split(' --> ')
                caption_list[len(caption_list) - 1]["start_time"] = time_list[0]
                caption_list[len(caption_list) - 1]["end_time"] = time_list[1]
                flag = 2
            elif flag == 2:
                caption_list[len(caption_list) - 1]["caption_group"].append(line)
        return caption_list


def get_config(config_path="default_config.json"):
    with open(config_path, "r", encoding="utf-8") as config_file:
        config = json.load(config_file)
        return config
