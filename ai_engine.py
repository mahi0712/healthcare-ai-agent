from groq import Groq

client = Groq(

    api_key="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"
)

def ask_ai(message):

    response = client.chat.completions.create(

        model="llama3-8b-8192",

        messages=[

            {
                "role": "system",

                "content": """

You are a healthcare assistant for elderly patients.

Rules:
- Give short healthcare advice
- Suggest doctor if serious
- Be polite
- Keep answers simple

"""
            },

            {
                "role": "user",

                "content": message
            }
        ]
    )

    return response.choices[0].message.content