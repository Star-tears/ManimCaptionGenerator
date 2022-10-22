import json
import re

from manim import *
from srt2json.srt_to_json import srt_to_json


class ManimCaptionGenerator(Scene):
    TEXT_CONFIG = {}
    now_time_tick: int
    now_dfs_count: int

    def construct(self):
        while True:
            print("[1]srt文件转换json [2]json转换video")
            print(">>> ", end='')
            op = input()
            if op == "1":
                print("srt文件路径: ", end='')
                srt_path = input()
                print("输出json路径: ", end='')
                output_json_path = input()
                srt_json_config_path = "default_srt_json_config.json"
                self.build_srt_json(srt_path, output_json_path, srt_json_config_path)
            elif op == "2":
                print("字幕json文件路径: ", end='')
                srt_json_path = input()
                srt_json_config = self.preload_srt_json(srt_json_path)
                self.init_attr()
                copy_text_config = {}
                self.add_attr_config_dict(self.TEXT_CONFIG, copy_text_config)
                # print(json.dumps(copy_text_config, indent=4, ensure_ascii=False))
                self.build_video(srt_json_config, copy_text_config)
                self.wait(1)
                self.now_time_tick += 1000
                break
            else:
                print("输入错误")

    def init_attr(self):
        self.now_time_tick = 0
        self.now_dfs_count = 0

    def build_srt_json(self, srt_path="default_files/MCG默认字幕文件.srt",
                       output_json_path="default_files/MCG默认字幕文件.json",
                       srt_json_config_path="default_srt_json_config.json"):
        srt_to_json(srt_path, output_json_path, srt_json_config_path)

    def preload_srt_json(self, json_path="default_files/MCG默认字幕文件.json"):
        srt_json_config = self.read_srt_json_config(json_path)
        # print(1)
        # print(srt_json_config)
        self.gradient_list2tuple(srt_json_config)
        # print(2)
        # print(srt_json_config)
        return srt_json_config

    def gradient_list2tuple(self, d1: dict):
        for key_d1 in d1.keys():
            if key_d1 == "style":
                style_dict: dict = d1[key_d1]
                for key_style_dict in style_dict.keys():
                    if key_style_dict == "gradient":
                        style_dict[key_style_dict] = tuple(style_dict[key_style_dict])
                    if key_style_dict == "t2g":
                        for key_style_dict in style_dict["t2g"].keys():
                            style_dict["t2g"][key_style_dict] = tuple(style_dict["t2g"][key_style_dict])
            if key_d1 == "caption_list":
                for sub_caption in d1["caption_list"]:
                    self.gradient_list2tuple(sub_caption)

    def read_srt_json_config(self, srt_json_config_path="default_files/MCG默认字幕文件.json") -> dict:
        with open(srt_json_config_path, "r", encoding="utf-8") as config_file:
            srt_json_config = json.load(config_file)
            return srt_json_config

    def build_video(self, now_config: dict, now_all_attr_config: dict):
        print(self.now_dfs_count)
        self.now_dfs_count += 1
        # print(json.dumps(now_all_attr_config, indent=4, ensure_ascii=False))
        self.add_attr_config_dict(now_config, now_all_attr_config)
        # print(json.dumps(now_all_attr_config, indent=4, ensure_ascii=False))
        # print(json.dumps(now_config, indent=4, ensure_ascii=False))
        if "caption_group" in now_config.keys():
            self.build_caption(now_config["caption_group"], now_all_attr_config)
        else:
            for sub_config in now_config["caption_list"]:
                copy_now_all_attr_config = {}
                self.add_attr_config_dict(now_all_attr_config, copy_now_all_attr_config)
                self.add_attr_config_dict(sub_config, copy_now_all_attr_config)
                self.build_video(sub_config, copy_now_all_attr_config)

    def add_attr_config_dict(self, d1: dict, d2: dict):
        for key_d1 in d1.keys():
            if key_d1 != "caption_group" and key_d1 != "caption_list":
                if type(d1[key_d1]) == type({}):
                    if key_d1 not in d2.keys():
                        d2[key_d1] = {}
                    self.add_attr_config_dict(d1[key_d1], d2[key_d1])
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
        # print(json.dumps(attr_config, indent=4, ensure_ascii=False))

        pre_wait_time_tick = start_time_tick - self.now_time_tick
        self.wait_safely(pre_wait_time_tick / 1000)
        self.now_time_tick = start_time_tick

        tot_time_tick: int = end_time_tick - start_time_tick
        create_animation_run_time: int = min(2000, int(tot_time_tick * 0.2))
        uncreate_animation_run_time: int = min(2000, int(tot_time_tick * 0.1))
        mid_run_time: int = tot_time_tick - create_animation_run_time - uncreate_animation_run_time

        caption_vgroup = self.build_caption_vgroup(caption_group_list, attr_config)

        self.create_caption(caption_vgroup, attr_config, create_animation_run_time / 1000)
        self.wait_safely(mid_run_time / 1000)
        self.uncreate_caption(caption_vgroup, attr_config, uncreate_animation_run_time / 1000)

        self.now_time_tick = end_time_tick

    def wait_safely(self, wait_run_time: float):
        if wait_run_time > 0:
            self.wait(wait_run_time)

    def create_caption(self, caption_vgroup, attr_config:dict, create_animation_run_time):
        if "animation" in attr_config.keys():
            ani_dict:dict = attr_config["animation"]
            if "create" in ani_dict.keys():
                match ani_dict["create"]:
                    case "Create":
                        self.play(Create(caption_vgroup), run_time=create_animation_run_time)
                    case "FadeIn":
                        self.play(FadeIn(caption_vgroup), run_time=create_animation_run_time)
                    case _:
                        self.play(Write(caption_vgroup), run_time=create_animation_run_time)
            else:
                self.play(Write(caption_vgroup), run_time=create_animation_run_time)
        else:
            self.play(Write(caption_vgroup), run_time=create_animation_run_time)

    def uncreate_caption(self, caption_vgroup, attr_config, uncreate_animation_run_time):
        if "animation" in attr_config.keys():
            ani_dict:dict = attr_config["animation"]
            if "uncreate" in ani_dict.keys():
                match ani_dict["uncreate"]:
                    case "Uncreate":
                        self.play(Uncreate(caption_vgroup), run_time=uncreate_animation_run_time)
                    case "Unwrite":
                        self.play(Unwrite(caption_vgroup), run_time=uncreate_animation_run_time)
                    case _:
                        self.play(FadeOut(caption_vgroup), run_time=uncreate_animation_run_time)
            else:
                self.play(FadeOut(caption_vgroup), run_time=uncreate_animation_run_time)
        else:
            self.play(FadeOut(caption_vgroup), run_time=uncreate_animation_run_time)

    def build_caption_vgroup(self, caption_group_list: list, attr_config: dict) -> VGroup:
        caption_vgroup: VGroup = VGroup()
        for content_caption_element in caption_group_list:
            caption_element = None
            if attr_config["content_type"] == "text":
                print(attr_config["style"])
                caption_element = Text(content_caption_element, **attr_config["style"])
            else:
                print(attr_config["latex_style"])
                caption_element = Tex(content_caption_element, tex_template=TexTemplateLibrary.ctex,
                                      **attr_config["latex_style"])
            caption_vgroup.add(caption_element)
        if "position" in attr_config.keys():
            pos_dict: dict = attr_config["position"]
            if "to_edge" in pos_dict.keys():
                match pos_dict["to_edge"]:
                    case "ORIGIN":
                        caption_vgroup.arrange(DOWN).to_edge(ORIGIN, buff=LARGE_BUFF)
                    case "UP":
                        caption_vgroup.arrange(DOWN).to_edge(UP, buff=LARGE_BUFF)
                    case "LEFT":
                        caption_vgroup.arrange(DOWN).to_edge(LEFT, buff=LARGE_BUFF)
                    case _:
                        caption_vgroup.arrange(DOWN).to_edge(DOWN, buff=LARGE_BUFF)
            else:
                caption_vgroup.arrange(DOWN).to_edge(DOWN, buff=LARGE_BUFF)
        else:
            caption_vgroup.arrange(DOWN).to_edge(DOWN, buff=LARGE_BUFF)

        return caption_vgroup
