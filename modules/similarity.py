#!/usr/bin/python
# -*- coding: utf-8 -*-

'''Module responsible for calculating the similarities in different categories.'''

import os
import io
import math

def get_similarity_references(path1, path2):
    '''Calculate the reference usage similiarty between two files.'''

    score = 0
    output = []
    string_ref = []
    bag1, bag2 = [], []

    output.extend([u'Сличност на референци меѓу ', os.path.basename(path1), u' и ',
                   os.path.basename(path2), '.\n\n'])
    path1 = os.path.join(path1, 'references.txt')
    with io.open(path1, 'r', encoding='utf8') as file_ref:
        for line in file_ref.readlines():
            bag1.append(line)

    path2 = os.path.join(path2, 'references.txt')
    with io.open(path2, 'r', encoding='utf8') as file_ref:
        for line in file_ref.readlines():
            bag2.append(line)

    for reference in bag1:
        if reference in bag2:
            score += 1
            string_ref.extend(['-', reference, '\n\n'])

    string_ref = ''.join(string_ref)

    if bag1 or bag2:
        freq = float(2*score)/(len(bag1) + len(bag2))
    elif not bag1 and not bag2:
        freq = 1
    else:
        freq = 0

    output.extend([u'Сличноста на референците е ', str(freq*100), '%.\n\n',
                   u'Број на референци на ', os.path.basename(path1), u' е ',
                   str(len(bag1)), '.\n\n', u'Број на референците на ',
                   os.path.basename(path1), u' е ', str(len(bag2)), '.\n\n',
                   u'Вкупно ', str(score), u' идентични референци.\n\n', string_ref])

    output = ''.join(output)

    return [freq, output]

def filter_word(word):
    '''Removing unwanted characters at the beginning and at the end
    of a given word.'''

    filter_symbols = ['[', '(', '{', u'„', u'“', ']', ')', '}', ',', '.', '!', '?', ':', ';']

    while len(word) > 1 and word[0] in filter_symbols:
        word = word[1:]
    while len(word) > 1 and word[-1] in filter_symbols:
        word = word[:-1]

    return word.strip().lower()

def paraphrases_trigrams(word1, word2, word3):
    '''Extract all trigram combinations out of three words.'''

    trigrams = []

    trigrams.append(word1+' '+word2+' '+word3)
    trigrams.append(word1+' '+word3+' '+word2)
    trigrams.append(word2+' '+word1+' '+word3)
    trigrams.append(word2+' '+word3+' '+word1)
    trigrams.append(word3+' '+word1+' '+word2)
    trigrams.append(word3+' '+word2+' '+word1)

    return trigrams

def get_similarity_paraphrased_text(path1, path2):
    '''Returns the similarity between two texts when the texts are paraphrased on
    a trigram level.'''

    score = 0
    output = []
    paraphrased = []

    output.extend([u'Сличност на парафразиран текст меѓу ', os.path.basename(path1),
                   u' и ', os.path.basename(path2), '.\n\n'])

    path1 = os.path.join(path1, 'plainText.txt')
    with io.open(path1, 'r', encoding='utf8') as text_file:
        text1 = text_file.read()

    path2 = os.path.join(path2, 'plainText.txt')
    with io.open(path2, 'r', encoding='utf8') as text_file:
        text2 = text_file.read()

    # Removal of unwanted symbols
    words = text2.split(' ')
    text2 = []
    for word1 in words:
        text2.extend([filter_word(word1).strip(), ' '])
    text2 = ''.join(text2)

    words = text1.split(' ')
    word1 = filter_word(words[0])
    word2 = filter_word(words[1])

    for i in range(2, len(words)):
        word3 = filter_word(words[i])

        if word3 == '':
            continue

        for trigram in paraphrases_trigrams(word1, word2, word3):
            if trigram in text2:
                paraphrased.extend([u'\t-пермутација: ', trigram, u' оригинален:',
                                    word1, ' ', word2, ' ', word3, '\n'])
                score += 1
                break

        word1, word2 = word2, word3

    paraphrased = ''.join(paraphrased)

    freq = float(score)/(len(words) -2)

    output.extend([u'Сличноста на парафразиран текст е ', str(freq*100), u'%.\n\n',
                   u'Вкупно ', str(score), u' идентични пермутации на триграми.\n\n',
                   paraphrased])

    output = ''.join(output)

    return [freq, output]

