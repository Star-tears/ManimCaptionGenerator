from manim import *
import enum


class ManimObjEnum:
    Write = "Write"
    Create = "Create"
    FadeIn = "FadeIn"
    Unwrite = "Unwrite"
    Uncreate = "Uncreate"
    FadeOut = "FadeOut"
    SMALL_BUFF = "SMALL_BUFF"
    MED_SMALL_BUFF = "MED_SMALL_BUFF"
    MED_LARGE_BUFF = "MED_LARGE_BUFF"
    LARGE_BUFF = "LARGE_BUFF"
    ORIGIN = "ORIGIN"
    CENTER = "CENTER"
    UP = "UP"
    DOWN = "DOWN"
    RIGHT = "RIGHT"
    LEFT = "LEFT"


class MixMapper:
    mixMapper: dict = {
        "Write": Write,
        "Create": Create,
        "FadeIn": FadeIn,
        "Unwrite": Unwrite,
        "Uncreate": Uncreate,
        "FadeOut": FadeOut,
        "SMALL_BUFF": SMALL_BUFF,
        "MED_SMALL_BUFF": MED_SMALL_BUFF,
        "MED_LARGE_BUFF": MED_LARGE_BUFF,
        "LARGE_BUFF": LARGE_BUFF,
        "ORIGIN": ORIGIN,
        "CENTER": ORIGIN,
        "UP": UP,
        "DOWN": DOWN,
        "RIGHT": RIGHT,
        "LEFT": LEFT
    }

    def getObjFromKey(self, key, default_key):
        if self.isKeyInDict(key, self.mixMapper):
            return self.mixMapper[key]
        return self.key2obj(default_key)

    def key2obj(self, key):
        if self.isKeyInDict(key, self.mixMapper):
            return self.mixMapper[key]
        return key

    def isKeyInDict(self, key, d1: dict) -> bool:
        return key in d1.keys()

    def isKeysInDict(self, keys_list: list, d1: dict) -> bool:
        d2 = d1
        for key in keys_list:
            if key not in d2.keys():
                return False
            d2 = d2[key]
        return True
