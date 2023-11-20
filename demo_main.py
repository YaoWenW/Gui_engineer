import numpy as np
import math
import collections

# 保存结果
res = collections.defaultdict(list)
sub_w = []  # 主观权重
obj_w = []  # 客观权重
com_w = []
N = []  # 确定度


def check_all_ones(matrix):
    for row in matrix:
        for element in row:
            if element != 1:
                return "no"
    return "yes"
def Subjective_W(A):
    """
    主观权重计算
    :param A:
    :return:
    """
    try:
        R = [sum(i) for i in A]  # 重要性排序指数
        n = len(R)
        if check_all_ones(A) == 'yes':
            W = [1/n for i in range(n)]
            return W

        r_max, r_min = max(R), min(R)
        Km = r_max / r_min

        # 判断矩阵B
        B = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if R[i] >= R[j]:
                    B[i][j] = (R[i] - R[j]) / (r_max - r_min) * (Km - 1) + 1
                else:
                    B[i][j] = 1 / ((R[j] - R[i]) / (r_max - r_min) * (Km - 1) + 1)
        # print(B)

        # 拟优一致传递矩阵
        B1 = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                xx = 0
                for k in range(0, n):
                    xx += (math.log(B[i][k], 10) - math.log(B[j][k], 10))
                B1[i][j] = math.pow(10, xx / n)
        # print(B1)

        # 计算特征值
        T = []
        for i in range(n):
            ww = 1
            for j in range(n):
                ww *= B[i][j]
            T.append(math.pow(ww, 1 / n))
        print(T)
        # 计算主观权重
        W = [round(T[i] / sum(T), 3) for i in range(len(T))]

        print(W)
    except ZeroDivisionError:
        W = "计算错误，请重新输入"
        print(W)
    return W


# def objective_W(X):
#     '''
#     计算客观权重
#     :param X:
#     :return:
#     '''
#     m, n = len(X), len(X[0])
#     Xj = []  # 均值
#     Sj = []  # 均方差
#     Vj = []  # 变异系数
#     Nj = []  # 相关系数
#     Cj = []  # 独立性系数
#     Wj = []  # 综合性系数
#     for j in range(n):
#         xj = 0
#         sj = 0
#         for i in range(m):
#             xj = xj + X[i][j]
#         xj = xj / m
#         for i in range(m):
#             sj = sj + (X[i][j] - xj) ** 2
#         sj = (sj / (m - 1)) ** (1 / 2)
#         vj = sj / xj
#
#         Xj.append(xj)
#         Sj.append(sj)
#         Vj.append(vj)
#
#     #  标准化
#     X_new = [[0] * n for _ in range(m)]
#     for i in range(m):
#         for j in range(n):
#             X_new[i][j] = (X[i][j] - Xj[j]) / Sj[j]
#     # print(X_new)
#
#     R = np.corrcoef(np.array(X_new).T)
#     for j in range(n):
#         nj = 0
#         for k in range(n):
#             nj = nj + (1 - R[j][k])
#         cj = Vj[j] * nj
#         Cj.append(cj)
#         Nj.append(nj)
#
#     for j in range(n):
#         wj = Cj[j] / sum(Cj)
#         Wj.append(round(wj, 3))
#     # print(Wj)
#
#     return Wj

def objective_W(X):
    '''
    计算客观权重
    :param X:
    :return:
    '''

    n = len(X)
    matrix = [[X[j] / X[i] for i in range(n)] for j in range(n)]
    eigenvalues, eigenvectors = np.linalg.eig(matrix)

    # 找到最大特征值的索引
    max_eigenvalue_index = np.argmax(eigenvalues)

    # 获取最大特征值和对应的特征向量
    max_eigenvalue = eigenvalues[max_eigenvalue_index]
    max_eigenvector = [i for i in eigenvectors[:, max_eigenvalue_index].real]
    obj_w = [round(i/sum(max_eigenvector),3) for i in max_eigenvector]
    # obj_w = [round(i, 3) for i in obj_w]
    # print("最大特征值:", max_eigenvalue)
    # print("对应的特征向量:", max_eigenvector)
    # print("客观权重:", obj_w)
    return max_eigenvalue, max_eigenvector, obj_w

