import sys
import hashlib
import argparse
import requests

__version__ = '0.0.1'
url = 'http://openapi.youdao.com/api?q={}&from={}&to={}&appKey=0caa4581f3a73a48&salt=2&sign={}'

def get_md5(txt):
    txt = '0caa4581f3a73a48'+txt+str(2)+'5lGrTMQoR3yWUBBSKoPHEvU3ffDAK8tB'
    m = hashlib.md5()
    m.update(txt.encode("utf8"))
    md5 = m.hexdigest()
    return md5

def get_parser():
    parser = [sys.argv[i] for i in range(1,len(sys.argv))]

    return parser

def command_line_parser():
    args = get_parser()
    if args[0]=='-v':
        print(__version__)
    if args[0]=='-c':
        txt = args[1]
        translation(url, txt, 'zh_CHS', 'EN', get_md5(txt))
        sys.exit()
    if args[0]=='-e':
        txt = ' '.join(args[1:])
        translation(url, txt, 'EN', 'zh_CHS', get_md5(txt))
        sys.exit()
    else:
        print('参数：'+'\n'
              '-v: 版本信息     '+"\n"+
              '-c: 翻译中文     '+"\n"+
              '-e: 翻译英文     '+"\n"+
              '用法示例：'+'\n'
              "yd.py -c 我是一个好男孩"+'\n'+
              "yd.py -e i am a good boy")

def translation(url,txt,fromLanguage,toLanguage,md5):
    url = url.format(txt,fromLanguage,toLanguage,md5)
    reponse = requests.get(url)
    printCmd(reponse.json())

def printCmd(jsondata):
    dictdata = dict(jsondata)
    print("翻译：\n"+dictdata['translation'][0])
    if (dictdata.get('basic')):
        print("\n基础释义：")
        for tran in dictdata['basic']['explains']:
            print(tran)
    if(dictdata.get('web')):
        print('\n网络释义：')
        for tran in dictdata['web']:
            print(' '.join(tran['value']))

if __name__=="__main__":
    command_line_parser()

