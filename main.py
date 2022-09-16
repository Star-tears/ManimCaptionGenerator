from manimlib import *


class TextExample(Scene):
    def construct(self):
        # 想要正确运行这个场景，你需要确保你的计算机中安装了Consolas字体
        # 关于Text全部用法，请见https://github.com/3b1b/manim/pull/680
        text = Text("Here is a text", font="Microsoft JhengHei UI", font_size=90)
        difference = Text(
            """
            你好 这是一个manim字幕生成器的中文测试\n
            you can change the font more easily, but can't use the LaTeX grammar
            """,
            font="HarmonyOS Sans SC", font_size=24,
            # t2c是一个由 文本-颜色 键值对组成的字典
            t2c={"你好": BLUE, "manim": BLUE, "LaTeX": ORANGE}
        )
        VGroup(text, difference).arrange(DOWN, buff=1)
        self.play(Write(text), run_time=0.1)
        self.play(FadeIn(difference, UP))
        self.wait(1)
