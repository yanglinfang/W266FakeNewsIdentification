import numpy as np
import re
import itertools
from collections import Counter


def clean_str(string):
    """
    Tokenization/string cleaning for all datasets except for SST.
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    """
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()


def load_data_and_labels(positive_data_file, negative_data_file):
    """
    Loads MR polarity data from files, splits the data into words and generates labels.
    Returns split sentences and labels.
    """
    # Load data from files
    positive_examples = list(open(positive_data_file, "r").readlines())
    positive_examples = [s.strip() for s in positive_examples]
    negative_examples = list(open(negative_data_file, "r").readlines())
    negative_examples = [s.strip() for s in negative_examples]
    # Split by words
    x_text = positive_examples + negative_examples
    x_text = [clean_str(sent) for sent in x_text]
    # Generate labels
    positive_labels = [[0, 1] for _ in positive_examples]
    negative_labels = [[1, 0] for _ in negative_examples]
    y = np.concatenate([positive_labels, negative_labels], 0)
    return [x_text, y]


def batch_iter(data, batch_size, num_epochs, shuffle=True):
    """
    Generates a batch iterator for a dataset.
    """
    data = np.array(data)
    data_size = len(data)
    num_batches_per_epoch = int((len(data)-1)/batch_size) + 1
    for epoch in range(num_epochs):
        # Shuffle the data at each epoch
        if shuffle:
            shuffle_indices = np.random.permutation(np.arange(data_size))
            shuffled_data = data[shuffle_indices]
        else:
            shuffled_data = data
        for batch_num in range(num_batches_per_epoch):
            start_index = batch_num * batch_size
            end_index = min((batch_num + 1) * batch_size, data_size)
            yield shuffled_data[start_index:end_index]


# Load data from yahoo dataset
def load_yahoo_data(label_used):
    header = []
    articleData = []
    with open('./news.csv', 'rb') as f:
        for line in f:
            if len(header) == 0:
                header = line.split('\t')
            else:
                articleData.append(line.split('\t'))
    columns = len(header)
    rows = len(articleData)
    print 'Loaded rows: ', rows,'columns: ', columns
    print 'Headers: ', header
    print 'Using label: ', label_used
    #print 'sample text: ', articleData[0][header.index('news article')]
    #print 'sample label: ', articleData[0][header.index(label_used)]
    
    texts = []
    targets = []
    for i in range(0, rows):
        labelStr = articleData[i][header.index(label_used)]
        if labelStr != '':
            texts.append(articleData[i][header.index('news article')])
            target = int(labelStr)
            labels = [[0,1]]
            if target <= 2:
                labels = [[1,0]]
            targets.append(labels)
    y = np.concatenate(targets, 0)
    return (texts, y)


# Load data from facebook dataset
def load_facebook_data():
    articleData = []
    labelStrs = []
    with open('./text_and_labels.tsv', 'rb') as f:
        for line in f:
            articleData.append(line.split('\t'))
    columns = 2
    rows = len(articleData)
    print 'Loaded rows: ', rows,'columns: ', columns
    
    texts = []
    targets = []
    for i in range(0, rows):
        labelStr = articleData[i][1]
        if labelStr != '':
            texts.append(articleData[i][0])
            if labelStr not in labelStrs:
                labelStrs.append(labelStr)
                
            if labelStr.startswith('mostly true'):
                target = 5
            if labelStr.startswith('mixture of true and false'):
                target = 3
            if labelStr.startswith('no factual content'):
                target = 2;
            if labelStr.startswith('mostly false'):
                target = 1;
         
            labels = [1]
            if target <= 3:
                labels = [0]
            targets.append(labels)
    y = np.concatenate(targets, 0)
    return (texts, y)
