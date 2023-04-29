import base64
import os
import sys
import json
import requests

engine_id = "stable-diffusion-512-v2-0"
api_host = os.getenv('API_HOST', 'https://api.stability.ai')
api_key = os.getenv("STABILITY_API_KEY")

if api_key is None:
    raise Exception("Missing Stability API key.")

# append args to json
texts = [{'text':arg} for arg in sys.argv[1:]]
print(texts)
json = {"text_prompts":texts,
        "cfg_scale": 7,
        "clip_guidance_preset": "FAST_BLUE",
        "height": 512,
        "width": 512,
        "samples": 1,
        "steps": 30,
    }

response = requests.post(
    f"{api_host}/v1/generation/{engine_id}/text-to-image",
    headers={
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    },
    json=json,
)
print(f"status:{response.status_code}")
if response.status_code != 200:
    raise Exception("Non-200 response: " + str(response.text))

data = response.json()
for i, image in enumerate(data["artifacts"]):
    with open(f"./out/v1_txt2img_{i}.png", "wb") as f:
        f.write(base64.b64decode(image["base64"]))
