import json
import os
import random
import time

from PIL import UnidentifiedImageError
import requests
from bs4 import BeautifulSoup
from mkepub import Book
from icecream import ic
from PIL import Image
from io import BytesIO
import lxml
#########################################
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True


# 解决 OSError: image file is truncated (66 bytes not processed)
########################################

def get_net_pic(pic_url):
    headers = {
        # 'accept-language': 'zh-CN,zh;q=0.9',
        # 'origin': 'https://www.zhihu.com',
        # 'referer': 'https://www.zhihu.com/question/268384579',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        # 'cookie': 'zap=f8e91f1b-2e3c-4b5a-b132-2b76f76e7fce; d_c0="AIDeBJZhoxOPTuqG3J8r0F_7DRqR9raab2M=|1630161840"; _xsrf=KOm3yZylNRPuWTSBZv4vfRT0G9sLjPGJ; l_cap_id="YjQ0M2RmMTQ2YzRkNDY3MTg1MmYzZjZhNWI5MThmOTA=|1630198419|0d1f8a4e56ae4cacae597f1977cf452b4971499d"; r_cap_id="NzA5NWIzOTFkYzBjNDBmZGJlOTMzMDBhNDNmY2ExYTg=|1630198419|cdde276ff6f76eb4c4de2d006e8eb8903031c719"; cap_id="YjIzMTczOGY3ZGUzNDA0Mzk5YTBmNmM3MGQ5OTcwNDk=|1630198419|74f4fa5bad42c4f9626ab6425008470b94263abb"; captcha_session_v2="2|1:0|10:1630198424|18:captcha_session_v2|88:bmN5RlpNUWVXK1dGbmFwMnE1N3BKS21CcTBtNkdvb21PU0lDZForRUtDUm5sTkErYS8xYlYyWkRaOXc2c3NZcA==|87076d3439ace7bb499fae7bb6e96ec846af7c612227ad0311c0837ae4e9a4f0"; __snaker__id=vaTTUPkkjz3YYGqS; gdxidpyhxdE=RPv0j9rxeXdmd3b9EesgLDKYTZB%2FD2MscO9yXuX52ePcCGkynOrkSOd1MghhX2d1lyrSBNRbLq3GqnEtBeq3jYq4lqApsBLkutXqo9cfkJt%2B3QIqMH5iTOSOHt8a%2BveK4U%2Fdm0e%2BNtVBZ%5CWOaeGjSpWtVLIVpc%2BNt3sai%2Fd0w5a92rUN%3A1630228132245; _9755xjdesxxd_=32; captcha_ticket_v2="2|1:0|10:1630198437|17:captcha_ticket_v2|704:eyJ2YWxpZGF0ZSI6IkNOMzFfbjJtc29mUm5JMXp2WWJIeUJGWjc2LmhhMHRIVFN1SnpBYS1oZEgydEpKaEVxeERScmpXZXJPTFNsSUh4NHh1a1g0UGFXOTF1ZVFqckhJWTA3TGhUZWtuUUliV1dTTVdveTZSZUl6TV9xUmd1Sm91UEhmR2I1eHVBZEpSekY1cHRTZUNFRjZCS0xuYVJLQ3ZsbFowT1gtMENSeEw4bnQxS0ctMm5CZDJtNFV1X3VNei5EZndTLTVNb2YtVUkxbmZzdWtUZkp5NXhwMEJEb0JDUFhSNFM0ZFhrU1ZaQVVldk1jUjFhaDl1SDZMaUh5Mk4tUXZuaFFPYUpJaS1wVkRnZzI2dUpoZC5WUlRvaHoxT2JYcTFKN3BGVnF1emJNTU93S004X2tPcmhUdDVETUZhTFVLYmpDOV9EWFJROV9aYTRGYUZhNEE0U3kua3FZWWZ6MDlhdm8tVHFCRDY3d2R0T2oyZ1ZFUzR3UFJNb0g1X0w1d3VoLUN4Sk5QVkxPZmhxVzUyOU5VT3pSdjEtOW1mS1FSaEkyVHVMSHpKX1ZheEhYczdfLl9aZng3eWhSem1SdW1Tc21RajIyZmFiVWVBT25feUo4ZGxiSU9jSkE0YWxnRkw2eHpxSHZ3VERhX0F4R2o4RTZ3UHFIX1RocERpeG05WUU2YVZnOTBYMyJ9|9b4972d4fed16bae1eec5a3f9da050a15b9d95fb729b096f08a659124e46d393"; z_c0="2|1:0|10:1630198437|4:z_c0|92:Mi4xZF9JckVBQUFBQUFBZ040RWxtR2pFeVlBQUFCZ0FsVk5wU2dZWWdCRXpUNjl5VmhXajQ1T01CZERWT1luYUlRQ01n|7ba608df89feedfcfdcf4477207f3eff46fdbb27903605b14e23522ea6426c36"; tshl=; q_c1=3565ebec9aa848d8821650ff5d26ef2f|1630668010000|1630668010000; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1630755589,1630755611,1630755693,1630760322; tst=r; SESSIONID=h6hfPC0SOCs4N2xdZlgFVNUiVwLuueqzhWPGk61eSE8; JOID=WlAVBEu5zPMuSY_sALb0pGTQ4Ucb0fKcTxHM1FT-j4gdALWUbJ7lx0BBh-MAf4lHg10vDgOeUwJkmdVsuCp71Oo=; osd=UV0VAkiywfMoSoThALD3r2nQ50QQ3PKaTBrB1FL9hIUdBrafYZ7jxEtMh-UDdIRHhV4kAwOYUAlpmdNvsyd70uk=; KLBRSID=4843ceb2c0de43091e0ff7c22eadca8c|1630807646|1630806301'
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
    except UnidentifiedImageError:
        # image_data = ""  # 待填写
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
        # 'referer': 'https://www.zhihu.com/question/379350200',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        # 'cookie': 'zap=f8e91f1b-2e3c-4b5a-b132-2b76f76e7fce; d_c0="AIDeBJZhoxOPTuqG3J8r0F_7DRqR9raab2M=|1630161840"; d_c0=KOm3yZylNRPuWTSBZv4vfRT0G9sLjPGJ; l_cap_id="YjQ0M2RmMTQ2YzRkNDY3MTg1MmYzZjZhNWI5MThmOTA=|1630198419|0d1f8a4e56ae4cacae597f1977cf452b4971499d"; r_cap_id="NzA5NWIzOTFkYzBjNDBmZGJlOTMzMDBhNDNmY2ExYTg=|1630198419|cdde276ff6f76eb4c4de2d006e8eb8903031c719"; cap_id="YjIzMTczOGY3ZGUzNDA0Mzk5YTBmNmM3MGQ5OTcwNDk=|1630198419|74f4fa5bad42c4f9626ab6425008470b94263abb"; captcha_session_v2="2|1:0|10:1630198424|18:captcha_session_v2|88:bmN5RlpNUWVXK1dGbmFwMnE1N3BKS21CcTBtNkdvb21PU0lDZForRUtDUm5sTkErYS8xYlYyWkRaOXc2c3NZcA==|87076d3439ace7bb499fae7bb6e96ec846af7c612227ad0311c0837ae4e9a4f0"; __snaker__id=vaTTUPkkjz3YYGqS; gdxidpyhxdE=RPv0j9rxeXdmd3b9EesgLDKYTZB%2FD2MscO9yXuX52ePcCGkynOrkSOd1MghhX2d1lyrSBNRbLq3GqnEtBeq3jYq4lqApsBLkutXqo9cfkJt%2B3QIqMH5iTOSOHt8a%2BveK4U%2Fdm0e%2BNtVBZ%5CWOaeGjSpWtVLIVpc%2BNt3sai%2Fd0w5a92rUN%3A1630228132245; _9755xjdesxxd_=32; captcha_ticket_v2="2|1:0|10:1630198437|17:captcha_ticket_v2|704:eyJ2YWxpZGF0ZSI6IkNOMzFfbjJtc29mUm5JMXp2WWJIeUJGWjc2LmhhMHRIVFN1SnpBYS1oZEgydEpKaEVxeERScmpXZXJPTFNsSUh4NHh1a1g0UGFXOTF1ZVFqckhJWTA3TGhUZWtuUUliV1dTTVdveTZSZUl6TV9xUmd1Sm91UEhmR2I1eHVBZEpSekY1cHRTZUNFRjZCS0xuYVJLQ3ZsbFowT1gtMENSeEw4bnQxS0ctMm5CZDJtNFV1X3VNei5EZndTLTVNb2YtVUkxbmZzdWtUZkp5NXhwMEJEb0JDUFhSNFM0ZFhrU1ZaQVVldk1jUjFhaDl1SDZMaUh5Mk4tUXZuaFFPYUpJaS1wVkRnZzI2dUpoZC5WUlRvaHoxT2JYcTFKN3BGVnF1emJNTU93S004X2tPcmhUdDVETUZhTFVLYmpDOV9EWFJROV9aYTRGYUZhNEE0U3kua3FZWWZ6MDlhdm8tVHFCRDY3d2R0T2oyZ1ZFUzR3UFJNb0g1X0w1d3VoLUN4Sk5QVkxPZmhxVzUyOU5VT3pSdjEtOW1mS1FSaEkyVHVMSHpKX1ZheEhYczdfLl9aZng3eWhSem1SdW1Tc21RajIyZmFiVWVBT25feUo4ZGxiSU9jSkE0YWxnRkw2eHpxSHZ3VERhX0F4R2o4RTZ3UHFIX1RocERpeG05WUU2YVZnOTBYMyJ9|9b4972d4fed16bae1eec5a3f9da050a15b9d95fb729b096f08a659124e46d393"; z_c0="2|1:0|10:1630198437|4:z_c0|92:Mi4xZF9JckVBQUFBQUFBZ040RWxtR2pFeVlBQUFCZ0FsVk5wU2dZWWdCRXpUNjl5VmhXajQ1T01CZERWT1luYUlRQ01n|7ba608df89feedfcfdcf4477207f3eff46fdbb27903605b14e23522ea6426c36"; tshl=; q_c1=3565ebec9aa848d8821650ff5d26ef2f|1630668010000|1630668010000; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1630755589,1630755611,1630755693,1630760322; tst=r; SESSIONID=h6hfPC0SOCs4N2xdZlgFVNUiVwLuueqzhWPGk61eSE8; JOID=WlAVBEu5zPMuSY_sALb0pGTQ4Ucb0fKcTxHM1FT-j4gdALWUbJ7lx0BBh-MAf4lHg10vDgOeUwJkmdVsuCp71Oo=; osd=UV0VAkiywfMoSoThALD3r2nQ50QQ3PKaTBrB1FL9hIUdBrafYZ7jxEtMh-UDdIRHhV4kAwOYUAlpmdNvsyd70uk=; KLBRSID=4843ceb2c0de43091e0ff7c22eadca8c|1630807646|1630806301'
    }
    answer_urls = [
        'https://www.zhihu.com/question/394344003',
        'https://www.zhihu.com/question/434171293',
        'https://www.zhihu.com/question/292901966',
        'https://www.zhihu.com/question/415594509',
        'https://www.zhihu.com/question/26037846',
        'https://www.zhihu.com/question/384408291',
        'https://www.zhihu.com/question/263470102',
        'https://www.zhihu.com/question/377437284',
        "https://www.zhihu.com/question/431601536",
        "https://www.zhihu.com/question/21252555",
        "https://www.zhihu.com/question/359009137",
        'https://www.zhihu.com/question/39167242',
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
            # browser.add_cookie({
            #     'domain': cookie['domain'],
            #     'name': cookie['name'],
            #     'value': cookie['value'],
            #     'path': cookie['path'],
            #     # 'expiry': cookie['expiry'],
            #     'httpOnly': cookie['httpOnly'],
            #     'secure': cookie['secure']
            # })
    cookies = "; ".join(cookies_list)
    # ic(cookies)
    headers['cookie'] = cookies
    for answer_url in answer_urls:
        headers['referer'] = answer_url
        question_id = answer_url.split("question/")[-1]
        now = time.time()
        run_time = 300
        s = requests.session()
        first_url = "https://www.zhihu.com/api/v4/questions/{}/answers?include=data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics&limit=20&offset=0&sort_by=default".format(question_id)
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
        book = Book(title=epub_name)
        count_pic = 0
        for url in urls:
            answers = s.get(url=url, headers=headers, ).json()
            time.sleep(random.randint(3, 10))
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
                book, count_pic = add_character(book=book, content=content, answer_name=answer_name,
                                                count_pic=count_pic)
            urls.append(answers['paging']['next'])
            if time.time() - now > run_time:
                # page_html = driver.page_source
                break
        try:
            book.save(epub_name + ".epub")
        except FileExistsError:
            os.remove(epub_name + ".epub")
            book.save(epub_name + ".epub")
        # print(answer_dict)
