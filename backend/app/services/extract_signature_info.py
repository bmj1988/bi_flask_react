import base64
from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def extract_signature_info(image_path):
    # Extracts names and addresses from single ballot image.
    print('!!!IMAGE PATH', image_path)

    # Getting the base64 string
    base64_image = encode_image(image_path)

    # open AI client definition
    openai_api_key = os.environ.get('OPENAI_API_KEY')
    client = OpenAI(api_key=openai_api_key)

    # prompt message
    messages = [
          {
            "role": "user",
            "content": [
              {
                "type": "text",
                "text": """Using the written text in the image create a list of dictionaries where each dictionary consists of keys 'Name', 'Address', 'Date', and 'Ward'. Ignore all values in the box labeled "CIRCULATOR'S AFFIDAVIT OF CERTIFCATION". Ignore all values in the box labeled "SIGNATURE". Addresses belong to the name printed in the box to the immediate right of the box labeled "ADDRESS". Fill in the values of each dictionary with the correct entries for each key. Write all the values of the dictionary in full, except in the case of 'Address', which should be truncated to exclude APT and the following Apartment Number. Only output the list of dictionaries. No other intro text is necessary. The output should be in JSON format, and look like
                {'data': [{"Name": "John Doe",
                          "Address": "123 Picket Lane",
                          "Date": "11/23/2024",
                          "Ward": "2"},
                          {"Name": "Jane Plane",
                          "Address": "456 Fence Field",
                          "Date": "11/23/2024",
                          "Ward": "3"},
                          ]} """
              },
              {
                "type": "image_url",
                "image_url": {
                  "url": f"data:image/jpeg;base64,{base64_image}"
                }
              }
            ]
          }
        ]

    # processing result through GPT
    results = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.0,
        response_format={"type": "json_object"}
    )
    # convert json into list
    signator_list = json.loads(results.choices[0].message.content)['data']

    print('!!!SIGNATOR LIST', signator_list)

    return signator_list
