def acronym(l):
    return list(map(lambda x: x[0], l))

def median(l):
    l = sorted(l)
    n = len(l)
    mid = n // 2
    return (l[mid] + l[-mid - 1]) / 2 if n % 2 == 0 else l[mid]

def square_root(x, y=1, eps=0.0001):
    return y if abs(y ** 2 - x) < eps else square_root(x, (y + x / y) / 2, eps)

def make_alpha_dict(s):
    s_list = s.split()
    letters = sorted(set(filter(lambda x: x.isalpha(), s)))
    return { char: [word for word in s_list if char in word] for char in letters }

def flatten(l):
    return sum([flatten(x) if isinstance(x, list) else [x] for x in l], [])


if __name__ == "__main__":
    acr_arg = ["Zakład", "Ubezpieczeń", "Społecznych"]
    print(f"acronym: {acr_arg} -> {acronym(acr_arg)}")

    median_arg = [1, 1, 19, 2, 3, 4, 4, 5, 1]
    print(f"median: {median_arg} -> {median(median_arg)}")

    square_root_arg = 2
    print(f"square_root: {square_root_arg} -> {square_root(square_root_arg)}")

    make_alpha_dict_arg = "on i ona"
    print(f"make_alpha_dict: {make_alpha_dict_arg} -> {make_alpha_dict(make_alpha_dict_arg)}")

    flatten_arg = [1, [2, 3], [[4, 5], 6]]
    print(f"flatten: {flatten_arg} -> {flatten(flatten_arg)}")