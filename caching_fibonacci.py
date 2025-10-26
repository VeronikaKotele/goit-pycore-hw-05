def caching_fibonacci():
    """
    Return a function fib(n) that computes the nth Fibonacci number.
    Uses a closure-local cache to store previously computed results.
    """
    cache = {0: 0, 1: 1}

    def fib(n: int) -> int:
        print("Calling fib for n =", n)
        if n < 0:
            raise ValueError("n must be non-negative")
        if n in cache:
            return cache[n]
        if n - 1 not in cache:
            cache[n - 1] = fib(n - 1) # Ensures also n-2 is computed and cached

        fib_value = cache[n - 1] + cache[n - 2]
        cache[n] = fib_value
        return fib_value

    return fib


if __name__ == "__main__":
    fib = caching_fibonacci()
    print(fib(10))  # 55
    print(fib(50))  # uses cached results efficiently