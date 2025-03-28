import websocket
import uuid
import json
import urllib.request
import urllib.parse

server_address = "127.0.0.1:8188"
client_id = str(uuid.uuid4())

with open("sdxl_lora.json", "r") as file:
    prompt = json.load(file)

def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request("http://{}/prompt".format(server_address), data=data)
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

def update_workflow(prompt, positive_text, negative_text, seed, lora_strength):
    prompt["11"]["inputs"]["text"] = "AquaXL, blue eyes, blue hair, long hair, anime girl, masterpiece, best quality"
    prompt["12"]["inputs"]["text"] = "low quality, worst quality, bad anatomy, deformed"
    prompt["13"]["inputs"]["seed"] = 7777777
    prompt["10"]["inputs"]["lora_1"]["strength"] = 0.5
    return prompt

updated_prompt = update_workflow(prompt, 
                                 positive_text="AquaXL, futuristic cyberpunk city, neon lights", 
                                 negative_text="low quality, bad composition", 
                                 seed=123456, 
                                 lora_strength=0.7)

ws = websocket.WebSocket()
ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
images = get_images(ws, updated_prompt)
ws.close()

for node_id in images:
    for image_data in images[node_id]:
        from PIL import Image
        import io
        image = Image.open(io.BytesIO(image_data))
        image.show()
