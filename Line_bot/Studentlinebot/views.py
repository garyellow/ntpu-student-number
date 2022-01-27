# Create your views here.
import random
import time

import requests
from bs4 import BeautifulSoup as BS4
from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from fake_useragent import UserAgent
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

D = {
    "712": "法律", "714": "法律", "716": "法律",
    "72": "公行",
    "73": "經濟",
    "74": "社會", "742": "社工", "744": "社學",
    "75": "財政",
    "76": "不動",
    "77": "會計",
    "78": "統計",
    "79": "企管",
    "80": "金融",
    "81": "中文",
    "82": "應外",
    "83": "歷史",
    "84": "休運",
    "85": "資工",
    "86": "通訊",
    "87": "電機"
}

G = {
    "712": "法學",
    "714": "司法",
    "716": "財法",
}

limit = 1000
DN = [""] * limit
all_text = [""] * limit
group_opening = [False] * limit
group_searching = [False] * limit
group_signature = [""] * limit
group_check = [False] * limit


@csrf_exempt
def callback(request):
    global DN
    global all_text
    global group_opening
    global group_signature
    global group_check

    if request.method == "POST":
        message = []

        signature = request.META["HTTP_X_LINE_SIGNATURE"]
        body = request.body.decode("utf-8")

        message.append(TextSendMessage(text=str(body)))

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                if event.message.text == "查詢個人" or event.message.text == "查詢全系" or event.message.text == "文法商" \
                        or event.message.text == "公社電資" or event.message.text == "人文學院" \
                        or event.message.text == "法律學院" or event.message.text == "商學院" \
                        or event.message.text == "公共事務學院" or event.message.text == "社會科學學院" \
                        or event.message.text == "電機資訊學院" or event.message.text == "中國文學系" \
                        or event.message.text == "應用外語學系" or event.message.text == "歷史學系" \
                        or event.message.text == "法學組" or event.message.text == "司法組" \
                        or event.message.text == "財法組" or event.message.text == "企業管理學系" \
                        or event.message.text == "金融與合作經濟學系" or event.message.text == "會計學系" \
                        or event.message.text == "統計學系" or event.message.text == "公共行政暨政策學系" \
                        or event.message.text == "不動產與城鄉環境學系" or event.message.text == "財政學系" \
                        or event.message.text == "經濟學系" or event.message.text == "社會學系" \
                        or event.message.text == "社會工作學系" or event.message.text == "電機工程學系" \
                        or event.message.text == "資訊工程學系" or event.message.text == "通訊工程學系":
                    continue
                elif event.message.text.isdecimal() and (
                        event.message.text[0] == "4" or event.message.text[0] == "3" or event.message.text[0] == "7"):
                    number = event.message.text

                    ua = UserAgent()
                    header_seed = ua.random
                    header = {"user-agent": header_seed}

                    url = "http://lms.ntpu.edu.tw/portfolio/search.php?fmScope=2&fmKeyword=" + number
                    web = requests.get(url, headers=header)
                    web.encoding = "utf-8"

                    html = BS4(web.text, "html.parser")
                    name = html.find("div", {"class": "bloglistTitle"})

                    try:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text=number + "  " + name.text))
                    except AttributeError:
                        line_bot_api.reply_message(
                            event.reply_token, TextSendMessage(text="學號" + number + "不存在\n請重新輸入學號"))

                elif event.message.text.isdecimal() and 0 < int(event.message.text) < 3000:
                    i_d = 0
                    while group_signature[i_d] != event.source.user_id:
                        i_d += 1

                    group_searching[i_d] = True

                    line_bot_api.reply_message(
                        event.reply_token, TemplateSendMessage(
                            alt_text="查詢中，請稍後",
                            template=ButtonsTemplate(
                                title="查詢中，請稍後",
                                text="總查詢時間約為1~2分鐘",
                                actions=[
                                    PostbackAction(
                                        label="查看查詢結果",
                                        data="D查看查詢結果"
                                    )
                                ]
                            )
                        )
                    )

                    if int(event.message.text) > 1911:
                        year = str(int(event.message.text) - 1911)
                    else:
                        year = event.message.text

                    dpm = '4' + "{:0>3d}".format(int(year)) + DN[i_d]

                    ua = UserAgent()
                    header_seed = ua.random
                    header = {"user-agent": header_seed}

                    all_text[i_d] = ""

                    for i in range(1, 999):
                        if int(DN[i_d]) <= 99:
                            student_number = dpm + "{:0>3d}".format(i)
                        else:
                            student_number = dpm + "{:0>2d}".format(i)

                        url = "http://lms.ntpu.edu.tw/portfolio/search.php?fmScope=2&fmKeyword=" + student_number

                        try:
                            web = requests.get(url, headers=header)
                            web.encoding = 'utf-8'

                            html = BS4(web.text, 'html.parser')
                            name = html.find('div', {'class': 'bloglistTitle'})

                            all_text[i_d] += student_number + "  " + name.text + "\n"
                        except requests.exceptions.ConnectionError:
                            group_check[i_d] = True
                        except AttributeError:
                            if DN[i_d] != "712" and DN[i_d] != "714" and DN[i_d] != "716":
                                all_text[i_d] += year + '學年度' + D[DN[i_d]] + '系共有' + str(i - 1) + '名學生'
                            else:
                                all_text[i_d] += year + '學年度' + D[DN[i_d]] + '系' + G[DN[i_d]] + '組共有' + str(
                                    i - 1) + '名學生'

                            all_text[i_d] += "\n\n查詢資料僅供參考\n會因為各種因素而變動\n資料來源為北大數位學苑2.0"

                            break

                        time.sleep(random.uniform(0.1, 0.5))

                    group_searching[i_d] = False

                else:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text="選擇模式",
                            template=ButtonsTemplate(
                                thumbnail_image_url="https://new.ntpu.edu.tw/assets/logo/ntpu_logo.png",
                                title="使用學號查訊姓名",
                                text="請選擇查詢模式",
                                actions=[
                                    PostbackAction(
                                        label="查詢個人",
                                        text="查詢個人",
                                        data="A查詢個人"
                                    ),
                                    PostbackAction(
                                        label="查詢全系",
                                        text="查詢全系",
                                        data="A查詢全系"
                                    )
                                ]
                            )
                        )
                    )

            elif isinstance(event, PostbackEvent):
                if event.postback.data[0] == "A":
                    mode = event.postback.data[1:]

                    if mode == "查詢個人":
                        line_bot_api.reply_message(
                            event.reply_token, TextSendMessage(text="請輸入完整學號"))

                    if mode == "查詢全系":
                        line_bot_api.reply_message(
                            event.reply_token,
                            TemplateSendMessage(
                                alt_text="選擇學院群",
                                template=ButtonsTemplate(
                                    # thumbnail_image_url="https://new.ntpu.edu.tw/assets/logo/ntpu_logo.png",
                                    title="選擇學院群",
                                    text="請選擇科系所屬學院群",
                                    actions=[
                                        PostbackAction(
                                            label="文法商",
                                            text="文法商",
                                            data="B文法商"
                                        ),
                                        PostbackAction(
                                            label="公社電資",
                                            text="公社電資",
                                            data="B公社電資"
                                        )
                                    ]
                                )
                            )
                        )

                elif event.postback.data[0] == "B":
                    dpm_s = event.postback.data[1:]

                    if dpm_s == "文法商":
                        line_bot_api.reply_message(
                            event.reply_token,
                            TemplateSendMessage(
                                alt_text="選擇學院",
                                template=ButtonsTemplate(
                                    # thumbnail_image_url="https://new.ntpu.edu.tw/assets/logo/ntpu_logo.png",
                                    title="選擇學院",
                                    text="請選擇科系所屬學院",
                                    actions=[
                                        PostbackAction(
                                            label="人文學院",
                                            text="人文學院",
                                            data="C人文學院"
                                        ),
                                        PostbackAction(
                                            label="法律學院",
                                            text="法律學院",
                                            data="C法律學院"
                                        ),
                                        PostbackAction(
                                            label="商學院",
                                            text="商學院",
                                            data="C商學院"
                                        )
                                    ]
                                )
                            )
                        )

                    if dpm_s == "公社電資":
                        line_bot_api.reply_message(
                            event.reply_token,
                            TemplateSendMessage(
                                alt_text="選擇學院",
                                template=ButtonsTemplate(
                                    # thumbnail_image_url="https://new.ntpu.edu.tw/assets/logo/ntpu_logo.png",
                                    title="選擇學院",
                                    text="請選擇科系所屬學院",
                                    actions=[
                                        PostbackAction(
                                            label="公共事務學院",
                                            text="公共事務學院",
                                            data="C公共事務學院"
                                        ),
                                        PostbackAction(
                                            label="社會科學學院",
                                            text="社會科學學院",
                                            data="C社會科學學院"
                                        ),
                                        PostbackAction(
                                            label="電機資訊學院",
                                            text="電機資訊學院",
                                            data="C電機資訊學院"
                                        )
                                    ]
                                )
                            )
                        )

                elif event.postback.data[0] == "C":
                    dpm = event.postback.data[1:]

                    if dpm == "人文學院":
                        line_bot_api.reply_message(
                            event.reply_token,
                            TemplateSendMessage(
                                alt_text="選擇科系",
                                template=ButtonsTemplate(
                                    thumbnail_image_url="https://walkinto.in/upload/-192z7YDP8-JlchfXtDvI.JPG",
                                    title="選擇科系",
                                    text="請選擇科系",
                                    actions=[
                                        PostbackAction(
                                            label="中國文學系",
                                            text="中國文學系",
                                            data="81"
                                        ),
                                        PostbackAction(
                                            label="應用外語學系",
                                            text="應用外語學系",
                                            data="82"
                                        ),
                                        PostbackAction(
                                            label="歷史學系",
                                            text="歷史學系",
                                            data="83"
                                        )
                                    ]
                                )
                            )
                        )

                    if dpm == "法律學院":
                        line_bot_api.reply_message(
                            event.reply_token,
                            TemplateSendMessage(
                                alt_text="選擇組別",
                                template=ButtonsTemplate(
                                    thumbnail_image_url="https://walkinto.in/upload/byupdk9PvIZyxupOy9Dw8.JPG",
                                    title="選擇組別",
                                    text="請選擇組別",
                                    actions=[
                                        PostbackAction(
                                            label="法學組",
                                            text="法學組",
                                            data="712"
                                        ),
                                        PostbackAction(
                                            label="司法組",
                                            text="司法組",
                                            data="714"
                                        ),
                                        PostbackAction(
                                            label="財法祖",
                                            text="財法祖",
                                            data="716"
                                        )
                                    ]
                                )
                            )
                        )

                    if dpm == "商學院":
                        line_bot_api.reply_message(
                            event.reply_token,
                            TemplateSendMessage(
                                alt_text="選擇科系",
                                template=ButtonsTemplate(
                                    thumbnail_image_url="https://walkinto.in/upload/ZJum7EYwPUZkedmXNtvPL.JPG",
                                    title="選擇科系",
                                    text="請選擇科系",
                                    actions=[
                                        PostbackAction(
                                            label="企業管理學系",
                                            text="企業管理學系",
                                            data="79"
                                        ),
                                        PostbackAction(
                                            label="金融與合作經濟學系",
                                            text="金融與合作經濟學系",
                                            data="80"
                                        ),
                                        PostbackAction(
                                            label="會計學系",
                                            text="會計學系",
                                            data="77"
                                        ),
                                        PostbackAction(
                                            label="統計學系",
                                            text="統計學系",
                                            data="78"
                                        )
                                    ]
                                )
                            )
                        )

                    if dpm == "公共事務學院":
                        line_bot_api.reply_message(
                            event.reply_token,
                            TemplateSendMessage(
                                alt_text="選擇科系",
                                template=ButtonsTemplate(
                                    thumbnail_image_url="https://walkinto.in/upload/ZJhs4wEaDIWklhiVwV6DI.jpg",
                                    title="選擇科系",
                                    text="請選擇科系",
                                    actions=[
                                        PostbackAction(
                                            label="公共行政暨政策學系",
                                            text="公共行政暨政策學系",
                                            data="72"
                                        ),
                                        PostbackAction(
                                            label="不動產與城鄉環境學系",
                                            text="不動產與城鄉環境學系",
                                            data="76"
                                        ),
                                        PostbackAction(
                                            label="財政學系",
                                            text="財政學系",
                                            data="75"
                                        )
                                    ]
                                )
                            )
                        )

                    if dpm == "社會科學學院":
                        line_bot_api.reply_message(
                            event.reply_token,
                            TemplateSendMessage(
                                alt_text="選擇科系",
                                template=ButtonsTemplate(
                                    thumbnail_image_url="https://walkinto.in/upload/WyPbshN6DIZ1gvZo2NTvU.JPG",
                                    title="選擇科系",
                                    text="請選擇科系",
                                    actions=[
                                        PostbackAction(
                                            label="經濟學系",
                                            text="經濟學系",
                                            data="73"
                                        ),
                                        PostbackAction(
                                            label="社會學系",
                                            text="社會學系",
                                            data="742"
                                        ),
                                        PostbackAction(
                                            label="社會工作學系",
                                            text="社會工作學系",
                                            data="744"
                                        )
                                    ]
                                )
                            )
                        )

                    if dpm == "電機資訊學院":
                        line_bot_api.reply_message(
                            event.reply_token,
                            TemplateSendMessage(
                                alt_text="選擇科系",
                                template=ButtonsTemplate(
                                    thumbnail_image_url="https://walkinto.in/upload/bJ9zWWHaPLWJg9fW-STD8.png",
                                    title="選擇科系",
                                    text="請選擇科系",
                                    actions=[
                                        PostbackAction(
                                            label="電機工程學系",
                                            text="電機工程學系",
                                            data="87"
                                        ),
                                        PostbackAction(
                                            label="資訊工程學系",
                                            text="資訊工程學系",
                                            data="85"
                                        ),
                                        PostbackAction(
                                            label="通訊工程學系",
                                            text="通訊工程學系",
                                            data="86"
                                        )
                                    ]
                                )
                            )
                        )

                elif event.postback.data[0] == "D":
                    i_d = 0

                    try:
                        while group_signature[i_d] != event.source.user_id:
                            i_d += 1
                    except IndexError:
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="未進行任何查詢"))
                        break

                    if not group_searching[i_d]:
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=all_text[i_d]))

                        DN[i_d] = ""
                        all_text[i_d] = ""
                        group_opening[i_d] = False
                        group_signature[i_d] = ""
                        group_check[i_d] = False

                    elif group_check[i_d]:
                        line_bot_api.reply_message(event.reply_token,
                                                   TextSendMessage(text=all_text[i_d] + "連線中斷，嘗試重連中😅\n若結果持續不變，請重新查詢"))

                        group_check[i_d] = False

                    else:
                        line_bot_api.reply_message(event.reply_token,
                                                   TextSendMessage(text=all_text[i_d] + "持續查詢中......"))

                else:
                    x = 0
                    while group_opening[x]:
                        x += 1

                    DN[x] = event.postback.data
                    group_opening[x] = True
                    group_signature[x] = event.source.user_id
                    line_bot_api.reply_message(
                        event.reply_token, TextSendMessage(text="請輸入入學學年度"))

        return HttpResponse()
    else:
        return HttpResponseBadRequest()
