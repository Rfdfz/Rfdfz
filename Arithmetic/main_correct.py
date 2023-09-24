from modules import *
import argparse

if __name__ == '__main__':
    # 定义命令行解析器
    parser = argparse.ArgumentParser()

    # 添加命令行参数
    parser.add_argument('--e', help='题目文件路径')
    parser.add_argument('--a', help='答题文件路径')

    # 解析命令行参数
    args = parser.parse_args()
    e = args.e
    a = args.a

    correct_answer(e, a)