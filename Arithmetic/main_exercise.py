from modules import *
import argparse


if __name__ == '__main__':
    # 定义命令行解析器
    parser = argparse.ArgumentParser()

    # 添加命令行参数
    parser.add_argument('--n', type=int, default=10, help='控制生成题目的个数')
    parser.add_argument('--r', type=int, help='控制题目中数值（自然数、真分数和真分数分母）的范围')

    # 解析命令行参数
    args = parser.parse_args()
    n = args.n
    r = args.r

    exercises(n, r)
