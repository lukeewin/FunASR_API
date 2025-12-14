# !/usr/bin/env python
# _*_ coding utf-8 _*_
# @Time: 2025/12/15 1:01
# @Author: Luke Ewin
# @Blog: https://blog.lukeewin.top
import subprocess
import threading
import uuid
from datetime import timedelta, datetime
from queue import Queue
import requests
import torch.cuda
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from urllib.parse import urlparse
import tempfile
import os
import uvicorn
from funasr import AutoModel
from db import SQLHelper

app = FastAPI()

_model = None

task_queue = Queue()

load_dotenv()

db_manager = SQLHelper()

home_directory = os.path.expanduser("~")
asr_model = os.path.join(home_directory, ".cache", "modelscope", "hub", "iic", "speech_seaco_paraformer_large_asr_nat-zh-cn-16k-common-vocab8404-pytorch")
vad_model = os.path.join(home_directory, ".cache", "modelscope", "hub", "iic", "speech_fsmn_vad_zh-cn-16k-common-pytorch")
punc_model = os.path.join(home_directory, ".cache", "modelscope", "hub", "iic", "punc_ct-transformer_zh-cn-common-vocab272727-pytorch")
spk_model = os.path.join(home_directory, ".cache", "modelscope", "hub", "iic", "speech_campplus_sv_zh-cn_16k-common")

def get_model():
    global _model
    if _model is None:
        try:
            print("加载模型中...")
            _model = AutoModel(
                model=asr_model,
                vad_model=vad_model,
                punc_model=punc_model,
                spk_model=spk_model,
                disable_update=True,
                disable_pbar=True,
                disable_log=True,
                ngpu=1 if torch.cuda.is_available() else 0,
                ncpu=os.cpu_count(),
            )
            print("模型加载成功")
        except Exception as e:
            print("模型加载失败")
            raise
    return _model

@app.on_event("startup")
async def startup_event():
    """应用启动时预加载模型"""
    get_model()
    t = threading.Thread(target=task, daemon=True)
    t.start()


def to_date(milliseconds):
    """将时间戳转换为SRT格式的时间"""
    time_obj = timedelta(milliseconds=milliseconds)
    return f"{time_obj.seconds // 3600:02d}:{(time_obj.seconds // 60) % 60:02d}:{time_obj.seconds % 60:02d}.{time_obj.microseconds // 1000:03d}"


def response_format(code: int, status: str, message: str, data: dict = None):
    return {
        "code": code,
        "status": status,
        "message": message,
        "data": data or {}
    }


@app.post("/trans/file")
async def trans(file: UploadFile = File(..., description="音频文件")):
    try:
        temp_file = None
        try:
            contents = await file.read()
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
                tmp.write(contents)
                temp_file = tmp.name
        
            model = get_model()

            result = model.generate(
                input=temp_file,
                batch_size_s=300
            )
            sentence_info = result[0]["sentence_info"]
            sentence_list = []
            for sentence in sentence_info:
                start = to_date(sentence['start'])
                end = to_date(sentence['end'])
                text = sentence['text']
                spk = sentence['spk']
                sentence_list.append({"text": text, "start": start, "endTime": end, "speaker": spk})

            return response_format(code=200, status="ok", message="success", data=sentence_list)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"识别失败: {str(e)}") 
        finally:
            if temp_file and os.path.exists(temp_file):
                os.unlink(temp_file)
    except Exception as e:
        return response_format(code=300, status="error", message="转写异常", data={})

@app.post("/trans/audio_url")
async def trans_audio_url(audio_url: str = Form(..., description="音频URL")):
    task_id = str(uuid.uuid4()).replace("-", "")
    try:
        task_queue.put({"task_id": task_id, "audio": audio_url})
        return response_format(code=200, status="success", message="上传成功", data={"task_id": task_id})
    except requests.exceptions.RequestException as e:
        print(f"下载音频失败：{e}")
        return response_format(code=300, status="error", message="下载音频报错", data={"task_id": task_id})
    except Exception as e:
        print(f"转写异常：{e}")
        return response_format(code=301, status="error", message="转写异常", data={"task_id": task_id})

@app.post("/result")
async def result(task_id: str = Form(..., description="任务ID")):
    try:
        sql = "SELECT sentence_index, text, start, end, spk FROM asr_result WHERE task_id = %s ORDER BY sentence_index"
        results = db_manager.get_list(sql, (task_id,))
        if results:
            delete_sql = "DELETE FROM asr_result WHERE task_id = %s"
            db_manager.modify(delete_sql, (task_id,))
            return response_format(code=200, status="success", message="获取结果成功", data={"sentences": results})
        else:
            return response_format(code=303, status="error", message="获取结果为空")
    except Exception as e:
        print(f"{task_id} - 获取结果报错: {e}")
        return response_format(code=302, status="error", message="获取结果报错")


def convert_audio_to_wav(input_path, output_path):
    """
    将音频转换为16k采样率、单声道、pcm_s16le格式的wav文件
    """
    try:
        cmd = [
            'ffmpeg',
            '-i', input_path,
            '-ac', '1',
            '-ar', '16000',
            '-acodec', 'pcm_s16le',
            '-y',
            output_path
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300
        )

        if result.returncode != 0:
            raise Exception(f"音频转码失败: {result.stderr}")

        print(f"音频转码完成: {input_path} -> {output_path}")
        return True
    except subprocess.TimeoutExpired:
        raise Exception("音频转码超时")
    except Exception as e:
        raise Exception(f"音频转码失败: {str(e)}")

def task():
    model = get_model()
    while True:
        task = task_queue.get()
        task_id = task["task_id"]
        audio = task["audio"]

        print(f"{task_id} - 正在下载")
        response = requests.get(audio, stream=True, timeout=30)
        response.raise_for_status()
        save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "upload")
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        parsed_url = urlparse(audio)
        filename = os.path.basename(parsed_url.path)
        file_extension = os.path.splitext(filename)[1].lower()
        temp_audio_path = os.path.join(save_path, "_" + task_id + file_extension)
        with open(temp_audio_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    f.flush()
        print(f"{task_id} - 已下载")
        print(f"{task_id} - 转码中")
        wav_audio_path = os.path.join(save_path, task_id + ".wav")
        try:
            convert_audio_to_wav(temp_audio_path, wav_audio_path)
            if os.path.exists(temp_audio_path):
                os.unlink(temp_audio_path)
            print(f"{task_id} - 转码完成")
        except Exception as e:
            print(f"{task_id} - 转码失败: {e}")
            wav_audio_path = temp_audio_path
        print(f"{task_id} - 转写中")
        trans_result = model.generate(input=wav_audio_path, batch_size_s=300)
        print(f"{task_id} - 转写完成")
        os.unlink(wav_audio_path)
        createtime = datetime.now()
        if trans_result:
            sentence_info = trans_result[0]["sentence_info"]
            i = 1
            for sentence in sentence_info:
                start = to_date(sentence['start'])
                end = to_date(sentence['end'])
                text = sentence['text']
                spk = sentence['spk']
                sql = "insert into asr_result (id, task_id, sentence_index, text, start, end, spk, createtime) values (%s, %s, %s, %s, %s, %s, %s, %s)"
                id = task_id + str(i)
                db_manager.create(sql, (id, task_id, i, text, start, end, spk, createtime))
                i += 1
            print(f"{task_id} - 数据已保存到数据库")
        else:
            print(f"{task_id} - 没有转写结果")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9090)
