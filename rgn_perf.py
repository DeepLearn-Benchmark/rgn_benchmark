#!/usr/bin/env python
# coding: utf-8

# # RGN performance evaluation  
# 
# This notebook is to evaluate the performance of [Recurrent Geometric Network (RGN)](https://github.com/aqlaboratory/rgn) in predicting the 3D structure of CASP12 targets. 
# 
# Detailed setup prior to running this notebook is available in the [README.md](). 
# 
# NOTE: Only prediction time is evaluated here. 

# In[1]:


import os 
import sys
import time 
import pickle 
import subprocess
from Bio import SeqIO
import pandas as pd


# ## Basic info 
# 
# Set up which gpu to use, rgn and database paths. 

# In[2]:


os.environ['CUDA_VISIBLE_DEVICES'] = str(0) 
rgn_path = '../rgn/' 
dbs_path = '../dbs/'
rgn_model_path = './RGN12/' 
seq_file = "./casp12.seq.txt"


# ## Executing RGN function 
# 
# A function to run RGN with Python subprocess32. 

# In[3]:


def exec_rgn(record): 
    """Executing RGN on a biopython SeqRecord""" 
    SeqIO.write(record, "%s.fa"%record.id, "fasta") 

    protein_name = record.id
    perf_dict = dict() 
    perf_dict['id'] = record.id 
    perf_dict['n_res'] = len(record.seq)

    # hmmer search for MSA
    hmmer_command = "bash %s/data_processing/jackhmmer.sh %s.fa %s/proteinnet12" % (rgn_path, record.id, dbs_path)
    time_start = time.time()
    hmmer_p = subprocess.Popen(hmmer_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    hmmer_p.wait() 
    perf_dict['hmmer'] = time.time() - time_start 

    # coversion to tf record format 
    tfrecord_commands = [
        'python {}/data_processing/convert_to_proteinnet.py {}.fa'.format(rgn_path, protein_name),                              
        'python {0}/data_processing/convert_to_tfrecord.py {1}.fa.proteinnet {1}.fa.tfrecord 42'.format(rgn_path, protein_name),                              
        'cp {}.fa.tfrecord {}/data/ProteinNet12Thinning90/testing/'.format(protein_name, rgn_model_path)] 
    time_start = time.time() 
    for command in tfrecord_commands: 
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
        p.wait()  
    perf_dict['tfrecord'] = time.time() - time_start 

    rgn_command = 'python {0}/model/protling.py '                '{1}/runs/CASP12/ProteinNet12Thinning90/configuration '                '-d {1} -p -e weighted_testing -g0'.format(rgn_path, rgn_model_path) 
    time_start = time.time()
    rgn_p = subprocess.Popen(rgn_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    rgn_p.wait() 
    perf_dict['rgn_predict'] = time.time() - time_start 

    return perf_dict 


# ## Run RGN through casp12 record 

# In[6]:


perf_record = []
targets = list(SeqIO.parse(seq_file, "fasta"))
for record in targets[:1]:
    print record.id
#     perf = exec_rgn(record) 
#     perf_record.append(perf)    


# ## Save the result to pickle 

# In[10]:


with open('perf_rgn.pickle', 'wb') as fp: 
    pickle.dump(perf_record, fp)

