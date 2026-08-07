import os
import sys
import json
import uuid
from io import BytesIO


# =========================
# 项目根目录
# =========================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(PROJECT_ROOT)


from flask import (
    Flask,
    request,
    render_template_string,
    send_file
)

from werkzeug.utils import secure_filename

from agents.product_agent import ProductAgent
from agents.script_agent import ScriptAgent
from agents.video_agent import VideoAgent

from services.agnes_video import AgnesVideo


app = Flask(__name__)


# =========================
# 文件目录
# =========================

UPLOAD_FOLDER = os.path.join(
    PROJECT_ROOT,
    "uploads"
)

JOB_FOLDER = os.path.join(
    PROJECT_ROOT,
    "output",
    "jobs"
)


os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

os.makedirs(
    JOB_FOLDER,
    exist_ok=True
)


app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# =========================
# 页面
# =========================

HTML_PAGE = """

<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<title>
Kazakh AI Commerce Agent
</title>


<style>

body {

    font-family: Arial, sans-serif;

    max-width: 1000px;

    margin: 40px auto;

    padding: 20px;

}


h1 {

    text-align: center;

}


input,
textarea,
select {

    width: 100%;

    padding: 10px;

    margin-top: 8px;

    margin-bottom: 20px;

    box-sizing: border-box;

}


textarea {

    min-height: 180px;

}


.script-box {

    min-height: 380px;

}


button {

    padding: 12px 25px;

    margin-right: 10px;

    margin-top: 10px;

    cursor: pointer;

    font-size: 15px;

}


.box {

    background: #f5f5f5;

    padding: 20px;

    margin-top: 25px;

    border-radius: 8px;

}


pre {

    white-space: pre-wrap;

}


.actions {

    margin-top: 15px;

}


.status {

    font-size: 18px;

    font-weight: bold;

    margin-top: 15px;

}


video {

    width: 100%;

    max-width: 800px;

    margin-top: 20px;

    border-radius: 8px;

}

</style>

</head>


<body>


<h1>
哈萨克 AI 商品营销助手
</h1>


<h2>
第一步：录入商品并生成视频脚本
</h2>


<form
    method="post"
    action="/generate_script"
    enctype="multipart/form-data"
>


<label>
商品图片（最多5张）
</label>

<input
    type="file"
    name="images"
    multiple
>


<label>
商品名称
</label>

<input
    name="name"
    placeholder="例如：哈萨克传统手工黑肥皂"
>


<label>
品牌
</label>

<input
    name="brand"
    placeholder="没有可以填写未知"
>


<label>
商品描述
</label>

<textarea
    name="description"
    placeholder="请输入商品特点、材质、用途、制作工艺等信息"
></textarea>


<label>
脚本版本
</label>

<select name="script_mode">

    <option value="both">
        哈萨克语西里尔 + 拉丁转写
    </option>

    <option value="cyrillic">
        只生成哈萨克语西里尔版本
    </option>

    <option value="latin">
        只生成哈萨克语拉丁转写版本
    </option>

</select>


<button type="submit">
生成视频脚本
</button>


</form>



{% if product_result %}

<div class="box">

<h2>
商品分析结果
</h2>

<pre>{{ product_result }}</pre>

</div>

{% endif %}



{% if script_result %}

<div class="box">

<h2>
第二步：检查或修改视频脚本
</h2>


<form method="post">


<input
    type="hidden"
    name="job_id"
    value="{{ job_id }}"
>


<textarea
    class="script-box"
    name="script_content"
>{{ script_result }}</textarea>


<div class="actions">


<button
    type="submit"
    formaction="/generate_video"
>
生成商品视频
</button>


<button
    type="submit"
    formaction="/download_script"
>
下载脚本
</button>


</div>


</form>


</div>

{% endif %}



{% if video_task_id %}

<div class="box">

<h2>
第三步：视频生成状态
</h2>


<div class="status">

当前状态：

{{ video_status }}

</div>


{% if video_progress is not none %}

<p>
生成进度：{{ video_progress }}%
</p>

{% endif %}


<p>
任务ID：
{{ video_task_id }}
</p>


<form
    method="post"
    action="/check_video"
>


<input
    type="hidden"
    name="job_id"
    value="{{ job_id }}"
>


<input
    type="hidden"
    name="task_id"
    value="{{ video_task_id }}"
>


<input
    type="hidden"
    name="script_content"
    value="{{ script_result }}"
>


<button type="submit">
查询视频状态
</button>


</form>


</div>

{% endif %}



{% if video_url %}

<div class="box">

<h2>
视频生成完成
</h2>


<video controls>

<source
    src="{{ video_url }}"
    type="video/mp4"
>

你的浏览器暂时无法播放该视频。

</video>


<p>

<a
    href="{{ video_url }}"
    target="_blank"
>
打开视频
</a>

</p>


</div>

{% endif %}



{% if video_message %}

<div class="box">

<h2>
视频服务返回
</h2>

<pre>{{ video_message }}</pre>

</div>

{% endif %}


</body>

</html>

"""


