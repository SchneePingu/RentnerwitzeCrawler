from argparse import ArgumentParser, FileType
from logging import error
from pathlib import Path
from sys import exit, stdout
import cv2
import pytesseract


def parse_command_line_arguments():
    parser = ArgumentParser(description='Process Rentnerwitz.')

    parser.add_argument('file', metavar='INPUTFILE',
        type=str, help='path to image with Rentnerwitz')
    parser.add_argument('-c', '--confidence', metavar='CONFIDENCE', default=80,
        type=int, help='minimum confidence level for an element to be recognized as word')

    return parser.parse_args()


def parse_image(arguments):
    for text_block in get_text_blocks(read_text(arguments)):
        print_non_empty_text_block(format_text_block(text_block))

def read_text(arguments):
    return remove_noise(
        arguments, pytesseract.image_to_data(
            cv2.imread(arguments.file), lang='deu', output_type='data.frame'))

def remove_noise(arguments, text):
    return text[text.conf >= arguments.confidence]

def get_text_blocks(text):
    return text.groupby('block_num')['text'].apply(list)

def format_text_block(text_block):
    word_separator = ' '
    return word_separator.join([word.strip() for word in text_block])

def print_non_empty_text_block(text_block):
    empty_string = ''
    if text_block != empty_string:
        print(text_block)

def main():
    arguments = parse_command_line_arguments()
    parse_image(arguments)
    
    return 0


if __name__ == "__main__":
    try:
        exit(main())
    except Exception as exception:
        error(exception)
        exit(1)

