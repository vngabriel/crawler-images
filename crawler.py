from bs4 import *
import requests
import os

PARENT_DIR = "/home/gabriel/Repositories/crawler-images/"
BCS_URL = "https://iplab.dmi.unict.it/BCS/"
BCS_DATABASE_URL = f"{BCS_URL}/dataset.html"
IMAGES_DIRECTORY = "images"
SHAPES_DIRECTORY = "shapes"


def create_directories() -> None:
    path = os.path.join(PARENT_DIR, IMAGES_DIRECTORY)
    os.mkdir(path)

    path = os.path.join(PARENT_DIR, SHAPES_DIRECTORY)
    os.mkdir(path)


def crawler(url: str) -> None:
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    html_table_components = soup.findAll("table")

    print(f"Total {len(html_table_components)} tables found!")

    count = 0
    if len(html_table_components) != 0:
        for html_table_component in html_table_components:
            html_tr_components = html_table_component.findAll("tr")

            if len(html_tr_components) == 4:
                html_td_components = html_tr_components[0].findAll("td")

                image_link: str = html_td_components[0].find("a")["href"]
                shape_link: str = html_td_components[2].find("a")["href"]
                bcs_1: str = html_td_components[3].find("font").text
                bcs_2: str = html_td_components[4].find("font").text

                image_link = f"{BCS_URL}/{image_link}"
                shape_link = f"{BCS_URL}/{shape_link}"

                r = requests.get(image_link).content
                with open(f"{IMAGES_DIRECTORY}/image{count + 1}_bcs1_{bcs_1}_bcs2_{bcs_2}.jpg", "wb+") as f:
                    f.write(r)

                r = requests.get(shape_link).content
                with open(f"{SHAPES_DIRECTORY}/shape{count + 1}_bcs1_{bcs_1}_bcs2_{bcs_2}.txt", "wb+") as f:
                    f.write(r)

                count += 1

        print(f"Total images downloaded: {count}")


if __name__ == "__main__":
    create_directories()
    crawler(BCS_DATABASE_URL)
