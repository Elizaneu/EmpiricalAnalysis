import random
import time


class Graph:

    def __init__(self, vertices):
        self.V = vertices
        self.E = vertices * 4
        self.graph = []

    def generate_graph(self, v, e):
        #e = random.randint(v - 1, v * (v - 1) / 2)
        graph = []
        big_graph = list([0] * v for i in range(0, v))
        initial_set = set()
        visited_set = set()
        vertices = set()

        for i in range(v):
            initial_set.add(str(i))
            vertices.add(str(i))

        cur_v = random.sample(initial_set, 1).pop()
        initial_set.remove(cur_v)
        visited_set.add(cur_v)

        # Строим список ребер
        while initial_set:
            adj_v = random.sample(initial_set, 1).pop()
            if cur_v < adj_v:
                edge = [int(cur_v), int(adj_v), random.randint(1, 10)]
            else:
                edge = [int(adj_v), int(cur_v), random.randint(1, 10)]
            graph.append(edge)
            big_graph[int(cur_v)][int(adj_v)] = 1
            big_graph[int(adj_v)][int(cur_v)] = 1
            initial_set.remove(adj_v)
            visited_set.add(adj_v)
            cur_v = adj_v

        tmp_e = v - 1

        # Выбираем оставшиеся E - V + 1 ребер
        while tmp_e < e:
            begin_v = random.randint(0, v - 1)
            end_v = random.randint(0, v - 1)
            if begin_v > end_v:
                begin_v, end_v = end_v, begin_v
            if big_graph[begin_v][end_v] == 0 and begin_v != end_v:
                is_exist_e = random.randint(False, True)
                if is_exist_e:
                    graph.append([begin_v, end_v, random.randint(1, 10)])
                    big_graph[begin_v][end_v] = 1
                    big_graph[end_v][begin_v] = 1
                    tmp_e += 1

        return graph

    # Функция поиска родительской вершины
    def find(self, parent, i):
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])

    # Функция объединения двух фрагментов
    def union(self, parent, rank, x, y):
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)

        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1

    def boruvkaMST(self):
        #print(self.graph)
        parent = []
        rank = []
        cheapest = []
        numTrees = self.V
        MSTweight = 0
        mst = []

        time_start = time.time()
        # Изначально каждая вершина - тривиальное дерево
        for node in range(self.V):
            parent.append(node)
            rank.append(0)
            cheapest = [-1]*self.V

        # Пока количество деревьев больше единицы,
        # находим самые легкие инцидентные фрагменту ребра и объединяем соотв. фрагменты
        while numTrees > 1:
            for i in range(len(self.graph)):
                u, v, w = self.graph[i]
                set1 = self.find(parent, u)
                set2 = self.find(parent, v)

                if set1 != set2:
                    if cheapest[set1] == -1 or cheapest[set1][2] > w:
                        cheapest[set1] = [u, v, w]
                    elif cheapest[set1][2] == w and cheapest[set1][1] > v:
                        cheapest[set1] = [u, v, w]

                    if cheapest[set2] == -1 or cheapest[set2][2] > w:
                        cheapest[set2] = [u, v, w]
                    elif cheapest[set2][2] == w and cheapest[set2][1] > v:
                        cheapest[set2] = [u, v, w]

            for node in range(self.V):
                if cheapest[node] != -1:
                    u, v, w = cheapest[node]
                    set1 = self.find(parent, u)
                    set2 = self.find(parent, v)

                    if set1 != set2:
                        MSTweight += w
                        self.union(parent, rank, set1, set2)
                        numTrees -= 1
                        mst.append([u, v, w])

            cheapest = [-1] * self.V

        time_end = time.time()
        alg_time = (time_end - time_start) * 1000
        return mst, alg_time, MSTweight
