#!/usr/bin/python
# -*- coding: utf-8 -*-

'''Main module that implements the logic for the plagiarism detection.'''

import os

from preprocessing import preprocess
from preprocessing import remove_suffix

from similarity import get_similarity_references
from similarity import get_similarity_paraphrased_text
from similarity import get_similarity_texts
from similarity import get_similarity_styles

def get_summary(categories, path1, path2):
    '''Summarizes the outcome for the UI.'''

    similarity = 0
    weight = 0
    summary = []
    details = []

    for element in categories:
        if element:
            weight += 1
    if weight != 0:
        weight = 100/float(weight*100)

    if categories[0]:
        sim_unweighted = get_similarity_references(path1, path2)
        similarity += sim_unweighted[0]*weight
        details.append(sim_unweighted[1])
        summary.extend([u'Сличноста на референци е: ',
                        str(round(sim_unweighted[0]*100, 2)), '%.\n\n'])

    if categories[1]:
        sim_unweighted = get_similarity_paraphrased_text(path1, path2)
        similarity += sim_unweighted[0]*weight
        details.append(sim_unweighted[1])
        summary.extend([u'Сличноста на парафразиран текст е: ',
                        str(round(sim_unweighted[0]*100, 2)), '%.\n\n'])

    if categories[2]:
        sim_unweighted = get_similarity_texts(path1, path2)
        similarity += sim_unweighted[0]*weight
        details.append(sim_unweighted[1])
        summary.extend([u'Сличноста на параграфи е: ',
                        str(round(sim_unweighted[0]*100, 2)), '%.\n\n'])

    if categories[3]:
        sim_unweighted = get_similarity_styles(path1, path2)
        similarity += sim_unweighted[0]*weight
        details.append(sim_unweighted[1])
        summary.extend([u'Сличноста на стил на пишување е: ',
                        str(round(sim_unweighted[0]*100, 2)), '%.\n\n'])

    summary = ''.join(summary)

    summary = u'Целосната сличност е: '+str(round(similarity*100, 2))+'%.\n\n'+summary
    summary = u'Пресметување на сличност меѓу '+path1+u' и '+path2+'\n\n'+summary

    if similarity*100 < 10:
        similarity = '0'+ str(round(similarity*100, 2))

    return details, summary

def detect_plagiarism(path1, path2, categories):
    '''The main function initialized to detect plagiarism.'''

    preprocess(path1)
    preprocess(path2)

    path1 = os.path.join(os.getcwd(), 'temp', remove_suffix(os.path.basename(path1)))
    path2 = os.path.join(os.getcwd(), 'temp', remove_suffix(os.path.basename(path2)))

    details, summary = get_summary(categories, path1, path2)

    return details, summary
