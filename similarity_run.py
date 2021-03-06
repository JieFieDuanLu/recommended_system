# -*- coding:utf-8 -*-
import os
import sys

# import shutil
sys.path.append("./program/")
import time
import multiprocessing
# def f(x):
# return corpora.Dictionary(jieba.lcut('我们可以'))
time_before = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
print time_before

import jieba.posseg as pseg
import codecs

# from program import *

def mkdir(path):
    # 引入模块
    import os

    # 去除首位空格
    path = str(path).strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        print path + ' 创建成功'
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print path + ' 目录已存在'
        return False

if __name__ == '__main__':
    import gc

    filesaved = 'article.sql'
    docpath = './nnews/'
    lsipath = './nlsi/'
    NUM_TOPIC = 300  # 主题的数量，默认为 300
    NUM_DOC = -1  # 所选取的语料集中的文件数量
    cpu_num = multiprocessing.cpu_count()
    doc_limit = 100
    t01 = time.time()
    print "cpu_num="+str(cpu_num)
    print "doc_limit="+str(doc_limit)
    if os.path.exists(docpath):
        from ar import filebyfileHandle
        filebyfileHandle(docpath, doc_limit, cpu_num, NUM_DOC)  # 100字符内的文件抛掉不处理,多进程不指定默认 multiprocess=4
    else:
        mkdir(docpath)
    t02 = time.time()

    print "prepare time = ", t02 - t01

    t11 = time.time()
    from dict_stream_train import getDictionary

    dict = getDictionary(lsipath=lsipath, docpath=docpath)
    t12 = time.time()
    print "dict time = ", t12 - t11

    t21 = time.time()
    from corpus_stream_train import getCorpus

    corpus = getCorpus(lsipath=lsipath, docpath=docpath)
    t22 = time.time()
    print "corpus time = ", t22 - t21


    #gc
    del dict, corpus
    gc.collect()

    t31 = time.time()
    from lsi_stream_train import getLsiModel

    lsimodel = getLsiModel(lsipath=lsipath, num_topics=NUM_TOPIC)
    t32 = time.time()
    print "lsimodel time = ", t32 - t31

    t41 = time.time()
    from index_stream_train import getIndex

    getIndex(lsipath, NUM_TOPIC)  # change by baobao ,add NUM_TOPIC
    t42 = time.time()

    print "prepare time = ", t02 - t01
    print "dict time = ", t12 - t11
    print "corpus time = ", t22 - t21
    print "lsimodel time = ", t32 - t31
    print "getIndex time = ", t42 - t41
# p = Pool(5)
# d = corpora.Dictionary(jieba.cut('我们可以'))
# print d
# print( corpora.Dictionary(jieba.lcut('我们可以')))
# print(p.map(f, ['aa', 'ab', 'ac']))

timenow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
print time_before
print timenow
