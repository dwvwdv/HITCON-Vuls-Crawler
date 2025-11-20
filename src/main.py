import cloudscraper
import re
from pynput import keyboard

import os
import sys

global page
page = 1

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
    if(response.status_code != 200):
        print(f"Waring : Status Code-{response.status_code}")
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


def on_press(key):
    global page
    if key == keyboard.Key.page_down:
        page += 1
        pageShow()
    elif key == keyboard.Key.page_up:
        page -= 1
        pageShow()
    elif key == keyboard.KeyCode(char = '/'):
        page = int(input())
        pageShow()
    elif key == keyboard.Key.f1:
        help()

def on_release(key):
    if(key == keyboard.Key.esc):
        sys.exit()

def help():
    print("Key Help:\n | page down:next page | page up : previous page | /:Input index jump to page | F1:help | Esc:exit |")

def init():
    help()
    writeClear()
    pageShow()
    with keyboard.Listener(on_press=on_press,suppress=False,on_release=on_release) as listener:
        listener.join()
    
def pageShow():
    print(f"---------------------------- Now Page : {page} -----------------------------")
    respText = reqeust_Open_Vulnerability(page)
    vuls = regular(respText)
    vulsDataShow(vuls)

if __name__ =='__main__':
    init()

    # writeInVuls(vuls)