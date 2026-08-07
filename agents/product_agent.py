import os

from llm import LLM



class ProductAgent:


    def __init__(self):

        self.llm = LLM()





    def run(
        self,
        product_info,
        image_paths=None
    ):


        # 获取项目根目录

        BASE_DIR = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )



        # =========================
        # 读取商品分析 Prompt
        # =========================


        prompt_path = os.path.join(

            BASE_DIR,

            "prompts",

            "product.txt"

        )



        with open(

            prompt_path,

            "r",

            encoding="utf-8"

        ) as f:

            prompt_template = f.read()





        # =========================
        # 多图片视觉分析
        # =========================


        vision_results = []



        if image_paths:


            print("====================")

            print("ProductAgent收到图片：")

            print(image_paths)

            print("====================")



            for image_path in image_paths:


                print("====================")

                print(
                    "检测图片路径：",
                    image_path
                )

                print(
                    "图片是否存在：",
                    os.path.exists(image_path)
                )

                print("====================")



                if os.path.exists(image_path):


                    vision_prompt = """

请分析这张商品图片。

请从电商营销角度输出：

1. 商品外观特点
2. 商品颜色、形状、包装特点
3. 可以观察到的材质信息
4. 可以用于短视频展示的视觉元素
5. 图片无法确认的信息

要求：

不要编造图片中不存在的信息。

"""



                    vision_result = self.llm.chat_with_image(

                        image_path,

                        vision_prompt

                    )



                    vision_results.append(

                        f"""

图片：

{image_path}


视觉分析结果：

{vision_result}

"""

                    )



        else:


            print("====================")

            print("没有上传商品图片")

            print("====================")





        # =========================
        # 合并视觉结果
        # =========================


        if vision_results:


            vision_content = "\n".join(

                vision_results

            )


        else:


            vision_content = """

没有有效图片分析结果。

请仅根据文字信息分析。

"""





        print("====================")

        print("视觉分析汇总完成")

        print("====================")





        # =========================
        # GLM-5.2 商品分析
        # =========================


        final_prompt = f"""

{prompt_template}



用户提供的商品信息：

{product_info}



商品图片视觉分析：

{vision_content}



请结合文字信息和图片视觉信息，

完成完整商品营销分析。

"""




        result = self.llm.chat(

            final_prompt

        )



        return result
