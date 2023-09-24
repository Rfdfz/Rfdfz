import argparse
import re
import random
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 10

# # 定义命令行解析器
# parser = argparse.ArgumentParser()
#
# # 添加命令行参数
# parser.add_argument('--n', default=10, help='控制生成题目的个数')
# parser.add_argument('--r', help='控制题目中数值（自然数、真分数和真分数分母）的范围')
#
# args = parser.parse_args()
# n = args.n
# r = args.r

n = 5
r = 10


class Arithmetic:
    def __init__(self):
        self.result = -1
        while self.result < 0:
            self.formula = self.generate_arithmetic()
            try:
                self.result = self.calculate_arithmetic(self.formula)
            except ZeroDivisionError:
                continue


    @staticmethod
    def generate_arithmetic():
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
        formula = formula.replace('=', '')
        formula = formula.replace('×', '*')
        formula = formula.replace('÷', '/')
        formula = formula.replace(' ', '')

        res = eval(re.sub(r'(\d+)', r'Fraction(\1)', formula))

        return res


def write_exercises(formula):
    with open('Exercises.txt', 'w') as f:
        for i, arithmetic in enumerate(formula):
            f.write(f"{i + 1}. {arithmetic}\n")


def read_exercises():
    with open('Exercises.txt', 'r') as f:
        formula = f.readlines()
    formula = [''.join(arithmetic.split(' ')[1:-1]) for arithmetic in formula]
    return formula


def write_answer(answer):
    with open('Answer.txt', 'w') as f:
        for i, ans in enumerate(answer):
            if ans > 1 and ans.numerator > ans.denominator != 1:
                res = f"{ans.numerator // ans.denominator}\'{ans.numerator % ans.denominator}/{ans.denominator}"
            else:
                res = ans
            f.write(f"{i + 1}. {res}\n")


def read_answer():
    with open('Answer_my.txt', 'r') as f:
        answer = f.readlines()
    formula = [''.join(ans.split(' ')[1:])[:-1] for ans in answer]
    return formula


def write_grade(correct_info, wrong_info):
    with open('Grade.txt', 'w') as f:
        f.write(correct_info+"\n")
        f.write(wrong_info)


def exercises():
    arithmetic_dict = {}
    while len(arithmetic_dict) != n:
        # 生成一道新的题目
        arithmetic = Arithmetic()
        arithmetic_dict[arithmetic.formula] = (arithmetic.result)

    write_exercises(arithmetic_dict.keys())
    write_answer(arithmetic_dict.values())


def correct_answer():
    key = read_exercises()
    value = read_answer()
    arithmetic_dict = dict(zip(key, value))

    correct_idx = []
    wrong_idx = []
    for idx, (k, v) in enumerate(arithmetic_dict.items()):
        if Fraction(v) == Arithmetic.calculate_arithmetic(k):
            correct_idx.append(idx+1)
        else:
            wrong_idx.append(idx+1)
    correct_info = f"Correct: {len(correct_idx)} ({''.join([f'{idx},' for idx in correct_idx])})"
    wrong_info = f"Wrong: {len(wrong_idx)} ({''.join([f'{idx},' for idx in wrong_idx])})"
    write_grade(correct_info, wrong_info)


if __name__ == '__main__':
    # exercises()
    correct_answer()
