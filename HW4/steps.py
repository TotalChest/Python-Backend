import cProfile
import pstats
import io


def climb_stairs(n: int) -> int:
    if n == 0 or n == 1:
        return 1
    return climb_stairs(n - 1) + climb_stairs(n - 2)


def climb_stairs_opt(n: int) -> int:
    if n == 1:
        return 1
    base = [1, 1, 0]
    for i in range(2, n + 1):
        base[2] = base[0] + base[1]
        base[0], base[1] = base[1], base[2]
    return base[2]


def profile_func(func, n):
    pr = cProfile.Profile()
    pr.enable()
    func(n)
    pr.disable()

    s = io.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())


if __name__ == "__main__":
    profile_func(climb_stairs, 35)

    print("--------------------------")

    profile_func(climb_stairs_opt, 35)