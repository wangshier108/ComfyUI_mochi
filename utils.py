import json
import urllib.parse
import urllib.request
import cv2
import torch
import numpy as np

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
            
def read_video_frames(video_path, num_frames, frame_size=(224, 224)):
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
