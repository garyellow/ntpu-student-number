import math
import msvcrt
import os
import random
import time

import requests
from bs4 import BeautifulSoup as BS4
from fake_useragent import UserAgent

d = {
    '法律': 71, '法學': 712, '司法': 714, '財法': 716,
    '公行': 72,
    '經濟': 73,
    '社會': 74, '社學': 742, '社工': 744,
    '財政': 75,
    '不動': 76,
    '會計': 77,
    '統計': 78,
    '企管': 79,
    '金融': 80,
    '中文': 81,
    '應外': 82,
    '歷史': 83,
    '休運': 84,
    '資工': 85,
    '通訊': 86,
    '電機': 87
}


def get_key(value):
    return str([k for k, v in d.items() if v == value]).strip("[']")


print('歡迎使用依學號查詢姓名程式')
print('本程式可用學號查到北大日間部學生之姓名')
print('查詢資料僅供參考，會因為各種因素而變動')
print('資料來源為北大數位學苑2.0\n')

while True:
    ua = UserAgent()
    header_seed = ua.random
    header = {'user-agent': header_seed}

    mode = input('1.查詢個人\n2.查詢全系\n請選擇查詢模式\n>> ')
    while mode not in ['1', '2']:
        print('\n請輸入 1 或 2\n')
        mode = input('1.查詢個人\n2.查詢全系\n請選擇查詢模式\n>> ')

    while True:
        if mode == '1':
            number = input('\n請輸入學號\n>> ')

            if not number.isdecimal():
                print('\n請輸入數字!!!\n')
                continue
            if int(number) > 500000000 or int(number) < 40000000:
                print('\n請輸入正確格式!!!\n')
                continue

            url = 'http://lms.ntpu.edu.tw/portfolio/search.php?fmScope=2&fmKeyword=' + number
            web = requests.get(url, headers=header)
            web.encoding = 'utf-8'

            html = BS4(web.text, 'html.parser')
            name = html.find('div', {'class': 'bloglistTitle'})

            try:
                print('\n' + number + ' ' + name.text + '\n\n')
            except AttributeError:
                print('\n學號' + number + '不存在')
                print('請重新輸入學號\n')
                continue

            break

        elif mode == '2':
            try:
                year = int(input('\n請輸入入學年度\n>> '))
            except ValueError:
                print('\n請輸入數字!!')
                continue

            if year >= 1911:
                year -= 1911

            if year > time.localtime(time.time()).tm_year:
                print('\n你未來人??\n')
                break
            elif year < 90:
                print('\n學校都還沒蓋好，急什麼XD\n')
                break
            elif year < 95:
                print('\n資料未建檔\n')
                break

            while True:
                department = input('\n請輸入科系名稱或編號\n>> ')
                try:
                    department = int(department)
                except ValueError:
                    try:
                        department = d[department.rstrip('系')]
                    except KeyError:
                        print('\n請輸入正確科系名稱或編號!!')
                        continue

                if department == d['法律']:
                    print('\n法律系請輸入法學、司法、財法或完整科系編號~')
                    continue
                elif department == d['社會']:
                    print('\n社會相關科系請輸入社學、社工或完整科系編號~')
                    continue
                elif department not in d.values():
                    print('\n請輸入正確科系名稱或編號!!')
                    continue

                break

            if not os.path.isdir('student'):
                os.mkdir('student')
            f = open('student/' + str(year) + '學年度' + (get_key(department) + '系' if math.floor(department / 10) != d['法律'] else get_key(int(department / 10)) + '系' + get_key(department) + '組') + '學生名單.txt', 'w+', encoding='utf-8')

            DPM = '4' + str(year) + str(department)

            print()
            for i in range(1, 999):
                if department <= 99:
                    student_number = DPM + '{:0>3d}'.format(i)
                else:
                    student_number = DPM + '{:0>2d}'.format(i)

                URL = 'http://lms.ntpu.edu.tw/portfolio/search.php?fmScope=2&fmKeyword=' + student_number
                web = requests.get(URL, headers=header)
                web.encoding = 'utf-8'

                html = BS4(web.text, 'html.parser')
                name = html.find('div', {'class': 'bloglistTitle'})

                try:
                    print(student_number + ' ' + name.text)
                    f.write(str(student_number + ' ' + name.text + '\n'))
                except AttributeError:
                    if math.floor(department / 10) == d['法律']:
                        print('\n' + str(year) + '學年度' + get_key(department / 10) + '系' + get_key(department) + '組共有' + str(i - 1) + '個學生\n')
                        f.write(str(year) + '學年度' + get_key(department / 10) + '系' + get_key(department) + '組共有' + str(i - 1) + '個學生\n')
                    else:
                        print('\n' + str(year) + '學年度' + get_key(department) + '系共有' + str(i - 1) + '個學生\n')
                        f.write(str(year) + '學年度' + get_key(department) + '系共有' + str(i - 1) + '個學生\n')

                    f.close()
                    break

                time.sleep(random.uniform(0, 0.2))

            break

    print('按Enter鍵重新查詢，其他鍵離開程式')
    if ord(msvcrt.getch()) != 13:
        break
    else:
        print()