def combine_W(W1, W2):
    '''
    计算组合权重
    :param W1:
    :param W2:
    :return:
    '''
    W1 = np.array(W1)
    W2 = np.array(W2)

    A = [[np.dot(W1, W1.T), np.dot(W1, W2.T)], [np.dot(W2, W1.T), np.dot(W2, W2.T)]]
    B = [[np.dot(W1, W1.T)], [np.dot(W2, W2.T)]]
    # print(A,B)

    ak1 = np.dot(np.linalg.inv(A), B)
    ak2 = [abs(i) for i in ak1]
    ak3 = [i / sum(ak2) for i in ak2]
    # print('a = ', ak3)
    W = W1 * ak3[0][0] + W2 * ak3[1][0]

    return W


def combine2_W(W1, W2):
    '''
    计算组合权重2
    :param W1:
    :param W2:
    :return:
    '''

    o = 5 if len(W1) == 25 else 3
    sub_w1, sub_w2 = W1[:o], W1[o:]
    obj_w2 = W2

    # com_w1 = combine_W(sub_w1, obj_w1)
    com_w2 = combine_W(sub_w2, obj_w2)
    com_w = [round(z, 3) for z in com_w2]
    print('组合权重为：', com_w)
    return com_w


def cal_N(X):
    '''
    单指标确定度计算
    :param X: 样本值
    :return: N: 确定度
    '''

    Ex = [[10, 30, 50, 70, 90],
          [10, 30, 50, 70, 90],
          [10, 30, 50, 70, 90],
          [52, 35, 15, 6.5, 1.5],
          [2.1, 2.3, 2.5, 2.7, 2.9],
          [10, 30, 50, 70, 90],
          [10, 30, 50, 70, 90],

          [10, 30, 50, 70, 90],
          [35, 42.5, 47.5, 52.5, 57.5],
          [10, 30, 50, 70, 90],

          [1.35, 1.05, 0.75, 0.45, 0.15],
          [11, 8, 5, 3, 1],
          [45, 35, 25, 15, 5],
          [22.5, 17.5, 12.5, 7.5, 2.5],

          [90, 70, 50, 30, 10],
          [6, 4.5, 3.0, 1.5, 0.5],
          [55, 45, 35, 25, 10],
          [9, 7, 5, 3, 1],

          [0.25, 0.75, 1.5, 4, 6.5],
          [21, 15, 9, 3.5, 0.5]
          ]
    En = [
        [3.333, 3.333, 3.333, 3.333, 3.333],
        [3.333, 3.333, 3.333, 3.333, 3.333],
        [3.333, 3.333, 3.333, 3.333, 3.333],
        [0.833, 5, 1.667, 1.167, 0.5],
        [0.033, 0.033, 0.033, 0.033, 0.033],
        [3.333, 3.333, 3.333, 3.333, 3.333],
        [3.333, 3.333, 3.333, 3.333, 3.333],

        [3.333, 3.333, 3.333, 3.333, 3.333],
        [1.667, 0.833, 0.833, 0.833, 0.833],
        [3.333, 3.333, 3.333, 3.333, 3.333],

        [0.05, 0.05, 0.05, 0.05, 0.05],
        [0.333, 0.667, 0.333, 0.333, 0.333],
        [1.667, 1.667, 1.667, 1.667, 1.667],
        [0.833, 0.833, 0.833, 0.833, 0.833],

        [3.333, 3.333, 3.333, 3.333, 3.333],
        [0.333, 0.167, 0.333, 0.167, 0.167],
        [1.667, 1.667, 1.667, 1.667, 3.333],
        [0.333, 0.333,0.333,0.333,0.333],

        [0.083, 0.083, 0.167, 0.667, 0.167],
        [1, 1, 1, 0.833, 0.167],
    ]
    # He = np.dot(En, 0.1)

    N = []
    for i in range(len(X)):
        x = X[i]
        path = []
        for j in range(5):
            u = math.exp(-1 * (x - Ex[i][j]) ** 2 / (2 * En[i][j] ** 2))
            path.append(u)
        N.append(path)
    print('单因素矩阵为', N)
    return N


