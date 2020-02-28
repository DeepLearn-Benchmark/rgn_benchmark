rgn_path=../rgn 
dbs_path=../dbs/
rgn_model_path=./RGN12/

bash $rgn_path/data_processing/jackhmmer.sh 1UBQ.fa $dbs_path/proteinnet12 
python $rgn_path/data_processing/convert_to_proteinnet.py 1UBQ.fa
python $rgn_path/data_processing/convert_to_tfrecord.py 1UBQ.fa.proteinnet 1UBQ.fa.tfrecord 42 
cp 1UBQ.fa.tfrecord RGN12/data/ProteinNet12Thinning90/testing/
python $rgn_path/model/protling.py $rgn_model_path/runs/CASP12/ProteinNet12Thinning90/configuration -d $rgn_model_path -p -e weighted_testing -g0 
