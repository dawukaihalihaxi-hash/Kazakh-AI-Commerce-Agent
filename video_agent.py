import os


from services.agnes_video import AgnesVideo




class VideoAgent:


    def __init__(self):

        self.video_service = AgnesVideo()



    def run(
        self,
        image_paths,
        script_result
    ):


        """
        视频生成 Agent

        输入：

        image_paths:
        商品图片列表


        script_result:
        ScriptAgent生成的视频脚本


        输出：

        Agnes视频生成结果

        """



        print("====================")

        print("Video Agent 开始运行")

        print("====================")



        # =====================
        # 检查图片
        # =====================


        if not image_paths:


            return {

                "error":
                "没有商品图片"

            }



        # =====================
        # MVP阶段：
        # 先使用第一张图片
        # =====================


        image_path = image_paths[0]



        print("====================")

        print(
            "使用视频生成图片：",
            image_path
        )

        print("====================")





        # =====================
        # 构造视频Prompt
        # =====================


        video_prompt = f"""

请根据商品图片和以下营销脚本，

生成一个电商短视频。


视频要求：

- 高级商业广告风格
- 展示商品特点
- 展示使用场景
- 适合短视频平台


营销脚本：

{script_result}


"""





        # =====================
        # 调用 Agnes
        # =====================


        result = self.video_service.generate_video(

            image_path,

            video_prompt

        )



        return result