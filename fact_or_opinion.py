import requests
from bs4 import BeautifulSoup
import nltk
import re


def get_urls(filename):
    """
    get_urls gets all the urls from a text file

    :param filename: is the file containing all the urls
    :return: a list of urls
    """
    urls = []
    with open(filename) as file:
        for line in file:
            line = line.strip()
            urls.append(line)
    return urls


def get_content(url_link):
    """
    get_content gets all the contents on an article page

    :param url_link is the article to scrape
    :return: a list paragraphs found on article
    """
    try:
        page = requests.get(url_link)
        soup = BeautifulSoup(page.text, "html.parser")
        soup.prettify()
        # Retrieve all of the paragraph tags
        paragraph_tags = soup.findAll('p')  # soup.find_all('article')
        return paragraph_tags
    except:
        return []


def get_keywords(urls):
    """
    get_keywords gets all the keywords from all the article pages

    :param urls: urls is a list of urls of all the article pages
    :return: a list a keywords
    """
    keywords = []
    for url in urls:
        paragraphs = get_content(url)
        for paragraph in paragraphs:
            for word in paragraph.text.split():
                word = re.split('[^a-zA-Z0-9]', word)[0]
                if word != '':
                    if word in english_vocab:  # or (word.isnumeric()):
                        if word not in nltk.corpus.stopwords.words('english'):
                            if word not in keywords:
                                keywords.append(word)
    return keywords


if __name__ == "__main__":
    nltk.download('words', quiet=True)
    nltk.download('stopwords', quiet=True)
    english_vocab = set(w.lower() for w in nltk.corpus.words.words())
    opinion_file = input("Opinion-Based Filename: ")
    fact_file = input("Fact-Based Filename: ")
    opinion_file = opinion_file.split()[0]
    fact_file = fact_file.split()[0]
    try:
        opinion_urls = get_urls(opinion_file)
        fact_urls = get_urls(fact_file)
        opinion_keywords = get_keywords(opinion_urls)
        fact_keywords = get_keywords(fact_urls)
        # print("Opinion-Based Keywords: ")
        # print(opinion_keywords)
        # print()
        # print("Fact-Based Keywords: ")
        # print(fact_keywords)
        url = input("URL: ")
        url = url.split()[0]
        keywords = get_keywords([url])
        opinion = 0
        fact = 0
        for key in keywords:
            if key in opinion_keywords:
                opinion += 1
            if key in fact_keywords:
                fact += 1
        total = opinion + fact
        print("Percentage of Factual Article: " + str(round(((fact / total) * 100), 2)) + "%")
        print("Percentage of Opinionated Article: " + str(round(((opinion / total) * 100), 2)) + "%")
        if fact > opinion:
            print("This article is more factual!")
        elif opinion > fact:
            print("This article is more opinionated!")
        else:
            print("This article is undetermined.")
    except FileNotFoundError:
        print("File does not exist.")
