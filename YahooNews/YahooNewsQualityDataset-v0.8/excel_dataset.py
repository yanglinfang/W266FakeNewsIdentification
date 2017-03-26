'''
Created on 29/10/2016

@author: PelejaF
'''

import os

news_tsv_folder = os.path.join(os.getcwd(),'dataset/tsvFiles/withText-body/')
sentences_tsv_folder = os.path.join(os.getcwd(),'dataset/tsvFiles/withText-sentences/')

news_csv = os.path.join(os.getcwd(),'news.csv')
sentences_csv = os.path.join(os.getcwd(),'sentences.csv')

news_csv_out = open(news_csv, 'w')
sentences_csv_out = open(sentences_csv, 'w')

# write headers
news_csv_out.write('id\tnews article name\tnews article\tFluency\tConciseness\tDescriptiveness\tNovelty\tCompleteness\t')
news_csv_out.write('Referencing\tFormality\tRichness\tAttractiveness\tTechnicality\tPopularity\tSubjectivity\t')
news_csv_out.write('Positive Emotion\tNegative Emotion\tQuality\tAnnotatorsConfidenceScore\n')

news_article_names = {}

curr_id = 1
for filename in os.listdir(news_tsv_folder):
	curr_file = open(os.path.join(news_tsv_folder, filename), 'r')
	line = curr_file.readline().replace('\n','').replace('\r','')
	line = line.split('\t')
	news_article_name = filename.replace('-sentences.txt','').replace('_sentences.txt','').replace('-body.txt','').replace('_body.txt','')
	news_article_names[news_article_name] = curr_id
	news_article = line[0]
	Fluency = line[1]
	Conciseness = line[2]
	Descriptiveness = line[3]
	Novelty = line[4]
	Completeness = line[5]
	Referencing = line[6]
	Formality = line[7]
	Richness = line[8]
	Attractiveness = line[9]
	Technicality = line[10]
	Popularity = line[11]
	Subjectivity = line[12]
	Positive_Emotion = line[13]
	Negative_Emotion = line[14]
	Quality = line[15]
	if len(line) == 17:
		AnnotatorsConfidenceScore = line[16]
	else:
		AnnotatorsConfidenceScore = ''
	news_csv_out.write(str(curr_id)+'\t'+news_article_name+'\t'+news_article+'\t'+Fluency+'\t'+Conciseness+'\t'+Descriptiveness+'\t'+Novelty+'\t'+Completeness+'\t')
	news_csv_out.write(Referencing+'\t'+Formality+'\t'+Richness+'\t'+Attractiveness+'\t'+Technicality+'\t')
	news_csv_out.write(Popularity+'\t'+Subjectivity+'\t'+Positive_Emotion+'\t'+Negative_Emotion+'\t'+Quality+'\t'+AnnotatorsConfidenceScore+'\n')
	curr_id = curr_id + 1
	curr_file.close()
news_csv_out.close()

# write headers
sentences_csv_out.write('id\tnews article name\tSentence\tSubjectivity\tPositivity\tNegativity\t')
sentences_csv_out.write('Ignore sentence (I) or sentence Splitting issue (S)\tAnnotatorsConfidenceScore\n')
for filename in os.listdir(sentences_tsv_folder):
	curr_file = open(os.path.join(sentences_tsv_folder, filename), 'r')
	news_article_name = filename.replace('-sentences.txt','').replace('_sentences.txt','').replace('-body.txt','').replace('_body.txt','')
	curr_id = news_article_names[news_article_name]
	while 1:	
		sentence = curr_file.readline()
		if not sentence:break
		line = sentence.replace('\n','').replace('\r','').split('\t')
		if len(line) == 1:break
		news_article = line[0]
		sentence = line[1]
		subjectivity = line[2]
		positivity = line[3]
		negativity = line[4]
		if len(line) == 6:
			I_S = line[5]
		else:
			I_S = ''
		if len(line) == 7:
			annotatorsConfidenceScore = line[6]
		else:
			annotatorsConfidenceScore = ''
		sentences_csv_out.write(str(curr_id)+'\t'+news_article_name+'\t'+news_article+'\t'+sentence+'\t'+subjectivity+'\t')
		sentences_csv_out.write(positivity+'\t'+negativity+'\t'+I_S+'\t'+annotatorsConfidenceScore+'\n')
	curr_file.close()
sentences_csv_out.close()


