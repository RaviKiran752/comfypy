from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import websocket
import uuid
import json
import urllib.request
import urllib.parse
from PIL import Image
import io
import base64

app = FastAPI()

server_address = "127.0.0.1:8188"
client_id = str(uuid.uuid4())

with open("sdxl_lora.json", "r") as file:
    base_prompt = json.load(file)

class ImageRequest(BaseModel):
    positive_prompt: str
    negative_prompt: str
    seed: int
    lora_strength: float

def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request(f"http://{server_address}/prompt", data=data)
    return json.loads(urllib.request.urlopen(req).read())

def get_images(ws, prompt):
    prompt_id = queue_prompt(prompt)['prompt_id']
    output_images = {}
    current_node = ""
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['prompt_id'] == prompt_id:
                    if data['node'] is None:
                        break  
                    else:
                        current_node = data['node']
        else:
            if current_node == '19': 
                images_output = output_images.get(current_node, [])
                images_output.append(out[8:])
                output_images[current_node] = images_output
    return output_images

@app.post("/generate")
def generate_image(request: ImageRequest):
    updated_prompt = base_prompt.copy()
    updated_prompt["11"]["inputs"]["text"] = request.positive_prompt
    updated_prompt["12"]["inputs"]["text"] = request.negative_prompt
    updated_prompt["13"]["inputs"]["seed"] = request.seed
    updated_prompt["10"]["inputs"]["lora_1"]["strength"] = request.lora_strength

    ws = websocket.WebSocket()
    ws.connect(f"ws://{server_address}/ws?clientId={client_id}")
    images = get_images(ws, updated_prompt)
    ws.close()

    image_data = []
    for node_id in images:
        for img_bytes in images[node_id]:
            img = Image.open(io.BytesIO(img_bytes))
            img_buffer = io.BytesIO()
            img.save(img_buffer, format="PNG")
            base64_img = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
            image_data.append(base64_img)
    
    return {"images": image_data}
