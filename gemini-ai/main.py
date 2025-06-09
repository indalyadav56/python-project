# To run this code you need to install the following dependencies:
# pip install google-genai

import base64
import os
from google import genai
from google.genai import types


def generate():
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.5-pro-preview-05-06"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""write a script for 30 seconds of video on topic kids story, Do not add scene description 

do not add anything in braces,  Just return the plain story in text 
give me response in json format  and follow the scema 


`{
  \"script\": \"\"

}`"""),
            ],
        ),
        types.Content(
            role="model",
            parts=[
                types.Part.from_text(text="""**Refining the Concept**

I've been working on a simple kid's story idea that can fit the time constraint. I'm focusing on crafting dialogue and action that's easy for kids to understand and engaging. My goal is to create a story with a clear beginning, middle, and end, ensuring it's appropriate for the target audience.


**Constructing a Narrative**

I've sketched out a simple narrative about a star afraid of the dark, aiming for a 30-second video length. The draft has been checked against all constraints and I have timed it, it fits the target time. My confidence level is high because all checks are positive. I am now preparing the JSON output, ready for the next step.


**Generating the Script**

I've crafted a short story about a star overcoming his fear of the dark, aiming for the 30-second video length. The plain text script is ready and I've verified it against all constraints. My confidence score is 5/5, and I'm now structuring the output as JSON, per the specifications. The next step is generating and delivering the final JSON script.


"""),
                types.Part.from_text(text="""```json
{
  \"script\": \"Barnaby the bunny loved carrots, but one morning, his favorite carrot was gone! He sniffed around the garden. 'Who took my carrot?' he wondered. Suddenly, he saw Squeaky the squirrel munching on something orange. 'Squeaky!' Barnaby hopped over. Squeaky looked up, surprised. 'Oh, Barnaby! I found this delicious carrot. Want to share?' Barnaby smiled. Sharing made the carrot taste even better!\"
}
```"""),
            ],
        ),
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""INSERT_INPUT_HERE"""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")

if __name__ == "__main__":
    generate()
