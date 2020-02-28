#!/usr/bin/env python
# coding: utf-8

# # RGN performance evaluation  
# 
# This notebook is to evaluate the performance of [Recurrent Geometric Network (RGN)](https://github.com/aqlaboratory/rgn) in predicting the 3D structure of CASP12 targets. 
# 
# Detailed setup prior to running this notebook is available in the [README.md](). 
# 
# NOTE: Only prediction time is evaluated here. 



import os 
import sys
import time 
import pickle 
import subprocess
from Bio import SeqIO

import pandas as pd
import matplotlib.pyplot as plt 


# ## Basic info 
# 
# Set up which gpu to use, rgn and database paths. 

os.environ['CUDA_VISIBLE_DEVICES'] = str(0) 
rgn_path = '..' 
dbs_path = '../../dbs'


# ## Executing RGN function 
# 
# A function to run RGN with Python subprocess32. 

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
        'python %s/data_processing/convert_to_proteinnet.py %s.fa' % (rgn_path, protein_name),                              
        'python %s/data_processing/convert_to_tfrecord.py {1}.fa.proteinnet {1}.fa.tfrecord 42'.format(rgn_path, protein_name),                              
        'cp {}.fa.tfrecord RGN12/data/ProteinNet12Thinning90/testing/'.format(protein_name)] 
    time_start = time.time() 
    for command in tfrecord_commands: 
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
        p.wait()  
    perf_dict['tfrecord'] = time.time() - time_start 

    rgn_command = 'python %s/model/protling.py '\
            'RGN12/runs/CASP12/ProteinNet12Thinning90/configuration '\
            '-d ./RGN12/ -p -e weighted_testing -g0'  % rgn_path
    time_start = time.time()
    rgn_p = subprocess.Popen(rgn_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    rgn_p.wait() 
    perf_dict['rgn_predict'] = time.time() - time_start 

    return perf_dict 


# ## Run RGN through casp12 record 
perf_record = []
for record in SeqIO.parse("./casp12.seq.txt", "fasta"):
    perf = exec_rgn(record) 
    perf_record.append(perf)    

# ## Save the result in pickle file 
with open('perf_rgn.pickle', 'wb') as fp: 
    pickle.dump(perf_record, fp)


# ```bash
# bash ../data_processing/jackhmmer.sh 1ubq.fa ../../dbs/proteinnet12 
# python ../data_processing/convert_to_proteinnet.py 1ubq.fa
# python ../data_processing/convert_to_tfrecord.py 1ubq.fa.proteinnet 1ubq.fa.tfrecord 42 
# cp 1ubq.fa.tfrecord RGN12/data/ProteinNet12Thinning90/testing/
# python ../model/protling.py RGN12/runs/CASP12/ProteinNet12Thinning90/configuration -d ./RGN12/ -p -e weighted_testing -g0 
# ```
