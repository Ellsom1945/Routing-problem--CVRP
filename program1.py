def Jeseph(n, k):
    a = []
    for i in range(n):
        a.append(i + 1)

    def cal(n, s):
        if n == 1:
            return a[0]
        s = (s + k) % n == 0 and n - 1 or (s + k) % n - 1
        print(a[s])
        a.remove(a[s])
        return cal(n - 1, s)

    print("ans:", cal(n, 0))


Jeseph(8, 3)
