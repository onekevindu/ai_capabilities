# from openai import OpenAI

# client = OpenAI(
#   api_key=""
# )

# completion = client.chat.completions.create(
#   model="gpt-4o-mini",
#   store=True,
#   messages=[
#     {"role": "user", "content": "write a haiku about ai"}
#   ]
# )

# print(completion.choices[0].message);

# setting env

import getpass
import os

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["OPENAI_API_KEY"] = getpass.getpass()