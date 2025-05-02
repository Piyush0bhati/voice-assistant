from openai import OpenAI
import time

client = OpenAI(
    api_key="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"
)

completion = client.chat.completions.create(

    model= "gpt-3.5-turbo",
    messages=[
        {"role":"system", "content": "you are a virtual assistant named loki skilled in genral tests like alexa and google cloud"},
        {"role": "user", "content": "what is coding"}
    ]
)
print(completion.choices[0].message)




