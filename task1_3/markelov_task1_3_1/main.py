import requests as req

#from requests_tor import RequestsTor
#req = RequestsTor()

from bs4 import BeautifulSoup
import json
import tqdm
import time

headers = {
    'location': 'https://noginsk.hh.ru/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}

#print(resp.text) #выводим весь текст
#tag = soup.find(attrs={'class': "bloko-header-section-3"}) #поиск по атрибутам
#print(tag.text)
#print(tag.attrs['class'])

#tag = soup.find("h1")
#tag = soup.find_all("h1") # - такой тег один
#tag = soup.find_all("a") # - таких тегов очень много
#tag = soup.find_all(id_= ... ) - ищем по id
#tag = soup.find_all(class_="supernova-logo supernova-logo_inversed supernova-logo_hh-ru") #ищем по названию класса

data = { 'data': []}

for page in tqdm.tqdm(range (0,40)):
    time.sleep(2)
    url = f'https://hh.ru/search/vacancy?text=python+%D1%80%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D1%87%D0%B8%D0%BA&from=suggest_post&area=&page={page}&hhtmFrom=vacancy_search_list'
    
    resp = req.get(url, headers=headers)
    
    print(resp.status_code)
    soup = BeautifulSoup(resp.text, 'lxml')
    tags = soup.find_all(attrs={'data-qa': "serp-item__title"}) #выведем все вакансии

    for iter in tags:
        #print(iter.text, iter.attrs['href'])
        url_object = iter.attrs['href']
        time.sleep(2)
        resp_object = req.get(url_object, headers=headers)
        soup_object = BeautifulSoup(resp_object.text, 'lxml')
        tag_price = soup_object.find(attrs={'data-qa':"vacancy-salary"}).text
        #print(tag_price)
        try: 
            tag_region = soup_object.find(attrs={'data-qa':"vacancy-serp__vacancy-address"}).text
        except AttributeError:
            tag_region = None

        tag_experience = soup_object.find(attrs={'data-qa':"vacancy-experience"}).text
        data['data'].append({'title':iter.text, 
                             'work experience': tag_experience,
                             'salary':tag_price, 
                             'region': tag_region})
        
        #print(iter.text,tag_region, tag_price)

        with open('data.json','w') as file:
            json.dump(data,file,ensure_ascii=False)
        
        
        


