# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 11:18:56 2021

@author: user
"""
'''
爬酒專案主程式測試:
利用wine.py檔案的函式庫
給酒圖檔
找出 中文名 英文名 圖片聯結 介紹
'''
from wine import upimgur
from wine import ocr
from wine import ocrInfo
from wine import find

# 用upimgur(CLIENT_ID, PATH)上傳酒圖片
CLIENT_ID = "c7e3a92e8697ac7"
PATH = r"C:/Users/user/Desktop/learn case/成果發表/OCR測試/S__29270021.png" 

#用upimgur() 函式透過本機路徑上傳圖片imgur網路API，並將網圖url存入pic_link
pic_link = upimgur(CLIENT_ID, PATH)

# 用 ocr() 函式進行OCR 並將分析字串結果存入winelabel
winelabel = ocr(url=pic_link, api_key='8b3380e83888957', OCREngine=2)

# 用 ocrInfo() 函式將ocr結果字串分析並賦値為需要的特徵値
a = (house, age, ch) = ocrInfo(winelabel)

# 用 find() 函式引入特徵値結果爬蟲，並賦値給需要的變數，得到酒資訊
b = (chname, enname, picurl, info) = find(house, age, ch)

print('中文名:', chname)
print('英文名:', enname)
print('圖片聯結:', picurl)
print('介紹資訊:', info)