# =========================
# 保存任务
# =========================

def save_job(
    job_id,
    image_paths,
    product_result
):


    job_path = os.path.join(
        JOB_FOLDER,
        f"{job_id}.json"
    )


    data = {

        "image_paths": image_paths,

        "product_result": product_result

    }


    with open(
        job_path,
        "w",
        encoding="utf-8"
    ) as f:


        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )


# =========================
# 读取任务
# =========================

def load_job(
    job_id
):


    job_path = os.path.join(
        JOB_FOLDER,
        f"{job_id}.json"
    )


    if not os.path.exists(
        job_path
    ):

        return None


    with open(
        job_path,
        "r",
        encoding="utf-8"
    ) as f:


        return json.load(f)


# =========================
# 首页
# =========================

@app.route(
    "/",
    methods=["GET"]
)

def index():


    return render_template_string(

        HTML_PAGE,

        product_result="",

        script_result="",

        video_task_id="",

        video_status="",

        video_progress=None,

        video_url="",

        video_message="",

        job_id=""

    )


# =========================
# 生成商品分析和脚本
# =========================

@app.route(
    "/generate_script",
    methods=["POST"]
)

def generate_script():


    name = request.form.get(
        "name",
        ""
    )


    brand = request.form.get(
        "brand",
        ""
    )


    description = request.form.get(
        "description",
        ""
    )


    script_mode = request.form.get(
        "script_mode",
        "both"
    )


    # =====================
    # 保存商品图片
    # =====================

    image_paths = []


    images = request.files.getlist(
        "images"
    )


    for image in images[:5]:


        if not image.filename:

            continue


        filename = secure_filename(
            image.filename
        )


        unique_filename = (

            f"{uuid.uuid4().hex}_"
            f"{filename}"

        )


        image_path = os.path.join(

            app.config["UPLOAD_FOLDER"],

            unique_filename

        )


        image.save(
            image_path
        )


        image_paths.append(
            image_path
        )


        print("====================")

        print("图片上传成功：")

        print(image_path)

        print("====================")


    print("====================")

    print("本次商品图片列表：")

    print(image_paths)

    print("====================")


    # =====================
    # 商品信息
    # =====================

    product_info = f"""

商品名称：

{name}


品牌：

{brand}


商品描述：

{description}

"""


    # =====================
    # Product Agent
    # =====================

    print("====================")

    print("Product Agent 开始运行")

    print("====================")


    product_agent = ProductAgent()


    product_result = product_agent.run(

        product_info,

        image_paths

    )


    # =====================
    # Script Agent
    # =====================

    print("====================")

    print("Script Agent 开始运行")

    print("====================")


    script_agent = ScriptAgent()


    script_result = script_agent.run(

        product_result,

        script_mode

    )


    # =====================
    # 创建任务
    # =====================

    job_id = uuid.uuid4().hex


    save_job(

        job_id,

        image_paths,

        product_result

    )


    print("====================")

    print("任务已保存")

    print(
        "job_id：",
        job_id
    )

    print(
        "保存图片：",
        image_paths
    )

    print("====================")


    return render_template_string(

        HTML_PAGE,

        product_result=product_result,

        script_result=script_result,

        video_task_id="",

        video_status="",

        video_progress=None,

        video_url="",

        video_message="",

        job_id=job_id

    )


# =========================
# 生成视频
# =========================

@app.route(
    "/generate_video",
    methods=["POST"]
)

