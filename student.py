import msvcrt
import random
import time

import requests
from bs4 import BeautifulSoup as BS4
from fake_useragent import UserAgent

d = {
    '法律': '71', '法學': '712', '司法': '714', '財法': '716',
    '公行': '72',
    '經濟': '73',
    '社會': '74', '社工': '742', '社學': '744',
    '財政': '75',
    '不動': '76',
    '會計': '77',
    '統計': '78',
    '企管': '79',
    '金融': '80',
    '中文': '81',
    '應外': '82',
    '歷史': '83',
    '休運': '84',
    '資工': '85',
    '通訊': '86',
    '電機': '87'
}

D = {
    '71': '法律', '712': '法學', '714': '司法', '716': '財法',
    '72': '公行',
    '73': '經濟',
    '74': '社會', '742': '社工', '744': '社學',
    '75': '財政',
    '76': '不動',
    '77': '會計',
    '78': '統計',
    '79': '企管',
    '80': '金融',
    '81': '中文',
    '82': '應外',
    '83': '歷史',
    '84': '休運',
    '85': '資工',
    '86': '通訊',
    '87': '電機'
}

print('歡迎使用依學號查詢姓名程式')
print('本程式可用學號查到北大日間部學生之姓名')
print('查詢資料僅供參考，會因為各種因素而變動')
print('資料來源為北大數位學苑2.0\n')

while True:
    ua = UserAgent()
    header_seed = ua.random
    header = {'user-agent': header_seed}
    f = open('save.txt', 'w', encoding='utf-8')

    mode = input('1.查詢個人\n2.查詢全系\n請選擇查詢模式\n>> ')

    while True:
        if mode == '1':
            number = input('\n請輸入學號\n>> ')

            if not number.isdecimal():
                print('\n請輸入數字!!!\n')
                continue
            if int(number) > 999999999 or int(number) < 99999999:
                print('\n請輸入正確學號!!!\n')
                continue

            url = 'http://lms.ntpu.edu.tw/portfolio/search.php?fmScope=2&fmKeyword=' + number
            web = requests.get(url, headers=header)
            web.encoding = 'utf-8'

            html = BS4(web.text, 'html.parser')
            name = html.find('div', {'class': 'bloglistTitle'})

            try:
                print('\n' + number + ' ' + name.text + '\n\n')
                f.write(str(number + ' ' + name.text + '\n'))
            except AttributeError:
                print('\n學號' + number + '不存在')
                print('請重新輸入學號\n')
                continue

            break

        elif mode == '2':
            year = input('\n請輸入入學年度\n>> ')

            if not year.isdecimal():
                print('\n請輸入數字!!!\n')
                continue
            if int(year) >= 2022:
                print('\n你未來人???\n')
                continue
            if int(year) < 50:
                print('\n你原始人???\n')
                continue
            if 110 < int(year) < 1911:
                print('\n請輸入正確年分!!!\n')
                continue
            if int(year) >= 1911:
                year = str(int(year) - 1911)

            department = input('\n請輸入科系名稱或編號\n>> ')
            if department.isdecimal():
                if not 71 <= int(department) <= 87 and int(department) != 712 and int(department) != 714 and int(
                        department) != 716 and int(department) != 742 and int(department) != 744:
                    print('\n請輸入正確科系編號!!!\n')
                    continue
                elif int(department) == 71:
                    print('\n法律系請輸入科系+組別編號!!!\n')
                    continue
                elif int(department) == 74:
                    print('\n社會系請輸入科系+組別編號!!!\n')
                    continue

                DPM = '4' + '{:0>3d}'.format(int(year)) + department

                print()
                for i in range(1, 999):
                    if int(department) <= 99:
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
                        print('\n' + year + '學年度' + D[department] + '系共有' + str(i - 1) + '個學生\n')
                        break

                    time.sleep(random.uniform(0, 0.2))
                break

            else:
                try:
                    d[department]
                except KeyError:
                    print('\n請輸入正確科系名稱(不須加「系」)')
                    continue

                if d[department] == '71':
                    case = input('\n1.法學\n2.司法\n3.財法\n請確認您的組別\n>> ')
                    while case != '1' and case != '2' and case != '3':
                        print('\n請輸入1、2或是3\n')
                        case = input('\n1.法學\n2.司法\n3.財法\n請確認您的組別\n>> ')
                    DPM = '4' + '{:0>3d}'.format(int(year)) + d[department] + str(int(case) * 2)

                elif d[department] == '74':
                    case = input('\n1.社學\n2.社工\n請確認您的系別\n>> ')
                    while case != '1' and case != '2':
                        print('\n請輸入1或2\n')
                        case = input('\n1.社學\n2.社工\n請確認您的系別\n>> ')
                    DPM = '4' + '{:0>3d}'.format(int(year)) + d[department] + str(int(case) * 2)

                else:
                    DPM = '4' + '{:0>3d}'.format(int(year)) + d[department]

                print()
                for i in range(1, 999):
                    if i == 60:
                        i = 1

                    if int(d[department]) <= 99 and int(d[department]) != 71 and int(d[department]) != 74:
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
                        print('\n' + year + '學年度' + department + '系共有' + str(i - 1) + '個學生\n')
                        break

                    time.sleep(random.uniform(0, 0.2))
                break
        else:
            print('\n請輸入1或2\n')
            mode = input('1.查詢個人\n2.查詢全系\n請選擇查詢模式\n>> ')

    f.close()

    print('按Enter鍵重新查詢，其他鍵離開程式')
    if ord(msvcrt.getch()) != 13:
        break
    else:
        print()
