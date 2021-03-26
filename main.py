from flask import send_from_directory
import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

from wine import upimgur
from wine import ocr
from wine import ocrInfo
from wine import find

#------------上傳檔案部分-----------------
UPLOAD_FOLDER = r'C:\Users\user\Desktop\winesnake\public'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__, static_folder='public')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']# 接收 post 檔案 
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # 檔案上傳
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                   filename))
            # return redirect(url_for('uploaded_file',
            #                         filename=filename))
    return render_template('index.html')
    


# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'],
#                                filename)

#-----------圖片處理部分---------------
@app.route('/resultFile')
def resultFile():
    # 設定已上傳的本機靜態檔案路徑為pic_Path
    pic_Path = r'C:\Users\user\Desktop\winesnake\public\wine.jpg'

    # 用upimgur(CLIENT_ID, PATH)上傳酒圖片
    CLIENT_ID = "c7e3a92e8697ac7"
    PATH = pic_Path 

    #用upimgur() 函式透過本機路徑上傳圖片imgur網路API，並將網圖url存入pic_link
    pic_link = upimgur(CLIENT_ID, PATH) 
    # print(pic_link) # CHKED

    # 用 ocr() 函式進行OCR 並將分析字串結果存入winelabel
    winelabel = ocr(url=pic_link, api_key='8b3380e83888957', language='eng', OCREngine=2)
    # print(winelabel) # CHKED   # wine.py set age = ['14'] for test

    # 用 ocrInfo() 函式將ocr結果字串分析並賦値為需要的特徵値
    a = (house, age, ch) = ocrInfo(winelabel)
    print(a)

    # 用 find() 函式引入特徵値結果爬蟲，並賦値給需要的變數，得到酒資訊
    b = (chname, enname, picurl, info, pageurl) = find(house, age, ch)
    print(b) # in age = ['14'] is fine

    return render_template('resultFile.html', ch=chname, en=enname, url=picurl, text=info, page = pageurl)

#---------字串搜尋-------------------
@app.route('/resultKeyword')
def resultKeyword():
    # 用get方法取得uploadfile表單中的keyword
    inputString = request.args.get('keyword','')

    # 用 ocrInfo() 函式將ocr結果字串分析並賦値為需要的特徵値
    a = (house, age, ch) = ocrInfo(inputString)

    # 用 find() 函式引入特徵値結果爬蟲，並賦値給需要的變數，得到酒資訊
    b = (chname, enname, picurl, info, pageurl) = find(house, age, ch)
    print(b) # in age = ['14'] is fine

    return render_template('resultKeyword.html', ch=chname, en=enname, url=picurl, text=info, page = pageurl)

if __name__ == '__main__':
    app.run(debug=True)

'''
參考
https://medium.com/@charming_rust_oyster_221/flask-%E6%AA%94%E6%A1%88%E4%B8%8A%E5%82%B3%E5%88%B0%E4%BC%BA%E6%9C%8D%E5%99%A8%E7%9A%84%E6%96%B9%E6%B3%95-1-c11097c23137
'''
'''
git try
'''