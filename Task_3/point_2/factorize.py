import multiprocessing
import time

# function
def factorize(number):
    factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            factors.append(i)
    return factors

# syncronized version
def sync_version(numbers):
    start = time.time()
    results = []
    for number in numbers:
        factors = factorize(number)
        results.append(factors)
        print(f"Factors of {number} are: {factors}")
    end = time.time()
    print(f"Sync version took {end - start} seconds")
    return results

# parallel version
def parallel_version(numbers):
    start = time.time()
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    results = pool.map(factorize, numbers)
    for number, factors in zip(numbers, results):
        print(f"Factors of {number} are: {factors}")
    end = time.time()
    print(f"Parallel version took {end - start} seconds")
    return results

if __name__ == '__main__':
    numbers = [128, 255, 99999, 10651060]
    a, b, c, d = sync_version(numbers)
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]

    a, b, c, d = parallel_version(numbers)
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
