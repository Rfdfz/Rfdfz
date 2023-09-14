import jieba
import argparse
import numpy as np
import logging
from sklearn.feature_extraction.text import TfidfVectorizer

# 将jieba的日志级别设置为ERROR，禁止输出信息
jieba.setLogLevel(logging.ERROR)


# 词元化
class Tokenizer(object):
    def __init__(self):
        # 标点符号
        self.punctuation = "，！？。《》；：\n“”、 "

    def __call__(self, string):
        try:
            if not isinstance(string, str):
                raise TypeError
        except TypeError:
            print('请输入正确的类型')
            return TypeError

        # 去除标点符号，以便分词
        for p in self.punctuation:
            string = string.replace(p, '')

        # 分词
        string = ' '.join(jieba.lcut(string))

        return string

    def add_extra_punctuation(self, extra_punctuation):
        try:
            if not isinstance(extra_punctuation, str):
                raise TypeError
        except TypeError:
            print("请输入正确的类型")
            return TypeError

        self.punctuation += extra_punctuation


def read_file(orig_path, orig_modify_path):
    try:
        with open(orig_path) as f1, open(orig_modify_path) as f2:
            orig_string = f1.read()
            orig_modify_string = f2.read()
    except FileNotFoundError as e:
        print('请输入正确的文件路径:', e)
        return FileNotFoundError
    else:
        return orig_string, orig_modify_string


def save_answer(answer_path, similarity):
    try:
        if not isinstance(similarity, float):
            raise TypeError
        elif similarity > 1.0 or similarity < 0:
            raise ValueError
    except TypeError:
        print("相似度类型错误")
        return TypeError
    except ValueError:
        print("相似度计算错误")
        return ValueError

    # 保存答案
    with open(answer_path, mode='w') as f:
        f.write("%.2f" % similarity)


def cal_similarity(orig_string, orig_modify_string, similarity_type):
    # Tokenize
    tokenizer = Tokenizer()
    orig_list, orig_modify_list = tokenizer(orig_string), tokenizer(orig_modify_string)

    # Vectorize
    try:
        vectorizer = TfidfVectorizer()
        feature = vectorizer.fit_transform([orig_list, orig_modify_list]).toarray()
    except ValueError as e:
        print('请输入正确的文本:', e)
        return ValueError
    else:
        try:
            if similarity_type not in ['cosine_similarity', 'euclidean_distance']:
                raise ValueError
        except ValueError:
            print("请输入正确的相似度类型")
            return ValueError
        else:
            if similarity_type == 'cosine_similarity':
                similarity = feature[0] @ feature[1].T / (np.linalg.norm(feature[0]) * np.linalg.norm(feature[1]))
                return similarity
            elif similarity_type == 'euclidean_distance':
                similarity = 1 / (1 + np.exp(-np.linalg.norm(feature[1] - feature[0])))
                return similarity


def main():
    # 定义命令行解析器
    parser = argparse.ArgumentParser()

    # 添加命令行参数
    parser.add_argument('--orig_path', type=str, help='原文绝对路径')
    parser.add_argument('--orig_modify_path', type=str, help='被检测文章绝对路径')
    parser.add_argument('--answer_path', type=str, help='答案文件绝对路径')
    parser.add_argument('--similarity_type', type=str, default='cosine_similarity', help='相似度类型: cosine_similarity, euclidean_distance')

    args = parser.parse_args()

    # 解析命令行参数
    orig_path = args.orig_path
    orig_modify_path = args.orig_modify_path
    answer_path = args.answer_path
    similarity_type = args.similarity_type

    try:
        if not isinstance(orig_path, str) or not isinstance(orig_modify_path, str) or not isinstance(answer_path, str) or not isinstance(similarity_type, str):
            raise TypeError
    except TypeError:
        print('请检查传入的参数类型是否正确')
        return TypeError

    orig_string, orig_modify_string = read_file(orig_path, orig_modify_path)

    similarity = cal_similarity(orig_string, orig_modify_string, similarity_type)

    save_answer(answer_path, similarity)


if __name__ == '__main__':
    main()