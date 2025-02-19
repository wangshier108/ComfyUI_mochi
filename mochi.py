import json
import os
from .utils import (
    send_post_request,
    read_video_frames
)

class mochi:
    API_URL = "http://0.0.0.0:10002/mochivideo"
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "Close-up of a chameleon's eye, with its scaly skin changing color. Ultra high resolution 4k."}),
                "steps": ("INT", {"default": 20, "min": 1, "max": 50}),
                "width": ("INT", {"default": 848, "min": 64, "max": 1536, "step": 8}),
                "height": ("INT", {"default": 480, "min": 64, "max": 1536, "step": 8}),
                "frames": ("INT", {"default": 96, "min": 1, "max": 4096}),
                "fps": ("INT", {"default": 22, "min": 8, "max": 64}),
                "filename": ("STRING", {"default": "mochi"}),               
            }
        }

    CATEGORY = "☁️BizyAir/Trellis"
    FUNCTION = "main"

    RETURN_TYPES = ("IMAGE",)
    # RETURN_NAMES = ("path",)
    OUTPUT_NODE = True
    OUTPUT_IS_LIST = (False,)

    def main(self, prompt, steps, width, height, frames, fps, filename):

        payload = {
            "prompt": prompt,
            "steps":steps,
            "width": width,
            "height": height,
            "frames": frames,
            "fps": fps,
            "outvideo": filename
        }

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
        }

        response: str = send_post_request(
            self.API_URL, payload=payload, headers=headers
        )
        msg = json.loads(response)

        if msg["type"] != "success":  
            raise Exception(f"Unexpected response type: {msg}")
        
        frames_tensor = read_video_frames(msg["outvideo"], frames, (width, height))
        os.remove(msg["outvideo"])
        return (frames_tensor, )
    
NODE_CLASS_MAPPINGS = {
    "mochi": mochi,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "mochi": "mochi"
}