def generate_video():


    job_id = request.form.get(
        "job_id",
        ""
    )


    script_content = request.form.get(
        "script_content",
        ""
    )


    print("====================")

    print("Video阶段读取任务")

    print(
        "job_id：",
        job_id
    )

    print("====================")


    job_data = load_job(
        job_id
    )


    if not job_data:


        return render_template_string(

            HTML_PAGE,

            product_result="",

            script_result=script_content,

            video_task_id="",

            video_status="",

            video_progress=None,

            video_url="",

            video_message=(
                "视频生成失败："
                "没有找到对应的商品任务。"
            ),

            job_id=job_id

        )


    image_paths = job_data.get(
        "image_paths",
        []
    )


    product_result = job_data.get(
        "product_result",
        ""
    )


    print("====================")

    print("Video阶段读取图片：")

    print(image_paths)

    print("====================")


    # =====================
    # Video Agent
    # =====================

    print("====================")

    print("Video Agent 开始运行")

    print("====================")


    video_agent = VideoAgent()


    video_result = video_agent.run(

        image_paths,

        script_content

    )


    print("====================")

    print("Video Agent 返回：")

    print(video_result)

    print("====================")


    # =====================
    # 读取 task_id
    # =====================

    video_task_id = ""

    video_status = ""

    video_progress = 0

    video_message = ""


    if isinstance(
        video_result,
        dict
    ):


        video_task_id = (

            video_result.get(
                "task_id"
            )

            or

            video_result.get(
                "video_id"
            )

            or

            video_result.get(
                "id"
            )

            or

            ""

        )


        video_status = video_result.get(
            "status",
            ""
        )


        video_progress = video_result.get(
            "progress",
            0
        )


        if not video_task_id:

            video_message = str(
                video_result
            )


    else:

        video_message = str(
            video_result
        )


    return render_template_string(

        HTML_PAGE,

        product_result=product_result,

        script_result=script_content,

        video_task_id=video_task_id,

        video_status=video_status,

        video_progress=video_progress,

        video_url="",

        video_message=video_message,

        job_id=job_id

    )


# =========================
# 查询视频状态
# =========================

@app.route(
    "/check_video",
    methods=["POST"]
)

def check_video():


    job_id = request.form.get(
        "job_id",
        ""
    )


    task_id = request.form.get(
        "task_id",
        ""
    )


    script_content = request.form.get(
        "script_content",
        ""
    )


    job_data = load_job(
        job_id
    )


    if job_data:


        product_result = job_data.get(
            "product_result",
            ""
        )


    else:

        product_result = ""


    print("====================")

    print("开始查询视频状态")

    print(
        "task_id：",
        task_id
    )

    print("====================")


    agnes_video = AgnesVideo()


    status_result = agnes_video.get_video_status(
        task_id
    )


    print("====================")

    print("视频状态查询结果：")

    print(status_result)

    print("====================")


    video_status = ""

    video_progress = 0

    video_url = ""

    video_message = ""


    if isinstance(
        status_result,
        dict
    ):


        video_status = status_result.get(
            "status",
            ""
        )


        video_progress = status_result.get(
            "progress",
            0
        )


        video_url = status_result.get(
            "video_url",
            ""
        )


        if status_result.get(
            "error"
        ):

            video_message = str(
                status_result
            )


    else:


        video_message = str(
            status_result
        )


    return render_template_string(

        HTML_PAGE,

        product_result=product_result,

        script_result=script_content,

        video_task_id=task_id,

        video_status=video_status,

        video_progress=video_progress,

        video_url=video_url,

        video_message=video_message,

        job_id=job_id

    )


# =========================
# 下载脚本
# =========================

@app.route(
    "/download_script",
    methods=["POST"]
)

def download_script():


    script_content = request.form.get(
        "script_content",
        ""
    )


    script_bytes = BytesIO(

        script_content.encode(
            "utf-8"
        )

    )


    script_bytes.seek(0)


    return send_file(

        script_bytes,

        as_attachment=True,

        download_name="video_script.txt",

        mimetype="text/plain; charset=utf-8"

    )


# =========================
# 启动
# =========================

if __name__ == "__main__":


    print("====================")

    print(
        "Kazakh AI Commerce Agent 启动"
    )

    print(
        "访问地址：http://127.0.0.1:8000"
    )

    print("====================")


    app.run(

        host="0.0.0.0",

        port=8000,

        debug=True

    )