import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import time

def fetch_reviews_html(app_id, cursor):
    url = f"https://store.steampowered.com/app/{app_id}/reviews"
    params = {
        'p': cursor,
        'filter': 'all',
        'language': 'all',
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error fetching reviews: {response.status_code}")
        return None

def scrape_reviews_by_language(app_id, review_limit=1000):
    language_count = defaultdict(int)
    total_reviews = 0
    cursor = 1

    while total_reviews < review_limit:
        html_content = fetch_reviews_html(app_id, cursor)
        if not html_content:
            break

        soup = BeautifulSoup(html_content, 'html.parser')
        reviews = soup.find_all('div', class_='review_box')

        if not reviews:
            break

        for review in reviews:
            if total_reviews >= review_limit:
                break
            language = review['data-language'] if 'data-language' in review.attrs else 'unknown'
            language_count[language] += 1
            total_reviews += 1

        cursor += 1
        time.sleep(1)

    return language_count, total_reviews

def print_language_distribution(language_count, total_reviews):
    print(f"Total Reviews Processed: {total_reviews}")
    print("Language Distribution:")
    for language, count in language_count.items():
        percentage = (count / total_reviews) * 100
        print(f"{language}: {count} ({percentage:.2f}%)")

if __name__ == "__main__":
    APP_ID = input("enter the app id ")
    review_limit = input("enter the maximum number of reviews")
    if (int(review_limit)<20):
        print("error, reviews must be at least 20")
    language_count, total_reviews = scrape_reviews_by_language(APP_ID, int(review_limit))
    print_language_distribution(language_count, total_reviews)
