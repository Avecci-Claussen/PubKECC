import argparse
import pandas as pd
import cupy as cp
import numpy as np
import timeit

def count_set_bits_in_chunk(start, end):
    numbers = cp.arange(start, end + 1, dtype=cp.int64)  # dtype is important
    set_bits_counts = cp.count_nonzero((numbers[:, None] & (1 << cp.arange(32))) != 0, axis=1)
    return numbers.get(), set_bits_counts.get()

def count_set_bits_in_range(start, end, chunk_size=10000):
    all_numbers = []
    all_counts = []
    for chunk_start in range(start, end + 1, chunk_size):
        chunk_end = min(chunk_start + chunk_size - 1, end)
        chunk_numbers, chunk_counts = count_set_bits_in_chunk(chunk_start, chunk_end)
        all_numbers.append(chunk_numbers)
        all_counts.append(chunk_counts)

    numbers = np.concatenate(all_numbers)
    counts = np.concatenate(all_counts)
    return numbers, counts

def main():
    parser = argparse.ArgumentParser(description="Calculate combinations and addresses")
    parser.add_argument("-n", type=int, required=True, help="Puzzle # to search")
    args = parser.parse_args()
    n = args.n

    target_sum_min = 2 ** (n - 1)
    target_sum_max = 2 ** n - 1  # You likely meant 2^n - 1, not 2^n
    
    numbers, counts = count_set_bits_in_range(target_sum_min, target_sum_max)

    data = {'Combinations': numbers, 'Set Bits': counts}
    df = pd.DataFrame(data)
    df.to_csv(f'combo_setbits_count_n{n}.csv', index=False)

if __name__ == "__main__":
    execution_time = timeit.timeit(lambda: main(), number=1)
    print(f"Execution Time: {execution_time:.2f} seconds")
