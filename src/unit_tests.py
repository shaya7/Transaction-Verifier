#!/usr/bin/python

import sys
from collections import defaultdict
import antifraud as unit_test


synthesized_graph = {'1': set(['2','3']),
          '2': set(['1','4']),
          '3': set(['1','5']),
          '4': set(['2','5','7']),
          '5': set(['4','3','6']),
          '6': set(['5','9']),
          '7': set(['4','8','10']),
          '8': set(['9','7']),
          '9': set(['8','6','12']),
          '10': set(['7','13']),
          '11': set(['12','14']),
          '12': set(['9','11','15']),
          '13': set(['10']),
          '14': set(['11']),
          '15': set(['12']),
          }
test_graph = defaultdict(set,synthesized_graph,)    
    
def main(args): 
    """ Main function to run the unit tests.
        Arguments: path to the test_graph text file e.g. ~/Transaction-Verifier/src/unittest_input_payment.txt.
    """
    print 'Running unit test for making the network graph... Result:'    
    batch_graph = unit_test.get_batch_graph(args[1])
    if (batch_graph == test_graph):
        print 'Pass'
    else:
        print 'Fail'    
    
    
    print 'Running unit test for checking existence of a direct link... Result:'
    out_direct = unit_test.check_direct_link(test_graph, '1', '3') 
    if (out_direct == 'trusted'):
        print 'Pass'
    else:
        print 'Fail'

    print 'Running unit test for checking existence of a degree 2 link... Result:'
    out_degree2 = unit_test.check_degree2_link(test_graph, '1', '4') 
    if (out_degree2 == 'trusted'):
        print 'Pass'
    else:
        print 'Fail'

    print 'Running unit test for checking existence of a length4 or shorter path with BFS... Result:'    
    out_bfs = unit_test.shortest_bfs_path(test_graph,'1','8', 4)
    if (out_bfs == 'trusted'):
        print 'Pass'
    else:
        print 'Fail'    
    return

    
if __name__ == '__main__':
    main(sys.argv)
