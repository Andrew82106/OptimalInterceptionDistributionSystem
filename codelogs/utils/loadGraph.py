import numpy as np
from typing import List

"""
输入图的格式：
a b w
从a到b，权重为w
零基准
"""
example = """
1 2 5
2 3 6
4 5 7
"""


def FormatChecker(Datain: str) -> List:
    _x = Datain.split("\n")
    res = []
    for i in _x:
        u = i.split(" ")
        if i == '\n' or len(i) == 0:
            continue
        elif len(u) == 3:
            res.append([int(u[0]), int(u[1]), int(u[2])])
        else:
            raise Exception("格式不合，无法读入")
    return res


def loadGraph(Datain: str, maxN: int, directed=True) -> np.ndarray:
    GraphList = FormatChecker(Datain)
    GraphMatrix = np.zeros((maxN, maxN))
    for i in GraphList:
        GraphMatrix[i[0]][i[1]] = i[2]
        if not directed:  # 如果是无向图那就加两条边
            GraphMatrix[i[1]][i[0]] = i[2]
    return GraphMatrix


if __name__ == '__main__':
    x = loadGraph(example, 10)
    print(x)
