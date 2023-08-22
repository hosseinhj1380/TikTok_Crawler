# from crawlling.connect_to_database import get_content,requests_model_search_tag,requests_model_explore,requests_model_search_username
import json

# from sqlalchemy.orm import sessionmaker
# from connect_to_database import engine
from post_crawler import Explore, Search
from selenium import webdriver
import time
from save_to_database import collection

import requests

CRAWLER_ID = 3
# Session = sessionmaker(bind=engine)
# session = Session()


# This function navigates to the TikTok login page and waits for 60 seconds. It's designed to allow the user to manually log in to TikTok.
def login(wd):
    wd.get("https://www.tiktok.com/en")
    time.sleep(60)


# This function fetches data from the "/explore" endpoint of the server, processes the data using the
# Explore
#  class, and saves the processed data to a MongoDB collection. It also sends a PUT request to the server to update the data.
def request_from_table_explore():
    def save_to_dataset(category, created_by, contents, task_handler_id):
        response = requests.post(
            "http://127.0.0.1:8000/explore/response/",
            json=[
                {
                    "crawler_id": CRAWLER_ID,
                    "task_handler_id": task_handler_id,
                    "category": category,
                    "created_by": created_by,
                    "content": contents,
                }
            ],
        )
        # print(response)

    response = requests.post(
        "http://127.0.0.1:8000/explore/task/", json={"crawler_id": CRAWLER_ID}
    )
    # print(response.json())
    #
    if response.status_code == 200:
        data = response.json()
    data = data[0]
    try:
        obj = Explore(
            category=data["category"],
            quantity=data["quantity"],
            created_by=data["created_by"],
            statistic=data["statistic"],
            comments=["comments"],
            description=data["description"],
        )
        obj.Select_Explore_Category(wd=wd)
        # if data['created_by']==True:
        #     result=obj.Select_content_by_creator(wd=wd)
        # else:
        result = obj.Select_content_by_count(wd=wd)

        save_to_dataset(
            category=data["category"],
            created_by=data["created_by"],
            contents=result,
            task_handler_id=data["task_handler_id"],
        )
    except Exception as e:
        print(f"error{e}")


# function fetches data from the "/search/tag" endpoint of the server, processes the data using the
# Search
#  class, and saves the processed data to a MongoDB collection. It also sends a PUT request to the server to update the data.
def request_from_table_search_tag():
    def save_to_dataset(title, contents, task_handler_id):
        response = requests.post(
            f"http://127.0.0.1:8000/search/tag/response/",
            json=[
                {
                    "crawler_id": CRAWLER_ID,
                    "task_handler_id": task_handler_id,
                    "title": title,
                    "content": contents,
                }
            ],
        )

    response = requests.post(
        "http://127.0.0.1:8000/search/tag/task/", json={"crawler_id": CRAWLER_ID}
    )
    if response.status_code == 200:
        data = response.json()
        if data is not None:
            try:
                obj = Search(
                    quantity=data["quantity"],
                    tag=data["title"],
                    statistic=data["statistic"],
                    comments=["comments"],
                    description=data["description"],
                )
                result = obj.search_with_tag(wd=wd)
                save_to_dataset(
                    data["title"], result, task_handler_id=data["task_handler_id"]
                )

            except Exception as e:
                print(f"error{e}")


# This function fetches data from the "/search/username" endpoint of the server, processes the data using the
# Search
#  class, and saves the processed data to a MongoDB collection. It also sends a PUT request to the server to update the data.
def request_from_table_search_username():
    def save_to_dataset(contents, task_handler_id, username):
        response = requests.post(
            "http://127.0.0.1:8000/search/username/response/",
            json=[
                {
                    "crawler_id": CRAWLER_ID,
                    "task_handler_id": task_handler_id,
                    "content": contents,
                    "username": username,
                }
            ],
        )
        # if response.status_code==200:
        # print(response.json())

    response = requests.post(
        "http://127.0.0.1:8000/search/username/task/", json={"crawler_id": CRAWLER_ID}
    )
    if response.status_code == 200:
        data = response.json()

    if data is not None:
        try:
            obj = Search(
                quantity=data["quantity"],
                username=data["username"],
                statistic=data["statistic"],
                comments=["comments"],
                description=data["description"],
            )
            result = obj.search_with_username(wd=wd)
            save_to_dataset(
                result,
                task_handler_id=data["task_handler_id"],
                username=data["username"],
            )

        except Exception as e:
            print(f"error{e}")


if __name__ == "__main__":
    wd = webdriver.Chrome()
    while True:
        request_from_table_explore()
        # request_from_table_search_tag()
        # request_from_table_search_username()
        time.sleep(10)