def cosine_similarity(bag_words1, bag_words2):
    '''Calculate cosine similarity between two bag of words.'''

    numerator = 0
    denominator1 = 0
    denominator2 = 0

    for i, _ in enumerate(bag_words1):
        numerator += (float(bag_words1[i])*float(bag_words2[i]))
        denominator1 += (float(bag_words1[i])*float(bag_words1[i]))
        denominator2 += (float(bag_words2[i])*float(bag_words2[i]))

    if math.sqrt(denominator1)*math.sqrt(denominator2) != 0:
        return float(numerator)/(math.sqrt(denominator1)*math.sqrt(denominator2))
    return 0

def get_bag_words(text):
    '''Getting a bag of words composed of unigrams, bigrams and trigrams.'''

    bag_words = []

    words = text.split(' ')
    n_words = len(words)

    # Unigrams
    for word in words:
        word = filter_word(word)
        if word not in bag_words:
            bag_words.append(word)

    # Bigrams
    if n_words > 1:
        first_word = filter_word(words[0])
        for i in range(1, n_words):
            second_word = filter_word(words[i])
            if second_word != '':
                combination = first_word+' '+second_word
                if combination not in bag_words:
                    bag_words.append(combination)
                first_word = second_word
    # Trigrams
    if n_words > 2:
        first_word = filter_word(words[0])
        second_word = filter_word(words[1])
        for i in range(2, n_words):
            third_word = filter_word(words[i])
            if third_word != '':
                combination = first_word+' '+second_word+' '+third_word
                if combination not in bag_words:
                    bag_words.append(combination)
                first_word = second_word
                second_word = third_word

    return bag_words

def get_dice(text1, text2):
    '''Calculating dice score of two texts.'''

    if len(text1) > 1 and len(text2) > 1:

        # Create bigram list.
        bigram_list1, bigram_list2 = [], []

        for i in range(1, len(text1)):
            bigram = text1[i-1:i+1]
            if bigram not in bigram_list1:
                bigram_list1.append(bigram)

        for i in range(1, len(text2)):
            bigram = text2[i-1:i+1]
            if bigram not in bigram_list2:
                bigram_list2.append(bigram)

        # Count common bigrams.
        numerator = 0

        for bigram in bigram_list1:
            if bigram in bigram_list2:
                numerator += 1

        return float(2*numerator)/(len(bigram_list1) + len(bigram_list2))

    return 0

def update_clusters(clusters, cluster1, cluster2, flag, treshold):
    '''Updates the clusters if two elements are similar above certain treshold.'''

    for element1 in cluster1:
        for element2 in cluster2:
            similarity = get_dice(element1, element2)
            if similarity >= treshold:
                temp = list(set(cluster1) | set(cluster2))
                clusters.remove(cluster1)
                clusters.remove(cluster2)
                clusters.append(temp)
                flag = True
                break
            if flag:
                break
        if flag:
            break
    return flag, clusters

def clustering(bag, treshold=0.7):
    ''' Clusters similar words and groups them according to their root.'''

    clusters = []
    dictionary = {}

    for element in bag:
        clusters.append([element])
    flag = True

    while flag:
        flag = False
        for cluster1 in clusters:
            for cluster2 in clusters:
                if cluster1 == cluster2:
                    continue
                flag, clusters = update_clusters(clusters, cluster1, cluster2,
                                                 flag, treshold)
                if flag:
                    break

    for cluster in clusters:
        dictionary[cluster[0]] = cluster
    return dictionary

def transform_text(text, clusters):
    ''' Transforms each word into its root in a given text.'''

    transformed_text = ''

    words = text.split(' ')
    for word in words:
        flag = False
        for key in clusters.keys():
            if word in clusters[key]:
                transformed_text += key+ ' '
                flag = True
        if not flag:
            transformed_text += word+' '

    return transformed_text.strip()

def get_list_present_words(text, bag):
    '''For each word in the bag, checks if it is contained in the text.'''

    presence_list = []

    words = text.split(' ')
    for element in bag:
        if element in words:
            presence_list.append(1)
        else:
            presence_list.append(0)

    return presence_list

