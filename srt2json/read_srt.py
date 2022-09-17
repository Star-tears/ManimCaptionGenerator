import json


def read_srt_file(srt_path="test_src_files/default_test.srt"):
    with open(srt_path, "r", encoding="utf-8") as srt_file:
        caption_list = []
        default_caption_list_element = {"start-time": "", "end-time": "", "caption-group": []}
        flag = 0
        for element in srt_file.readlines():
            line = element.strip()
            if len(line) == 0:
                flag = 0
                continue
            if flag == 0 and int(line) == len(caption_list) + 1:
                caption_list.append(default_caption_list_element)
                flag = 1
                continue
            if flag == 1:
                time_list = line.split(' --> ')
                caption_list[len(caption_list) - 1]["start-time"] = time_list[0]
                caption_list[len(caption_list) - 1]["end-time"] = time_list[1]
                flag = 2
            elif flag == 2:
                caption_list[len(caption_list) - 1]["caption-group"].append(line)
        print(caption_list)
