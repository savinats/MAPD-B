# cpu_intensive_multiprocessing.py
import time
import math
import random
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, wait
from multiprocessing import Pool

def f(x):
    """An arbitrary mathematical function"""
    return (math.sin(1/(x*(2-x))))**2
            
def cpu_function(seed):
    """A function performing an MC integration 
    of `f(x)` taking as input a given seed.
    """
    time_start = time.time()

    # Number of points to generate
    _n = 2_000_000

    # Initialize a local random number generator
    local_random = random
    local_random.seed(seed)

    # Perform the numerical integration
    _count = 0
    for _ in range(_n):
        x = 2 * local_random.random()
        y = local_random.random()
        if y < f(x):
            _count += 1

    print(f'time to perform numerical integration over {_n} entries = {time.time()-time_start:.2f} sec')

    # Return the count
    return (_count, _n)    
    
    
if __name__ == '__main__':
    
    # Start a timer
    start = time.time()

    # Define the number of processes 
    N_PROCESSES = 4

    # Number of chunks
    n_chunks = 10

    # Total number of points and count
    total_n = 0
    total_count = 0


    """ `Pool` + `map` alternative """
    # Create a pool of processes
    # pool = Pool(N_PROCESSES)

    # Submit multiple instances of the function  
    # future_results = pool.map_async(cpu_function, [_ for _ in range(n_chunks)])
    
    # Get the results
    # results = future_results.get()
    """ --- """


    """ Alternative based on `concurrent.futures` library """
    # Create an executor for a number of processes
    executor = ProcessPoolExecutor(max_workers=N_PROCESSES)

    # Submit the applications as multiple processes 
    futures = [executor.submit(cpu_function, _) for _ in range(n_chunks)]   

    # Wait for all processes to be done
    wait(futures)

    # Get the process results and the total sums
    results = [f.result() for f in futures]
    """ --- """  
    
    
    for res in results:
        total_count += res[0]
        total_n += res[1]
    
    # Compute the integral
    integral = 2 * total_count / total_n

    # Stop the timer
    end = time.time()
    
    print()
    print(f'Integral evaluated over {total_n} points = {integral}')
    print()
    print(f'Time taken = {end - start:.2f} sec')
