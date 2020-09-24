#!/usr/bin/env python
# coding: utf-8

# In[12]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.stats import zmap


# In[13]:


DA_timepoints = pd.read_csv(r'C:\Users\Research11\Desktop\dkm\SAFE ACCESS TO MATERNAL MEDICINE INTERVENTION PHASE\SAFEACCESSTOMATERNAL_DATA_LABELS_2020-09-21_0657.csv', index_col=['record_no']) 
DA_patients = pd.read_csv(r'C:\Users\Research11\Desktop\dkm\SAFE ACCESS TO MATERNAL MEDICINE INTERVENTION PHASE\SAFEACCESSTOMATERNAL_DATA_LABELS_2020-09-21_0657.csv', index_col=['record_no']) 


# In[18]:


def timepoints_from_patient_variable(variable, value, patients, timepoints):
    temp = patients.index[variable == value]
    row_inds = row_inds = [np.where(timepoints.index == record_number)[0] for record_number in temp]
    timepoints_table = timepoints.iloc[np.hstack(row_inds)]
  
    return timepoints_table


# In[20]:


DA_timepoints_oxytocin = timepoints_from_patient_variable (DA_patients.drug,'Oxytocin', DA_patients, DA_timepoints)
DA_timepoints_mgso4 = timepoints_from_patient_variable (DA_patients.drug, 'Magnesium Sulphate', DA_patients, DA_timepoints)


# In[21]:


DA_total_patient_count = len(DA_patients['participants_number'].unique())
DA_mgso4_patient_count = sum(DA_patients.drug== 'Magnesium Sulphate')
DA_oxytocin_patient_count = sum(DA_patients.drug== 'Oxytocin')


# In[22]:


DA_mgso4_infused_bags = sum(DA_timepoints_mgso4['infusion_stop'] == 'Yes')
DA_oxytocin_infused_bags = sum(DA_timepoints_oxytocin['infusion_stop'] == 'Yes')


# In[23]:


def mgso4_accuracy(timepoints_mgso4):
 
    mgso4_bag_stats = pd.DataFrame()
    
    # infusion rate for MgSO4 is in mL/hr 
    mgso4_bag_stats['mgso4_error_ratios'] = (timepoints_mgso4['bag_average_rate_ml/hr'] - timepoints_mgso4['prescribed_rate'])/timepoints_mgso4['prescribed_rate']
    mgso4_error_ratios = mgso4_bag_stats['mgso4_error_ratios'] 
     
    mgso4_bag_stats['accurate_bags'] = sum(abs(mgso4_error_ratios) <= 0.1)
    mgso4_bag_stats['inaccurate_bags'] = sum(abs(mgso4_error_ratios) > 0.1)
    
    mgso4_bag_stats['slow_bags'] = sum(mgso4_error_ratios < -0.1)
    mgso4_bag_stats['fast_bags'] = sum(mgso4_error_ratios > 0.1)
    
    mgso4_bag_stats['total_bags'] = mgso4_bag_stats['accurate_bags'] + mgso4_bag_stats['inaccurate_bags']
    mgso4_bag_stats['total_bags_check'] = mgso4_bag_stats['fast_bags'] + mgso4_bag_stats['slow_bags']
    #add bug check- do inaccurate + accurate and slow + fast
    
    mgso4_bag_stats['percent_accurate'] = mgso4_bag_stats['accurate_bags'] / mgso4_bag_stats['total_bags']
    mgso4_bag_stats['percent_inaccurate'] = mgso4_bag_stats['inaccurate_bags'] / mgso4_bag_stats['total_bags'] 
    mgso4_bag_stats['percent_slow'] = mgso4_bag_stats['slow_bags'] / mgso4_bag_stats['total_bags'] 
    mgso4_bag_stats['percent_fast'] = mgso4_bag_stats['fast_bags'] / mgso4_bag_stats['total_bags'] 

    return (mgso4_bag_stats)


# In[31]:


DA_mgso4_accuracy= mgso4_accuracy(DA_timepoints_mgso4)
    


# In[28]:


def mgso4_ratio_hist(timepoints_mgso4):
    
    mgso4_observation_error_ratio = (timepoints_mgso4['observ_avg_rate_ml/hr'] - timepoints_mgso4['prescribed_rate'])/timepoints_mgso4['prescribed_rate']
    mgso4_observation_error_ratio = mgso4_observation_error_ratio[mgso4_observation_error_ratio < 1000] #cutoff "infinity" points that are data entry issues 
    plt.figure(figsize=(12,8))
    sns.set_style("darkgrid")
    sns.set_context('paper')
    
    #bag_error_ratio_series = pd.Series(mgso4_bag_stats['mgso4_error_ratios'], name="MgSO4 Whole Bag Infusion Relative Error Distribution")
    observation_error_ratio_series = pd.Series(mgso4_observation_error_ratio, name="MgSO4 Hourly Infusion Relative Error Distribution")
    
    p = sns.distplot(observation_error_ratio_series, vertical = True)
    p.set(ylim=(-2,2))
    p.set(xlim=(0,4))
    


# In[35]:


mgso4_ratio_hist(DA_timepoints_mgso4)
print('bag_average_rate_ml/hr')


# In[33]:


DA_mgso4_accuracy= mgso4_accuracy(DA_timepoints_mgso4)


# In[41]:





# In[ ]:




