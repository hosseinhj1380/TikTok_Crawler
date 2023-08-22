import random
import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import os
import shutil

import re

"""
Code Documentation: TikTok Content Scraper
Overview
This script is designed to scrape TikTok content using the Selenium framework. 
It interacts with TikTok's web interface to retrieve various details about users, posts, and comments. 
The script defines classes for exploring content, including Explore, Search, and get_content.

"""
Source_download_folder = r"C:\Users\admin\Desktop\New folder (2)"
Destination_download_folder = r"C:\Users\admin\Desktop\TiktokDownload"


# wd=webdriver.Chrome()


class get_content(object):
    def __init__(
        self, statistic=False, comments=False, description=False, delay=3, tags=False
    ):
        # self.has_been_viewed_count=has_been_viewed_count
        self.comments = comments
        self.statistic = statistic
        self.description = description
        # self.wd=wd
        self.delay = delay
        self.tags = tags

    # Methods
    # get_Comments(): Retrieves comments and related information from a TikTok post.
    def get_Comments(self, wd):
        result = []
        time.sleep(3)
        bodies = []

        def mini_profile(bodies):
            element = bodies.find_element(By.CLASS_NAME, "e1g2efjf4")
            action = ActionChains(wd)
            action.move_to_element(element).perform()
            time.sleep(2)

            body = wd.find_element(By.CLASS_NAME, "er095112")
            nickname = body.find_element(By.CLASS_NAME, "er095115")
            try:
                bio = body.find_element(By.CLASS_NAME, "er0951110")
                bio = bio.text
            except:
                bio = ""
            numbers = body.find_elements(By.CLASS_NAME, "er095118")
            num = []
            for number in numbers:
                num.append(number.text)
            res = {
                "nickname": nickname.text,
                "bio": bio,
                "follower_numbers": self.change_str_static_to_int(num=num[0]),
                "likes_number": self.change_str_static_to_int(num=num[1]),
            }

            element = wd.find_element(By.CLASS_NAME, "e1aa9wve1")
            action.move_to_element(element).perform()

            return res

        def scroll_down():
            while True:
                long = len(bodies)
                # print("long=", long)
                time.sleep(2)
                bodies = wd.find_elements(By.CLASS_NAME, "eo72wou0")
                for body in bodies:
                    try:
                        while True:
                            subcomment = body.find_element(By.CLASS_NAME, "eo72wou4")

                            if subcomment is not None and "View " in subcomment.text:
                                subcomment.click()
                                time.sleep(1)
                            else:
                                break

                    except:
                        pass

                        # wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                tst = bodies[-1]
                tst.click()
                if len(bodies) == long:
                    break

        scroll_down()

        def download_comments(body, wd):
            res = []
            # body=body.find_element(By.CLASS_NAME, "e1g2efjf0")

            usernames = body.find_element(By.CLASS_NAME, "e1g2efjf3")
            likes_number = body.find_element(By.CLASS_NAME, "ezxoskx3")
            dates_commented = body.find_element(By.CLASS_NAME, "e1g2efjf8")
            comments = body.find_element(By.CLASS_NAME, "e1g2efjf6")
            min_prof = mini_profile(bodies=body)
            lst = {
                "comment": comments.text,
                "username": usernames.text,
                "like_number": likes_number.text,
                "date_commented": dates_commented.text,
                "mini_profile": min_prof,
            }
            res.append(lst)

            return res

        bodies = wd.find_elements(By.CLASS_NAME, "eo72wou0")
        for body in bodies:
            main = body.find_element(By.CLASS_NAME, "e1g2efjf0")
            main_comment = download_comments(main)
            try:
                sub = body.find_element(By.CLASS_NAME, "eo72wou1")

                if sub is not None:
                    res_sub_comm = []
                    subcomments = sub.find_elements(By.CLASS_NAME, "e1g2efjf0")
                    for subcomment in subcomments:
                        comm = download_comments(subcomment)
                        res_sub_comm.append(comm)
            except:
                res_sub_comm = []

            res = {"main_comment": main_comment, "sub_comment": res_sub_comm}

            result.append(res)

        return result

    # get_Username(): Retrieves the username associated with a TikTok post.

    def get_Username(self, wd):
        time.sleep(self.delay)
        element = wd.find_element(By.CLASS_NAME, "evv7pft1")

        return element.text

    # get_Description(): Retrieves the description of a TikTok post.

    def get_Description(self, wd):
        time.sleep(self.delay)
        element = wd.find_element(By.CLASS_NAME, "efbd9f0")
        return element.text

    # get_Tags(): Retrieves the tags associated with a TikTok post.

    def get_Tags(self, wd):
        time.sleep(self.delay)
        res = []
        elements1 = wd.find_element(
            By.CSS_SELECTOR, ".tiktok-1vrp1yb-DivContainer.ejg0rhn0"
        )

        elements = elements1.find_elements(By.CLASS_NAME, "ejg0rhn2")
        for element in elements:
            # if element is not None:
            res.append(element.text)

        res = [item for item in res if item is not None]
        return res

    # get_Statistic(): Retrieves the statistics (likes, saves, shares, comments) of a TikTok post.

    def get_Statistic(self, wd):
        time.sleep(self.delay)

        res = []
        time.sleep(self.delay)
        elements = wd.find_elements(
            By.CSS_SELECTOR, ".tiktok-1y8adbq-StrongText.e1hk3hf92"
        )
        comment = wd.find_element(By.CLASS_NAME, "e1aa9wve2")
        # Example string containing the comment count

        # Use regular expression to extract the number within parentheses
        number_match = re.search(r"\((\d+)\)", comment.text)

        # Check if a match is found
        if number_match:
            # Extract the number from the match object and convert it to an integer
            comment_count = int(number_match.group(1))

        for i, element in enumerate(elements):
            res.append(element.text)
            if i == 3:
                break
            result = {
                "likes_number": self.change_str_static_to_int(res[0]),
                "saved_number": self.change_str_static_to_int(res[1]),
                "shared_number": self.change_str_static_to_int(res[2]),
                "comments_number": comment_count,
            }
        return result

    # get_Download_video(): Downloads and renames a TikTok video.

    def get_Download_video(self, wd):
        def move_and_rename_file(
            source_folder, destination_folder, filename, new_filename
        ):
            # Build the absolute paths for source and destination files
            source_file_path = os.path.join(source_folder, filename)
            destination_file_path = os.path.join(destination_folder, new_filename)

            try:
                # Copy the file from the source folder to the destination folder
                shutil.move(source_file_path, destination_file_path)
                return "succes"
            except FileNotFoundError:
                print(f"File '{filename}' not found in '{source_folder}'.")
            except shutil.SameFileError:
                print(
                    f"Destination file '{new_filename}' already exists in '{destination_folder}'."
                )
            except Exception as e:
                print(f"An error occurred: {str(e)}")

        element = wd.find_element(By.CLASS_NAME, "e1yey0rl2")

        actions = ActionChains(wd)

        actions.context_click(element).perform()

        element = wd.find_element(By.CLASS_NAME, "e5bhsb13")
        if element.text == "Download video":
            element.click()
        while (
            os.path.exists(r"C:\Users\admin\Desktop\New folder (2)\download.mp4")
            == False
        ):
            time.sleep(2)

        source_folder = Source_download_folder
        destination_folder = Destination_download_folder
        filename = "download.mp4"  # Replace with the actual file name you want to copy
        new_filename = f"{random.randint(1,100)}.mp4"
        res = move_and_rename_file(
            source_folder, destination_folder, filename, new_filename
        )
        if res == "succes":
            return f"{destination_folder}\{new_filename}"

    # get_Link_video(): Retrieves the link to a TikTok video.

    def get_Link_video(self, wd):
        time.sleep(self.delay)
        element = wd.find_element(By.CLASS_NAME, "ehlq8k34")
        return element.text

    # scroll_down(): Scrolls down the page.

    def scroll_down(self, wd):
        side_element = wd.find_element(
            By.CSS_SELECTOR,
            ".tiktok-1s9jpf8-ButtonBasicButtonContainer-StyledVideoSwitch.e11s2kul12",
        )

        side_element.click()

    # get_current_url(): Retrieves the current URL.

    def get_current_url(self, wd):
        return wd.current_url

    # get_post_time(): Retrieves the post timestamp.

    def get_post_time(self, wd):
        def extract_something(input_string):
            separator = "\n·\n"
            parts = input_string.split(separator)
            if len(parts) == 2:
                return parts[1].strip()
            else:
                return None

        element = wd.find_element(By.CLASS_NAME, "evv7pft3")

        result = extract_something(element.text)

        return result

    # get_nickname(): Retrieves the user's nickname.

    def get_nickname(self, wd):
        def extract_something(input_string):
            separator = "\n·\n"
            parts = input_string.split(separator)
            if len(parts) == 2:
                return parts[0].strip()
            else:
                return None

        element = wd.find_element(By.CLASS_NAME, "evv7pft3")

        result = extract_something(element.text)

        return result

    # change_str_static_to_int(num=None): Converts abbreviated numbers to integers.

    def change_str_static_to_int(self, num=None):
        if "K" in num:
            suffix_index = num.find("K")
            number_str = num[:suffix_index]
            number = float(number_str)

            return number * 1000
        elif "M" in num:
            suffix_index = num.find("M")
            number_str = num[:suffix_index]
            number = float(number_str)
            return number * 1000000
        else:
            return num

    # mini_profile_info(): Retrieves mini profile information.

    def mini_profile_info(self, wd):
        element = wd.find_element(By.CLASS_NAME, "evv7pft1")
        action = ActionChains(wd)
        action.move_to_element(element).perform()
        body = wd.find_element(By.CLASS_NAME, "er095111")
        nickname = body.find_element(By.CLASS_NAME, "er095115")
        bio = body.find_element(By.CLASS_NAME, "er0951110")
        numbers = body.find_elements(By.CLASS_NAME, "er095118")
        num = []
        for number in numbers:
            num.append(number.text)
        result = {
            "nickname": nickname.text,
            "bio": bio.text,
            "follower_numbers": self.change_str_static_to_int(num=num[0]),
            "likes_number": self.change_str_static_to_int(num=num[1]),
        }
        return result


