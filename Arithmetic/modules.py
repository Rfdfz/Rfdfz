import re
import random
from fractions import Fraction


# Arithmetic 算数类
class Arithmetic:
    def __init__(self, r):
        try:
            if not isinstance(r, int) or r < 0:
                raise TypeError
        except TypeError:
            print("输入的参数范围值必须是自然数")
            return
        self.result = -1
        while self.result < 0:
            self.formula = self.generate_arithmetic(r)
            try:
                self.result = self.calculate_arithmetic(self.formula)
            except ZeroDivisionError:
                continue

    @staticmethod
    def generate_arithmetic(r):
        """
        :param r: 数字上限
        :return: 字符串:算式
        """
        num_operator = random.randint(1, 3)
        operator_list = []
        for _ in range(num_operator):
            idx = random.randint(0, 3)
            operator = '+-×÷'
            operator_list.append(operator[idx])
        operator_list.append('=')

        # 生成运算数
        number_list = []
        for i in range(num_operator + 1):
            number = random.randint(0, r)
            if i != 0:
                if operator_list[i - 1] == '-':
                    number = random.randint(0, int(number_list[i - 1]))
                elif operator_list[i - 1] == '÷':
                    if number_list[i - 1] == 0:
                        number = random.randint(1, r)
                    else:
                        number = random.randint(int(number_list[i - 1]), r)

            number_list.append(number)
        # 加括号
        idx_left_bracket = random.randint(0, len(number_list) - 2)

        arithmetic = []
        for i in range(len(number_list)):
            if i == idx_left_bracket and num_operator > 1:
                arithmetic.append('( ' + str(number_list[i]) + ' ' + operator_list[i] + ' ')
            elif i == idx_left_bracket + 1 and num_operator > 1:
                arithmetic.append(str(number_list[i]) + ' ) ' + operator_list[i] + ' ')
            else:
                arithmetic.append(str(number_list[i]) + ' ' + operator_list[i] + ' ')

        arithmetic = ''.join(arithmetic)

        return arithmetic

    @staticmethod
    def calculate_arithmetic(formula):
        """
        :param formula: string:算式
        :return: Fraction对象:答案
        """
        # 将符号替换成python能识别的运算符
        formula = formula.replace('=', '')
        formula = formula.replace('×', '*')
        formula = formula.replace('÷', '/')
        formula = formula.replace(' ', '')

        # 使用正则表达式将所有数字转换为Fraction类型，便于分数计算，再使用eval()函数计算字符串内的表达式
        res = eval(re.sub(r'(\d+)', r'Fraction(\1)', formula))

        return res


def write_exercises(formula):
    # 写入题目
    with open('Exercises.txt', 'w') as f:
        for i, arithmetic in enumerate(formula):
            f.write(f"{i + 1}. {arithmetic}\n")


def read_exercises(path):
    try:
        # 读取题目
        with open(path, 'r') as f:
            formula = f.readlines()
        formula = [''.join(arithmetic.split(' ')[1:-1]) for arithmetic in formula]
        return formula
    except FileNotFoundError:
        print("请输入正确的文件路径")
        return FileNotFoundError


def write_answer(answer):
    # 写入答案
    with open('Answer.txt', 'w') as f:
        for i, ans in enumerate(answer):
            if ans > 1 and ans.numerator > ans.denominator != 1:
                res = f"{ans.numerator // ans.denominator}\'{ans.numerator % ans.denominator}/{ans.denominator}"
            else:
                res = ans
            f.write(f"{i + 1}. {res}\n")


def read_answer(path):
    try:
        # 读取答卷
        with open(path, 'r') as f:
            answer = f.readlines()
        formula = [''.join(ans.split(' ')[1:])[:-1] for ans in answer]

        for idx in range(len(formula)):
            if "\'" in formula[idx]:
                splited_fml = formula[idx].split("\'")
                formula[idx] = eval(re.sub(r'(\d+)', r'Fraction(\1)', f"{splited_fml[0]} + {splited_fml[1]}"))
        return formula
    except FileNotFoundError:
        print("请输入正确的文件路径")
        return FileNotFoundError


def write_grade(correct_info, wrong_info):
    # 写入成绩
    with open('Grade.txt', 'w') as f:
        f.write(correct_info + "\n")
        f.write(wrong_info)


def exercises(n, r):
    """
    :param n: int:题目数量
    :param r: int:范围限定
    """
    print("题目如下:")
    arithmetic_dict = {}
    while len(arithmetic_dict) != n:
        #  实例化一个算式类，生成一道新的题目
        arithmetic = Arithmetic(r)
        # 将算式以及答案存入字典中
        arithmetic_dict[arithmetic.formula] = arithmetic.result
        print(arithmetic.formula)
    # 将题目和答案分别写入文件
    write_exercises(arithmetic_dict.keys())
    write_answer(arithmetic_dict.values())


def correct_answer(e, a):
    """
    :param e: string:题目路径
    :param a: string:答卷路径
    """
    # 读取题目和答卷
    key = read_exercises(e)
    value = read_answer(a)
    arithmetic_dict = dict(zip(key, value))

    correct_idx = []
    wrong_idx = []
    for idx, (k, v) in enumerate(arithmetic_dict.items()):
        # 判断答案是否正确
        if Fraction(v) == Arithmetic.calculate_arithmetic(k):
            correct_idx.append(idx + 1)
        else:
            wrong_idx.append(idx + 1)
    # 生成正确和错误的信息
    correct_info = f"Correct: {len(correct_idx)} ({''.join([f'{idx},' for idx in correct_idx])})"
    wrong_info = f"Wrong: {len(wrong_idx)} ({''.join([f'{idx},' for idx in wrong_idx])})"

    # 打印信息
    print("答题情况如下")
    print(correct_info)
    print(wrong_info)

    # 写入成绩
    write_grade(correct_info, wrong_info)
