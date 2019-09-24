
# coding: utf-8

# In[24]:


import requests
import numpy as np
import pandas as pd
from pprint import pprint as pp


# In[2]:


json_city = requests.get("https://www.metaweather.com/api/location/search/?query=St Petersburg").json()


# In[3]:


print(json_city)


# In[6]:


ident = json_city[0]['woeid']


# In[7]:


pp(requests.get("https://www.metaweather.com/api/location/"+ str(ident)+"/2019/10/1/").json())


# In[14]:


pd.DataFrame(requests.get("https://www.metaweather.com/api/location/"+ str(ident)+"/2019/9/24/").json())


# In[49]:


tbl = []


# In[50]:


for i in range(24,28):
    for i in requests.get("https://www.metaweather.com/api/location/"+ str(ident)+"/2019/9/"+str(i)+"/").json():
        tbl.append(i)
    


# In[ ]:


len(tbl)


# In[68]:


tbl


# In[59]:


a=pd.DataFrame(tbl)


# In[62]:


max(a.predictability)


# In[64]:


sr=a[a.predictability==max(a.predictability)]


# In[67]:


#Определите c помощью возможностей модуля pandas 
#для города Санкт-Петербург в период с 24 по 27 сентября 
#среднюю наиболее вероятную минимальную температуру.
np.average(sr.min_temp)

