#!/usr/bin/env bash

# The run script for running the fraud detection algorithm

# The input directory is paymo_input
# Outputs the files in the directory paymo_output
# You don't have to give any additional input arguments in order to run the optional features. Just set the optional_feature_flag to 1 in the antifraud.py file.

python ./src/antifraud.py ./paymo_input/batch_payment.txt ./paymo_input/stream_payment.txt ./paymo_output/output1.txt ./paymo_output/output2.txt ./paymo_output/output3.txt