def get_uni_bag_words(text):
    '''Extract unigrams and store them in bag of words.'''

    bag_words = []

    words = text.split(' ')

    for word in words:
        word = filter_word(word)
        if word not in bag_words:
            bag_words.append(word)

    return bag_words

def get_similarity_paragraphs(paragraph1, paragraph2):
    '''Calculating similarity between two paragraphs.'''

    bag = get_uni_bag_words(paragraph1)
    bag2 = get_uni_bag_words(paragraph2)

    for element in bag2:
        if element not in bag:
            bag.append(element)

    print('Clustering... Please wait...')
    clusters = clustering(bag)

    transformed_text1 = transform_text(paragraph1, clusters)
    transformed_text2 = transform_text(paragraph2, clusters)

    bag = get_bag_words(transformed_text1)
    bag2 = get_bag_words(transformed_text2)

    for element in bag2:
        if element not in bag:
            bag.append(element)

    present_words1 = get_list_present_words(transformed_text1, bag)
    present_words2 = get_list_present_words(transformed_text2, bag)

    score = cosine_similarity(present_words1, present_words2)

    return score

def get_similarity_texts(path1, path2):
    ''' Calculating the similarity between two texts.'''

    freq = 0
    count = 0
    output = []
    text = []

    output.extend([u'Сличност на текст меѓу ', os.path.basename(path1),
                   u' и ', os.path.basename(path2), '.\n\n'])

    for paragraph_name1 in os.listdir(path1):

        if '.' in paragraph_name1:
            continue

        with io.open(os.path.join(path1, paragraph_name1, 'paragrafText.txt'), 'r',
                     encoding='utf8') as paragraph_file:
            text1 = paragraph_file.read()

        count += 1
        max_similarity = 0
        max_paragraph = max_paragraph_name = ''

        for paragraph_name2 in os.listdir(path2):

            if '.' in paragraph_name2:
                continue

            with io.open(os.path.join(path2, paragraph_name2, 'paragrafText.txt'),
                         'r', encoding='utf8') as paragraph_file:
                text2 = paragraph_file.read()

            similarity = get_similarity_paragraphs(text1, text2)

            if similarity > max_similarity:
                max_similarity = similarity
                max_paragraph = text2
                max_paragraph_name = paragraph_name2

        freq += max_similarity

        text.extend([u'Сличноста меѓу ', path1, '/', paragraph_name1, u' и ',
                     path2, '/', max_paragraph_name, u' е ', str(max_similarity*100), '%.\n\n',
                     path1, '/', paragraph_name1, '\n', text1, '\n\n', path2, '/',
                     max_paragraph_name, '\n', max_paragraph, '\n\n\n'])

    text = ''.join(text)

    if count != 0:
        freq = float(freq)/count

    output.extend([u'Сличноста на текстот е ', str(freq*100), '%.\n\n', text])

    output = ''.join(output)

    return [freq, output]

def get_style_symbols(style, text, n_chars):
    '''Getting the frequencies for some of the symbols in the text.'''

    # Relative frequency of space after comma.
    if text.count(',') != 0:
        style.append(text.count(', ')/text.count(','))
    else:
        style.append(0)

    # Relative frequency of space after comma, ! and ?.
    if (text.count('.')+text.count('!')+text.count('?')) != 0:
        style.append(float(text.count('. ')+text.count('! ')+text.count('? ')) / \
                     (text.count('.')+text.count('!')+text.count('?')))
    else:
        style.append(0)

    # Relative full stop frequency.
    if n_chars != 0:
        style.append(text.count('.')/n_chars)
    else:
        style.append(0)

    # Relative question mark frequency.
    if n_chars != 0:
        style.append(text.count('?')/n_chars)
    else:
        style.append(0)

    # Relative exclamation mark frequency.
    if n_chars != 0:
        style.append(text.count('!')/n_chars)
    else:
        style.append(0)

    return style

