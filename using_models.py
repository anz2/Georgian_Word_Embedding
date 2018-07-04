import argparse
import os
from math import sqrt
from pyfasttext import FastText

import gensim


class WordModel:
    def __init__(self):
        self.model_name = None
        self.model = None
        self.model_path = None

    def get_vector(self, word):
        try:
            vector = self.model[word]
        except KeyError:
            vector = None

        return vector

    def get_full_path(self, relative_path):
        pwd = os.path.dirname(os.path.abspath(__file__))
        pwd = os.path.join(pwd, relative_path)
        return pwd

    def path_exists(self, relative_path):
        full_path = self.get_full_path(relative_path)
        return os.path.exists(full_path)

    def validate_model_path(self, path):
        if path is None or not self.path_exists(path):
            if self.model_name == 'fasttext':
                default_path = self.get_full_path('models/fasttext_skipgram_model.bin')
            else:
                default_path = self.get_full_path('models/word2vec_skipgram.w2v')

            return default_path
        else:
            path = self.get_full_path(path)

            return path

    def validate_model_name(self, name):
        if name is not None and name in ['fasttext', 'word2vec']:
            correct_name = name
        else:
            correct_name = 'fasttext'

        return correct_name

    def get_numpy_vector(self, word):
        if self.model_name == 'fasttext':
            return self.model.get_numpy_vector(word, normalized=True)
        else:
            try:
                np_vector = self.model.wv(word, normalized=True)
            except KeyError:
                np_vector = None

            return np_vector

    def load_model(self):
        if not os.path.exists(self.model_path):
            raise FileNotFoundError('model file not found!')
        if self.model_name == 'fasttext':
            self.model = FastText(self.model_path)
        else:
            self.model = gensim.models.Word2Vec.load(self.model_path, mmap='r')

    def get_most_similar_words(self, word, k=5):
        if self.model_name == 'fasttext':
            return self.model.nearest_neighbors(word, k=k)
        else:
            try:
                similar_words = self.model.similar_by_word(word, topn=k)
            except KeyError:
                similar_words = []

            return similar_words

    def get_words_for_vector(self, vector, k=3):
        if self.model_name == 'fasttext':
            return self.model.words_for_vector(vector, k)
        else:
            try:
                similar_words = self.model.similar_by_vector(vector, topn=k)
            except KeyError:
                similar_words = []

            return similar_words

    def similarity(self, word_1, word_2):
        if self.model_name == 'fasttext':
            return self.model.similarity(word_1, word_2)
        else:
            try:
                sim = self.model.wv.similarity(word_1, word_2)
            except KeyError:
                sim = 0
            return sim

    def word_analogies(self, words, k=3):
        word_list = words.split()
        if len(word_list) == 3:
            word_vec_1 = self.get_numpy_vector(word_list[0])
            word_vec_2 = self.get_numpy_vector(word_list[1])
            word_vec_3 = self.get_numpy_vector(word_list[2])
            word_vec_4 = word_vec_3 - word_vec_1 + word_vec_2
            return self.get_words_for_vector(word_vec_4, k)

    def odd_one_out(self, words):
        word_list = words.split()
        if len(word_list) == 4:
            scores = [0.0, 0.0, 0.0, 0.0]

            for index in range(len(word_list)):
                for another_word in word_list:
                    if another_word != word_list[index]:
                        scores[index] += self.similarity(word_list[index], another_word) ** 2
                scores[index] = sqrt(scores[index] / 3.0)

            min_index = scores.index(min(scores))

            result = f'{word_list[min_index]}\n'
            result += '\n'

            scores, word_list = zip(*sorted(zip(scores, word_list)))
            for word, score in zip(word_list, scores):
                result += f'{word}: {score}\t'

            return result


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser('using technique of word embedding in high dimensional vectors...')

    arg_parser.add_argument('-wanl',
                            '--word_analogies',
                            dest='word_analogies',
                            required=False,
                            action='store_true',
                            help='given "king queen man" returns woman with high probability.')
    arg_parser.add_argument('-msw',
                            '--most_similar_words',
                            dest='most_similar_words',
                            required=False,
                            action='store_true',
                            help='find k most similar words for given word.')
    arg_parser.add_argument('-ooo',
                            '--odd_one_out',
                            dest='odd_one_out',
                            required=False,
                            action='store_true',
                            help='given " apple banana potato pear" removes potato with high probability .')
    arg_parser.add_argument('-w',
                            '--word',
                            type=str,
                            dest='word',
                            required=False,
                            default=None,
                            help='one word or several words separated by space.')
    arg_parser.add_argument('-m',
                            '--model_name',
                            type=str,
                            dest='model_name',
                            required=False,
                            default='fasttext',
                            help='choose model name from models: {fasttext (ft), word2vec (wv)}.')
    arg_parser.add_argument('-mp',
                            '--model_path',
                            type=str,
                            dest='model_path',
                            required=False,
                            default=None,
                            help='give the model path to load.')
    arg_parser.add_argument('-k',
                            '--neighbours',
                            type=int,
                            dest='k',
                            required=False,
                            default=None,
                            help='number of most similar words to find for a given word.')
    arg_parser.add_argument('-cmp',
                            '--compare_models',
                            dest='compare_models',
                            required=False,
                            action='store_true',
                            default=None,
                            help='show both model results.')

    flags, _ = arg_parser.parse_known_args()

    word = flags.word
    k = flags.k
    compare_models = flags.compare_models

    if not compare_models:
        model = WordModel()
        model.model_name = model.validate_model_name(flags.model_name)
        model.model_path = model.validate_model_path(flags.model_path)
        model.load_model()
    else:
        fasttext_model = WordModel()
        fasttext_model.model_name = fasttext_model.validate_model_name('fasttext')
        fasttext_model.model_path = fasttext_model.validate_model_path('using default path')
        fasttext_model.load_model()

        word2vec_model = WordModel()
        word2vec_model.model_name = word2vec_model.validate_model_name('word2vec')
        word2vec_model.model_path = word2vec_model.validate_model_path('using default path')
        word2vec_model.load_model()

    if not compare_models:
        if flags.most_similar_words:
            while True:
                word = input()
                print(model.get_most_similar_words(word, k))
        elif flags.word_analogies:
            while True:
                word = input()
                print(model.word_analogies(word, k))
        elif flags.odd_one_out:
            while True:
                word = input()
                print(model.odd_one_out(word))
        else:
            print("Please use --help to see available functions and samples for each of them")
    else:
        if flags.most_similar_words:
            while True:
                word = input()
                print('FastText:')
                print(fasttext_model.get_most_similar_words(word, k))
                print('Word2Vec:')
                print(word2vec_model.get_most_similar_words(word, k))
        elif flags.word_analogies:
            while True:
                word = input()
                print('FastText:')
                print(fasttext_model.word_analogies(word, k))
                print('Word2Vec:')
                print(word2vec_model.word_analogies(word, k))
        elif flags.odd_one_out:
            while True:
                word = input()
                print('FastText:')
                print(fasttext_model.odd_one_out(word))
                print('Word2Vec:')
                print(word2vec_model.odd_one_out(word))
        else:
            print("Please use --help to see available functions and samples for each of them")
