"""
This code generates an image based on a given prompt using the OpenAI API.
"""

import base64
import requests
import os
from openai import OpenAI
import datetime
import sys

# PROMPT = "Create an image of a crowded subway car during rush hour. The passengers are standing and sitting, with many holding onto metal bars and handles. Most of them are wearing masks, indicating a health precaution. The interior of the subway car features ventilation systems and bright lighting. Many passengers are engaged with their smartphones or other devices. The overall atmosphere should convey the hustle and bustle of a busy urban subway, with a slightly vintage or retro color palette. The scene should look realistic and detailed, capturing the essence of a typical city commute with polaroid style"
# prompt = "Create a Polaroid-style photograph of vibrant pink roses in full bloom, set against the backdrop of a rustic stone wall. The image should capture the soft, nostalgic feel of a sunny day in a quaint garden, with hints of lush green leaves framing the flowers."


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


# get arg 1 to get image name
IMAGE_NAME = sys.argv[1]
prompt = get_description(IMAGE_NAME)
print(prompt)
generate_image(prompt)