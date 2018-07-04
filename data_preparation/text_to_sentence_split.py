import re
import os
import argparse
import fnmatch

# for using script in pycharm
os.chdir('/home/anz2/PycharmProjects/Sentinel/data_preparation/')

# declare default variables
georgian_letters = 'აბგდევზთიკლმნოპჟრსტუფქღყშჩცძწჭხჯჰ'
digits = '0123456789'
punctuation_marks = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \n'
whitespaces = '\t\n\r\x0b\x0c'


def read_text(in_path):
    with open(in_path) as file:
        content = file.read()
        # print(content)
        text = ''
        for c in content:
            if c in georgian_letters or c in digits or c in punctuation_marks:
                text += c
    return text


def strip_whitespaces(text):
    for whitespace in whitespaces:
        text = text.replace(whitespace, ' ')
    return text


def remove_initials(text):
    text = re.sub(' \w\.', '', text)
    return text


def split_dot_separated_sentences(text):
    sentences = text.split('. ')
    return sentences


def split_sentences_into_words(sentences):
    words_of_sentences = []
    for sentence in sentences:
        for punctuation in punctuation_marks.replace(' ', ''):
            sentence = sentence.replace(punctuation, '')

        for digit in digits:
            sentence = sentence.replace(digit, '')

        sentence = re.sub(' +', ' ', sentence)
        sentence.strip()
        words_list = sentence.split(' ')
        if '' in words_list:
            words_list.remove('')
        if len(' '.join(words_list)) >= min_sentence_length:
            words_of_sentences.append(words_list)
    return words_of_sentences


def save_sentences(words_of_sentences, out_path):
    with open(out_path, 'w') as out_file:
        for sentence_words in words_of_sentences:
            out_sentence = ' '.join(sentence_words)
            out_file.write(out_sentence + '\n')


def concatenate_files_in_dir(output_dir, file_name):
    file_path = os.path.join(output_dir, file_name)
    full_text = ''
    for root, dirs, files in os.walk(output_dir):
        for file in files:
            if file.endswith('.txt'):
                with open(os.path.join(output_dir, file), 'r') as f:
                    full_text += f.read()
    with open(file_path, 'w') as f:
        f.write(full_text)


def run_all_steps(input_path, output_path):
    content = read_text(input_path)
    content = strip_whitespaces(content)
    content = remove_initials(content)
    content_sentences = split_dot_separated_sentences(content)
    content_words_of_sentences = split_sentences_into_words(content_sentences)
    save_sentences(content_words_of_sentences, output_path)


def run_all_steps_for_directory(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    for root, _, files in os.walk(input_dir):
        out_root = root.replace(input_dir, output_dir)
        if not os.path.exists(out_root):
            os.mkdir(out_root)
        for file in fnmatch.filter(files, "*.txt"):
            run_all_steps(os.path.join(root, file), os.path.join(out_root, file))


def concatenate_all_files_in_directory(input_dir, output_file=None):
    if output_file is None:
        output_file = str(input_dir.rstrip('/'))
        output_file = output_file.replace(output_file.split('/')[-1], 'BIG_DATA_SPLITTED.txt')
    if os.path.exists(output_file):
        raise ValueError(f'Output file {output_file} already exists!\nPlease remove it and run again!.')
    with open(output_file, 'a') as out:
        for root, _, files in os.walk(input_dir):
            for file in fnmatch.filter(files, "*.txt"):
                with open(os.path.join(root, file), 'r') as file_reader:
                    opened_file = file_reader.read()
                    out.write(opened_file)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser('Splitting raw text into words of sentences...')
    arg_parser.add_argument('-ifp',
                            '--input_file_path',
                            dest='in_path',
                            required=False,
                            default='',
                            help='path of file containing text.')
    arg_parser.add_argument('-ofp',
                            '--output_file_path',
                            dest='out_path',
                            required=False,
                            default='',
                            help='path of file containing sentences.')
    arg_parser.add_argument('-ifd',
                            '--input_files_directory',
                            dest='in_dir',
                            required=False,
                            default='',
                            help='directory of files containing text.')
    arg_parser.add_argument('-ofd',
                            '--output_files_directory',
                            dest='out_dir',
                            required=False,
                            default='',
                            help='directory of files containing sentences.')
    arg_parser.add_argument('-msl',
                            '--min_sentence_length',
                            type=int,
                            dest='min_sentence_length',
                            required=False,
                            default=25,
                            help='minimum length of sentence.')
    arg_parser.add_argument('-co',
                            '--concatenate_outputs',
                            dest='concatenate_outputs',
                            required=False,
                            action='store_true',
                            default=False,
                            help='output only one file in dir with concatenated text from all files')
    arg_parser.add_argument('-ds',
                            '--do_splitting',
                            dest='do_splitting',
                            required=False,
                            action='store_true',
                            default=False,
                            help='do text splitting into words of sentences')
    arg_parser.add_argument('-cofp',
                            '--concatenated_output_file_path',
                            dest='concatenated_output_file_path',
                            required=False,
                            default='',
                            help='path of file with concatenated text from all files')
    flags, _ = arg_parser.parse_known_args()

    in_path = flags.in_path
    out_path = flags.out_path
    in_dir = flags.in_dir
    out_dir = flags.out_dir
    do_splitting = flags.do_splitting
    concatenate_outputs = flags.concatenate_outputs
    min_sentence_length = flags.min_sentence_length
    concatenated_output_file_path = flags.concatenated_output_file_path

    if os.path.exists(in_path) and do_splitting:
        run_all_steps(in_path, out_path)
    elif os.path.exists(in_dir) and do_splitting:
        run_all_steps_for_directory(in_dir, out_dir)
        if concatenate_outputs:
            concatenate_all_files_in_directory(out_dir, concatenated_output_file_path)
    elif os.path.exists(in_dir) and concatenate_outputs:
        concatenate_all_files_in_directory(in_dir, concatenated_output_file_path)
    else:
        print('please provide directory paths or file paths containing text files and choose any available operation !')
