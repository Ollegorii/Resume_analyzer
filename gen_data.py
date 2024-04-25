#Генерация данных для обучения через сервис Яндекс Облака, предоставляющий доступ к YaGPT
import requests
import json
import pandas as pd
import time

resume_vac = pd.DataFrame(columns=['resume', 'vaccancy'])
resume = pd.read_csv("resume_data_1.csv", index_col=0)
for i in range(868,1000):
    txt = resume.iloc[i].text

    FOLDER_ID = "b1gqm3mh92ir3bae1daj" #идентификатор_каталога из ЛК яндекс облако
    IAM_TOKEN = "t1.9euelZqXkMqXzc2WxseZloqZkcjHmO3rnpWaip6Ymo2Ti5nJzZnHlMiYx53l8_c4ECxP-e97aRQ1_d3z93g-KU_573tpFDX9zef1656VmpePjJqax8uax42Li5qazIue7_zF656VmpePjJqax8uax42Li5qazIue.5Am91A1jY6cLhDTyYyjsXDlFJ8GmTjYTPr3yM-b1bcW93dyI6t8lntkoJq8CENY7E8zoDI45aDl-J2GIHOreDA"
    #IAM_TOKEN сгенерирован через IAM-токен (из инструкции яндекса) и ковертацию его через командную строку
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {IAM_TOKEN}",
        "x-folder-id": FOLDER_ID
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {IAM_TOKEN}",
        "x-folder-id": FOLDER_ID
    }

    data = {
        "modelUri": "gpt://b1gqm3mh92ir3bae1daj/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.3,
            "maxTokens": "2000"
        },
        "messages": [
            {
                "role": "system",
                "text": "Представь, что ты директор по персоналу. Тебе приходит резюме. Сгенерируй требования вакансии под которые это резюме подходит. Выдай только требования вакансии"
            },
            {
                "role": "user",
                "text": txt
            }
        ]
    }

    response = requests.post("https://llm.api.cloud.yandex.net/foundationModels/v1/completion", headers=headers, json=data)
    print('response = ', response.text)
    js = json.loads(response.text)

    vac = js["result"]["alternatives"][0]["message"]['text']
    add = pd.DataFrame({'resume': [txt], 'vaccancy': [vac]})
    resume_vac = pd.concat([resume_vac, add], ignore_index=True)
    time.sleep(2)
    if i % 50:
        resume_vac.to_csv('resume_vac9.csv', encoding='utf-8')
resume_vac.to_csv('resume_vac9.csv', encoding='utf-8')