import json
import requests
from bs4 import BeautifulSoup
import lxml
import time
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_full_content(url):
    try:
        time.sleep(2)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "lxml")
            article_content = soup.find("div", class_="article-content")

            if article_content:
                for tag in ["script", "style", "iframe", "noscript"]:
                    for element in article_content.find_all(tag):
                        element.decompose()
                return article_content.get_text(strip=True)
        return None

    except Exception as e:
        logging.error(f"Error extracting full content: {str(e)}")
        return None


def main():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
        }

        response = requests.get("https://techcrunch.com/", headers=headers)
        soup = BeautifulSoup(response.content, "lxml")
        articles = soup.find_all("div", {"class": "loop-card__content"})

        blog_posts = []

        for article in articles:
            try:
                title_element = article.find("a", class_="loop-card__title-link")
                title = title_element.get_text(strip=True) if title_element else None
                source_url = title_element["href"] if title_element else None

                category_element = article.find("a", class_="loop-card__cat")
                category = (
                    category_element.get_text(strip=True) if category_element else None
                )

                author_element = article.find("a", class_="loop-card__author")
                author = author_element.get_text(strip=True) if author_element else None

                date_element = article.find("time", class_="loop-card__time")
                published_date = date_element["datetime"] if date_element else None

                excerpt = article.find("div", class_="loop-card__description")
                summary = excerpt.get_text(strip=True) if excerpt else None

                if title and source_url:
                    full_content = get_full_content(source_url)

                    blog_posts.append(
                        {
                            "title": title,
                            "category": category,
                            "author": author,
                            "published_date": published_date,
                            "source_url": source_url,
                            "summary": summary,
                            "full_content": full_content,
                        }
                    )

                    logging.info(f"Extracted data for: {title}")

            except Exception as e:
                logging.error(f"Error extracting data: {str(e)}")
                continue

        if blog_posts:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"techcrunch_articles_{timestamp}.json"

            with open(filename, "w", encoding="utf-8") as f:
                json.dump(blog_posts, f, ensure_ascii=False, indent=4)
            logging.info(f"Saved {len(blog_posts)} articles to {filename}")
        else:
            logging.warning("No articles found")

    except Exception as e:
        logging.error(f"Main execution error: {str(e)}")


if __name__ == "__main__":
    main()
