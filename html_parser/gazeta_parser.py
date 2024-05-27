import requests
import datetime
from bs4 import BeautifulSoup
import csv


def parse():
    URL = "https://www.gazeta.ru/news/"
    links = []

    page = requests.get(URL)
    soup = BeautifulSoup(page.text, "html.parser")
    all_articles = soup.find("div", id="_id_article_listing")
    articles = all_articles.find_all("a")
    for article in articles:
        link = "https://www.gazeta.ru" + article["href"]

    print(f"Got {len(links)} links.")

    parse_result = []

    for link in links:
        parse_result.append(parse_one_link(link))

    write_to_csv(parse_result)


def write_to_csv(data: list):

    with open("output.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(["Ссылка", "Текст", "Дата"])

        for row in data:
            writer.writerow([row["link"], row["text"], row["date"]])


def parse_one_link(url: str):
    try:
        all_text = ""
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        header = soup.find("h1").get_text()
        all_text = all_text + header + " "
        try:
            header_1 = soup.find("h2", class_="subheader").get_text()
            all_text = all_text + header_1 + " "
        except Exception:
            pass

        texts = soup.find("div", class_="b_article-text")
        texts = texts.find_all("p")
        for text in texts:
            all_text = all_text.strip() + " " + text.get_text().strip()

        time_news = soup.find("time", itemprop="datePublished")
        time_news = time_news["datetime"].replace("T", " ")[:-6]
        time_news = datetime.datetime.strptime(time_news.strip(), "%Y-%m-%d %H:%M:%S")

        result = {"link": url, "text": all_text.replace("\xa0", " "), "date": time_news}
        return result

    except Exception as err:
        print(f"Ошибка парсинга")


if __name__ == "__main__":
    print("Начало парсинга")
    parse()
