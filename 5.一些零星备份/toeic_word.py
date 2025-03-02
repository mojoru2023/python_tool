#! -*- coding:utf-8 -*-


import datetime
import re
import os
import time

import xlrd
from xlrd import xldate_as_tuple
import datetime
import pymysql
import requests
from lxml import etree
from requests.exceptions import RequestException
from lxml import etree
def call_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None




#app选择好(完成)
# 单个下载脚本测试好（完成）
# 需要读取本地excel文件的程序（完成）
# 整理专门的excel文件
# 在服务器上进行适配
# 放到服务器上去跑



import xlrd

def read_xlrd(excelFile):
    data = xlrd.open_workbook(excelFile)
    table = data.sheet_by_index(0)
    dataFile = []
    for rowNum in range(table.nrows):
        dataFile.append(table.row_values(rowNum))

       # # if 去掉表头
       # if rowNum > 0:


    return dataFile


def text_save(filename, data):#filename为写入CSV文件的路径，data为要写入数据列表.
    file = open(filename,'a')
    for i in range(len(data)):
        s = str(data[i]).replace('[','').replace(']','')#去除[],这两行按数据不同，可以选择
        s = s.replace("'",'').replace(',','') +'\n'   #去除单引号，逗号，每行末尾追加换行符
        file.write(s)
    file.close()
    print("保存文件成功")

if __name__ == '__main__':
    lpath = 'C:\\Users\\user\\Downloads\\YD_mp3Cards-master\\toeic'
    # lpath =  os.getcwd()
    excelFile = '{0}\\toeic.xlsx'.format(lpath)
    full_items = read_xlrd(excelFile=excelFile)
    for single_name in full_items:
        print(single_name)
        url = 'https://www.youdao.com/w/{0}/#keyfrom=dict2.top'.format(single_name[0])
        html = call_page(url)
        selector = etree.HTML(html)
        mp3_c = selector.xpath('//*[@id="phrsListTab"]/h2/div/span[2]/a/@data-rel')


        try:
            big_list = []
            if len(mp3_c) != 0:
                for item in mp3_c:
                    big_list.append('https://dict.youdao.com/dictvoice?audio={0}'.format(item))

            for mp3_url in big_list:
                res = requests.get(mp3_url)

                music = res.content

                with open(r'{0}\{1}.mp3'.format(lpath,single_name[1]), 'ab') as file:  # 保存到本地的文件名
                    file.write(res.content)
                    file.flush()
                    time.sleep(0.3)
        except:

            pass



