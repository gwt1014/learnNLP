
# coding: utf-8

# In[1]:


import pandas as pd
import jieba
import sys
import time
import jieba.posseg as pseg
import numpy as np


# In[2]:


path = 'C:/Users/GWT/pyfiles/nlp/'


# In[3]:


df = pd.read_csv(path + 'datasource/jly.csv',encoding='gbk',header=None)
df.columns = ['comment','count']
df['count'].astype(int)


# In[4]:


def getjieba_n(comment):
    txt = pseg.cut(comment)
    result = []
    for i in txt:
        if i.flag == "n":
            result.append(i.word)
    return "".join(result)


# In[5]:


def getjieba_a(comment):
    txt = pseg.cut(comment)
    result = []
    for i in txt:
        if i.flag == "a":
            result.append(i.word)
    return "".join(result)
        


# In[6]:


df['n']=df['comment'].map(lambda x: getjieba_n(x))


# In[7]:


df['a'] =df['comment'].map(lambda x: getjieba_a(x))


# In[8]:


df.replace('',np.NAN)


# In[9]:


result = df.groupby(['n']).sum().reset_index().sort_values('count',ascending=True)


# In[10]:


result = result.drop(axis=1,index = 0)


# In[11]:


result


# In[12]:


result.to_csv(path + 'output/sum.csv',encoding="gbk")


# In[13]:


from pyecharts import Bar,WordCloud
from pyecharts_snapshot.main import make_a_snapshot


# In[14]:


n = result[result['count']>4000]['n'].tolist()
count = result[result['count']>4000]['count'].tolist()
bar1 = Bar('名词排序')
bar1.add("",n,count,is_convert =True)
bar1.render('bar1.html')
make_a_snapshot('bar1.html',path+'/output/bar1.png')
bar1


# In[15]:


n = result[result['count']>30]['n'].tolist()
count = result[result['count']>30]['count'].tolist()

cloud = WordCloud("词云")
cloud = WordCloud(width=900, height=600)
cloud.add('名词词云',n,count, word_size_range=[20,150],shape = 'star')
cloud.render('cloud.html')
make_a_snapshot('cloud.html',path+'/output/cloud.png')

cloud

