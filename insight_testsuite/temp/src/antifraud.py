#!/usr/bin/python

import sys
from collections import defaultdict as dfdict
import csv
import logging
import copy


"""Optional feature flag. Set to 0 if you don't want to analyze the optional feature."""
optional_feature_flag = 0
if optional_feature_flag:
    from numpy import average as ave


logger = logging.getLogger(__name__)
logging.basicConfig(format='%(message)s', level=logging.INFO)

def get_batch_graph(infile):
    """
    Function to form the user network graph from the input file e.g. batch_paymet.csv.
    Input: batch payment file
    Output: user network graph
    """
    csv.field_size_limit(sys.maxsize)
    batch_graph = dfdict(set)   # initialize the network graph 
    with open(infile,'rU') as fin: 
        batchfile = csv.DictReader(fin,skipinitialspace=True)
        for line in batchfile:
            try: # check for the input irregularity
                _ = int(line['id1'])    # line['id1'] is user1
                _ = int(line['id2'])    # line['id2'] is user2
            except:
                continue
            # add the transaction to the network graph
            batch_graph[line['id1']].add(line['id2'])   
            batch_graph[line['id2']].add(line['id1'])

    return (batch_graph)


def check_direct_link(graph, node1, node2):
    """ Function to check whether there exists an edge (direct link) between node1 and node2 of the graph. 
        It will return 'trusted' if an edge exists, otherwise it will return 'unverified'.
    """
    if node1 in graph[node2]:
        return('trusted') #There is a direct link between node1 and node2
    else:
        return('unverified') #There is no direct link between node1 and node2


def check_degree2_link(graph, node1, node2):
    """ Function to check whether node1 and node2 of the graph have any common adjacent nodes i.e. there
        exists at least one degree2 link between them. 
        It will return 'trusted' if such a link exists, otherwise it will return 'unverified'.
    """
    if bool(graph[node1].intersection(graph[node2])): # check if node1 and node2 have any common adjacent nodes
        return('trusted') 
    else:
        return('unverified') 


def shortest_bfs_path(graph, node1, node2, degree): 
    """ Function that uses Breadth First Search (BFS) method on the graph to find the shortest path 
        between node1 and node2 the length of which is not longer than the specified degree.
        If such a path exists the function will return 'trusted', otherwise it will return 'unverified'. 
    """
    start_node = node1
    end_node = node2
    # If node2 has fewer adjacent nodes, start the search from it
    if len(graph[node1]) > len(graph[node2]): 
        start_node = node2
        end_node = node1
    queue = [(start_node, [start_node])]
    while queue:
        (vertex, path) = queue.pop(0)
        for nextnode in graph[vertex] - set(path):
            if nextnode == end_node:
                return ('trusted')
            elif len(path) < degree: #if the current paths are of length (degree) don't go further
                queue.append((nextnode, path + [nextnode]))
    return ('unverified')
 
 
def feature1_verification(graph, infile, outfile):
    """ Function to check the feature1 for each line of the input file. It writes the result ('trusted' or 'unverified')
    in the corresponding line of the output file.
    Inputs: network graph i.e. output of get_batch_graph function, stream_payment file, output file.
    """
    f1_graph = copy.deepcopy(graph) # graph to be used and updated during feature1 analysis
    with open(outfile,'wb') as fout:
        with open(infile,'rU') as fin:
            file_to_process = csv.DictReader(fin,skipinitialspace=True) 
            csv.field_size_limit(sys.maxsize)
            for line in file_to_process:
                # check for the input irregularity
                try: 
                    _ = int(line['id1'])
                    _ = int(line['id2'])
                except:
                    continue
                if line['id1'] == line['id2']: # user1 and user2 are the same person
                    fout.write('trusted' +'\n')
                else:
                    fout.write(check_direct_link(f1_graph, line['id1'], line['id2']) +'\n')
                # update the network
                f1_graph[line['id1']].add(line['id2']) 
                f1_graph[line['id2']].add(line['id1'])
                
    return 
    
    
