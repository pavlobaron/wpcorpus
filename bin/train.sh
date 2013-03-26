#!/bin/sh

cd ~/opt/nltk-trainer

./train_classifier.py --reader wpcorpus.wikireader.CategorizedWikiCorpusReader --algorithm NaiveBayes --instances files --cat_pattern "Politics----Politics|Government----Internet memes|Internet slang" --filename ~/nltk_data/classifiers/politics.pickle --filter-stopwords english wpcorpus

