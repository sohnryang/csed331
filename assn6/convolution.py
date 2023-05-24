from sys import stdin

infast = lambda: stdin.readline().strip()

T = int(infast())
for _ in range(T):
    N, M, D = map(int, infast().split())
    mat = []
    for _ in range(N):
        line = [int(x) for x in infast().split()]
        mat.append(line)

    psum = []
    for _ in range(N):
        psum.append([0] * M)
    psum[0][0] = mat[0][0]
    for i, row_entry in enumerate(mat[0][1:], 1):
        psum[0][i] = psum[0][i - 1] + row_entry
    for i in range(1, N):
        psum[i][0] = psum[i - 1][0] + mat[i][0]
    for i, row in enumerate(mat[1:], 1):
        for j, entry in enumerate(row[1:], 1):
            psum[i][j] = psum[i - 1][j] + psum[i][j - 1] - psum[i - 1][j - 1] + entry

    for i in range(D - 1, N):
        for j in range(D - 1, M):
            print(
                psum[i][j]
                - (psum[i - D][j] if i >= D else 0)
                - (psum[i][j - D] if j >= D else 0)
                + (psum[i - D][j - D] if i >= D and j >= D else 0),
                end=" ",
            )
        print()
