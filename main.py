import json
import re

from manim import *
from srt2json.srt_to_json import srt_to_json


class ManimCaptionGenerator(Scene):
    TEXT_CONFIG = {
        "content_type": "text",
        "style": {
            "font": "HarmonyOS Sans SC",
            "font_size": 25,
            "color": "GREEN"
        },
        "animation": {},
        "start_time": "",
        "end_time": ""
    }
    now_time_tick: int
    now_dfs_count: int

    def construct(self):
        self.build_srt_json()
        srt_json_config = self.read_srt_json_config()
        self.init_attr()
        self.build_video(srt_json_config, self.TEXT_CONFIG.copy())
        self.wait(1)
        self.now_time_tick += 1000

    def init_attr(self):
        self.now_time_tick = 0
        self.now_dfs_count = 0

    def build_srt_json(self, srt_path="default-files/MCG默认字幕文件.srt",
                       output_json_path="default-files/MCG默认字幕文件.json",
                       srt_json_config_path="default_srt_json_config.json"):
        srt_to_json(srt_path, output_json_path, srt_json_config_path)

    def read_srt_json_config(self, srt_json_config_path="default-files/MCG默认字幕文件.json") -> dict:
        with open(srt_json_config_path, "r", encoding="utf-8") as config_file:
            srt_json_config = json.load(config_file)
            return srt_json_config

    def build_video(self, now_config: dict, now_all_attr_config: dict):
        print(self.now_dfs_count)
        self.now_dfs_count += 1
        # print(json.dumps(now_all_attr_config, indent=4, ensure_ascii=False))
        self.merge_attr_config_dict(now_config, now_all_attr_config)
        # print(json.dumps(now_all_attr_config, indent=4, ensure_ascii=False))
        # print(json.dumps(now_config, indent=4, ensure_ascii=False))
        if "caption_group" in now_config.keys():
            self.build_caption(now_config["caption_group"], now_all_attr_config)
        else:
            for sub_config in now_config["caption_list"]:
                self.build_video(sub_config, now_all_attr_config.copy())

    def merge_attr_config_dict(self, d1: dict, d2: dict):
        for key_d1 in d1.keys():
            if key_d1 != "caption_group" and key_d1 != "caption_list":
                if type(d1[key_d1]) == type({}):
                    if key_d1 not in d2.keys():
                        d2[key_d1] = {}
                    self.merge_attr_config_dict(d1[key_d1], d2[key_d1])
                else:
                    d2[key_d1] = d1[key_d1]

    def time_to_int(self, s1: str) -> int:
        tmp_time_tick: int = 0
        l1 = re.split('[:,]', s1)
        tmp_time_tick += int(l1[3])
        tmp_time_tick += int(l1[2]) * 1000
        tmp_time_tick += int(l1[1]) * 1000 * 60
        tmp_time_tick += int(l1[0]) * 1000 * 60 * 60
        return tmp_time_tick

    def build_caption(self, caption_group_list: list, attr_config: dict):
        start_time_tick = self.time_to_int(attr_config["start_time"])
        end_time_tick = self.time_to_int(attr_config["end_time"])
        print("start_time: ", attr_config["start_time"], start_time_tick)
        print("end_time: ", attr_config["end_time"], end_time_tick)
        print(caption_group_list)
        print(json.dumps(attr_config, indent=4, ensure_ascii=False))

        pre_wait_time_tick=start_time_tick-self.now_time_tick
        if(pre_wait_time_tick>0):
            self.wait(pre_wait_time_tick/1000)
        self.now_time_tick = start_time_tick

        tot_time_tick: int = end_time_tick - start_time_tick
        create_animation_run_time: int = min(2000, int(tot_time_tick * 0.2))
        uncreate_animation_run_time: int = min(2000, int(tot_time_tick * 0.1))
        wait_run_time: int = tot_time_tick - create_animation_run_time - uncreate_animation_run_time

        caption_vgroup = VGroup()
        for content_caption_element in caption_group_list:
            caption_element=None
            if (attr_config["content_type"] == "text"):
                caption_element = Text(content_caption_element, **attr_config["style"])
            else:
                caption_element = Tex(content_caption_element, tex_template=TexTemplateLibrary.ctex,
                                      **attr_config["latex_style"])
            caption_vgroup.add(caption_element)
        caption_vgroup.arrange(DOWN).to_edge(DOWN)
        self.create_caption(caption_vgroup, attr_config, create_animation_run_time / 1000)
        self.wait(wait_run_time / 1000)
        self.uncreate_caption(caption_vgroup, attr_config, uncreate_animation_run_time / 1000)

        self.now_time_tick = end_time_tick

    def create_caption(self, caption_vgroup, attr_config, create_animation_run_time):
        self.play(Write(caption_vgroup), run_time=create_animation_run_time)

    def uncreate_caption(self, caption_vgroup, attr_config, uncreate_animation_run_time):
        self.play(FadeOut(caption_vgroup), run_time=uncreate_animation_run_time)
