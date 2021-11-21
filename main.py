import requests
from bs4 import BeautifulSoup


def get_soup_object(url):
    headers = {'accept': '*/*',
    'user-agent': 'MMozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup

def get_data_preview_posts(soup):
    url = 'https://habr.com'
    data_post_preview = {}
    articles = soup.find_all('article', {'class': 'tm-articles-list__item'})

    for post_numbers, article in enumerate(articles, start=1):
        hubs_post = []

        # Получаем заголовки постов:
        headers = article.find('a', class_='tm-article-snippet__title-link')
        if headers is not None:
            post_haders = headers.text
        else:
            post_haders = ''

        # Получаем ссылки на посты:
        links_heders = article.find('a', class_='tm-article-snippet__title-link', href=True)
        if links_heders is not None:
            link = url + links_heders['href']
        else:
            link = ''
    
        # Получаем дату и время публикации поста:
        date_time = article.find('time')['title']

        # Получаем хабы поста:
        hubs = article.find_all('a', class_='tm-article-snippet__hubs-item-link')
        for hub in hubs:
            hubs_post.append(hub.text.replace('\xa0', '').strip())

        # Получаем текст под постом
        text_posts = article.find_all('p')
        texts = []
        for text_post in text_posts:
            texts.append(text_post.text)
        
            
        # Получаем словарь из всех собранных данных:
        data_post_preview[f'post_{post_numbers}'] = {
            'headers': post_haders,
            'link': link,
            'hubs_post': hubs_post,
            'date_time': date_time,
            'text_post': texts
        }

       
    return data_post_preview
            

if __name__ == '__main__':
    KEYWORDS = ['Winamp', 'Звук', 'DEP-09', 'вложенность', 'PHP', 'OrderLine', 'Python']
    
    soup = get_soup_object('https://habr.com/ru/all/')
    data_preview_posts = get_data_preview_posts(soup)
    posts = []
    for data_preview in data_preview_posts.values():
        data_text = (', '.join(data_preview['hubs_post'] + data_preview['text_post'])) + data_preview['headers']

        for keyword in KEYWORDS:
            if keyword in data_text:
                posts_text = (f'{data_preview["headers"]}\n{data_preview["date_time"]}\n{data_preview["link"]}\n{"-" * 50}')
                posts.append(posts_text)
    posts = list(set(posts))
    if not len(posts) == 0:
        for post in posts:
            print(post)
    else:
        (print('Упс! Ничего не найдено'))