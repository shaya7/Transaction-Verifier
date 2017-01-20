

***
# Table of Contents

1. Project (README.md#Project)
2. [Implementation Summary] (README.md#implementation-summary)
3. [Implementation Details] (README.md#implementation-details)
4. [Implementation Notes] (README.md#implementation-notes)
5. [Inputs, Outputs, and Results] (README.md#inputs,-outputs,-and-results)
6. [Unit Tests and Synthesized-input Tests] (README.md#inputs,-outputs,-and-results)
7. [Ideas for Extending Features] (README.md#ideas-for-extending-features)


##Project

The implemented code builds a user network based on previous and incoming transactions and verifies the incoming transactions based on specific network features. 

Important Note:
`run.sh` requires the two input files to be named `batch_payment.txt` and `stream_payment.txt` (not `.csv'`s)

##Implementation Summary

* programming language: python 2.7

* required python modules: sys, collections, csv, numpy, copy, logging

* There is an `optional_feature_flag` variable at the begining of `antifraud.py` file. It is set to `0`. Please set it to `1` if you wish to process the optional features and get their outputs.
 
##Implementation Details

* **User network** is represented by a graph implemented as a python dictionary.
	- each node represents a user
	- each edge represents a transaction between the two end users
	
* **Feature1,** for each transaction checks if there is an edge (direct link) between the two user nodes.

* **Feature2,** for each transaction first looks for a direct link between the two user nodes, if it exists the feature is `'trusted'` but if it doesn't exist, checks if a degree2 link exists between the user nodes (the intersection of neighbors of user1 and neighbors of user2 is nonempty).

* **Feature3,** for each transaction first checks for a direct link between the two users, if it doesn't exist checks for a degree2 link between the user nodes, if this one doesn't exist either uses the Breadth Firs Search (BFS) method to find out if there is a path of length 4 or less between the two user nodes.
 
* **Optional-Feature1,** for each transaction checks if the transaction amount is less than a predefined maximum limit i.e. `amount <= limit`. If that's the case the feature will be `'trusted'`, otherwise it will be `'unverified'`.
The limit is set to $25. You can change it in the antifraud.py file.

* **Optional-Feature2,** for each transaction finds the average amount that each user has payed so far and checks if the transaction to be verified has an amount less than or equal to twice that average i.e. `amount <= 2 x user paid average`. If this is the case the feature will be `'trusted'`. Otherwise it will be `'unverified'`.
The payer average amount is updated after processing each transaction.
You can change the criterion to three times the average or more in the antifraud.py file.

##Implementation Notes	

* **Execution speed** of features for each transaction is very fast (it takes a few miliseconds). It will still be faster if there is no requirement to dynamically update the user network while reading and processing the `stream_payment.txt` file.

* Different features are calculated **separately and independant** of each other. Therefore you can choose to calculate only one of the features and comment out the rest of them in the code.

* The network graph is **updated** after processing each line of the `stream_payment.txt` file.

* This implementation handles input **irregularities**:
	- If in an input line one or both user id's of a transaction are not integers, that line is ignored.
	- Only in processing the optional features if the amount in an input line is not a float number, that line is ignored.

##Inputs, Outputs, and Results

* Output of feature1 is uploaded in the folder `paymo_output` as `output1.txt` which corresponds to the whole `stream_payment.txt` file.

* Output of feature2 is uploaded in the folder `paymo_output` as `output2.txt` which corresponds to the whole `stream_payment.txt` file.

* Output of feature3 is uploaded in the folder `paymo_output` as `output3.txt` which corresponds to the first 1,014,348 lines of `stream_payment.txt` file.

* Output of optional feature1 is uploaded in the folder `paymo_output` as `output_optional1.txt` which corresponds to the whole `stream_payment.txt` file.

* Output of optional feature2 is uploaded in the folder `paymo_output` as `output_optional2.txt` which corresponds to the whole `stream_payment.txt` file.

* Number of output lines is slightly smaller than the number of input lines because the irregular input lines are ignored.

* Optional feature1 does not need `batch_payment.txt` as an input, just the `stream_payment.txt` is required but a `batch_payment.txt` file is uploaded in `test_optional_feature1/paymo_input` just to be consistent with the framework.

##Unit Test and Synthesized-input Tests

* Two sets of tests have been developed to verify the implementation:

	**1.** Unit tests: the `unit_tests.py` script is added to `src` folder. It contains 4 different unit tests for verification of 4 main functions of the algorithm.
			The input file to `unit_test.py` is in the same folder and is called `unittest_input_payment.txt`.
			To run the unit tests please set your working directory to the src folder and execute the following command:
			
					python unit_test.py unittest_input_payment.txt
					
					
	**2.** Synthesized-input Tests: The folder `insight_testsuite/shayas_tests` contains the synthesized inputs and corresponding outputs for the optional features. The outputs are the same as expected outputs which verifies the algorithms.
		The same test procedure have been used for features 1 to 3 and the results confirmed the correctness of the algorithms but the inputs and results are not uploades to avoid redundancy.


##Ideas for Extending Features
* If the location of the paying `user X` is available, another feature can check whether `X` has ever had a transaction with same location and generate a warning if this is not the case.
* If the MAC adress of the payer is available, one feature can check if that user has had a transaction with same MAC adress before and generate a warning if this is not the case.

