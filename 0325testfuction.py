# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 15:27:37 2021

@author: user
"""
from wine import upimgur
from wine import ocr
from wine import ocrInfo
from wine import find

# 用get方法取得index表單中的picroute
# picurl = request.args.get('picroute','')
# picurl = r'C:\Users\user\Desktop\winesnake\public\wine.png'

# # 用upimgur(CLIENT_ID, PATH)上傳酒圖片
# CLIENT_ID = "c7e3a92e8697ac7"
# PATH = picurl 
# #用upimgur() 函式透過本機路徑上傳圖片imgur網路API，並將網圖url存入pic_link
# pic_link = upimgur(CLIENT_ID, PATH)
# 用 ocr() 函式進行OCR 並將分析字串結果存入winelabel
winelabel = ocr(url=r'C:\Users\user\Desktop\winesnake\public\wine.png', api_key='8b3380e83888957', OCREngine=2)
print(winelabel)
# 用 ocrInfo() 函式將ocr結果字串分析並賦値為需要的特徵値
a = (house, age, ch) = ocrInfo(winelabel)
# 用 find() 函式引入特徵値結果爬蟲，並賦値給需要的變數，得到酒資訊
b = (chname, enname, picurl, info) = find(house, age, ch)