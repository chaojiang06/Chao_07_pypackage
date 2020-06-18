#!/usr/bin/env python
#-*- coding:utf-8 -*-
import pickle
import csv
import json

from pprint import pprint
from sklearn.utils.extmath import softmax



def output_test():
    print("this is io_util") 

def write_tsv_file_in_BERT_format(sent_pair_list, csv_path):
        
    with open(csv_path, 'w', encoding = 'utf-8') as myFile:  
        writer = csv.writer(myFile, delimiter='\t', quotechar='', quoting=csv.QUOTE_NONE)
        writer.writerows(sent_pair_list)
        
def read_prediction_logit_file(path):

    prediction = read_tsv_file(path)
    prediction = softmax([[float(i[0]), float(i[1])] for i in prediction])
    prediction = [i[0] for i in prediction]

    return prediction

def read_pickle_file(path):
    with open(path, 'rb') as handle:
        b = pickle.load(handle)
        
    return b

def write_pickle_file(file, path, protocol = None):
    if protocol == None:
        with open(path, 'wb') as handle:
            pickle.dump(file, handle)
    else:
        with open(path, 'wb') as handle:
            pickle.dump(file, handle, protocol = protocol)

def write_tsv_file(file,csv_path ):
    
    with open(csv_path, 'w', encoding = 'utf-8') as myFile:  
        writer = csv.writer(myFile, delimiter='\t', quotechar='', quoting=csv.QUOTE_NONE)
        writer.writerows(file)
        
def read_tsv_file(path):
    
    data = []
    
    with open(path, 'r') as f:
        reader = csv.reader(f, delimiter='\t', quotechar='', quoting=csv.QUOTE_NONE)    
        for idx, line in enumerate(reader):
            data.append(line)
    
    return data

def read_txt_file(path):
        
    with open(path) as f:
        data = f.readlines()
    
    return data

def read_json_file(path):
    with open(path) as f:
        data = json.load(f)
    return data

def write_json_file(file, path):
    with open(path, 'w') as outfile:
        json.dump(file, outfile)

def separate_lines_into_paragraphs(data):
    """
    Input:
        A list that every element is a sentence, empty line represents a new paragraph
    Action:
        Separate the list into paragraphs at every empty line
    Output:
        A list, every element is a paragraph, it contains a list of sentences
    """
    
    current_paragraph = []
    paragraph_list = []
    
    for sent in data:
        if sent != "":
            current_paragraph.append(sent)
        else:
            paragraph_list.append(current_paragraph)
            current_paragraph = []
    
    if current_paragraph != []:
        paragraph_list.append(current_paragraph)
    
    return paragraph_list
