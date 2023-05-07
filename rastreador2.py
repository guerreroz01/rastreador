import requests
import openai
import json
from bs4 import BeautifulSoup

def get_page_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    main_content = soup.find_all('p')
    page_text = ' '.join([p.get_text() for p in main_content])
    clean_text = " ".join(page_text.split())
    return clean_text

def generate_summary(text):
    openai.api_key = "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"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "assistant",
                "content": f"Resumir el siguiente texto:\n\n{text}\n\nResumen:"
            }
        ],
        max_tokens=150,
    )

    return response.choices[0].message.content.strip()

def save_summary_to_json(summary, url, file_name="search.json"):
    with open(file_name, "w") as outfile:
        json.dump({"summary": summary,"url": url }, outfile)

if __name__ == "__main__":
    url = input("Por favor, ingresa la URL de la página web que deseas resumir: ")
    text = get_page_text(url)
    summary = generate_summary(text)
    save_summary_to_json(summary, url)

    print("\nEl resumen del contenido de la página web se ha guardado en search.json")