def feature2_verification(graph, infile, outfile):
    """ Function to check the feature2 for each line of the input file. It writes the result ('trusted' or 'unverified')
    in the corresponding line of the output file.
    Inputs: network graph i.e. output of get_batch_graph function, stream_payment file, output file.
    """
    f2_graph = copy.deepcopy(graph) # graph to be used and updated during feature2 analysis
    with open(outfile,'wb') as fout:
        with open(infile,'rU') as fin:
            file_to_process = csv.DictReader(fin,skipinitialspace=True) 
            csv.field_size_limit(sys.maxsize)
            for line in file_to_process:
                # check for the input irregularity
                try: 
                    _ = int(line['id1'])
                    _ = int(line['id2'])
                except:
                    continue
                if line['id1'] == line['id2']: # user1 and user2 are the same person
                    fout.write('trusted' +'\n')
                elif check_direct_link(f2_graph, line['id1'], line['id2']) =='trusted':
                    fout.write('trusted' +'\n')
                    continue
                else:
                    fout.write(check_degree2_link(f2_graph, line['id1'], line['id2']) +'\n')
                    # update the network
                    f2_graph[line['id1']].add(line['id2'])
                    f2_graph[line['id2']].add(line['id1'])

                
    return    
 
    
def feature3_verification(graph, infile, outfile):
    """ Function to check the feature3 for each line of the input file. It writes the result ('trusted' or 'unverified')
    in the corresponding line of the output file.
    Inputs: network graph i.e. output of get_batch_graph function, stream_payment file, output file.
    """
    f3_graph = copy.deepcopy(graph) # graph to be used and updated during feature3 analysis
    with open(outfile,'wb') as fout:
        with open(infile,'rU') as fin:
            file_to_process = csv.DictReader(fin,skipinitialspace=True)
            csv.field_size_limit(sys.maxsize)
            for line in file_to_process:
                # check for the input irregularity
                try: 
                    _ = int(line['id1'])
                    _ = int(line['id2'])
                except:
                    continue
                if line['id1'] == line['id2']: # user1 and user2 are the same person
                    fout.write('trusted' +'\n')
                elif check_direct_link(f3_graph, line['id1'], line['id2'])=='trusted':
                    fout.write('trusted' +'\n')
                    continue
                elif check_degree2_link(f3_graph, line['id1'], line['id2'])=='trusted':
                    fout.write('trusted' +'\n')
                    # update the network
                    f3_graph[line['id1']].add(line['id2']) 
                    f3_graph[line['id2']].add(line['id1'])
                    continue
                else:
                    fout.write(shortest_bfs_path(f3_graph, line['id1'], line['id2'], 4) +'\n')
                    # update the network
                    f3_graph[line['id1']].add(line['id2'])
                    f3_graph[line['id2']].add(line['id1'])            
    return    

def optional_feature1_verification(max_amount, infile, outfile):
    """
    Function to check if the amount of each transaction is less than or equal to the maximum amount allowed to transfer.
    writes 'unverified' in the corresponding line of output file if the amount is larger than maximum allowed and 'trusted otherwise.
    """
    with open(outfile,'wb') as fout:
        with open(infile,'rU') as fin:
            file_to_process = csv.DictReader(fin,skipinitialspace=True)
            csv.field_size_limit(sys.maxsize)
            for line in file_to_process:
                try:
                    if float(line['amount']) > max_amount:
                        fout.write('unverified'+'\n')
                    else:
                        fout.write('trusted'+'\n') 
                except:
                    continue
    return 
    
    
