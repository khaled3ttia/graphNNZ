#!/bin/bash 

facebook=facebook_combined
twitter=twitter_combined
ca=CA-HepTh

vectorSizes=(4 8 16 32)

for v in ${vectorSizes[@]}; do
    time python graphNNZ.py --input data/$facebook.txt --no-rename --vsize $v > results/facebook_v${v}_ud_results.out 

    time python graphNNZ.py --input data/$ca.txt --rename --vsize $v > results/ca_v${v}_ud_results.out

done 
