import json
import os
import random
import time
from io import BytesIO

import requests
from PIL import Image
#########################################
from PIL import ImageFile
from PIL import UnidentifiedImageError
from bs4 import BeautifulSoup
from icecream import ic
from mkepub import Book

ImageFile.LOAD_TRUNCATED_IMAGES = True


# 解决 OSError: image file is truncated (66 bytes not processed)
########################################

def get_net_pic(pic_url):
    pic_headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    }
    try:
        response = requests.get(url=pic_url, headers=pic_headers)
        image = Image.open(BytesIO(response.content))
        # with open(image, 'rb') as image_data:
        b_img = BytesIO()
        image = image.convert("RGB")
        image.save(b_img, format='jpeg')
        image_data = b_img.getvalue()
        # ic()
    except UnidentifiedImageError:
        image_data = False  # 待填写
        ic("出错了")
    return image_data


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
                        if image_name != False:
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
    headers = {
        'accept-language': 'zh-CN,zh;q=0.9',
        'origin': 'https://www.zhihu.com',
        'content - encoding': 'br',
        # 'referer': 'https://www.zhihu.com/question/379350200',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        # 'cookie':
    }
    answer_urls = [
        # 'https://www.zhihu.com/question/394344003',
        # 'https://www.zhihu.com/question/434171293',
        # 'https://www.zhihu.com/question/292901966',
        # 'https://www.zhihu.com/question/415594509',
        # 'https://www.zhihu.com/question/26037846',
        # 'https://www.zhihu.com/question/384408291',
        # 'https://www.zhihu.com/question/263470102',
        # 'https://www.zhihu.com/question/377437284',
        # "https://www.zhihu.com/question/431601536",
        # "https://www.zhihu.com/question/21252555",
        # "https://www.zhihu.com/question/359009137",
        # 'https://www.zhihu.com/question/39167242',
        "https://www.zhihu.com/question/264213676"
    ]
    cookies_list = []
    with open('cookies.json', 'r', encoding='utf-8') as f:
        listCookies = json.loads(f.read())
    for cookie in listCookies:
        if cookie['name'] in ["zap", "d_c0", "d_c0", "l_cap_id", "r_cap_id", "cap_id", "captcha_session_v2",
                              "__snaker__id", "gdxidpyhxdE", "_9755xjdesxxd_", "captcha_ticket_v2", "z_c0", "tshl",
                              "q_c1", "Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49", "tst", "SESSIONID", "JOID", "osd",
                              "KLBRSID"]:
            cookies_list.append(cookie['name'] + "=" + cookie['value'])
    cookies = "; ".join(cookies_list)
    # ic(cookies)
    headers['cookie'] = cookies
    for answer_url in answer_urls:
        ic(answer_url)
        headers['referer'] = answer_url
        question_id = answer_url.split("question/")[-1]
        now = time.time()
        run_time = 300
        s = requests.session()
        first_url = "https://www.zhihu.com/api/v4/questions/{}/answers?include=data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics&limit=20&offset=0&sort_by=default".format(
            question_id)
        # for url in urls:
        #     time.sleep(random.randint(2, 3))
        with open('cookies.json', 'r', encoding='utf-8') as f:
            listCookies = json.loads(f.read())
        urls = [first_url]
        ic(s.get(url=urls[0], headers=headers))
        answers = s.get(url=urls[0], headers=headers).json()
        # ic(answers.json())
        try:
            epub_name = answers['data'][0]['question']['title']
        except (IndexError, KeyError):
            ic(answers)
            continue
        epub_book = Book(title=epub_name)
        count_pic = 0
        for url in urls:
            try:
                answers = s.get(url=url, headers=headers, ).json()
                ic()
                ic(time.sleep(random.randint(3, 10)))
                # ic(answers.json())
                # try:
                #     epub_name = answers['data'][0]['question']['title']
                # except (IndexError, KeyError):
                #     epub_name = "匿名用户"
                ic()
                for data in answers['data']:
                    answer_name = data['author']['name']
                    content = data['content']
                    # ic(content)
                    epub_book, count_pic = add_character(book=epub_book, content=content, answer_name=answer_name,
                                                    count_pic=count_pic)
                urls.append(answers['paging']['next'])
            except requests.exceptions.ConnectionError:
                pass
            if time.time() - now > run_time:
                # page_html = driver.page_source
                break
        try:
            epub_book.save(epub_name + ".epub")
        except FileExistsError:
            os.remove(epub_name + ".epub")
            epub_book.save(epub_name + ".epub")
        # print(answer_dict)