def cal_L(N, W):
    '''
    隶属度及可靠性评价
    :param N: 确定度
    :param W: 组合权重
    :return:
    '''
    L = []  # 隶属度
    for j in range(5):
        l = 0
        for i in range(len(N)):
            l += N[i][j] * W[i]
        L.append(round(l, 4))
    level_list = ['一级（低可靠性）', '二级（较低可靠性）', '三级（中等可靠性）', '四级（较高可靠性）', '五级（高可靠性）']
    level = level_list[L.index(max(L))]
    print('隶属度为：', L)
    print('可靠性等级为', level)
    return L, level



# # 1. 计算主观权重
# # 输入比较矩阵-设计阶段
# AU = [[1, 2, 1],
#       [0, 1, 2],
#       [1, 0, 1]]
# AAU = [[1, 2, 1, 0, 1],
#        [0, 1, 2, 1, 2],
#        [1, 0, 1, 0, 0],
#        [2, 1, 2, 1, 2],
#        [1, 0, 2, 0, 1],
#        ]
# AU1 = [[1, 0, 0, 0, 0, 0, 0],
#        [2, 1, 1, 2, 0, 2, 2],
#        [2, 1, 1, 1, 0, 1, 2],
#        [2, 0, 1, 1, 0, 1, 0],
#        [2, 2, 2, 2, 1, 2, 1],
#        [2, 0, 1, 1, 0, 1, 1],
#        [2, 0, 0, 2, 1, 1, 1]]
# AU2 = [[1, 0, 2],
#        [2, 1, 2],
#        [0, 0, 1]]
# AU3 = [[1, 2, 2, 1],
#        [0, 1, 2, 2],
#        [0, 0, 1, 1],
#        [1, 0, 1, 1]]
# AU4 = [[1, 2, 2, 1],
#        [0, 1, 1, 1],
#        [0, 1, 1, 1],
#        [1, 1, 1, 1]]
# AU5 = [[1, 2],
#        [0, 1]]
# sub_w = []
# for a in [AU, AU1, AU2, AU3]:
#     sub_w.extend(Subjective_W(a))

# # 权重归一化
# o = 5 if len(sub_w) == 25 else 3
# M = [7, 3, 4, 4, 2]
# s = 0
# for i in range(o):
#     for j in range(M[i]):
#         sub_w[o + s] = sub_w[i] * sub_w[o + s]
#         s += 1
# print('设计阶段主观权重为:', sub_w)
#
# sub_w = []
# for a in [AAU, AU1, AU2, AU3, AU4, AU5]:
#     sub_w.extend(Subjective_W(a))
# print('全寿命阶段主观权重为:', sub_w)

# 2. 计算客观权重
# max_eigenvalue, max_eigenvector, obj_w = objective_W(X)
# X = [0.1, 0.2,1.5,1,2,0.033,0.6,0.885,1.045,0.51,2.4,0.35,0.15,0.225,0.66, 0.198, 0.33, 2.04, 2.15, 1]
# 3. 计算组合权重
# com_w = com_w1.extend(com_w2)
# zhw = combine2_W(sub_w, obj_w)
# print('组合权重为:', zhw)
#
# # 4. 单指标确定度计算
# X1 = [100, 100, 100, 7, 2.8, 100, 100, 58, 30, 80, 0.72, 2.5, 6, 7.13, 11.46, 1.1, 7, 1.5, 7, 1]
# N = cal_N(X1)
# print('单因素确定度矩阵为:', N)
#
# # 5. 隶属度及可靠性评价
# WW1 = [0.015, 0.063, 0.038, 0.150, 0.109, 0.024, 0.030,
#        0.056, 0.132, 0.031,
#        0.053, 0.063, 0.172, 0.063]  # 设计阶段
# WW2 = [0.008, 0.029, 0.018, 0.021, 0.055, 0.012, 0.015,
#        0.044, 0.099, 0.022,
#        0.026, 0.033, 0.056, 0.038,
#        0.073, 0.099, 0.146, 0.091,
#        0.075, 0.040
#        ]  # 全寿命周期
#
# com_w = zhw
# # com_w = WW1
# L, level = cal_L(N, com_w)
# print('隶属度为:', L)
# print('可靠性等级为:', level)
