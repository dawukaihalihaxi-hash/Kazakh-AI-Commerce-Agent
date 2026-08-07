import os


from llm import LLM




class ScriptAgent:


    def __init__(self):

        self.llm = LLM()





    def run(
        self,
        product_analysis,
        script_mode="both"
    ):


        # =========================
        # 获取项目根目录
        # =========================


        BASE_DIR = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )



        # =========================
        # 读取 Prompt
        # =========================


        prompt_path = os.path.join(

            BASE_DIR,

            "prompts",

            "script.txt"

        )



        with open(

            prompt_path,

            "r",

            encoding="utf-8"

        ) as f:


            prompt_template = f.read()





        # =========================
        # 根据用户选择生成版本
        # =========================


        if script_mode == "cyrillic":


            language_instruction = """

请只生成哈萨克语西里尔字母版本。

不要生成拉丁转写版本。

"""



        elif script_mode == "latin":


            language_instruction = """

请只生成哈萨克语拉丁字母转写版本。

不要生成西里尔字母版本。

"""



        else:


            language_instruction = """

请同时生成：

1. 哈萨克语西里尔字母版本

2. 哈萨克语拉丁字母转写版本

"""






        # =========================
        # 组合最终 Prompt
        # =========================


        final_prompt = f"""

{prompt_template}



以下是商品分析结果：

{product_analysis}



脚本语言要求：

{language_instruction}



请根据以上商品信息，

生成适合短视频平台的哈萨克语营销视频脚本。

"""






        # =========================
        # 调用大模型
        # =========================


        result = self.llm.chat(

            final_prompt

        )



        return result
