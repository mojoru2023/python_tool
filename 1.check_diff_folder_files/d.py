# -*- coding: utf-8  -*-
import os
import chardet
import sys
from rich.console import Console
from rich.text import Text


# 读取文件的函数，自动检测编码
def read_file(file_path):
    """以文本方式读取文件，自动转换为 UTF-8 编码"""
    with open(file_path, 'rb') as f:  # 以二进制方式读取，自动检测编码
        raw_data = f.read()
        detected_encoding = chardet.detect(raw_data)['encoding']  # 检测文件编码
        if detected_encoding is None:
            detected_encoding = 'utf-8'  # 如果无法检测编码，默认使用 utf-8
    with open(file_path, 'r', encoding=detected_encoding, errors='ignore') as f:
        return f.readlines()


# 比较文件内容并记录差异
def compare_files(file1, file2, result_folder, file_name):
    """比较两个文件的差异并输出"""
    df1 = read_file(file1)
    df2 = read_file(file2)

    diff_file_path = os.path.join(result_folder, 'diff_result.txt')
    check_counts_path = os.path.join(result_folder, 'check_counts.txt')

    with open(diff_file_path, 'a', encoding='utf-8') as diff_file:
        diff_file.write(f"文件: {file_name}\n")

        # 逐行比较文件1和文件2的内容
        max_lines = max(len(df1), len(df2))
        diff_found = False

        for line_idx in range(max_lines):
            # 获取每一行的内容，确保不会超出文件范围
            line1 = df1[line_idx].strip() if line_idx < len(df1) else ""
            line2 = df2[line_idx].strip() if line_idx < len(df2) else ""

            # 如果两行内容不同，打印差异
            if line1 != line2:
                diff_found = True
                diff_file.write(f"差异位置: 行 {line_idx + 1}\n")
                diff_file.write(f"文件1: {line1}  -- 文件2: {line2}\n")
                diff_file.write("-" * 50 + "\n")

        # 如果有差异，更新计数
        if diff_found:
            with open(check_counts_path, 'a', encoding='utf-8') as count_file:
                count_file.write(f"差异文件: {file_name}\n")

        return diff_found


# 主函数，处理两个文件夹
def compare_folders(folder1, folder2):
    """比较两个文件夹中的文件"""
    # 确保结果文件夹存在
    result_folder = 'result'
    if not os.path.exists(result_folder):
        os.makedirs(result_folder)

    # 1. 获取文件夹中的所有文件
    files_folder1 = set(os.listdir(folder1))
    files_folder2 = set(os.listdir(folder2))

    # 2. 比较文件名
    check_filename_path = os.path.join(result_folder, 'check_filename.txt')
    with open(check_filename_path, 'w', encoding='utf-8') as check_file:
        check_file.write("文件名差异:\n")
        diff_files = sorted(files_folder1.symmetric_difference(files_folder2))
        for file_name in diff_files:
            check_file.write(f"{file_name}\n")

    # 3. 比较相同文件名的文件内容
    total_files = 0
    diff_files = 0
    for file_name in files_folder1.intersection(files_folder2):
        file1 = os.path.join(folder1, file_name)
        file2 = os.path.join(folder2, file_name)

        total_files += 1
        if compare_files(file1, file2, result_folder, file_name):
            diff_files += 1

    # 4. 写入总统计数据
    check_counts_path = os.path.join(result_folder, 'check_counts.txt')
    with open(check_counts_path, 'w', encoding='utf-8') as count_file:
        count_file.write(f"总共比较文件数: {total_files}\n")
        count_file.write(f"有差异的文件数: {diff_files}\n")

    print(f"比较完成！检查文件差异请查看 result 文件夹中的 'check_filename.txt' 和 'diff_result.txt' 文件。")


# 从命令行参数获取文件夹路径
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python3 check_diff.py <文件夹1> <文件夹2>")
        sys.exit(1)

    folder1 = sys.argv[1]
    folder2 = sys.argv[2]

    # 运行文件夹比较
    compare_folders(folder1, folder2)
