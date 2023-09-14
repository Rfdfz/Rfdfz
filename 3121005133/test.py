import unittest
import random
import string
from main import *


class MyTestCase(unittest.TestCase):
    def test_same_string(self):
        characters = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(characters) for _ in range(1000))
        self.assertEqual(cal_similarity(random_string, random_string, 'cosine_similarity'), 1.0)

    def test_empty_string(self):
        empty_string = ''
        self.assertEqual(cal_similarity(empty_string, empty_string, 'cosine_similarity'), ValueError)

    def test_read_file(self):
        self.assertEqual(read_file('不存在的路径', '不存在的路径'), FileNotFoundError)

    def test_args_paser(self):
        self.assertEqual(main(), TypeError)

    def test_tokenizer(self):
        tokenizer = Tokenizer()
        self.assertEqual(tokenizer(1), TypeError)

    def test_tokenizer_add_extra_punctuation(self):
        tokenizer = Tokenizer()
        self.assertEqual(tokenizer.add_extra_punctuation(1), TypeError)

    def test_save_file_similarity_type(self):
        self.assertEqual(save_answer('Test.txt', 'Error Type'), TypeError)

    def test_save_file_similarity_value_positive(self):
        self.assertEqual(save_answer('Test.txt', 10.0), ValueError)

    def test_save_file_similarity_value_negative(self):
        self.assertEqual(save_answer('Test.txt', -1.0), ValueError)

    def test_similarity_type(self):
        self.assertEqual(cal_similarity("Hello World", "Hello World", "earth_mover_distance"), ValueError)
