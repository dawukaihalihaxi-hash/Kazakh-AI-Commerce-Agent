import requests
import base64
import mimetypes


from config import (
    API_KEY,
    BASE_URL,
    TEXT_MODEL,
    VISION_MODEL
)



class LLM:


    def __init__(self):

        self.api_key = API_KEY

        self.base_url = BASE_URL

        self.text_model = TEXT_MODEL

        self.vision_model = VISION_MODEL




    def chat(self, prompt):

        """
        文本模型调用

        使用：
        TEXT_MODEL
        """

        headers = {

            "Authorization": f"Bearer {self.api_key}",

            "Content-Type": "application/json"

        }



        body = {

            "model": self.text_model,

            "messages": [

                {

                    "role": "user",

                    "content": prompt

                }

            ]

        }



        try:


            print("====================")

            print("正在请求文本 AI")

            print(
                "当前文本模型：",
                self.text_model
            )

            print("====================")



            response = requests.post(

                self.base_url,

                headers=headers,

                json=body,

                timeout=180

            )



            print(
                "HTTP状态码：",
                response.status_code
            )



            response.raise_for_status()



            data = response.json()



            return data["choices"][0]["message"]["content"]



        except Exception as e:


            return f"文本模型请求失败：{e}"







    def chat_with_image(
        self,
        image_path,
        prompt
    ):

        """
        视觉模型调用

        使用：
        VISION_MODEL

        输入：
        图片路径 + 提示词
        """



        try:


            mime_type, _ = mimetypes.guess_type(
                image_path
            )



            if mime_type is None:

                mime_type = "image/jpeg"




            with open(
                image_path,
                "rb"
            ) as image_file:


                image_data = base64.b64encode(

                    image_file.read()

                ).decode(
                    "utf-8"
                )




            image_url = (

                f"data:{mime_type};base64,{image_data}"

            )




            headers = {

                "Authorization":

                f"Bearer {self.api_key}",


                "Content-Type":

                "application/json"

            }




            body = {


                "model": self.vision_model,


                "messages": [

                    {

                        "role": "user",


                        "content": [

                            {

                                "type": "text",

                                "text": prompt

                            },


                            {

                                "type": "image_url",

                                "image_url": {

                                    "url": image_url

                                }

                            }

                        ]

                    }

                ]

            }




            print("====================")

            print("正在请求视觉 AI")

            print(
                "当前视觉模型：",
                self.vision_model
            )

            print("====================")




            response = requests.post(

                self.base_url,

                headers=headers,

                json=body,

                timeout=180

            )




            print(

                "HTTP状态码：",

                response.status_code

            )




            response.raise_for_status()



            data = response.json()



            return data["choices"][0]["message"]["content"]




        except Exception as e:


            return f"视觉模型请求失败：{e}"