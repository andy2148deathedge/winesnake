# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 15:30:05 2021

@author: user
"""
from wine import upimgur
from wine import ocr
from wine import ocrInfo
from wine import find

inputString = 'Omar Sherry'

# 用 ocrInfo() 函式將ocr結果字串分析並賦値為需要的特徵値
a = (house, age, ch) = ocrInfo(inputString)
print(a)

# 用 find() 函式引入特徵値結果爬蟲，並賦値給需要的變數，得到酒資訊
b = (chname, enname, picurl, info, pageurl) = find(house, age, ch)
print(b) # in age = ['14'] is fine