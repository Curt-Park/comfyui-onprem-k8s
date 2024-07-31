#!/usr/bin/python3
# https://github.com/aws-samples/comfyui-on-eks/blob/main/test/comfyui_api_utils.py
# https://github.com/aws-samples/comfyui-on-eks/blob/main/test/invoke_comfyui_api.py

import requests
import json
import urllib
import random
import sys
import time


# Send prompt request to server and get prompt_id and AWSALB cookie
def queue_prompt(prompt, client_id, server_address):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode("utf-8")
    response = requests.post("{}/prompt".format(server_address), data=data)
    if "Set-Cookie" not in response.headers:
        print("No ALB, test directly to EC2.")
        aws_alb_cookie = None
    else:
        aws_alb_cookie = response.headers["Set-Cookie"].split(";")[0]
    prompt_id = response.json()["prompt_id"]
    return prompt_id, aws_alb_cookie


# Check if input image is ready
def check_input_image_ready(filename, server_address):
    data = {"filename": filename, "subfolder": "", "type": "input"}
    url_values = urllib.parse.urlencode(data)
    response = requests.get("{}/view?{}".format(server_address, url_values))
    if response.status_code == 200:
        print("Input image {} is ready, skip upload.".format(filename))
        return True
    print(
        "Input image {} not exists, uploading from current directory.".format(filename)
    )
    return False


# Upload image to server, POST to /upload/image/
def upload_image(image_path, server_address):
    with open(image_path, "rb") as f:
        files = {"image": f}
        response = requests.post("{}/upload/image".format(server_address), files=files)
    print(response.text)


# Get image from server
def get_image(filename, subfolder, folder_type, server_address, aws_alb_cookie):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    response = requests.get(
        "{}/view?{}".format(server_address, url_values),
        headers={"Cookie": aws_alb_cookie},
    )
    return response.content


# Get invocation history from server
def get_history(prompt_id, server_address, aws_alb_cookie):
    response = requests.get(
        "{}/history/{}".format(server_address, prompt_id),
        headers={"Cookie": aws_alb_cookie},
    )
    return response.json()


# Check if the image is ready, if not, upload it
def review_prompt(prompt, server_address):
    for node in prompt:
        if (
            "inputs" in prompt[node]
            and "image" in prompt[node]["inputs"]
            and isinstance(prompt[node]["inputs"]["image"], str)
        ):
            filename = prompt[node]["inputs"]["image"]
            if not check_input_image_ready(filename, server_address):
                # image need to be placed at the same dir
                upload_image(filename, server_address)


# Set random seed for the prompt
def random_seed(prompt):
    for node in prompt:
        if "inputs" in prompt[node]:
            if "seed" in prompt[node]["inputs"]:
                prompt[node]["inputs"]["seed"] = random.randint(0, sys.maxsize)
            if "noise_seed" in prompt[node]["inputs"]:
                prompt[node]["inputs"]["noise_seed"] = random.randint(0, sys.maxsize)
    return prompt


# Get the ComfyUI output images
def get_images(prompt, client_id, server_address):
    prompt_id, aws_alb_cookie = queue_prompt(prompt, client_id, server_address)
    output_images = {}

    print("Generation started.")
    while True:
        history = get_history(prompt_id, server_address, aws_alb_cookie)
        if len(history) == 0:
            print("Generation not ready, sleep 1s ...")
            time.sleep(1)
            continue
        else:
            print("Generation finished.")
            break

    history = history[prompt_id]
    for node_id in history["outputs"]:
        node_output = history["outputs"][node_id]
        if "images" in node_output and node_output["images"][0]["type"] == "output":
            images_output = []
            for image in node_output["images"]:
                image_data = get_image(
                    image["filename"],
                    image["subfolder"],
                    image["type"],
                    server_address,
                    aws_alb_cookie,
                )
                images_output.append(image_data)
            output_images[node_id] = images_output
    return output_images, prompt_id
