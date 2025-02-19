import json
import urllib.parse
import urllib.request
import cv2
import torch
import numpy as np
import requests
import os

def send_post_request(api_url, payload, headers):
    """
    Sends a POST request to the specified API URL with the given payload and headers.

    Args:
        api_url (str): The URL of the API endpoint.
        payload (dict): The payload to send in the POST request.
        headers (dict): The headers to include in the POST request.

    Raises:
        Exception: If there is an error connecting to the server or the request fails.
    """
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(api_url, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req) as response:
            response_data = response.read().decode("utf-8")
        return response_data
    except urllib.error.URLError as e:
        if "Unauthorized" in str(e):
            raise Exception(
                "Key is invalid, please refer to https://cloud.siliconflow.cn to get the API key.\n"
                "If you have the key, please click the 'BizyAir Key' button at the bottom right to set the key."
            )
        else:
            raise Exception(
                f"Failed to connect to the server: {e}, if you have no key, "
            )
            
def read_video_frames_url(video_path, num_frames, frame_size=(224, 224)):
        """
        read video file with tensor return

        :param video_path: 视频文件路径
        :param num_frames: 需要读取的帧数
        :param frame_size: 帧的大小 (宽度, 高度)
        :return: 一个包含视频帧的Tensor (num_frames, width, height, channel)
        """
        # 创建临时文件
        temp_dir = './temp'
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        temp_file_path = os.path.join(temp_dir, 'temp_video.mp4')
        try:
            # 下载视频文件
            response = requests.get(video_path)
            response.raise_for_status()  # 检查请求是否成功
            
            # 将视频内容写入临时文件
            with open(temp_file_path, 'wb') as temp_file:
                temp_file.write(response.content)
            
        except requests.RequestException as e:
            raise ValueError(f"无法下载视频文件: {e}")

        cap = cv2.VideoCapture(temp_file_path)
        frames = []

        if not cap.isOpened():
            raise ValueError(f"cannot open video file: {video_path}")

        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        # if num_frames > frame_count:
        #     raise ValueError(f"request frames {num_frames} exceed total frames {frame_count}")
        num_frames = min(frame_count, num_frames)
        # frame index
        frame_indices = np.linspace(0, frame_count - 1, num_frames, dtype=int)

        for index in frame_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, index)
            ret, frame = cap.read()
            if not ret:
                raise ValueError(f"cannot read {index} frame")
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, frame_size)
            # Tensor (H, W, C) -> (W, H, C)
            frame = torch.from_numpy(frame).float() / 255.0
            frames.append(frame)

        cap.release()

        #(num_frames, width, height, channel)
        frames_tensor = torch.stack(frames)
        os.remove(temp_file_path)
        return frames_tensor


def read_video_frames_local(video_path, num_frames, frame_size=(224, 224)):
        """
        read video file with tensor return

        :param video_path: 视频文件路径
        :param num_frames: 需要读取的帧数
        :param frame_size: 帧的大小 (宽度, 高度)
        :return: 一个包含视频帧的Tensor (num_frames, width, height, channel)
        """

        cap = cv2.VideoCapture(video_path)
        frames = []

        if not cap.isOpened():
            raise ValueError(f"cannot open video file: {video_path}")

        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        # if num_frames > frame_count:
        #     raise ValueError(f"request frames {num_frames} exceed total frames {frame_count}")
        num_frames = min(frame_count, num_frames)
        # frame index
        frame_indices = np.linspace(0, frame_count - 1, num_frames, dtype=int)

        for index in frame_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, index)
            ret, frame = cap.read()
            if not ret:
                raise ValueError(f"cannot read {index} frame")
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, frame_size)
            # Tensor (H, W, C) -> (W, H, C)
            frame = torch.from_numpy(frame).float() / 255.0
            frames.append(frame)

        cap.release()

        #(num_frames, width, height, channel)
        frames_tensor = torch.stack(frames)

        return frames_tensor


def get_video_url_from_json(json_url):
    """
    从JSON内容中提取视频文件的URL

    :param json_url: 包含视频文件URL的JSON内容的网络地址
    :return: 视频文件的URL
    """
    try:
        response = requests.get(json_url)
        response.raise_for_status()  # 检查请求是否成功
        json_data = response.json()
        video_url = json_data['payload'][0][0]
        return video_url
    except requests.RequestException as e:
        raise ValueError(f"无法下载JSON内容: {e}")
    except (KeyError, IndexError) as e:
        raise ValueError(f"JSON内容格式错误: {e}")