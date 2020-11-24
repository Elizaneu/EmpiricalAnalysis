import matplotlib.pyplot as plt
import numpy as np
from boruvkaAlgorithm import Graph

RANGE_N = (10, 101)


def empirical_f_plot(empirical_f):
    x = np.arange(*RANGE_N)
    fig, ax = plt.subplots()
    ax.scatter(x, empirical_f, c='red', edgecolor='black', label="$f(n)$")
    ax.set_title("Измеренные значения трудоемкости")
    ax.set_xlabel("Размер входных данных (n)")
    ax.set_ylabel("Трудоемкость (мс)")
    ax.legend()
    plt.show()
    fig.savefig('data/empirical_f.png')


def empirical_f_plot_asymptotic(empirical_f, c1, c2):
    x = np.arange(*RANGE_N)
    low = c1 * x * np.log2(x)
    up = c2 * x * np.log2(x)
    fig, ax = plt.subplots()
    ax.plot(x, up, color="green", label="$C_2n*log(n)$")
    ax.scatter(x, empirical_f, c="red",edgecolor='black', label="$f(n)$")
    ax.plot(x, low, color="orange", label="$C_1n*log(n)$")
    ax.set_title("Верхняя и нижняя асимптотика измеренных значений трудоёмкости")
    ax.set_xlabel("Размер входных данных (n)")
    ax.set_ylabel("Трудоёмкость (мс)")
    ax.legend()
    plt.show()
    fig.savefig('data/empirical_analysis.png')


def ratio_plot(range_n, ratio_f_g, c):
    fig, ax = plt.subplots()
    ax.set_title("Отношение измеренных значений трудоёмкости к теоретическим")
    ax.set_xlabel("Размер входных данных (n)")
    ax.scatter(range(*range_n), ratio_f_g, s=4, c="red", edgecolor='black')
    ax.plot(range(*range_n), ratio_f_g, color="red", linestyle='--', label="$f(n)/v*log(v)$")
    ax.plot(range(*range_n), [c] * (range_n[1] - range_n[0]), color="green", linestyle='--', label="C")
    ax.legend()
    plt.show()
    fig.savefig('data/ratio_f_g.png')


def ratio_f2n_fn_plot(ratio_f2_f1, n):
    fig, ax = plt.subplots()
    ax.set_title("Отношение измеренных значений трудоемкости\n при удвоении размера входных данных")
    ax.set_xlabel("Размер входных данных (n)")
    ax.scatter(n, ratio_f2_f1, marker='o', c="red", edgecolor='black')
    ax.plot(n, ratio_f2_f1, color="red", label="$f(2n)/f(n)$")
    ax.legend()
    plt.show()
    fig.savefig('data/ratio_f2_f1.png')


def empirical_analysis():
    range_n = RANGE_N
    m = 30
    repeats = 30
    f = [None] * (range_n[1] - range_n[0])

    # Search f and make plot
    for i, n in enumerate(range(*range_n)):
        f_n = [None] * m
        for j in range(m):
            g = Graph(n)
            g.graph = g.generate_graph(g.V, g.E)
            f_rep = [None] * repeats
            for k in range(repeats):
                _, f_rep[k], _ = g.boruvkaMST()
            f_n[j] = sum(f_rep) / repeats
        f[i] = sum(f_n) / m
        print(n)

    empirical_f_plot(f)

    with open('data/empirical_f_data.txt', 'w') as data:
        for fi in f:
            data.write(f"{str(fi)}\n")

    # f / g plot with asymptotic c1 & c2
    n = np.arange(*range_n)
    f = np.array(f)
    g = (n * np.log2(n))
    ratio_f_g = f / g
    for i in range(len(n)):
        c1 = min(ratio_f_g[i:])
        c2 = max(ratio_f_g[i:])
        if c1 > 0 and c2 > 0:
            print('n0:', n[i])  # n0 = 10
            print('C1:', c1)  # c1 = 0.002860566402893131
            print('C2:', c2)  # c2 = 0.007902311720114314
            break

    empirical_f_plot_asymptotic(f, c1, c2)

    # # f / g plot with asymptotic c
    # c = min(ratio_f_g)  # c = 0.002860566402893131
    # print('C: ', c)
    # ratio_plot(range_n, ratio_f_g, c)

    # f(2n) / f(n) plot
    n = range(*range_n)[:range_n[1] // 2 - range_n[0] + 1]
    f_n_1 = np.array(f[:range_n[1] // 2 - range_n[0] + 1])
    f_n_2 = np.array(f[range_n[0] * 2 - range_n[0]::2])
    ratio_f2_f1 = f_n_2 / f_n_1

    ratio_f2n_fn_plot(ratio_f2_f1, n)
