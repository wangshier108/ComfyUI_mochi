import json
import urllib
from .utils import (
    send_post_request,
)

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

class mochi:
    API_URL = "http://0.0.0.0:10002/mochivideo"
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "Close-up of a chameleon's eye, with its scaly skin changing color. Ultra high resolution 4k."}),
                "steps": ("INT", {"default": 20, "min": 1, "max": 50}),
                "width": ("INT", {"default": 64, "min": 64, "max": 1560, "step": 8}),
                "height": ("INT", {"default": 64, "min": 64, "max": 1560, "step": 8}),
                "frames": ("INT", {"default": 96, "min": 1, "max": 4096}),
                "fps": ("INT", {"default": 22, "min": 8, "max": 64}),
                              
            }
        }

    CATEGORY = "☁️BizyAir/Trellis"
    FUNCTION = "main"

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("path",)
    OUTPUT_NODE = True
    OUTPUT_IS_LIST = (False,)

    def main(self, prompt, steps, width, height, frames, fps):

        payload = {
            "prompt": prompt,
            "steps":steps,
            "width": width,
            "height": height,
            "frames": frames,
            "fps": fps,
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

        return (msg["outvideo"],)

NODE_CLASS_MAPPINGS = {
    "mochi": mochi,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "mochi": "mochi"
}