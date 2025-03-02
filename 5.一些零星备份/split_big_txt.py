# -*- coding:utf-8 –*-


import os
import time




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


cutFile(sourceFile)