def get_style(text):
    '''Extracting the writing style from a given text. This is done by calculating
    the frequency of a certain word usage.'''

    style = []

    words = text.split(' ')

    n_words = float(len(words))
    n_chars = float(len(text))

    style = get_style_symbols(style, text, n_chars)

    # Relative comma frequency.
    if n_chars != 0:
        style.append(text.count(',')/n_chars)
    else:
        style.append(0)

    # Average sentence size.
    if text.count('.')+text.count('!')+text.count('?') != 0:
        style.append(n_words/(text.count('.')+text.count('!')+text.count('?')))
    else:
        style.append(0)

    style.append(text.count(u'è')+text.count(u'ѝ')/n_chars)

    # Relative fequency of using comparative and superlative.
    count = 0
    for word in words:
        if word.startswith(u'по') or word.startswith(u'нај'):
            count += 1
    style.append(count/n_words)

    style.append((text.count(u'„')+text.count(u'“'))/n_chars)

    # Relative abbreviation frequency.
    style.append((text.count(u'др.')+text.count(u'сл.')+ \
                 text.count(u'пр.')+text.count(u'итн.'))/n_words)

    # Filter the words
    for i in range(int(n_words)):
        words[i] = filter_word(words[i])

    # Relative number(in digit) frequency.
    count = 0
    for word in words:
        if word.isnumeric():
            count += 1
    style.append(count/n_words)

    mk_word_groups = {'predlozi' : [u'без', u'во', u'в', u'врз', u'до', u'за', u'зад', u'заради',
                                    u'кај', u'како', u'кон', u'крај', u'меѓу', u'место', u'на',
                                    u'над', u'низ', u'од', u'одавде', u'оданде', u'отаде',
                                    u'околу', u'освен', u'по', u'под', u'поради', u'потем',
                                    u'пред', u'през', u'преку', u'при', u'против', u'со', u'сосе',
                                    u'според', u'спрема', u'спроти', u'сред'],
                      'cestici' : [u'де', u'бе', u'ма', u'барем', u'пак', u'меѓутоа', u'просто',
                                   u'да', u'не', u'ни', u'ниту', u'зар', u'и', u'дали', u'само',
                                   u'единствено', u'точно', u'токму', u'скоро', u'речиси',
                                   u'рамно', u'би', u'нека', u'ќе', u'уште', u'притоа', u'имено',
                                   u'токму', u'баш', u'ете', u'еве', u'ене'],
                      'licni_zamenki' : [u'јас', u'ти', u'тој', u'таа', u'тоа', u'ние', u'вие',
                                         u'тие', u'мене', u'ме', u'тебе', u'те', u'него', u'го',
                                         u'неа', u'ја', u'нас', u'нè', u'вас', u'ве', u'нив',
                                         u'ги', u'мене', u'ми', u'тебе', u'ти', u'нему', u'му',
                                         u'нејзе', u'ѝ', u'нам', u'ни', u'вам', u'ви', u'ним',
                                         u'им', u'себе', u'се', u'си'],
                      'licno_predmetni_zamenki' : [u'кој', u'која', u'кое', u'кои', u'кого',
                                                   u'кому', u'некој', u'секој', u'никој', u'што',
                                                   u'сешто', u'нешто', u'ништо', u'чиј', u'чија',
                                                   u'чие', u'чии'],
                      'pokazni_zamenki' : [u'овој', u'оваа', u'ова', u'овие', u'оној', u'онаа',
                                           u'она', u'оние', u'тој', u'таа', u'тоа', u'тие'],
                      'svrznici' : [u'и', u'ни', u'ниту', u'па', u'та', u'а', u'но', u'ама',
                                    u'туку', u'ами', u'меѓутоа', u'или', u'само', u'единствено',
                                    u'кога', u'штом', u'штотуку', u'тукушто', u'откако',
                                    u'откога', u'дури', u'додека', u'зашто', u'бидејќи', u'дека',
                                    u'оти', u'да', u'ако', u'ли', u'иако', u'што', u'кој',
                                    u'којшто', u'чиј', u'чијшто', u'како', u'дали', u'кога'],
                      'prisvojni_zamen_pridavki' : [u'мој', u'моја', u'мое', u'мои', u'твој',
                                                    u'твоја', u'твое', u'твои', u'негов',
                                                    u'негова', u'негово', u'негови', u'нејзин',
                                                    u'нејзина', u'нејзино', u'нејзини', u'наш',
                                                    u'наша', u'наше', u'наши', u'ваш', u'ваша',
                                                    u'ваше', u'ваши', u'нивни', u'нивна',
                                                    u'свој', u'своја', u'свое', u'свои'],
                      'pok_kvalit_zamen_pridavki' : [u'ваков', u'ваква', u'вакво', u'вакви',
                                                     u'таков', u'таква', u'такво', u'такви',
                                                     u'каков', u'каква', u'какво', u'какви',
                                                     u'онаков', u'онаква', u'онакво', u'онакви',
                                                     u'секаков', u'секаква', u'секакви',
                                                     u'некаков', u'некаква', u'некакво',
                                                     u'некакви', u'никаков', u'никаква',
                                                     u'никакво', u'никакви', u'толкав',
                                                     u'толкава', u'толкаво', u'толкави',
                                                     u'колкав', u'колкава', u'колкаво',
                                                     u'колкави', u'олкав', u'олкава', u'олкаво',
                                                     u'олкави', u'онолкав', u'онолкава',
                                                     u'онолкаво', u'онолкави', u'сиот',
                                                     u'сета', u'сето', u'сите', u'сам',
                                                     u'сама', u'само', u'сами', u'ист',
                                                     u'иста', u'исто', u'исти', u'друг',
                                                     u'друга', u'друго', u'други']}

    # Calculating relative frequencies of different word groups.
    for word_group in mk_word_groups:
        count = 0

        for word in words:
            if word in mk_word_groups[word_group]:
                count += 1

        style.append(count/n_words)

    return style

