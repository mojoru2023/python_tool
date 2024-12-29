import sys
import re


def clean_file(input_file, output_file):
    # 正则表达式用于匹配时间格式 (hh:mm)
    time_pattern = re.compile(r'^\d{1,2}:\d{2}$')

    # 读取输入文件内容
    try:
        with open(input_file, 'r', encoding='utf-8') as file:  # 可以改为适合的编码格式
            lines = file.readlines()
    except FileNotFoundError:
        print(f"错误: 找不到文件 {input_file}.")
        return
    except UnicodeDecodeError:
        print(f"错误: 文件 '{input_file}' 的编码无法解码。请检查文件编码。")
        return

    cleaned_lines = []

    for line in lines:
        stripped_line = line.strip()

        if time_pattern.match(stripped_line):  # 如果是时间，前后加换行符
            cleaned_lines.append('\n' + stripped_line + '\n')
        elif stripped_line:  # 非空行，加上空格后添加
            cleaned_lines.append(stripped_line + ' ')

    # 将清理后的内容写入输出文件
    with open(output_file, 'w', encoding='utf-8') as new_file:  # 可以改为适合的编码格式
        new_file.writelines(cleaned_lines)

    print(f"已成功处理文件 {input_file}，结果写入 {output_file}.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python clean_lines.py <处理前的文件名> <处理后的文件名>")
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    clean_file(input_filename, output_filename)
