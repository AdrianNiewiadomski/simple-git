def main():
    aa = "file1", "abcd"
    bb = "file2", "abcd"
    cc = "file2", "bbbb"
    dd = "file4", "abcd"
    ee = "file5", "abcd"

    l1 = {aa, bb, cc, dd}
    print(l1)
    l2 = {bb, cc, ee}
    print(l2)

    print(l1.difference(l2))
    print(l2.difference(l1))

    diff1 = list(l1.difference(l2))
    print(diff1)
    print(diff1[0])
    print(diff1[0][0])


if __name__ == "__main__":
    main()
