def forall(pred, iterable):
    return len(list((filter(pred, iterable)))) == len(iterable)

def exists(pred, iterable):
    return len(list((filter(pred, iterable)))) >= 1

def atleast(n, pred, iterable):
    return len(list((filter(pred, iterable)))) >= n

def atmost(n, pred, iterable):
    return len(list(filter(pred, iterable))) <= n


if __name__ == "__main__":
    lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(f"list: {lst}")

    pred = lambda x: x > 5
    print(f"pred: x > 5")

    print(f"forall: {forall(pred, lst)}")
    print(f"exists: {exists(pred, lst)}")

    n_atleast = 5
    print(f"atleast {n_atleast}: {atleast(n_atleast, pred, lst)}")

    n_atmost = 3
    print(f"atmost {n_atmost}: {atmost(n_atmost, pred, lst)}")