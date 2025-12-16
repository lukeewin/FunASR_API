# 0. 效果演示
转写请求接口: 
<img src=./img/trans.png width="80%"/> \
获取结果接口：
<img src=./img/result.png width="80%"/> \
视频讲解:
<iframe src="//player.bilibili.com/player.html?isOutside=true&aid=115719857510386&bvid=BV1dum6BsESc&cid=34742600655&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>
# 1. 项目背景说明
这个项目基于阿里开源的 FunASR 进行开发，使用 fastapi 开发成 API 接口，数据存储到 MySQL 中。
该项目可以运行于 Linux，MacOS 和 Windows 系统中，在对应系统中安装 Python 环境即可运行。
该项目是一个 API 接口，没有界面，适用于其它项目通过 HTTP 进行调用。可支持任意语言发送 HTTP 请求进行调用，比如支持：Java, C++，C，PHP，Go，JavaScript 等均可调用本接口。

# 2. 项目环境安装
这里以 Windows 为例，当然 Linux 和 MacOS 也是支持的，这里写文档以在 Windows 安装使用为例子，其它系统类似。
## 2.1. 安装显卡驱动
首先选择安装“显卡驱动”如果你想要使用"CUDA"来加速推理，当然前提是你要有英伟达显卡。
大部分电脑已经自动给你安装好了的，这个一般不需要你操作安装。可使用下面命令查看你电脑或者服务器中目前的显卡驱动版本。
```shell
nvidia-smi
```
## 2.2. 安装CUDA
这个也是你使用英伟达显卡才需要安装，如果你使用的 Mac 的芯片，无需安装，可跳过这步骤。
可访问下面地址选择你对应的版本和系统。注意：安装的 CUDA 版本一定要是 nvidia-smi 中支持的版本。
```markdown
https://developer.nvidia.com/cuda-downloads
```
安装完成之后可以使用 nvcc -V 查看是否可以输出版本信息，如果是 Linux 和 MacOS 还需要配置系统环境变量。具体如何配置可以查看我之前发布的文章，访问下面地址。
```markdown
https://blog.lukeewin.top/archives/linux-cuda-cudnn
```
## 2.3. 安装FFMPEG
这个 ffmpeg 在本项目中用于音频的统一编码用，必须安装。
可访问下面网址下载 ffmpeg，解压然后配置系统环境变量。
```markdown
https://ffmpeg.org/download.html
```
如何配置系统环境变量，网上有很多教程，这里不展开。
安装并配置好环境变量之后，可以验证一下是否可正常使用，使用下面命令，如果有版本信息输出，说明配置正确。
```shell
ffmpeg -version
```
## 2.4. 安装Miniconda
可访问下面网址，下载安装 Miniconda
```markdown
https://www.anaconda.com/download
```
为了方便大家的下载，这里直接给出不同系统的下载地址。
下面是 Windows X86_64 系统对应的 Miniconda 安装包。
```markdown
https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe
```
下面是 MacOS 苹果芯片的对应安装包。(图形界面)
```markdown
https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.pkg
```
下面是 MacOS 苹果芯片对应的安装包。（命令行）
```markdown
https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh
```
下面是 MacOS 英特尔芯片对应的安装包。（图形界面）
```markdown
https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.pkg
```
下面是 MacOS 英特尔芯片对应的安装包。（命令行）
```markdown
https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
```
Linux 的对应安装包。（这里只给 X86_64 的安装包，如果需要其它的安装包，需要自己到官方网站中获取下载链接）
```markdown
https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```
# 3. 创建虚拟环境并安装Python依赖
创建虚拟环境，使用下面命令：
```shell
conda create -n funasr python=3.11
```
进入环境
```shell
conda activate funasr
```
安装依赖
```shell
pip install -U funasr modelscope python-dotenv fastapi uvicorn PyMySQL DBUtils
```
# 4. 运行和使用
## 4.1 运行
运行之前需要在项目目录中创建 .env 文件，写入下面配置信息。
```markdown
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=123456
DB_NAME=funasr_api
```
这里使用的是 MySQL 数据库，你需要在 MySQL 中创建一个名为 funasr_api 的数据库，然后执行 funasr_api.sql 文件。
```shell
python app.py
```
默认使用的是 9090 端口。
## 4.2 使用
转写接口 /asr
```markdown
发送POST请求，form-data形式，传入参数file，类型File
```
/asr 接口响应如下：
```json
{
    "text": "现在我来录制十秒钟的音频来测试一下一句话识别，看看识别的速度怎么样。",
    "segments": [
        {
            "text": "现在我来录制十秒钟的音频来测试一下一句话识别，",
            "start": "00:00:00.780",
            "end": "00:00:07.400",
            "speaker": 0
        },
        {
            "text": "看看识别的速度怎么样。",
            "start": "00:00:07.620",
            "end": "00:00:10.015",
            "speaker": 0
        }
    ],
    "language": "zh"
}
```
转写接口 /trans/file
```markdown
发送POST请求，form-data形式，传入参数file，类型File
```
/trans/file 接口响应如下：
```json
{
    "code": 200,
    "status": "ok",
    "message": "success",
    "data": {
        "sentences": [
            {
                "text": "现在我来录制十秒钟的音频来测试一下一句话识别，",
                "start": "00:00:00.780",
                "endTime": "00:00:07.400",
                "speaker": 0
            },
            {
                "text": "看看识别的速度怎么样。",
                "start": "00:00:07.620",
                "endTime": "00:00:10.015",
                "speaker": 0
            }
        ]
    }
}
```
转写接口 /trans/audio_url
```markdown
发送POST请求，form-data形式，传入参数audio_url，类型String
```
/trans/audio_url 响应如下：
```json
{
    "code": 200,
    "status": "success",
    "message": "上传成功",
    "data": {
        "task_id": "75681bf99f144616979e062fb3480067"
    }
}
```
获取转写结果接口 /result
```markdown
发送POST请求，form-data形式，字段task_id，类型String
```
响应如下：
```json
{
    "code": 200,
    "status": "success",
    "message": "获取结果成功",
    "data": {
        "sentences": [
            {
                "sentence_index": 1,
                "text": "嗯，",
                "start": "00:00:00.370",
                "end": "00:00:00.610",
                "spk": 0
            },
            {
                "sentence_index": 2,
                "text": "那么今天我们就简单的进行一下那个新生招聘的嗯讨论吧。",
                "start": "00:00:00.630",
                "end": "00:00:06.890",
                "spk": 0
            },
            {
                "sentence_index": 3,
                "text": "因为现在不是好像就新生到校嘛，",
                "start": "00:00:06.910",
                "end": "00:00:10.050",
                "spk": 0
            },
            {
                "sentence_index": 4,
                "text": "然后我们社团呢也需要招聘一些新的社员，",
                "start": "00:00:10.350",
                "end": "00:00:13.450",
                "spk": 0
            },
            {
                "sentence_index": 5,
                "text": "然后就今天就大概就讨论一下嗯怎么招聘的内容吧。",
                "start": "00:00:13.950",
                "end": "00:00:18.890",
                "spk": 0
            },
            {
                "sentence_index": 6,
                "text": "嗯，",
                "start": "00:00:19.250",
                "end": "00:00:19.490",
                "spk": 0
            },
            {
                "sentence_index": 7,
                "text": "我们就首先想一下那个招聘的地点在哪里吧？",
                "start": "00:00:19.570",
                "end": "00:00:23.505",
                "spk": 0
            },
            {
                "sentence_index": 8,
                "text": "嗯，",
                "start": "00:00:24.370",
                "end": "00:00:24.590",
                "spk": 1
            },
            {
                "sentence_index": 9,
                "text": "地点的话，",
                "start": "00:00:24.590",
                "end": "00:00:25.230",
                "spk": 1
            },
            {
                "sentence_index": 10,
                "text": "我们现在可以有三个选择。",
                "start": "00:00:25.230",
                "end": "00:00:27.190",
                "spk": 1
            },
            {
                "sentence_index": 11,
                "text": "嗯，",
                "start": "00:00:27.610",
                "end": "00:00:27.850",
                "spk": 1
            },
            {
                "sentence_index": 12,
                "text": "第一个的话，",
                "start": "00:00:27.910",
                "end": "00:00:28.550",
                "spk": 1
            },
            {
                "sentence_index": 13,
                "text": "我们可以选择在操场，",
                "start": "00:00:28.550",
                "end": "00:00:30.810",
                "spk": 1
            },
            {
                "sentence_index": 14,
                "text": "因为那儿嗯学生流动量也挺大的，",
                "start": "00:00:30.970",
                "end": "00:00:34.720",
                "spk": 1
            },
            {
                "sentence_index": 15,
                "text": "操场的话，",
                "start": "00:00:34.920",
                "end": "00:00:35.800",
                "spk": 0
            },
            {
                "sentence_index": 16,
                "text": "这这段时间太热了，",
                "start": "00:00:36.340",
                "end": "00:00:38.220",
                "spk": 0
            },
            {
                "sentence_index": 17,
                "text": "我怕那个人流量有点少。",
                "start": "00:00:38.220",
                "end": "00:00:40.579",
                "spk": 0
            },
            {
                "sentence_index": 18,
                "text": "嗯，",
                "start": "00:00:41.060",
                "end": "00:00:41.300",
                "spk": 1
            },
            {
                "sentence_index": 19,
                "text": "那我们还可以有第二个选择呀，",
                "start": "00:00:41.380",
                "end": "00:00:43.280",
                "spk": 1
            },
            {
                "sentence_index": 20,
                "text": "嗯我们可以在图书馆楼下那里有一块可以遮阴的地方哦，",
                "start": "00:00:43.640",
                "end": "00:00:49.080",
                "spk": 1
            },
            {
                "sentence_index": 21,
                "text": "图书馆我觉得应该还可以吧。",
                "start": "00:00:49.220",
                "end": "00:00:51.485",
                "spk": 0
            }
        ]
    }
}
```
# 5. 联系
这个项目已经开源，有一定编程能力的人可以自行修改源码，如果不会如何部署的朋友，可以让作者有偿给你部署，[可点击这里](https://lukeewin.taobao.com)。
如果觉得这个项目不错，记得在右上角点击"Star"。
微信公众号：<img src=./img/img.png width="30%"/>
# 6. 其它项目
1. 基于 Celery + Redis 开发的分布式私有化语音识别接口，可联系作者 lukeewin01 进行项目演示。该项目支持多机多卡部署，适合中大型公司使用，可分布式部署在多台服务器中，使用多张显卡。目前该项目不开源。[点击这里查看文章](https://blog.lukeewin.top/archives/celeryredisasrspk)。
2. 基于 Java 开发的一句话实时语音识别接口，在阿里云高性能计算性服务器中转写 10 秒一句话音频耗时 100 毫秒左右。该项目不需要 GPU，运行在纯 CPU 环境中，使用 onnxruntime 推理模型。（非开源项目）
3. 基于 Java 开发的长音频转写接口，在阿里云高性能计算性服务器中转写 1 分钟音频耗时 1.1 秒。该项目也不需要显卡，运行在纯 CPU 环境中，使用 onnxruntime 推理模型。（非开源项目）
# 7. 模型下载
```shell
modelscope download --model iic/speech_seaco_paraformer_large_asr_nat-zh-cn-16k-common-vocab8404-pytorch
modelscope download --model iic/speech_fsmn_vad_zh-cn-16k-common-pytorch
modelscope download --model iic/punc_ct-transformer_zh-cn-common-vocab272727-pytorch
modelscope download --model iic/speech_campplus_sv_zh-cn_16k-common
```
