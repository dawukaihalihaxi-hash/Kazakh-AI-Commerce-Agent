import requests
import base64
import mimetypes


from config import (
    AGNES_API_KEY,
    AGNES_BASE_URL,
    AGNES_VIDEO_MODEL
)



class AgnesVideo:


    def __init__(self):

        self.api_key = AGNES_API_KEY

        self.base_url = AGNES_BASE_URL.rstrip("/")

        self.model = AGNES_VIDEO_MODEL



    # =========================
    # 公共请求头
    # =========================

    def get_headers(self):

        return {

            "Authorization":
            f"Bearer {self.api_key}",

            "Content-Type":
            "application/json"

        }



    # =========================
    # 创建视频任务
    # =========================

    def generate_video(
        self,
        image_path,
        prompt
    ):


        try:


            # =====================
            # 检查图片
            # =====================

            if not image_path:

                return {
                    "error":
                    "没有提供商品图片"
                }



            # =====================
            # 获取图片类型
            # =====================

            mime_type, _ = mimetypes.guess_type(
                image_path
            )


            if mime_type is None:

                mime_type = "image/jpeg"



            # =====================
            # 图片转 Base64
            # =====================

            with open(
                image_path,
                "rb"
            ) as image_file:


                image_base64 = base64.b64encode(

                    image_file.read()

                ).decode(
                    "utf-8"
                )



            image_data = (

                f"data:{mime_type};base64,"
                f"{image_base64}"

            )



            # =====================
            # 请求参数
            # =====================

            body = {

                "model":
                self.model,

                "prompt":
                prompt,

                "image":
                image_data,

                "duration":
                5

            }



            print("====================")

            print("正在请求 Agnes 视频模型")

            print(
                "当前视频模型：",
                self.model
            )

            print("====================")



            response = requests.post(

                self.base_url,

                headers=self.get_headers(),

                json=body,

                timeout=180

            )



            print(
                "HTTP状态码：",
                response.status_code
            )


            print("====================")

            print("Agnes返回：")

            print(
                response.text
            )

            print("====================")



            # =====================
            # HTTP错误
            # =====================

            if response.status_code != 200:

                return {

                    "error":
                    "视频任务创建失败",

                    "status_code":
                    response.status_code,

                    "response":
                    response.text

                }



            data = response.json()



            # =====================
            # 获取任务ID
            # =====================

            task_id = (

                data.get("task_id")
                or
                data.get("video_id")
                or
                data.get("id")

            )



            if not task_id:

                return {

                    "error":
                    "视频任务已经提交，但没有返回 task_id",

                    "response":
                    data

                }



            return {

                "success":
                True,

                "task_id":
                task_id,

                "status":
                data.get(
                    "status",
                    "queued"
                ),

                "progress":
                data.get(
                    "progress",
                    0
                ),

                "response":
                data

            }



        except Exception as e:


            return {

                "error":
                f"Agnes视频生成请求失败：{e}"

            }





    # =========================
    # 查询视频任务
    # =========================

    def get_video_status(
        self,
        task_id
    ):


        try:


            if not task_id:

                return {

                    "error":
                    "没有提供 task_id"

                }



            # Agnes 使用 OpenAI 风格视频接口。
            # 视频任务地址：
            # /v1/videos/{task_id}

            status_url = (

                f"{self.base_url}/"
                f"{task_id}"

            )



            print("====================")

            print("正在查询 Agnes 视频状态")

            print(
                "task_id：",
                task_id
            )

            print("====================")



            response = requests.get(

                status_url,

                headers=self.get_headers(),

                timeout=60

            )



            print(
                "查询HTTP状态码：",
                response.status_code
            )


            print("====================")

            print("视频状态返回：")

            print(
                response.text
            )

            print("====================")



            if response.status_code != 200:

                return {

                    "error":
                    "视频状态查询失败",

                    "status_code":
                    response.status_code,

                    "response":
                    response.text

                }



            data = response.json()



            status = data.get(
                "status",
                "unknown"
            )


            progress = data.get(
                "progress",
                0
            )



            # =====================
            # 尝试寻找最终视频URL
            # =====================

            video_url = (

                data.get("video_url")

                or

                data.get("url")

                or

                data.get("output_url")

            )



            # 某些接口把结果放在 output 中

            output = data.get(
                "output"
            )


            if (
                not video_url
                and
                isinstance(
                    output,
                    dict
                )
            ):

                video_url = (

                    output.get(
                        "video_url"
                    )

                    or

                    output.get(
                        "url"
                    )

                )



            return {

                "success":
                True,

                "task_id":
                task_id,

                "status":
                status,

                "progress":
                progress,

                "video_url":
                video_url,

                "response":
                data

            }



        except Exception as e:


            return {

                "error":
                f"Agnes视频状态查询失败：{e}"

            }