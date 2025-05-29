from functools import lru_cache

def make_generator(func):
    def generator():
        n = 1
        while True:
            yield func(n)
            n += 1
    return generator()

#zad5
def make_generator_mem(func):
    return make_generator(lru_cache(None)(func))

@lru_cache(None) #or fib_mem = lru_cache(None)(fibonacci_rec)
def fibonacci_rec(n):
    if n <= 2:
        if n == 1:
            return 0
        return 1
    return fibonacci_rec(n-1) + fibonacci_rec(n-2)
#zad5

def fibonacci(n):
    fibo_list = [0, 1]
    for i in range(2, n):
        fibo_list.append(fibo_list[i - 1] + fibo_list[i - 2])
    return fibo_list[n - 1]

gen_fibo = make_generator(fibonacci)
gen_mem_fibo = make_generator_mem(fibonacci)
gen_fibo_rec_mem = make_generator_mem(fibonacci_rec)
gen_arith = make_generator(lambda n: 2 * n + 2)
gen_geo = make_generator(lambda n: 2 ** n)


if __name__ == "__main__":
    print(f"gen_fibo: {list((next(gen_fibo) for _ in range(10)))}")
    print(f"gen_mem_fibo: {list((next(gen_mem_fibo) for _ in range(10)))}")
    print(f"gen_fibo_rec_mem: {list((next(gen_fibo_rec_mem) for _ in range(10)))}")
    print(f"gen_arith: {list((next(gen_arith) for _ in range(10)))}")
    print(f"gen_geo: {list((next(gen_geo) for _ in range(10)))}")