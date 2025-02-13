
# 实时预览markdown
# 安装markdown all in one插件以后

# 编写markdown文档可以, 通过command + shift + p打开 vscode的配置，
# 输入>Markdown: Open Preview to the Side 即可打开预览效果如图
# 也可以通过快捷键ctrl + shift + v


import os
import pandas as pd
from markitdown import MarkItDown

def convert_files_in_directory(input_directory):
    # 创建输出目录
    output_directory = os.path.join(input_directory, "md_result")
    os.makedirs(output_directory, exist_ok=True)

    # 记录转换统计
    file_counter = {}
    total_files_converted = 0

    # 支持的文件扩展名
    supported_extensions = [
        ".html",   # HTML 文件
        ".htm",    # HTML 文件
        ".docx",   # DOCX 文件
        ".pdf",    # PDF 文件
        ".zip",    # 压缩文件
        ".xlsx",   # Excel 文件
        ".xls",    # Excel 文件
        ".wav",    # 音频文件
        ".pptx"    # PowerPoint 文件
    ]

    # 遍历输入目录
    for root, dirs, files in os.walk(input_directory):
        for filename in files:
            # 分离文件名和扩展名
            file_name, file_extension = os.path.splitext(filename)

            # 检查是否是支持的文件类型
            if file_extension.lower() in supported_extensions:
                input_file_path = os.path.join(root, filename)
                md = MarkItDown(enable_plugins=False)  # 可根据需要启用插件

                try:
                    # 转换文件
                    result = md.convert(input_file_path)
                    content = result.text_content
                    
                    # 统计字数（去除 NaN）
                    word_count = len([word for word in content.split() if word.strip()])  # 统计非空字符串的数量
                    
                    # 修改输出文件名格式
                    output_file_name = f"{file_name}-{file_extension[1:]}-to.md"  # 去掉点并添加后缀
                    output_file_path = os.path.join(output_directory, output_file_name)

                    # 保存转换后的内容
                    with open(output_file_path, 'w', encoding='utf-8') as output_file:
                        output_file.write(content)

                    # 更新统计信息
                    total_files_converted += 1
                    file_counter[file_extension] = file_counter.get(file_extension, 0) + 1
                    file_counter[f"{file_extension}-word-count"] = file_counter.get(f"{file_extension}-word-count", 0) + word_count

                except Exception as e:
                    print(f"Error converting {input_file_path}: {e}")

    # 写入文件统计信息
    with open(os.path.join(output_directory, 'file_counter.txt'), 'w', encoding='utf-8') as counter_file:
        counter_file.write(f"Total converted files: {total_files_converted}\n")
        for ext, count in file_counter.items():
            counter_file.write(f"{ext}: {count}\n")

    print("Conversion completed. Check the 'md_result' folder.")

# 使用示例
if __name__ == "__main__":
    input_directory = "C:\\Users\\user\\Desktop\\New folder"  # 替换为你自己的目录路径
    convert_files_in_directory(input_directory)
