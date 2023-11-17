#
# Construct a simple multiprocessing frameworkd
#
#
# 

import multiprocessing as mp
import time

# a closure to save the init state will not work with multiprocessing
# https://www.stevenengelhardt.com/2013/01/16/python-multiprocessing-module-and-closures/
class fitness:
    def __init__(self, extraState):
        self.extraState = extraState

    def __call__(self, x):
        # Do work, using self.extraState as needed
        return self.extraState * x * x * x




start_time = time.time()
if __name__ == '__main__':

    with mp.Pool(4) as p:
        p.map(fitness(2), range(100000000), 100)
    print('Execution time = %0.1f sec ' % (time.time() - start_time))