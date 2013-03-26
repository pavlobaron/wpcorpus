# wpcorpus - NLP corpus based on Wikipedia's full article dump

wpcorpus is an "active" corpus for natural language processing. Active because it uses an index and not only text. And you will need some components in order to use it, so you can't just throw it onto your NLP library of choice. The implementation is in Python, though it would be easy to migrate it to whatever platform you like - based on the idea or even using some underlying technologies I use here. And the most important part of it being "active" is: I don't offer a download. You will have to create the corpus on your own, based on the instructions below.

Paths and file names are configured directly in the scripts right now. Of course it makes sense to move the configuration to command line parameters. But, well, I didn't yet.

## Getting a dump

First, you need a Wikipedia article dump. You can get them in whatever language Wikipedia offers: [http://dumps.wikimedia.org/backup-index.html](http://dumps.wikimedia.org/backup-index.html). Pick a language, and download a full article dump like enwiki-20121201-pages-articles.xml (of course, with a newer date). You will need the XML file, so feel free to un-bzip it first. What you get is, well, a huge dump file.

## Chunking the dump

The dump file is huge, so you want to chunk it in order to parallelise processing later. And generally: devide and conquer, you know. 

Chunking is done in one step and without parallelisation. bin/chunk.sh is what you need. Configure the chunk size, paths and other parameters in the lib/wpcorpus/chunk.py if you like. What you will get is a bunch of files that are valid Wikipedia XML files including parts of the whole dump.

## Processing

Processing is basically preparing N text files and indexing them. Both in combination build the later corpus. Text files are just extracts where all XML and unnecessary Wiki markup is stripped. The current solution works with 4 such files. The number 4 maps directly to the number of parallel workers doing the job and has no further meaning. You can configure it for more cores you want to use in bin/process.sh. I wouldn't recommend using a number higher than available cores, but it's up to you.

The other part processing does is indexing. Index is built using [PyTables](http://www.pytables.org/moin), so you need to install it first. Also, during the processing, a RabbitMQ queue is used for communication between the processing script and the indexer. So, you need [RabbitMQ](http://www.rabbitmq.com).  

When you have all components installed and configured, run bin/index.sh first and bin/process.sh next. They work as a pair. Yes, indeed, I could have implemented a top script that takes care of firing up both and shuttding it down properly.

## Usage

In order to use the result, you need to go with [NLTK](ihttp://nltk.org) and [nltk-trainer](https://github.com/japerk/nltk-trainer). If you don't know anything about any of these, well, you're probably wrong here. Or you will have to port this wpcorpus to whatever you use for NLP. I go with NLTK and the trainer.

First of all, create a symbolic link (yes, Windows user, a symbolic link) to the corpus folder (where you'll find subfolders with chunks and index after you went through the steps above). Call it wpcorpus or change its name in bin/train.sh.

From here, it's easy. In the bin/train.sh you will find a simple example how to pickle a classifier with nltk-trainer. It tries to distinguish political texts from trolling (see notes below on how reliable this would be). In the bin/train.sh, you see the class name to go with, a | separated list of Wikipedia categories to use for this class, where all articles of these categories will contribute text to this class training, followed by a similar list of anti-categories that will contribute to the counterpart. The anti-categories all together contribute to the class called irr.

Look up in the nltk-trainer and the NLTK documentation how to use the created pickle for classification. From here, all the work (and it's a lot of work) will go into finding right categories and playing with anti-categiries, accuracy and such. But this is also a fun part. To play with categories, you either can go with the Wikipedia web page, or just extract categories from the index file using PyTables. Or just search in the index directly.

## Weird parts

By the time of writing, libxml has exposed a pretty weird memory leak, so I frequently restart workers using some weird synchronization through temp files. I went with Celery first, and it worked great, until libxml has helped Linux kernel's OOM killer to kick my workers.

One possible question can also be: why not use Hadoop for that? Well, the answer is: why use Hadoop for that? It's just a tiny bunch of scripts and can run in an hour or two on a modern notebook without any file system abstractions. Or without any abstractions, to be honest. Think yourself the rest.

Another incompleteness is that right now only word based NLTK training is possible. I didn't yet implement sentenses and paragraphs, but this would be easy to do.

Speaking of Wikipedia's category chaos: in order to train your classifiers in a way that is usable, you would end up having long lists of categories and anti-gategories. The better you can separate them, the better the accuracy. And still, it's text, so trying to reliably distinguish a political text from the one on economics using wpcorpus, might lead to misclassification. It will lead to misclassification. On the other hand, using completely unrelated anti-categories the way I use in the example, is also not really helpful. You would only have to go with the accuracy of the political articles on Wikipedia, which is from my experience not absolutely reliable.

One last word about languages: Wikipedia is best in English. German works too, but the size and the quality of articles are questionable sometimes. Check out your language if it comes with enough useful information at all. nltk-trainer might be the next problem - with stopwords etc. But this problems are general in NLP, not just around my tiny contribution.

## Possible further research options:

What would be interesting is to use a graph database to build a graph of categories and to use it as index. This way around, classes can be described with one single category as entry point, and all subcategories would recursively contribute articles to it. The problem that I see is that Wikipedia categories are kind of chaotic. I might work on this in the future, but feel free to do this if you like.

I appreciate constructive feedback and of course any sort of contribution.
