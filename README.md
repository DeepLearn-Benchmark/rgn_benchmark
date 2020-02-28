# RGN prediction benchmarks

# Setup & Run

1. Obtain RGN and benchmark repo from GitHub  

   ```bash 
   git clone https://github.com/aqlaboratory/rgn.git
   git clone https://github.com/DeepLearn-Benchmark/rgn_benchmark.git
   ```

2. Download necessary database and models  

   * [ProteinNet12](https://sharehost.hms.harvard.edu/sysbio/alquraishi/proteinnet/sequence_dbs/proteinnet12.gz) is a raw CASP12 sequence database for HMMER. 

     More sequence databases are [available](https://github.com/aqlaboratory/proteinnet/blob/master/docs/raw_data.md). 

   * [RGN12](https://sharehost.hms.harvard.edu/sysbio/alquraishi/rgn_models/RGN12.tar.gz) is trained RGN model on ProteinNet12/CASP12 dataset.  

     RGN models trained on different dataset are also [available](https://github.com/aqlaboratory/rgn#pre-trained-models). 

3. Unzip and place the uncompressed files 
    All the databases and models are needed to run the benchmark. Their paths need to specified in `rgn_perf.py` or `rgn_perf.ipynb`. 

     ```bash
     gzip proteinnet12.gz
     tar xvf RGN12.tar.gz
     ```

     It is recommended to set up the directory as 

     ```bash
     .
     ├── dbs
     |   └── proteinnet12
     ├── rgn
     └── rgn_benchmark
         └── RGN12
     ```

     

4. Get `conda` environment 

    ```bash 
    cd rgn_benchmark 
    conda env create -f environment.yml 
    source activate rgn_tf 
    ```
   
5. Run benchmark 
    After defining the path information in step 3, run the benchmark can be simple as 
    ```bash 
    python rgn_perf.py 
    ```
    NOTE: The code will take rather longer time due to the preprocessing to a sequence for PSSM.  
    
6. Analyze the performace 

    The runtime info will be stored in a pickle file `perf_rgn.pickle`. The [notebook `Result_plot.ipynb`](https://github.com/DeepLearn-Benchmark/rgn_benchmark/blob/master/Result_plot.ipynb) contains the script to read the results with `pandas` and render a performace profile of runtime against number of amino acids in sequence. 

