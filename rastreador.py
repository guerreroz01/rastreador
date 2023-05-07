import requests
import time
from bs4 import BeautifulSoup
from googlesearch import search
import openai
import sys
import json
from requests.exceptions import SSLError

def get_page_text(url):
    try:
        response = requests.get(url)
    except SSLError as e:
        print(f"Error de SSL al obtener el contenido de la URL: {url}")
        print(f"Detalles del error: {e}")
        return None
    
    soup = BeautifulSoup(response.text, "lxml")

    main_content = soup.find_all('p')
    

    if main_content:
        for script in soup(["script", "style"]):
            script.extract()

        page_text = ' '.join([p.get_text() for p in main_content])
        clean_text = " ".join(page_text.split())
        return clean_text
    else:
        for script in soup(["script", "style"]):
            script.extract()

        page_text = soup.get_text()
        clean_text = " ".join(page_text.split())
        return clean_text


query = sys.argv[1]
num_results = 7
search_results = []

for url in search(query):
    search_results.append(url)
    if len(search_results) >= num_results:
        break


texts = [get_page_text(url) for url in search_results if get_page_text(url) is not None]

openai.api_key = "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"
relevant_texts = []
max_tokens_per_segment = 4000

for i, text in enumerate(texts):
    text_segments = [text[j:j+max_tokens_per_segment]
                     for j in range(0, len(text), max_tokens_per_segment)]
    
    for segment in text_segments:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "assistant",
                    "content": f"Resumir el siguiente texto y determinar si es relevante para la búsqueda haciendo una calificacion del 1 al 10'{query}':\n\n{segment}\n\nResumen: ",
                },
            ],
        )
        time.sleep(3)

        summary = response.choices[0].message.content

        # if "relevante = true" in summary.lower():
        if summary.lower():
            relevant_texts.append(
                {"url": search_results[i], "summary": summary})
            break

def save_to_json_file(data, file_name):
    with open(file_name, 'w') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)


save_to_json_file(relevant_texts, "search.json")
#for relevant_text in relevant_texts:
#    print("---------------------------------------------------------------")
#    print(f"URL: {relevant_text['url']}")
##    print("***************************************************************")
#    print(relevant_text)
#    print("---------------------------------------------------------------")