class Explore(get_content):
    def __init__(
        self,
        category="Dance and Music",
        quantity=0,
        created_by=None,
        statistic=False,
        comments=False,
        description=False,
        delay=3,
        tags=False,
    ):
        self.category = category
        self.quantity = quantity
        # self.view_count_at_least=view_count_at_least
        self.created_by = created_by
        # self.delay=delay
        get_content.__init__(
            self,
            statistic=statistic,
            comments=comments,
            description=description,
            delay=delay,
            tags=tags,
        )

    # Select_Explore_Category(wd): Selects an explore category using a web driver.

    def Select_Explore_Category(self, wd):
        wd.get("https://tiktok.com/explore")
        time.sleep(7)
        elements = wd.find_elements(By.CLASS_NAME, "e13i6o243")

        for element in elements:
            if element.text == self.category:
                element.click()
                break

        time.sleep(7)
        element = wd.find_element(By.CLASS_NAME, "e1yey0rl0")

        element.click()

        time.sleep(5)

    # Select_content_by_count(wd): Selects content by count and retrieves details.

    def Select_content_by_count(self, wd):
        result = []
        if self.quantity == 0:
            return None
        else:
            for i in range(self.quantity):
                if self.statistic == True:
                    statistic = self.get_Statistic(wd)
                if self.description == True:
                    description = self.get_Description(wd)
                if self.comments == True:
                    comments = self.get_Comments(wd)
                if self.tags == True:
                    tags = self.get_Tags(wd)

                username = self.get_Username(wd)
                link = self.get_Link_video(wd)
                post_date = self.get_post_time(wd)
                video_url = self.get_Download_video(wd)

                res = {
                    "username": username,
                    "link": link,
                    "statistic": statistic,
                    "tags": tags,
                    "description": description,
                    "comments": comments,
                    "post_date": post_date,
                    "video_url": video_url
                    # "video_url": video_url
                }
                result.append(res)
                print(i)

                self.scroll_down()

        return result

    # Select_content_by_creator(wd): Selects content by creator and retrieves details.

    def Select_content_by_creator(self, wd):
        result = []
        if self.quantity == 0:
            return None
        else:
            for i in range(self.quantity):
                username = self.get_Username()
                if username == self.created_by:
                    if self.statistic == True:
                        statistic = self.get_Statistic()
                    if self.description == True:
                        description = self.get_Description()
                    if self.comments == True:
                        comments = self.get_Comments()
                    if self.tags == True:
                        tags = self.get_Tags()

                    username = self.get_Username()
                    link = self.get_Link_video()
                    post_date = self.get_post_time()

                    video_url = self.get_Download_video()

                    res = {
                        "username": username,
                        "link": link,
                        "statistic": statistic,
                        "tags": tags,
                        "description": description,
                        "comments": comments,
                        "post_date": post_date,
                        "video_url": video_url
                        # "video_url": video_url
                    }
                    result.append(res)

                self.scroll_down()

        return result


