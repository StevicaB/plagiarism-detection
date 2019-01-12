#!/usr/bin/python
# -*- coding: utf-8 -*-

'''Module responsible for preprocessing the input files.'''

import os
import shutil
import io

def remove_suffix(path):
    '''Removes the suffix from a given path.'''

    return path.split('.')[0]

def get_plain_text(path):
    '''Extracting the plain text from a given file.'''

    if path.endswith('.txt'):
        return

    text = ''

    with io.open(os.path.join(remove_suffix(path), 'plainText.txt'), 'w',
                 encoding='utf8') as text_file:
        text = text_file.read()

    with io.open(path, 'r', encoding='utf8') as plain_text_file:
        plain_text_file.write(text)

def get_references(path):
    '''Extracting the references from a given file.'''

    text = ''
    references = []

    with io.open(os.path.join(remove_suffix(path), 'plainText.txt'), 'r',
                 encoding='utf8') as plain_text_file:
        text = plain_text_file.readlines()

    for line in text:
        words = line.split(' ')

        for word in words:
            if 'http' in word and word not in references:
                references.append(word)

    with io.open(os.path.join(remove_suffix(path), '/references.txt'),
                 'w', encoding='utf8') as ref_file:
        for link in references:
            ref_file.write(link)


def get_paragraphs(path):
    '''Extracting paragraphs from a given file.'''

    text = ''
    count = 1

    with io.open(os.path.join(remove_suffix(path), 'plainText.txt'),
                 'r', encoding='utf8') as plain_text_file:
        text = plain_text_file.readlines()

    #prepend = os.path.join(os.getcwd(), 'temp', remove_suffix(os.path.basename(path)))
    os.chdir(os.path.join('temp', remove_suffix(os.path.basename(path))))

    for line in text:
        words = line.split(' ')
        if len(words) > 20 and not os.path.exists(os.path.join('paragraf'+str(count))):
            os.mkdir(os.path.join('paragraf'+str(count)))

            with io.open(os.path.join('paragraf'+str(count), 'paragrafText.txt'), 'w',
                         encoding='utf8') as paragraph_file:
                paragraph_file.write(line)

            count += 1

    os.chdir('..')
    os.chdir('..')

def preprocess(path):
    '''Copies the file into the local directory and extracts the plain text,
    references and paragraphs.'''

    if not os.path.isdir('temp'):
        os.mkdir('temp')

    if '.' in path:
        new_path = os.path.join(os.getcwd(), 'temp', os.path.basename(path))
        shutil.copy(path, new_path)

        if not os.path.isdir(remove_suffix(new_path)):
            os.mkdir(remove_suffix(new_path))

        if path.endswith('.txt'):
            get_plain_text(new_path)
            get_references(new_path)
            get_paragraphs(new_path)
