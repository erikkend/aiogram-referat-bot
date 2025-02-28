import aiohttp
import asyncio
import google.generativeai as genai



genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

async def main(theme: str) -> str:
    messages = [
        {'role': 'user',
         'parts': [f'Напиши реферат на тему "{theme}"']}
    ]
    response = model.generate_content(messages)
    print(response.text)
    messages.append({'role': 'model',
                     'parts': [response.text]})
    messages.append({'role': 'user',
                     'parts': ["Напиши этот же реферат другими словами"]})
    print('+++++++++++++++++++++++++++++++++')
    response = model.generate_content(messages)
    print(response.text)
    pass

asyncio.run(main("наркотики"))
