from newspaper import Article
from googlesearch import search
import requests
import random
import string
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import warnings

warnings.filterwarnings('ignore')

nltk.download('punkt', quiet=True)
# query = 'apple'
# link = search(query, tld="co.in", num=10, stop=10, pause=2)
print('Tec Bot : I am Tec Bot , I will Answer Your queries about anything . if you want to exit, '
      'type bye')
query = input(('Tec Bot : Enter the keyword on what you want to know?'))

exit_list = ['exit', 'bye', 'see you later', 'quit', 'break']

links = []
for j in search(query, tld="co.in", num=10, stop=10, pause=2):
    links.append(j)


def get_Link(links):
    # printing link For users
    link = random.choice(links)
    print('Tec Bot: Im using this link : \n ')
    print(link)
    print('If you want to change the link type "change" anytime')
    return link


# Article
# article = Article(
#      'https://www.infoq.com/articles/java-16-new-features/?topicPageSponsorship=eb23c8b0-5fa3-4f9a-8c59-be00f5b6e3bd')
article = Article(get_Link())
article.download()
article.parse()
article.nlp()
corpus = article.text

# Artical print
# print(corpus)

# Tokenization

text_value = corpus
sentence_list = nltk.sent_tokenize(text_value)


# check out the list
# print(sentence_list)


# Greeting Response


def greeting_response(text):
    text = text.lower()

    # Bot Greetings
    bot_greeting = ['Hi', 'Hello', 'Hey']
    # User Greetings
    user_greeting = ['hi', 'hello', 'hey', 'wassup', 'howdy']

    for word in text.split():
        if word in user_greeting:
            return random.choice(bot_greeting)


def index_sort(list_var):
    length = len(list_var)
    list_index = list(range(0, length))

    x = list_var
    for i in range(length):
        for j in range(length):
            if x[list_index[i]] > x[list_index[j]]:
                temp = list_index[i]
                list_index[i] = list_index[j]
                list_index[j] = temp

    return list_index


# Bot response
def bot_response(user_input):
    user_input = user_input.lower()
    input = user_input
    sentence_list.append(user_input)
    bot_response_value = ''
    cm = CountVectorizer().fit_transform(sentence_list)
    similarity_scores = cosine_similarity(cm[-1], cm)
    similarity_scores_list = similarity_scores.flatten()
    index = index_sort(similarity_scores_list)
    index = index[1:]
    response_flag = 0

    j = 0
    for i in range(len(index)):
        if similarity_scores_list[index[i]] > 0.0:
            bot_response_value = bot_response_value + ' ' + sentence_list[index[i]]
            response_flag = 1
            j = j + 1
        if j > 2:
            break

    if response_flag == 0:
        bot_response_value = bot_response_value + ' ' + "I apologize I don't understand"

    sentence_list.remove(user_input)

    return bot_response_value


# Test_ bot_response Function
# user_input = 'hellow world'
# sentence_list.append(user_input)
# bot_response = ''
# cm = CountVectorizer().fit_transform(sentence_list)
# similarity_scores = cosine_similarity(cm[-1], cm)
# similarity_scores_list = similarity_scores.flatten()
# index = index_sort(similarity_scores_list)
#
# print(similarity_scores_list)
# print(index)


# Starting chat


while True:
    user_input = input('User: ')
    if user_input.lower() in exit_list:
        print('Tec Bot: Chat With you later!')
        break
    if user_input.lower() == 'change':
        print()
        break
    else:
        if greeting_response(user_input) is not None:
            print('Tec Bot: ' + greeting_response(user_input))
        else:
            print('Tec Bot: ' + bot_response(user_input))
