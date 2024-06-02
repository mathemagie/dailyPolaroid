# Daily Polaroid Image Generator

This Python script generates a Polaroid-style image based on a given prompt using the OpenAI API.

## How it works

The script takes an image name as an argument, retrieves a description for the image using the OpenAI API, and then generates an image based on the description.

The image generation is done using the `generate_image` function in `create_daily.py`. This function uses the OpenAI API to generate an image based on the given prompt.

The description retrieval is done using the `get_description` function in `create_daily.py`. This function sends a POST request to the OpenAI API with a payload containing the image data and a request for a description.

## Usage

To use this script, you need to have an OpenAI API key. The key is expected to be in an environment variable named `OPENAI_API_KEY`.

Run the script with the image name as an argument:

