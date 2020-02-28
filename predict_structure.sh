bash ../data_processing/jackhmmer.sh 1UBQ.fa ../../dbs/proteinnet12 
python ../data_processing/convert_to_proteinnet.py 1UBQ.fa
python ../data_processing/convert_to_tfrecord.py 1UBQ.fa.proteinnet 1UBQ.fa.tfrecord 42 
cp 1UBQ.fa.tfrecord RGN12/data/ProteinNet12Thinning90/testing/
python ../model/protling.py RGN12/runs/CASP12/ProteinNet12Thinning90/configuration -d ./RGN12/ -p -e weighted_testing -g0 
