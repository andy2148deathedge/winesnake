# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 10:27:07 2021

@author: user
"""
'''
爬酒專案全部函式整合:
'''
'''
1. 將本機圖片上傳至imgur(可能參數需改為圖檔而非path)
'''
def upimgur(CLIENT_ID, PATH, title = 'winepic'):
    '''
    此函式可將本機圖片利用imgur API 上傳至imgur，並返回圖片短網址聯結
    
    CLIENT_ID: imgur網站的API CLIENT_ID
    PATH: 本地圖片路徑
    title: 圖片取名
    '''
    import pyimgur
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title=title)
    # print(uploaded_image.title) # 上傳的名稱
    # print(uploaded_image.link) # 上傳圖片之聯結
    # print(uploaded_image.type) # 上傳圖片資料型態
    link = uploaded_image.link
    
    return link
'''
2. 根據已上傳至imgur圖片的url link做OCR
'''
def ocr(url, overlay=False, api_key='helloworld', language='eng', OCREngine=1):
    """ OCR.space API request with remote file.
        Python3.5 - not tested on 2.7
    :param url: Image url.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """
    import requests
    
    payload = {'url': url,
                'isOverlayRequired': overlay,
                'apikey': api_key,
                'language': language,
                }
    r = requests.post('https://api.ocr.space/parse/image',
                      data=payload,
                      )
    return r.content.decode()
'''
3. 將OCR字串結果轉為酒廠(字串)、年份(list)、特徵(list)
'''
def ocrInfo(ocrResult):
    '''
    此函式將OCR結果轉為酒廠(字串)、年份(list)、特徵(list)等需要資訊
    '''
    #-----------------這邊是搜尋關鍵字池----------------------------------------
    
    houses = ['CLYNELISH', 'OMAR'] # 酒廠列表
    housesDict = {'CLYNELISH':'克里尼利基','OMAR':'南投酒廠'} # 酒廠字典
    
    characteristics = ['BOURBON', 'SHERRY']# 特徵列表
    chDict = {'BOURBON':'波本','SHERRY':'雪莉'}# 特徵字典
    
    #---------------------------------------------------------------------
    import re
    
    ocrResult = ocrResult.upper() # 全轉大寫
    
    house = ''
    for i in houses:
        houseWord = re.findall(i , ocrResult)
        if houseWord != []:
            house = houseWord[0]
    # print(house) # 建立house字串
    
    age = []
    pattern = '\n(\d{2})'
    ageWord = re.findall(pattern, ocrResult)
    age = ageWord
    # print(ageWord) # 建立age串列
    
    ch = []
    for i in characteristics:
        chWords = re.findall(i , ocrResult)
        if chWords != []:
            ch.append(chWords[0])
    
    # print(ch) # 建立特徵串列
    
    house = housesDict[house]
    # 酒廠轉中
    # print(house)
    
    for i in range(len(ch)):
        ch[i] = chDict[ch[i]]
    # 特徵轉中
    # print(ch)
    
    age=['14'] # 測試碼(gonna remove)
    
    return house, age, ch
'''
4. 將酒廠(字串)、年份(list)、特徵(list)爬出網頁結果
'''
def find(house, age=[], ch=[]):
    '''
    給定以下參數，此函式可返回酒名(中文)、酒名(英文)、圖片URL、該酒資訊(介紹)
    EX :
    house = '百齡譚' # 酒廠字串
    age = ['17'] # ex: age = ['12'] 只有一個元素的年份串列
    ch = []  # 其他特徵串列，可為空串列
    # 特徵串列可為空，每個元素都是一特徵，需為字串 EX: ch = ['雪莉','雙桶']
    '''
    import requests
    from bs4 import BeautifulSoup
    import re 
    
    '''
    https://www.609.com.tw/Parts/PartQuery/克里尼利基
    
    https://www.609.com.tw/Parts/PartQuery/麥卡倫
    
    https://www.609.com.tw/Parts/PartQuery/大摩
    '''
    url = 'https://www.609.com.tw/Parts/PartQuery/' + house
    webpage = requests.get(url)
    # print(webpage.text)
    
    # 建立該品牌酒類網頁物件
    soup = BeautifulSoup(webpage.text, 'html.parser')
    # print(soup)
    
    # 爬取品牌所有酒品名稱
    winesTitle = soup.find_all('h6')
    
    wines = []
    for i in winesTitle:
        wine = i.get_text()
        wine = re.findall('(.*忌)[0-9]{3,4}ml', wine)
        wines += wine
    
    # print(wines) 
    
    # 爬取品牌所有酒品聯結&圖片
    winesLink = soup.select('a')
    links = []
    pics = []
    for i in winesLink:
        # print(i['href'])
        links.append(i['href'])
        # print(i.img['src'])
        pics.append(i.img['src'])
    
    # print(links)
    # print(pics)
    
    point = [] # 搜尋權重評分
    for i in range(0, len(wines)):
        point.append(0)
    
    for i in range(0, len(wines)):
        for j in range(0, len(age)):
            target = re.findall(age[j], wines[i])
            if (target == [age[j]]):
                    point[i] = point[i] + 1
            
    # print(point) # 年份權重評分
    
    for i in range(0, len(wines)):
        for j in range(0, len(ch)):
            target = re.findall(ch[j], wines[i])
            # print(target)
            if (target == [ch[j]]):
                point[i] = point[i] + 1
                
    # print(point) # 再加上特徵表評分
    index = point.index(max(point)) # 找出特徵最大値
    # print(index) # 找出預搜尋產品再品牌ajax網頁中的順序索引値
    
    targetName = wines[index] # 目標酒名
    # print(targetName)
    targetLink = 'https://www.609.com.tw/' + links[index]
    # print(targetLink)
    targetPic = 'https://www.609.com.tw/' + pics[index]
    # print(targetPic)
    #------------爬取目標內容-------------------
    url = targetLink
    webpage_bottle = requests.get(url)
    # print(webpage.text)
    
    # 建立該酒支網頁物件
    wine_soup = BeautifulSoup(webpage_bottle.text, 'html.parser')
    
    wine_Name = wine_soup.select('body > div.outerWrap.b-box > div:nth-child(2) > div.mainArea.ins > div > div:nth-child(2) > div > div.col-sm-7 > div.text-left > div:nth-child(2)')
    wineName = wine_Name[0].getText()
    
    wineInfo = wine_soup.select('body > div.outerWrap.b-box > div:nth-child(2) > div.mainArea.ins > div > div:nth-child(2) > div > div.col-sm-7 > div.text-left > div:nth-child(8)')
    wineInfo = wineInfo[0].get_text()
    
    # print(wineName) # 酒支英文名
    # print(wineInfo) # wineInfo為含有div+br標籤的整個html區塊
    
    return targetName, wineName, targetPic, wineInfo




#--------------------------以下為程式--------------------------------
'''
程式聯接測試: 
給酒圖檔
找出 中文名 英文名 圖片聯結 介紹
'''
# # 用upimgur(CLIENT_ID, PATH)上傳酒圖片
# CLIENT_ID = "c7e3a92e8697ac7"
# PATH = r"C:/Users/user/Desktop/learn case/成果發表/OCR測試/S__29270021.png" 

# #用upimgur() 函式透過本機路徑上傳圖片imgur網路API，並將網圖url存入pic_link
# pic_link = upimgur(CLIENT_ID, PATH)

# # 用 ocr() 函式進行OCR 並將分析字串結果存入winelabel
# winelabel = ocr(url=pic_link, api_key='8b3380e83888957', OCREngine=2)

# # 用 ocrInfo() 函式將ocr結果字串分析並賦値為需要的特徵値
# a = (house, age, ch) = ocrInfo(winelabel)

# # 用 find() 函式引入特徵値結果爬蟲，並賦値給需要的變數，得到酒資訊
# b = (chname, enname, picurl, info) = find(house, age, ch)

# print('中文名:', chname)
# print('英文名:', enname)
# print('圖片聯結:', picurl)
# print('介紹資訊:', info)

















