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
# 4. 运行项目
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
# 5. 联系
这个项目已经开源，有一定编程能力的人可以自行修改源码，如果不会如何部署的朋友，可以让作者有偿给你部署，[可点击这里](https://lukeewin.taobao.com)。
如果觉得这个项目不错，记得在右上角点击"Star"。
微信公众号：<img src=./img/img.png width="30%"/>
# 6. 其它项目
1. 基于 Celery + Redis 开发的分布式私有化语音识别接口，可联系作者 lukeewin01 进行项目演示。该项目支持多机多卡部署，适合中大型公司使用，可分布式部署在多台服务器中，使用多张显卡。目前该项目不开源。[点击这里查看文章](https://blog.lukeewin.top/archives/celeryredisasrspk)。
2. 基于 Java 开发的一句话实时语音识别接口，在阿里云高性能计算性服务器中转写 10 秒一句话音频耗时 100 毫秒左右。该项目不需要 GPU，运行在纯 CPU 环境中，使用 onnxruntime 推理模型。（非开源项目）
3. 基于 Java 开发的长音频转写接口，在阿里云高性能计算性服务器中转写 1 分钟音频耗时 1.1 秒。该项目也不需要显卡，运行在纯 CPU 环境中，使用 onnxruntime 推理模型。（非开源项目）
