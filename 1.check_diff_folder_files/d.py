import os
import sys


# 读取文件的函数，自动检测编码
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.readlines()


# 比较文件内容并记录差异
def compare_files(file1, file2, result_folder, file_name):
    """比较两个文件的差异并输出"""
    df1 = read_file(file1)
    df2 = read_file(file2)

    diff_file_path = os.path.join(result_folder, 'diff_result.txt')
    same_info_file_path = os.path.join(result_folder, 'same_info_result.txt')
    check_counts_path = os.path.join(result_folder, 'check_counts.txt')



    # 逐行比较文件1和文件2的内容
    max_lines = max(len(df1), len(df2))
    diff_found = False

    for line_idx in range(max_lines):
        # 获取每一行的内容，确保不会超出文件范围
        line1 = df1[line_idx].strip() if line_idx < len(df1) else ""
        line2 = df2[line_idx].strip() if line_idx < len(df2) else ""

        # 如果两行内容不同，打印差异
        if line1 != line2:
            with open(diff_file_path, 'a', encoding='utf-8') as diff_file:
                diff_file.write(f"文件: {file_name}\n")
                diff_found = True
                diff_file.write(f"差异位置: 行 {line_idx + 1}\n")
                diff_file.write(f"文件1: {line1}\n")
                diff_file.write(f"文件2: {line2}\n")
                diff_file.write("-" * 88 + "\n")

    # 如果有差异，更新计数
    if diff_found:
        with open(check_counts_path, 'a', encoding='utf-8') as count_file:
            count_file.write(f"差异文件: {file_name}\n")
    else:
        with open(same_info_file_path, 'a', encoding='utf-8') as same_file:
            same_file.write(f"文件: {file_name}\n")
    return diff_found


def compare_folders(folder1, folder2):
    """比较两个文件夹中的文件"""

    # 定义结果文件夹路径，并确保该文件夹存在
    result_folder = 'result'
    if not os.path.exists(result_folder):
        os.makedirs(result_folder)

    # 获取文件夹中的所有文件
    files_folder1 = set(os.listdir(folder1))
    files_folder2 = set(os.listdir(folder2))

    # 用于存储差异的集合
    only_in_folder1 = set()
    only_in_folder2 = set()
    duplicate_files = set()

    # 比较文件名并分类存储差异
    for file_name in files_folder1:
        if file_name not in files_folder2:
            only_in_folder1.add(file_name)
        else:
            duplicate_files.add(file_name)

    for file_name in files_folder2:
        if file_name not in files_folder1:
            only_in_folder2.add(file_name)

    # 一次性写入文件名差异
    check_filename_path = os.path.join(result_folder, 'check_filename.txt')
    with open(check_filename_path, 'w', encoding='utf-8') as check_file:
        check_file.write("文件名差异:\n")

        # 输出在 folder1 中而不在 folder2 中的文件
        if only_in_folder1:
            check_file.write("在 {0} 中而不在 {1} 中的文件:\n".format(folder1,folder2))
            for file_name in sorted(only_in_folder1):
                check_file.write(f"{file_name}\n")

        # 输出在 folder2 中而不在 folder1 中的文件
        if only_in_folder2:
            check_file.write("在 {1} 中而不在 {0} 中的文件:\n".format(folder1,folder2))
            for file_name in sorted(only_in_folder2):
                check_file.write(f"{file_name}\n")

        # 输出重复文件名
        if duplicate_files:
            check_file.write("\n重复的文件名（在两个文件夹中都有）：\n")
            for file_name in sorted(duplicate_files):
                check_file.write(f"{file_name}\n")

    # 比较相同文件名的文件内容
    total_files = 0
    diff_files = 0
    for file_name in duplicate_files:
        file1 = os.path.join(folder1, file_name)
        file2 = os.path.join(folder2, file_name)

        total_files += 1
        if compare_files(file1, file2, result_folder, file_name):
            diff_files += 1

    # 写入总统计数据
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

    folder1_name = sys.argv[1]
    folder2_name = sys.argv[2]

    # 获取当前工作目录
    current_dir = os.getcwd()

    # 将命令行输入的文件夹名称与当前工作目录结合
    folder1 = os.path.join(current_dir, folder1_name)
    folder2 = os.path.join(current_dir, folder2_name)

    # 确保文件夹路径存在
    if not os.path.exists(folder1) or not os.path.exists(folder2):
        print(f"错误: 其中一个文件夹路径不存在：{folder1} 或 {folder2}")
        sys.exit(1)

    # 运行文件夹比较
    compare_folders(folder1, folder2)
