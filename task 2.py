import time
import multiprocessing
from multiprocessing import Pool

def get_factors(n):
    factors = []
    for i in range(1, n + 1):
        if n % i == 0:
            factors.append(i)
    return factors

def factorize_sync(*numbers):
    return [get_factors(number) for number in numbers]

def factorize_async(*numbers):
    with Pool(processes=multiprocessing.cpu_count()) as pool:
        result = pool.map(get_factors, numbers)
    return result

start_time = time.time()
a_sync, b_sync, c_sync, d_sync = factorize_sync(128, 255, 99999, 10651060)
end_time = time.time()
print(f"Time taken (synchronous): {end_time - start_time} seconds")

start_time = time.time()
a_async, b_async, c_async, d_async = factorize_async(128, 255, 99999, 10651060)
end_time = time.time()
print(f"Time taken (multiprocessing): {end_time - start_time} seconds")

expected_a = [1, 2, 4, 8, 16, 32, 64, 128]
expected_b = [1, 3, 5, 15, 17, 51, 85, 255]
expected_c = [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
expected_d = [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]

assert a_sync == expected_a
assert b_sync == expected_b
assert c_sync == expected_c
assert d_sync == expected_d

assert a_async == expected_a
assert b_async == expected_b
assert c_async == expected_c
assert d_async == expected_d

print("Both synchronous and multiprocessing versions are correct")