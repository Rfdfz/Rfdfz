import unittest
import modules


class MyTestCase(unittest.TestCase):

    # 测试生成算式时参数范围不是自然数
    def test_arithmetic_parameters(self):
        modules.Arithmetic(-2)

    # 测试生成10条算式是否符合要求
    def test_generate_formular(self):
        for _ in range(10):
            formular = modules.Arithmetic.generate_arithmetic(8)
            print(formular)

    # 测试能否生成一万条算式
    def test_generate_enough_formular(self):
        for _ in range(10000):
            formular = modules.Arithmetic.generate_arithmetic(10)
            print(formular)

    # 测试计算的答案表示是否符合要求
    def test_answer_express(self):
        formular = '3 + 6 ÷ 7 ='
        answer = modules.Arithmetic.calculate_arithmetic(formular)
        print(formular, "", answer)

    # 测试生成算式后计算的答案是否正确
    def test_formular_answer(self):
        for _ in range(10):
            formular = modules.Arithmetic.generate_arithmetic(8)
            answer = modules.Arithmetic.calculate_arithmetic(formular)
            print(formular, " ", answer)

    # 测试将生成的题目和答案写入指定文件
    def test_write_file(self):
        formular_list = []
        answer_list = []
        for _ in range(10):
            arithmetic = modules.Arithmetic(10)
            formular_list.append(arithmetic.formula)
            answer_list.append(arithmetic.result)
        modules.write_exercises(formular_list)
        modules.write_answer(answer_list)

    # 测试读取的题目文件和答案文件不存在
    def test_read_not_exist_file(self):
        formular_list = modules.read_exercises("train.txt")
        answer_list = modules.read_answer("result.txt")
        print(formular_list)
        print(answer_list)

    # 测试将题目文件和答案文件进行读取
    def test_read_file(self):
        formular_list = modules.read_exercises("Exercises.txt")
        answer_list = modules.read_answer("Answer.txt")
        print(formular_list)
        print(answer_list)

    # 测试生成算式和计算相应答案，并写入到指定文件
    def test_exercises(self):
        modules.exercises(10, 10)

    # 测试校对答案
    def test_correct_answer(self):
        modules.correct_answer("Exercises.txt", "Answer.txt")


if __name__ == '__main__':
    unittest.main()
