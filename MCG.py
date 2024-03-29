import json
import re

from manim import *
from srt2json.srt_to_json import srt_to_json
from MapperUtils.manimMapper.MixMapper import *

mp: MixMapper = MixMapper()


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
        if "caption_group" in now_all_attr_config.keys():
            self.build_caption(now_all_attr_config)
        else:
            for sub_config in now_config["caption_list"]:
                copy_now_all_attr_config: dict = {}
                self.add_attr_config_dict(now_all_attr_config, copy_now_all_attr_config)
                self.add_attr_config_dict(sub_config, copy_now_all_attr_config)
                self.build_video(sub_config, copy_now_all_attr_config)

    def add_attr_config_dict(self, d1: dict, d2: dict):
        """
        将d1字典的属性递归加到d2字典，已有属性进行覆盖

        :param d1: 加字典
        :param d2: 被加字典
        :return: void
        """
        for key_d1 in d1.keys():
            if key_d1 != "caption_list":
                if type(d1[key_d1]) == type({}):
                    if key_d1 not in d2.keys():
                        d2[key_d1] = {}
                    self.add_attr_config_dict(d1[key_d1], d2[key_d1])
                else:
                    d2[key_d1] = d1[key_d1]
            elif key_d1 == "caption_group":
                d2[key_d1] = d1[key_d1]

    def time_to_int(self, s1: str) -> int:
        tmp_time_tick: int = 0
        l1 = re.split('[:,]', s1)
        tmp_time_tick += int(l1[3])
        tmp_time_tick += int(l1[2]) * 1000
        tmp_time_tick += int(l1[1]) * 1000 * 60
        tmp_time_tick += int(l1[0]) * 1000 * 60 * 60
        return tmp_time_tick

    def build_caption(self, attr_config: dict):
        caption_group_list: list = attr_config["caption_group"]
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
        create_animation_run_time_tick: int = min(2000, int(tot_time_tick * 0.2))
        uncreate_animation_run_time_tick: int = min(2000, int(tot_time_tick * 0.1))
        mid_run_time_tick: int = tot_time_tick - create_animation_run_time_tick - uncreate_animation_run_time_tick

        caption_vgroup = self.build_caption_vgroup(attr_config)

        self.create_caption(caption_vgroup, attr_config, create_animation_run_time_tick / 1000)
        if mp.isKeysInDict(["animation", "transform_target"], attr_config):
            self.add_attr_config_dict(attr_config["animation"]["transform_target"], attr_config)
            caption_vgroup2 = self.build_caption_vgroup(attr_config)
            self.transform_caption(caption_vgroup, caption_vgroup2, mid_run_time_tick)
        else:
            self.wait_safely(mid_run_time_tick / 1000)
        self.uncreate_caption(caption_vgroup, attr_config, uncreate_animation_run_time_tick / 1000)

        self.now_time_tick = end_time_tick

    def wait_safely(self, wait_run_time: float):
        if wait_run_time > 0:
            self.wait(wait_run_time)

    def create_caption(self, caption_vgroup, attr_config: dict, create_animation_run_time):
        key = None
        if mp.isKeysInDict(["animation", "create"], attr_config):
            key = attr_config["animation"]["create"]
        self.play(mp.getObjFromKey(key, ManimObjEnum.Write)(caption_vgroup), run_time=create_animation_run_time)

    def transform_caption(self, caption_vgroup, caption_vgroup2, tot_run_time_tick: int):
        pre_wait_run_time_tick: int = min(2000, int(tot_run_time_tick * 0.2))
        transform_run_time_tick: int = min(2000, int(tot_run_time_tick * 0.2))
        wait_run_time_tick: int = tot_run_time_tick - pre_wait_run_time_tick - transform_run_time_tick
        self.wait_safely(pre_wait_run_time_tick / 1000)
        self.play(Transform(caption_vgroup, caption_vgroup2), run_time=transform_run_time_tick / 1000, rate_func=smooth)
        self.wait_safely(wait_run_time_tick / 1000)

    def uncreate_caption(self, caption_vgroup, attr_config, uncreate_animation_run_time):
        key = None
        if mp.isKeysInDict(["animation", "uncreate"], attr_config):
            key = attr_config["animation"]["uncreate"]
        self.play(mp.getObjFromKey(key, ManimObjEnum.FadeOut)(caption_vgroup), run_time=uncreate_animation_run_time)

    def build_caption_vgroup(self, attr_config: dict) -> VGroup:
        caption_group_list: list = attr_config["caption_group"]
        caption_vgroup: VGroup = VGroup()
        print(attr_config)
        for content_caption_element in caption_group_list:
            caption_element = None
            if attr_config["content_type"] == "text":
                caption_element = Text(content_caption_element, **attr_config["style"])
            else:
                caption_element = Tex(content_caption_element, tex_template=TexTemplateLibrary.ctex,
                                      **attr_config["latex_style"])
            caption_vgroup.add(caption_element)

        key = None
        if mp.isKeysInDict(["position", "to_edge"], attr_config):
            key = attr_config["position"]["to_edge"]
        print("transform position:", key)
        caption_vgroup.arrange(DOWN).to_edge(mp.getObjFromKey(key, ManimObjEnum.DOWN),
                                             buff=mp.key2obj(ManimObjEnum.LARGE_BUFF))

        return caption_vgroup