def optional_feature2_verification(batch_infile, stream_infile, outfile):
    """
    Function to check if the amount of each transaction is less than or equal to twice the average amounts payed by user1 so far.
    writes 'unverified' in the corresponding line of output file if the amount is larger and 'trusted otherwise.
    """
    csv.field_size_limit(sys.maxsize)
    batch_dict = dfdict(list)   # initialize the dictionary that contains the amounts of transactions of each user 
    with open(batch_infile,'rU') as fin: 
        batchfile = csv.DictReader(fin,skipinitialspace=True)
        for line in batchfile:
            try: # check for the input irregularity
                _ = int(line['id1'])    # line['id1'] is user1
                amnt = float(line['amount'])
                # add the transaction to the user dictionary
                batch_dict[line['id1']].append(amnt)  
            except:
                continue
             
            
    # dictionary to contain the number and average amount of transactions for each user        
    average_dict = dict()   
    for user in batch_dict:
        # create entry {user:[average amount, number of transactions]}
        average_dict[user] = [ave(batch_dict[user]),len(batch_dict[user])]
        
    with open(outfile,'wb') as fout:
        with open(stream_infile,'rU') as fin:
            file_to_process = csv.DictReader(fin,skipinitialspace=True)
            csv.field_size_limit(sys.maxsize)
            for line in file_to_process:
                try: 
                    # check for the input irregularity
                    _ = int(line['id1'])    # line['id1'] is user1
                    amnt = float(line['amount'])
                    if  amnt > 2*average_dict[line['id1']][0]:
                        fout.write('unverified'+'\n')
                    else:
                        fout.write('trusted'+'\n')
                    count = average_dict[line['id1']][1]
                    ave_old = average_dict[line['id1']][0]
                    new_count = count+1
                    new_ave = (ave_old*count + amnt)/float(new_count)
                    average_dict[line['id1']] = [new_ave, new_count]
                except:
                    continue

    return


def main(inputs): 
    
    batch_infile = inputs[1]
    stream_infile = inputs[2]
    outfile1 = inputs[3]
    outfile2 = inputs[4]
    outfile3 = inputs[5]
    
    logger.info("Constructing the Network of users form the batch_payment file ... ")
    batch_graph = get_batch_graph(batch_infile) 
    logger.info("completed")
     
    # Use feature1 to verify transactions (direct link)
    logger.info("Using feature1 for stream file transaction verification ... ")
    feature1_verification(batch_graph, stream_infile, outfile1)
    logger.info("completed")
              
    # Use feature2 to verify transactions (friend of friend)
    logger.info("Using feature2 for stream file transaction verification ... ")
    feature2_verification(batch_graph, stream_infile, outfile2)
    logger.info("completed")
 
    # Use feature3 to verify transactions (friend of friend)
    logger.info("Using feature3 for stream file transaction verification ...")
    feature3_verification(batch_graph, stream_infile, outfile3)    
    logger.info("completed")
    
    if optional_feature_flag:
        """ Optional feature1: define a limit for the amount of each transaction.
        Transactions with amounts not larger than the limit are 'trusted'. The rest of transactions are 'unverified'.
        """
        opt_outfile1 = outfile3.replace(outfile3.split('/')[-1],'output_optional1.txt') # save the output in the same directory as outfile3
        max_amount = 25 # Maximum amount that can be transferred between users in a single transaction.
        logger.info("Using optional feature1 for stream file transaction verification ...")
        optional_feature1_verification(max_amount, stream_infile, opt_outfile1)    
        logger.info("completed")
        
        """ Optional feature2: find the average amount payed by user1 (the payer) so far. If the transaction of
        user1 to be verified has an amount larger than twice the average mark the transaction as 'unverified'.
        """ 
        opt_outfile2 = outfile3.replace(outfile3.split('/')[-1],'output_optional2.txt') # save the output in the same directory as outfile3
        logger.info("Using optional feature2 for stream file transaction verification ...")
        optional_feature2_verification(batch_infile, stream_infile, opt_outfile2)    
        logger.info("completed")
    
    return

    
if __name__ == '__main__':
    main(sys.argv)
