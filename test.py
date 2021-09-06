import os
import time
from io import BytesIO

from mkepub import Book
import requests
import zhihu_oauth
# import zhihu_oauth.zhcls.people
from PIL import Image
from bs4 import BeautifulSoup
from icecream import ic
#########################################
from PIL import ImageFile
from PIL import UnidentifiedImageError

ImageFile.LOAD_TRUNCATED_IMAGES = True


# 解决 OSError: image file is truncated (66 bytes not processed)
########################################

def zhihu_login():
    client = zhihu_oauth.ZhihuClient()
    if not os.path.exists("load_token.txt"):
        try:
            client.login('ffghyhuvh.441564@qq.com', 'zpf@0601')
            # client.save_token("load_token.txt")
        except zhihu_oauth.NeedCaptchaException:
            with open('a.gif', 'wb') as f:
                f.write(client.get_captcha())
            captcha = input('please input captcha:')
            client.login('ffghyhuvh.441564@qq.com', 'zpf@0601', captcha)
        client.save_token("load_token.txt")
    else:
        client.load_token('load_token.txt')
    return client


def get_net_pic(pic_url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/69.0.3497.100 Safari/537.36',
    }
    try:
        response = requests.get(url=pic_url, headers=headers)
        image = Image.open(BytesIO(response.content))
        # with open(image, 'rb') as image_data:
        b_img = BytesIO()
        image = image.convert("RGB")
        image.save(b_img, format='jpeg')
        image_data = b_img.getvalue()
        # ic()
        return image_data
    except UnidentifiedImageError:
        # image_data = ""  # 待填写
        ic("出错了")
        return False
    # return image_data


def add_character(book, content, answer_name, count_pic):
    text = ""
    try:
        soup = BeautifulSoup(content, "lxml").html
        for i in soup:
            for j in i.children:
                if j.name == "p" and ("".join(j.stripped_strings)).replace(" ", "") != "":
                    # print(i)
                    text += str(j)
                if j.name == "figure":
                    # ic(j.img.name)
                    try:
                        count_pic += 1
                        image_name = str(count_pic).rjust(4, '0') + '.jpg'
                        image_data = get_net_pic(j.img.attrs['data-original'])
                        if image_data:
                            book.add_image(name=image_name, data=image_data)
                            text += '<img src="images/{}">'.format(image_name)
                    except (KeyError, UnboundLocalError):
                        pass
        book.add_page(title=answer_name, content=text)
        return book, count_pic
    except TypeError:
        return book, count_pic
        # pass


if __name__ == "__main__":
    zhihu_client = zhihu_login()
    zhihu_question = zhihu_client.question(394344003)
    epub_name = zhihu_question.title
    ic(epub_name)
    book = Book(title=epub_name)
    count = 0
    now = time.time()
    run_time = 300
    for answer in zhihu_question.answers:
        author_name = answer.author.name
        # ic(name)
        count += 1
        answer_content = answer.content
        add_character(book, answer_content, author_name, count)
        if time.time() - now > run_time:
            # page_html = driver.page_source
            break
        # book.add_page(title=author_name,content=)
        # print(content)
    try:
        book.save(epub_name + ".epub")
    except FileExistsError:
        os.remove(epub_name + ".epub")
        book.save(epub_name + ".epub")
