from selenium import webdriver
from selenium.webdriver.common.by import By
import os


def export_article(article_title, picture_link, article_link, article_text):
    div_template = open('div_template.html', 'r').read()
    div_template = div_template.replace('[[:article_title:]]', article_title)
    div_template = div_template.replace('[[:picture_link:]]', picture_link)
    div_template = div_template.replace('[[:article_link:]]', article_link)
    div_template = div_template.replace('[[:article_text:]]', article_text)
    return div_template


def extract_from(web_link, file_name):
    driver.get(web_link)
    final_articles = ''
    article_lists = driver.find_elements(By.CLASS_NAME, 'stream-list')
    for article_list in article_lists:
        articles = article_list.find_elements(By.TAG_NAME, 'a')
        for article in articles:
            article_title = article.find_element(By.TAG_NAME, 'h2').accessible_name
            picture_link = article.find_element(By.TAG_NAME, 'source').get_attribute('srcset')
            article_link = article.get_attribute('href')
            article_text = article.find_element(By.CLASS_NAME, 'item_lead').get_attribute('innerText')
            if len(article_text) > 320:
                article_text = article_text[:320] + '...'
            final_articles += export_article(article_title, picture_link, article_link, article_text)

    file_name = 'http/' + file_name + '.html'
    f = open(file_name, 'w')
    template = open('template.html', 'r').read()
    title = driver.find_element(By.CLASS_NAME, 'category-list_title').text
    template = template.replace('[[:title:]]', title)
    template = template.replace('[[:source:]]', final_articles)
    f.write(template)
    f.close()


def create_html(title, name):
    file_name = 'http/' + name + '.html'
    f = open(file_name, 'w')
    template = open('template.html', 'r').read()
    template = template.replace('[[:title:]]', title)
    template = template.replace('[[:source:]]', '')
    f.write(template)
    f.close()


driver = webdriver.Chrome()
links = ['technologie', 'gospodarka', 'biznes', 'praca']
try:
    os.mkdir("http/")
except:
    pass
for i in links:
    link = 'https://businessinsider.com.pl/' + i
    extract_from(link, i)
create_html('Menu', 'index')

driver.close()
os.system('python -m http.server 8000 -d http')
