from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# chrome://version/
# 配置 Chrome WebDriver 的路径
# CHROME_DRIVER_PATH = 'path/to/chromedriver'  # 替换为你的 ChromeDriver 路径
USER_DATA_DIR="C:\\Users\\user\\AppData\\Local\\Google\\Chrome\\User Data"
PROFILE_NAME = 'Default'  # 替换为你希望使用的配置文件名，例如 'Profile 1', 'Profile 2', 'Default'

def read_txt_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.readlines()  # 读取文件内容并按行分割
            return [line.strip() for line in content]  # 去掉每行的空白字符
    except FileNotFoundError:
        print("文件未找到，请检查路径。")
        return []
    except Exception as e:
        print(f"发生错误：{e}")
        return []


def load_html_and_input(file_path, lines):



    options = webdriver.ChromeOptions()

    options.add_argument(f"user-data-dir={USER_DATA_DIR}")  # 指定用户数据目录
    options.add_argument(f"--profile-directory={PROFILE_NAME}")  # 指定用户配置文件

    driver = webdriver.Chrome(options=options)
    # 启动浏览器



    # 加载本地 HTML 文件
    driver.get(file_path)

    try:
        for line in lines:
            # 找到输入框并输入文本（使用 XPath）
            input_box = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/input')  # 根据实际情况修改 XPath
            input_box.clear()  # 清空输入框
            input_box.send_keys(line)  # 输入内容

            # 找到按钮并点击（使用 XPath）
            button = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/button')  # 根据实际情况修改 XPath
            button.click()  # 点击按钮

            time.sleep(1)  # 等待 1 秒以便能查看输入结果（可根据需要调整）

    except Exception as e:
        print(f"发生错误：{e}")

    finally:
        time.sleep(5)  # 等待几秒钟以查看最终结果
        driver.quit()  # 关闭浏览器


if __name__ == "__main__":
    # txt_file_path = input("请输入要读取的 TXT 文件路径：")  # 获取用户输入的 TXT 文件路径
    # html_file_path = input("请输入要加载的 HTML 文件路径：")  # 获取用户输入的 HTML 文件路径
    html_file_path = "file:///C:/Users/user/Downloads/YD_mp3Cards-master/toeic/toeic_word/toeic_word_v2.html"
    lines = read_txt_file("t.txt")  # 读取 TXT 文件内容
    if lines:
        load_html_and_input(html_file_path, lines)  # 调用加载函数