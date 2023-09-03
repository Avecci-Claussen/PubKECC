import argparse
import pandas as pd
import numpy as np
import timeit
import numba as nb

def print_progress(iterable, desc, total=None):
    total = total or len(iterable)
    count = 0
    start_time = time.time()

    for item in iterable:
        yield item
        count += 1
        progress = count / total
        elapsed_time = time.time() - start_time
        if progress > 0:
            estimated_time_remaining = (1 / progress - 1) * elapsed_time
        else:
            estimated_time_remaining = 0
        print(f"{desc}: {count}/{total} ({progress:.0%}) - Elapsed time: {elapsed_time:.2f}s - Estimated time remaining: {estimated_time_remaining:.2f}s", end='\r')
    print()  # Add a newline to ensure the next output goes to a new line

@nb.njit  # Use Numba's JIT decorator
def calculate_sums(target_sum_min, target_sum_max, n):
    num_combinations = target_sum_max - target_sum_min + 1
    sums = np.arange(target_sum_min, target_sum_max + 1, dtype=np.int64)
    return sums

def main():
    parser = argparse.ArgumentParser(description="Calculate combinations and addresses")
    parser.add_argument("-n", type=int, required=True, help="Puzzle # to search")
    args = parser.parse_args()
    n = args.n

    target_sum_min = 2**(n - 1)
    target_sum_max = 2**n

    #start_time = time.time()

    sums = calculate_sums(target_sum_min, target_sum_max, n)

    #end_time = time.time()
    #elapsed_time = end_time - start_time

    # Measure execution time
    execution_time = timeit.timeit(lambda: calculate_sums(target_sum_min, target_sum_max, n), number=1)
    sums = calculate_sums(target_sum_min, target_sum_max, n)
    
    # Create a DataFrame for sums using pandas
    df_sums = pd.DataFrame({'Sum': sums})
    print(df_sums)

    print(f"Execution Time: {execution_time:.2f} seconds")
    
    # Write the DataFrame to a CSV file
    df_sums.to_csv(f'combo_sum_n{n}.csv', index=False)

if __name__ == "__main__":
    main()


