'''
專案後端主程式

圖本地路徑: 
r"C:/Users/user/Desktop/learn case/成果發表/OCR測試/S__29270021.png"
'''
#-------flask------------
from flask import Flask
from flask import request
from flask import render_template
#-------wine-------------
from wine import upimgur
from wine import ocr
from wine import ocrInfo
from wine import find

app = Flask(__name__, static_folder='public', static_url_path='/')

@app.route('/')
def index(): 
    return render_template('index.html')


@app.route('/result')
def result():
    # 用get方法取得index表單中的picroute
    picurl = request.args.get('picroute','')

    # 用upimgur(CLIENT_ID, PATH)上傳酒圖片
    CLIENT_ID = "c7e3a92e8697ac7"
    PATH = picurl 
    #用upimgur() 函式透過本機路徑上傳圖片imgur網路API，並將網圖url存入pic_link
    pic_link = upimgur(CLIENT_ID, PATH)
    # 用 ocr() 函式進行OCR 並將分析字串結果存入winelabel
    winelabel = ocr(url=pic_link, api_key='8b3380e83888957', OCREngine=2)
    # 用 ocrInfo() 函式將ocr結果字串分析並賦値為需要的特徵値
    a = (house, age, ch) = ocrInfo(winelabel)
    # 用 find() 函式引入特徵値結果爬蟲，並賦値給需要的變數，得到酒資訊
    b = (chname, enname, picurl, info, pageurl) = find(house, age, ch)

    return render_template('result.html', ch=chname, en=enname, url=picurl, text=info, page = pageurl)

app.run(port=3000)