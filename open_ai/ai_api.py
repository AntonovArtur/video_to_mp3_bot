import openai

openai.api_key = "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"


def create_image(text):
    response = openai.Image.create(
        prompt=text,
        n=1,
        size="512x512"
    )
    return response['data'][0]['url']


def generate_text(prompt_text):
    # Задаем текст для генерации продолжения
    # prompt_text = "Once upon a time in a faraway kingdom, there was a brave knight who"

    # Генерируем продолжение текста
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt_text,
        temperature=0.7,
        max_tokens=2000
    )
    print(str(response))
    return response['choices'][0]['text']
