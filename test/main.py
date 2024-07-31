#!/usr/bin/python3
# https://github.com/aws-samples/comfyui-on-eks/blob/main/test/invoke_comfyui_api.py
import argparse
import requests
import uuid
import json
import urllib.parse
import time
import threading
import io

import utils

from PIL import Image


# Invoke the ComfyUI API with one workflow
def single_inference(server_address, request_api_json):
    start = time.time()
    client_id = str(uuid.uuid4())
    with open(request_api_json, "r") as f:
        prompt = json.load(f)
    utils.review_prompt(prompt, server_address)
    prompt = utils.random_seed(prompt)
    images, prompt_id = utils.get_images(prompt, client_id, server_address)
    end = time.time()
    for node_id in images:
        for image_data in images[node_id]:
            image = Image.open(io.BytesIO(image_data))
            image.show()
    timespent = round((end - start), 2)
    print("Inference finished.")
    print(f"ClientID: {client_id}.")
    print(f"PromptID: {prompt_id}.")
    print(f"Num of images: {len(images)}.")
    print(f"Time spent: {timespent}s.")
    print("------")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--workflow", type=str, default="workflow_api.json")
    parser.add_argument("-s", "--server", type=str, default="http://localhost:50000")
    args = parser.parse_args()

    single_inference(args.server, args.workflow)
