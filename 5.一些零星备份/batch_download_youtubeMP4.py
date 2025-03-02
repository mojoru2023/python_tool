
#! coding:utf-8

import csv
import os

from selenium import webdriver


prefix_name = "【日本広告鉴赏】"

from selenium.common.exceptions import NoSuchElementException



def readDatafile(filename):
    line_list = []
    with open(filename,"r", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip("\n")
            line_list.append(line)
    return line_list




import time

def use_selenium_request(url):
    try:

        driver.get(url)
        time.sleep(30)
        # //*[@id="sf_result"]/div/div/div[2]/div[2]/div[1]
        click_element = driver.find_element_by_xpath('//*[@id="sf_result"]/div/div/div[2]/div[2]/div[1]')
        click_element.click()
    except NoSuchElementException as e:
        pass





start_time = time.time()

sourceFile = "urls.txt"  # 要分割的文本文件


def cutFile(sourceFile):
    print("正在读取文件...")
    sourceFileData = open(sourceFile, 'r', encoding='utf-8')
    # 将读取的文件内容按行分割，然后存到一个列表中
    ListOfLine = sourceFileData.read().splitlines()
    n = len(ListOfLine)
    print("文件共有" + str(n) + "行")
    print("请输入需要将文件分割的个数:")
    # 定义分割的文件个数
    m = int(input(""))
    p = n // m + 1
    print("需要将文件分成 " + str(m) + " 个子文件")
    print("每个文件最多有 " + str(p) + " 行")
    print("开始进行分割···")
    for i in range(m):
        print("正在生成第 " + str(i + 1) + " 个子文件")
        # 定义分割后新生成的文件
        destFileName = os.path.splitext(sourceFile)[0] + "_part" + str(i + 1) + ".txt"
        destFileData = open(destFileName, "w", encoding='utf-8')
        if (i == m - 1):
            for line in ListOfLine[i * p:]:
                destFileData.write(line + '\n')
        else:
            for line in ListOfLine[i * p:(i + 1) * p]:
                destFileData.write(line + '\n')
        destFileData.close()

    sourceFileData.close()
    end_time = time.time()
    duration = end_time - start_time
    print('处理完成，一共耗时', duration, '秒')








if __name__ == '__main__':
    # cutFile(sourceFile) #切割大文件
    # 300个太多了就把大文件切分成小的，每20个一组，每20个打开一次文件如何下载完了就关闭
    exec_file_list = []
    for (dirname, subdir, subfile) in os.walk(os.getcwd()):
        ret_file = [os.path.join(dirname, x) for x in subfile]
        for item in ret_file:
            exec_file_list.append(item)

    #
    # for item in exec_file_list:
    #     exec_file = item.split("\\")[-1]

        # if ".txt" in exec_file and sourceFile not in exec_file:
        #     print(exec_file)
    url_list = readDatafile(sourceFile)
    driver = webdriver.Chrome()
    for oneURL in url_list:
        print("{0}   -----   ok    -----".format(oneURL))
        # print("-" * 88)
        use_selenium_request(oneURL)
    time.sleep(100)
    driver.quit()



            # use_selenium_request(oneURL)
            # os.system(exec_pep8_cmd.format(item))

    #
    #
    # for oneURL in url_list:
    #
    # driver.quit()




