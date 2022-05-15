# import the libraries

from bs4 import BeautifulSoup
import pandas as pd
import requests
import urllib.request
import time
import nltk
from newspaper import Article
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import datetime

nltk.download('punkt') # "Punkt Tokenizer Models" divides the text into a list of sentences using ML algorithm



# Number of pages to scrap
n = 3

# search theme
search_theme = 'energia'


def scrape_cnn_website(search, page):
# """ 
# Scrapes the CNN Website based on a theme and a page number and returns a News based DataFrame.
# """
    page_theme = search
    page_number = str(page)

    url = 'https://www.cnnbrasil.com.br/tudo-sobre/' + page_theme + '/' + 'pagina' + page_number +'/' 
    webpage = requests.get(url)
    soup = BeautifulSoup(webpage.text, 'html.parser')

    # Get the location of the information

    article_date = soup.find_all('span', attrs= {'class': 'home__title__date'}) # location of data information
    article_title = soup.find_all('h2', attrs= {'class': 'news-item-header__title'} ) # location of title information
    article_tag = soup.find_all('span', attrs= {'class': 'latest__news__category'} ) # location of the tag
    article_theme = soup.find_all('h1', attrs= {'class': 'tags__topics__title'} ) # location of the theme
    article_links = soup.find_all('a',attrs={'class': 'home__list__tag'} )# location of the links

    # Loop through the article_date

    for i in article_date:
        temp=0
        temp = i.text.strip()
        date = temp[0:10]
        time = temp[14:19]
        date_time = date +'-'+ time

        date_time = pd.to_datetime(date_time,format= '%d/%m/%Y-%H:%M').strftime('%d/%m/%Y - %H:%M')
        dates.append(date_time)

    # Loop through the article_titles and set the theme

    for i in article_title:
        temp = 0
        temp = i.text.strip()
        title.append(temp)
        theme.append(article_theme[0].text.strip().split()[2])

    # Loop through the article_tags

    for i in article_tag:
        temp = 0
        temp = i.text.strip()
        tag.append(temp)

    # Loop through the article_links

    for i in article_links:
        href = i.get('href')
        links.append(href)

          # NLP Process

        article = Article(href)
        article.download()
        article.parse()
        article.nlp()

        site_name = article.meta_data['og']['site_name']
        # title = article.meta_data['og']['title']
        text = article.text
        summary = article.summary
        # author = article.authors
        texts.append(text)
        summarys.append(summary)
        authors.append(site_name)

# Create lists to store the scraped data
theme = []
tag = []
title = []
authors = []
dates = []
links = []
texts = []
summarys = []





# applying the function
for i in range(1 , n):

    scrape_cnn_website(search_theme, i )
    print(
    len(authors), 
    len(links), 
    len(theme), 
    len(tag), 
    len(title),
    len(dates), 
    len(texts), 
    len(summarys) 
)

# create a Data_Frame
df = pd.DataFrame( columns= ['dates','theme','authors','tag','title','summarys','texts','links' ] )
df.dates = dates
df.dates = pd.to_datetime(df.dates,format= '%d/%m/%Y - %H:%M')
df.theme = theme
df.authors = authors
df.tag = tag
df.title = title
df.summarys = summarys
df.texts = texts
df.links = links

date_min = str(df.dates.dt.date.min().strftime('%d/%m/%Y'))+' at '+ str(df.dates.dt.time.min())
date_max = str(df.dates.dt.date.max().strftime('%d/%m/%Y'))+' at '+ str(df.dates.dt.time.max())

df_date_range = 'DF Date Rage: from ['+ date_min + '] to [' + date_max + ']'

print(df_date_range)


# filter by date

df_filtered = df[df.dates > '2022-01-01']

date_min = str(df_filtered.dates.dt.date.min().strftime('%d/%m/%Y'))+' at '+ str(df_filtered.dates.dt.time.min())
date_max = str(df_filtered.dates.dt.date.max().strftime('%d/%m/%Y'))+' at '+ str(df_filtered.dates.dt.time.max())

date_range = 'Date Rage: from ['+ date_min + '] to [' + date_max + ']'

print(date_range)

df_filtered

# WordCloud text and additional parameters

text = " ".join(s.lower() for s in df_filtered.texts)
wordcloud_theme = df_filtered.theme[0].lower()
wordcloud_title = 'Author: '+ df_filtered.authors[0]+' │ Theme: ' + df_filtered.theme[0] +' │ '+ date_range     # WordCloud text and additional parameters

text = " ".join(s.lower() for s in df_filtered.texts)
wordcloud_theme = df_filtered.theme[0].lower()
wordcloud_title = 'Author: '+ df_filtered.authors[0]+' │ Theme: ' + df_filtered.theme[0] +' │ '+ date_range     


# StopWords parameters

PORTUGUESE_STOPWORDS_PATCH_1 = r'https://gist.githubusercontent.com/alopes/5358189/raw/2107d809cca6b83ce3d8e04dbd9463283025284f/stopwords.txt'


response_PATCH = requests.get(PORTUGUESE_STOPWORDS_PATCH_1)

pt_stopwords = response_PATCH.text

pt_stopwords = pt_stopwords.replace(" ","").splitlines()  



stop_words  = list(pt_stopwords) + list(STOPWORDS) + [wordcloud_theme,
                                                    'cerca',
                                                    'país',
                                                    'disse',
                                                    'agora',
                                                    'ouvir',
                                                    'notícia',
                                                    'ano' ,
                                                    'entanto',
                                                    'episódio',
                                                    'ainda',
                                                    'acordo',
                                                    'demanda',
                                                    'maior',
                                                    'dia',
                                                    'segundo',
                                                    'pode',
                                                    'desde',
                                                    'todo',
                                                    'sobre',
                                                    'getty',
                                                    'getty images',
                                                    'anadolu',
                                                    'images',
                                                    'agency']
                                               

# Plot the WordCloud


plt.figure(figsize=(20,10))



wordcloud = WordCloud(min_font_size=50, 
               max_font_size=500, 
               background_color='white', 
            #    max_words = 80,
               mode="RGB",
               colormap='tab10',
               stopwords=stop_words,
               width=3000, 
               height=1500,
               normalize_plurals= True
).generate(text)




plt.title(wordcloud_title, fontsize=10, color="black")
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
plt.to_file('CNN'+search_theme+'.png') 