def get_similarity_styles(path1, path2):
    '''Calculates the similarity between the writing styles of two files.'''

    output = []

    output.extend([u'Сличност на стил на пишување меѓу ', os.path.basename(path1), u' и ',
                   os.path.basename(path2), '.\n\n'])

    with io.open(os.path.join(path1, 'plainText.txt'), 'r', encoding='utf8') as text_file:
        text1 = text_file.read()

    with io.open(os.path.join(path2, 'plainText.txt'), 'r', encoding='utf8') as text_file:
        text2 = text_file.read()

    style1 = get_style(text1)
    style2 = get_style(text2)

    list_categories = [u'релативна фрекфенција на ставање на празно место после запирка',
                       u'релативна фрекфенција на ставање на празно место после точка,'+ \
                       u'извичник или прашалник',
                       u'релативна фрекфенција на појавување на точки',
                       u'релативна фрекфенција на појавување на прашалници',
                       u'релативна фрекфенција на појавување на извичници',
                       u'релативна фрекфенција на појавување на запирки',
                       u'просечна должина на реченица(во зборови)',
                       u'релативна фрекфенција на појавување на надреден знак',
                       u'релативна фрекфенција на компаратив(по-) и суперлатив(нај-)',
                       u'релативна фрекфенција на појавување на наводници',
                       u'релативна фрекфенција на користење кратенки',
                       u'релативна фрекфенција на броеви(напишани во цифри)',
                       u'релативна фрекфенција на предлози',
                       u'релативна фрекфенција на честици',
                       u'релативна фрекфенција на лични заменки',
                       u'релативна фрекфенција на лично-предметни заменки',
                       u'релативна фрекфенција на показни заменки',
                       u'релативна фрекфенција на сврзници',
                       u'релативна фрекфенција на присвојни заменски придавки',
                       u'релативна фрекфенција на заменски придавки со показно'+ \
                       u'и квалитативно значење']

    score = cosine_similarity(style1, style2)

    output.extend([u'Сличноста на стилот на пишување е ', str(score*100), u'%.\n\n',
                   u'Стил на пишување на ', os.path.basename(path1), u':\n\n'])

    for i, _ in enumerate(style1):
        output.extend([u'\t-', list_categories[i], u':', str(style1[i]), u'\n'])

    output.extend([u'\n\nСтил на пишување на ', os.path.basename(path2), u':\n\n'])

    for i, _ in enumerate(style2):
        output.extend([u'\t-', list_categories[i], u':', str(style2[i]), u'\n'])

    output.extend([u'\n\n'])

    output = ''.join(output)

    return [score, output]
