# NTPU student number
## 功能
1. 可以用學號查詢單一學生的姓名
2. 可以範圍查詢某學年度的某系所有學生
## 查詢範圍限制
只能查詢到
* [國立臺北大學](https://new.ntpu.edu.tw/)的學生
* 日間部的學生
* 95學年度入學的學生
## 使用方法
1. 使用執行檔查詢 (方便快速)
    1. 從[release頁面](https://github.com/garyellow/student_number/releases)下載student.exe
    2. 執行exe檔，接著依據提示操作即可
        > 由於範圍查詢會自動產生txt紀錄檔在子目錄(student)，所以要注意檔案的存放位置是否可寫  
        > 可能會跳出這個程式有風險的訊息，放心裡面真的沒病毒，如果還有資安疑慮可以改用第2個方法
2. 使用python執行py檔查詢 (安全、可自訂、跨系統)
    1. 從[release頁面](https://github.com/garyellow/student_number/releases)下載student.py檔
    2. 打開命令提示字元，開啟到存有student.py的資料夾
    3. 執行`python student.py`或`python3 student.py`
        > python的版本跟套件要自行確認過
        > 可以打開py檔看有引入什麼套件
    4. 接著依據提示操作即可
## 資料來源
* [國立臺北大學數位學苑2.0](http://lms.ntpu.edu.tw/)
