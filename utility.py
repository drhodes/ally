def odd(n): return n % 2 != 0

def pairify(lst):
    if odd(len(lst)):
        raise ValueError("Odd number of elements passed to pairify")

    if len(lst) == 0:
        return []

    return [(lst[0], lst[1])] + pairify(lst[2:])

if __name__ == "__main__":
    print pairify([1, 2,3,4]) == [(1,2),(3,4)] 
    
