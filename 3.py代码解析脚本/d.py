import os
import re
import sys


def is_valid_variable_name(name):
    """ 检查是否为有效的变量名 """
    return re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name) is not None


def extract_symbols_from_file(file_path):
    symbols = []

    # 使用 'utf-8' 编码方式打开文件
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    current_class = None
    indent_level = 0
    in_function_body = False
    current_function_lines = []  # 用于存储完整的函数定义行

    for line in lines:
        stripped_line = line.strip()

        # 检查是否为类定义
        if stripped_line.startswith('class '):
            current_class = stripped_line
            symbols.append(f'类名: {current_class}\n')

        # 检查类变量（在类定义下方）
        elif current_class and not stripped_line.startswith('def ') and '=' in stripped_line:
            variable_name = stripped_line.split('=')[0].strip()
            if is_valid_variable_name(variable_name):  # 确保变量名称有效
                symbols.append(f'  类变量: {variable_name}\n')

        # 检查是否为函数定义
        if stripped_line.startswith('def '):
            current_function = stripped_line
            symbols.append('\n---------------------------------\n')
            symbols.append(f'函数: {current_function}\n')

            # 存储函数定义的行
            current_function_lines = [stripped_line]
            indent_level = len(line) - len(line.lstrip())
            in_function_body = True  # 标记进入函数体

        # 如果当前我们在函数体内，检查函数变量
        elif in_function_body:
            current_indent = len(line) - len(line.lstrip())

            # 如果发现缩进大于当前函数定义的缩进，可能是在函数内部
            if current_indent > indent_level:
                current_function_lines.append(stripped_line)  # 继续添加到函数定义中

                # 检查是否有等号，表示可能存在定义变量
                if '=' in stripped_line:
                    parts = stripped_line.split('=')
                    left_side = parts[0].strip()  # 获取等号左侧内容

                    # 确保等号两边都符合变量名的规则
                    if len(parts) == 2 and is_valid_variable_name(left_side):
                        symbols.append(f'  函数变量: {left_side}\n')
            else:
                # 完成函数定义的解析
                in_function_body = False

                # 先添加分隔符，再解析完整的函数参数

                parse_function_parameters(current_function_lines, symbols)

    return symbols


def parse_function_parameters(function_lines, symbols):
    """ 从函数定义行中解析参数 """
    full_definition = " ".join(function_lines)

    start_index = full_definition.find('(')
    end_index = full_definition.rfind(')')

    if start_index != -1 and end_index != -1:
        params_str = full_definition[start_index + 1:end_index]
        params = [param.strip() for param in params_str.split(',')]

        for param in params:
            if param:  # 确保参数不为空
                symbols.append(f'  函数参数: {param}\n')


def main(directory):
    output_file = 'output.txt'  # 输出文件名

    with open(output_file, 'w', encoding='utf-8') as out_file:
        for dirpath, _, filenames in os.walk(directory):
            for filename in filenames:
                if filename.endswith('.py'):  # 只处理 Python 文件
                    full_path = os.path.join(dirpath, filename)
                    out_file.write(f'文件路径: {full_path}\n')  # 首先输出文件路径
                    symbols = extract_symbols_from_file(full_path)
                    out_file.writelines(symbols)
                    out_file.write('\n')  # 在每个文件之间添加空行

    print(f'解析完了 {output_file}.')


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <directory>")
        sys.exit(1)

    target_directory = sys.argv[1]
    main(target_directory)