class Search(get_content):
    def __init__(
        self,
        quantity=0,
        tag=None,
        username=None,
        tags=False,
        delay=3,
        description=False,
        comments=False,
        statistic=False,
    ):
        self.tag = tag
        self.username = username
        self.quantity = quantity
        get_content.__init__(
            self,
            statistic=statistic,
            comments=comments,
            description=description,
            delay=delay,
            tags=tags,
        )

    # search_with_tag(wd): Searches for content using a specified tag.

    def search_with_tag(self, wd):
        wd.get(f"https://www.tiktok.com/search?q={self.tag}")
        time.sleep(10)
        element = wd.find_element(
            By.CSS_SELECTOR, ".tiktok-1jxhpnd-DivContainer.e1yey0rl0"
        )
        element.click()
        time.sleep(3)

        result = []
        if self.quantity == 0:
            return None
        else:
            for i in range(self.quantity):
                if self.statistic == True:
                    statistic = self.get_Statistic(wd)
                if self.description == True:
                    description = self.get_Description(wd)
                if self.comments == True:
                    comments = self.get_Comments(wd)
                if self.tags == True:
                    tags = self.get_Tags(wd)

                username = self.get_Username(wd)
                link = self.get_Link_video(wd)
                post_date = self.get_post_time(wd)
                video_url = self.get_Download_video(wd)

                res = {
                    "username": username,
                    "link": link,
                    "statistic": statistic,
                    "tags": tags,
                    "description": description,
                    "comments": comments,
                    "post_date": post_date,
                    "video_url": video_url
                    # "video_url": video_url
                }
                result.append(res)
                # print(i)

                self.scroll_down()

            return result

    # search_with_username(wd): Searches for content associated with a username.

    def search_with_username(self, wd):
        wd.get(f"https://www.tiktok.com/@{self.username}")
        time.sleep(20)

        page_statistic = []

        elements = wd.find_elements(
            By.CSS_SELECTOR, ".tiktok-rxe1eo-DivNumber.e1457k4r1"
        )

        for element in elements:
            page_statistic.append(element.text)

        element1 = wd.find_element(By.CLASS_NAME, "e1457k4r3")
        bio = element1.text

        element = wd.find_element(
            By.CSS_SELECTOR, ".tiktok-1jxhpnd-DivContainer.e1yey0rl0"
        )
        element.click()
        time.sleep(5)
        element = wd.find_element(
            By.CSS_SELECTOR, ".tiktok-1jxhpnd-DivContainer.e1yey0rl0"
        )
        element.click()
        time.sleep(10)

        result = []
        if self.quantity == 0:
            return None
        else:
            for i in range(self.quantity):
                if self.statistic == True:
                    statistic = self.get_Statistic(wd)
                if self.description == True:
                    description = self.get_Description(wd)
                if self.comments == True:
                    comments = self.get_Comments(wd)
                if self.tags == True:
                    tags = self.get_Tags(wd)

                username = self.get_Username(wd)
                link = self.get_Link_video(wd)
                post_date = self.get_post_time(wd)
                video_url = self.get_Download_video(wd)

                res = {
                    "username": username,
                    "link": link,
                    "statistic": statistic,
                    "tags": tags,
                    "description": description,
                    "comments": comments,
                    "post_date": post_date,
                    "video_url": video_url,
                }
                result.append(res)
                # print(i)

                self.scroll_down()

            return [page_statistic, bio, result]

    # search_top_accounts(wd): Searches for top user accounts.

    def search_top_accounts(
        self,
        wd,
    ):
        wd.get(f"https://www.tiktok.com/search/user?q={self.username}")

        time.sleep(10)
        elements = wd.find_elements(By.CLASS_NAME, "e10wilco4")
        follower_numbers_element = wd.find_elements(By.CLASS_NAME, "e10wilco5")

        # Use regular expression to find the desired pattern
        i = 0

        result = []
        for element, follower_numbers in zip(elements, follower_numbers_element):
            if i < 10:
                match = re.search(r"\d+\.\d+[KMBT]?", follower_numbers.text)

                if match:
                    follower_number = match.group()
                    number = self.change_str_static_to_int(num=follower_number)

                    res = {"username": element.text, "follower_number": number}
                    result.append(res)
            i += 1

        return result

    # login(): Simulates a login action.

    def login(self):
        wd.get("https://www.tiktok.com/en")

        time.sleep(20)


# if __name__=="__main__":

# obj=Search(username="ronaldo")
# obj.login()
# result=obj.search_top_accounts(wd=wd)
# print(result)


# wd=webdriver.Chrome()
# time.sleep(10)
