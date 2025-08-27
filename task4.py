import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://www.detik.com/search/searchall?query={query}&page={page}&result_type=latest"

def scraping(query, max_pages=3):
    results = []

    for page in range(1, max_pages+1):
        url = BASE_URL.format(query=query, page=page)
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.exceptions.Timeout as e:
            print(f"Timeout saat fetch halaman {page}. Coba lagi nanti. {e}")
            continue
        except requests.exceptions.ConnectionError as e:
            print(f"Gagal koneksi ke server saat fetch halaman {page}. {e}")
            continue
        except requests.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("article")
        for article in articles:
            try:
                link_tag = article.find("a", class_="media__link")
                if not link_tag:
                    continue
                dtr_act = link_tag.get("dtr-act", "")
                if "video" in dtr_act or "foto" in dtr_act:
                    continue

                title_tag = article.find("h3")
                title = title_tag.get_text(strip=True)

                img_tag = article.find("img")
                img_link = img_tag["src"]

                body_tag = article.find("div", class_="media__desc")
                body_text = body_tag.get_text(strip=True)

                time_tag = article.find("div", class_="media__date")
                pub_time_tag = time_tag.find("span")
                pub_time = pub_time_tag["title"]

                results.append({
                    "title": title,
                    "image": img_link,
                    "body": body_text,
                    "publish_time": pub_time
                })
            except Exception as e:
                print(f"Error parsing article: {e}")
                continue
        time.sleep(1)
    return results


if __name__ == "__main__":
    query = "teknologi"
    data = scraping(query)
    if not data:
        print("Tidak ada hasil scraping.")
    else :
      for idx, item in enumerate(data, start=1):
          print(f"{idx}.Judul:{item['title']}")
          print(f"   Image link: {item['image']}")
          print(f"   Body: {item['body']}")
          print(f"   Published: {item['publish_time']}\n")
