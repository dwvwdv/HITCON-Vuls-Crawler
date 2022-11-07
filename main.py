import cloudscraper
import re
from pynput import keyboard

import os
import sys

def regular(text):
    reg = re.compile('title tx-overflow-ellipsis"><a href="(.*?)">(.*?)</a>')
    return re.findall(reg,text)

def download(img_url,index):
    try:
        img = cloudscraper.get(img_url)
        with open(f'pic/picture{index}.jpg','wb',) as f:
            f.write(img.content)
        print('download finish.')
    except:
        print("download failed.")

def reqeust_Open_Vulnerability(pageNum):
    url = f'https://zeroday.hitcon.org/vulnerability/disclosed/page/{pageNum}'
    scraper = cloudscraper.create_scraper(delay=300, browser={'custom': 'ScraperBot/1.0',})
    response = scraper.get(url)
    return response.text

def parseSystemParam(args,responseHtml):
    if len(args) == 0:
        return 
    elif args[0] == '-o':
        SaveFile = os.getcwd() + '/output.html'
        with open(SaveFile,'w',encoding='u8') as f:
            f.write(responseHtml)
        print('WriteFile finish.')
        os.system(f'cmd /c start chrome "{SaveFile}"')

def vulsDataShow(vuls):
    for vul in vuls:
        link = 'https://zeroday.hitcon.org' + vul[0] 
        print(link,vul[1])

def writeInVuls(vuls):
    SaveFile = os.getcwd() + '/vuls.txt'
    for vul in vuls:
        link = 'https://zeroday.hitcon.org' + vul[0] 
        with open(SaveFile,'a',encoding='u8') as f:
            f.writelines(f'{link} {vul[1]}\n')

def writeClear():
    SaveFile = os.getcwd() + '/vuls.txt'
    with open(SaveFile,'w',encoding='u8') as f:
        f.write('')

def init():
    writeClear()

def on_release(key):
    page = 1
    if key == keyboard.Key.down:
        respText = reqeust_Open_Vulnerability(++page)

if __name__ =='__main__':
    respText = reqeust_Open_Vulnerability(1)
    parseSystemParam(sys.argv[1:],respText)
    vuls = regular(respText)
    
    vulsDataShow(vuls)
    writeInVuls(vuls)