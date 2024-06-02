"""
This code generates an image based on a given prompt using the OpenAI API.
"""

import base64
import requests
import os
from openai import OpenAI
import datetime
import sys


def generate_image(prompt):
    """
    Generate an image based on the given prompt.

    Args:
        prompt (str): The prompt for generating the image.

    Returns:
        None
    """
    client = OpenAI()
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        style="vivid",
        response_format="b64_json",
        size="1024x1024",
    )

    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"generated_image_{current_time}.png"

    image_data = response.data[0].b64_json
    image_bytes = base64.b64decode(image_data)

    with open(filename, "wb") as image_file:
        image_file.write(image_bytes)

    print("Image saved as generated_image.png")


def get_description(image):
    """
    This function retrieves a description using the OpenAI API Key.
    """
    api_key = os.environ.get("OPENAI_API_KEY")

    # Function to encode the image
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    # Path to your image
    image_path = image

    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "write me a prompt for dalle-3 with style polaroid",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        "max_tokens": 300,
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    )

    return response.json()["choices"][0]["message"]["content"]
import sys
import os

# Check if command line argument exists
if len(sys.argv) > 1:
    # get arg 1 to get image name
    IMAGE_NAME = sys.argv[1]
    
    # Check if the file is a PNG file
    _, file_extension = os.path.splitext(IMAGE_NAME)
    if file_extension.lower() != '.png':
        print("Invalid file type. Please provide a PNG file.")
        print("Usage: python create_daily.py <image_name.png>")
    else:
        prompt = get_description(IMAGE_NAME)
        print(prompt)
        generate_image(prompt)
else:
    print(
        "No image name provided. Please provide an image name as a command line argument."
    )
    print("Usage: python create_daily.py <image_name.png>")
