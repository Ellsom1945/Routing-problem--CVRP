# # import tensorflow as tf
# # import numpy as np
# # import matplotlib.pyplot as plt
# #
# # tf.compat.v1.disable_eager_execution()
# # # 构造输入数据（我们用神经网络拟合x_data和y_data之间的关系）
# # x_data = np.linspace(-1, 1, 300)[:, np.newaxis]  # -1到1等分300份形成的二维矩阵
# # noise = np.random.normal(0, 0.05, x_data.shape)  # 噪音，形状同x_data在0-0.05符合正态分布的小数
# # y_data = np.square(x_data) - 0.5 + noise  # x_data平方，减0.05，再加噪音值
# # plt.plot(x_data, y_data)
# # # plt.show()
# #
# # # 输入层（1个神经元）
# # xs = tf.compat.v1.placeholder(tf.float32, [None, 1])  # 占位符，None表示n*1维矩阵，其中n不确定
# # ys = tf.compat.v1.placeholder(tf.float32, [None, 1])  # 占位符，None表示n*1维矩阵，其中n不确定
# #
# # # 隐层（10个神经元）
# # W1 = tf.Variable(tf.compat.v1.random_normal([1, 10]))  # 权重，1*10的矩阵，并用符合正态分布的随机数填充
# # b1 = tf.Variable(tf.zeros([1, 10]) + 0.1)  # 偏置，1*10的矩阵，使用0.1填充
# # Wx_plus_b1 = tf.matmul(xs, W1) + b1  # 矩阵xs和W1相乘，然后加上偏置 shape=[1,10]
# # output1 = tf.nn.relu(Wx_plus_b1)  # 激活函数使用tf.nn.relu
# #
# # # 输出层（1个神经元）
# # W2 = tf.Variable(tf.compat.v1.random_normal([10, 1]))
# # b2 = tf.Variable(tf.zeros([1, 1]) + 0.1)
# # Wx_plus_b2 = tf.matmul(output1, W2) + b2  # shape=[1, 1]
# # output2 = Wx_plus_b2
# #
# # # 损失
# # loss = tf.reduce_mean(tf.compat.v1.reduce_sum(tf.square(ys - output2), reduction_indices=[1]))  # 在第一维上，偏差平方后求和，再求平均值，来计算损失
# # train_step = tf.compat.v1.train.GradientDescentOptimizer(0.1).minimize(loss)  # 使用梯度下降法，设置步长0.1，来最小化损失
# #
# # # 初始化
# # init = tf.compat.v1.global_variables_initializer()  # 初始化所有变量
# # sess = tf.compat.v1.Session()
# # sess.run(init)  # 变量初始化
# #
# # # 训练
# # lxq = []
# # for i in range(1000):  # 训练1000次
# #     _, loss_value = sess.run([train_step, loss], feed_dict={xs: x_data, ys: y_data})  # 进行梯度下降运算，并计算每一步的损失
# #     # lxq.append(loss_value)
# #     # if(i%50==0):
# #     #     print(loss_value) # 每50步输出一次损失
# #
# # y = sess.run(output2, feed_dict={xs: x_data})
# # print(y.shape)
# # for i in range(100):
# #     print(y[i] - y[i + 1])
# # print(y)
# # plt.plot(x_data, y)
# # # plt.plot(lxq)
# # plt.show()
# import random
# # from H_Hy_Men import VRPLibReader
#
# import matplotlib.pyplot as plt
#
#
# # 产生新解——逆序
# def chpa1(tpath):
#     x = random.randint(0, len(tpath) - 1)
#     y = random.randint(0, len(tpath) - 1)
#     while x == y:
#         x = random.randint(0, len(tpath) - 1)
#     if x < y:
#         while x != y and x < y:
#             tpath[x], tpath[y] = tpath[y], tpath[x]
#             x += 1
#             y -= 1
#     else:
#         while x != y and y < x:
#             tpath[x], tpath[y] = tpath[y], tpath[x]
#             y += 1
#             x -= 1
#     return tpath
#
#
# # 产生新解——三变化
# def chpa2(tpath):
#     path = []
#     x = random.randint(0, len(tpath) - 2)
#     y = random.randint(0, len(tpath) - 2)
#     while x == y:
#         x = random.randint(0, len(tpath) - 2)
#     if x < y:
#         z = random.randint(y + 1, len(tpath) - 1)
#         path[0:x] = tpath[0:x]
#         path.append(tpath[z])
#         path[x + 1:y + 2] = tpath[x:y + 1]
#         path[y + 2:z + 1] = tpath[y + 1:z]
#         if z + 1 <= len(tpath) - 1:
#             path[z + 1:] = tpath[z + 1:]
#     else:
#         z = random.randint(y + 1, len(tpath) - 1)
#         path[0:y] = tpath[0:y]
#         path.append(tpath[z])
#         path[y + 1:x + 2] = tpath[y:x + 1]
#         path[x + 2:z + 1] = tpath[x + 1:z]
#         if z + 1 <= len(tpath) - 1:
#             path[z + 1:] = tpath[z + 1:]
#     return path
#
#
# # 产生新解——移位
# def chpa3(tpath):
#     path = []
#     x = random.randint(0, len(tpath) - 2)
#     y = random.randint(0, len(tpath) - 2)
#     while x == y:
#         x = random.randint(0, len(tpath) - 2)
#     if x < y:
#         z = random.randint(1, len(tpath) - 1 - y)
#         j = len(tpath) - 1
#         for i in range(z):
#             path.append(tpath[j])
#             j -= 1
#         path[z:] = tpath[:len(tpath) - z]
#     else:
#         z = random.randint(1, len(tpath) - 1 - x)
#         j = len(tpath) - 1
#         for i in range(z):
#             path.append(tpath[j])
#             j -= 1
#         path[z:] = tpath[:len(tpath) - z]
#     return path
#
#
# def chpa4(tpath):
#     x = random.randint(0, len(tpath) - 1)
#     y = random.randint(0, len(tpath) - 1)
#     while x == y:
#         x = random.randint(0, len(tpath) - 1)
#     tpath[x], tpath[y] = tpath[y], tpath[x]
#     return tpath
#
#
# def swap(path):
#     for i in path:
#         if len(i) > 4:
#             for sw_from in range(1, len(i) - 3):
#                 for sw_to in range(sw_from + 1, len(i) - 2):
#                     if abs(sw_from - sw_to) == 1:
#                         sw_to = max(sw_from, sw_to)
#                         sw_from = min(sw_from, sw_to)
#                         minus_cost1 = VRPLibReader.distmat[i[sw_from - 1]][i[sw_from]]
#                         minus_cost2 = 0
#                         minus_cost3 = 0
#                         minus_cost4 = VRPLibReader.distmat[i[sw_to]][i[sw_to + 1]]
#                         added_cost1 = VRPLibReader.distmat[i[sw_from - 1]][i[sw_to]]
#                         added_cost2 = 0
#                         added_cost3 = 0
#                         added_cost4 = VRPLibReader.distmat[i[sw_to + 1]][i[sw_from]]
#                     else:
#                         minus_cost1 = VRPLibReader.distmat[i[sw_from - 1]][i[sw_from]]
#                         minus_cost2 = VRPLibReader.distmat[i[sw_from]][i[sw_from + 1]]
#                         minus_cost3 = VRPLibReader.distmat[i[sw_to - 1]][i[sw_to]]
#                         minus_cost4 = VRPLibReader.distmat[i[sw_to]][i[sw_to + 1]]
#                         added_cost1 = VRPLibReader.distmat[i[sw_from - 1]][i[sw_to]]
#                         added_cost2 = VRPLibReader.distmat[i[sw_from + 1]][i[sw_to]]
#                         added_cost3 = VRPLibReader.distmat[i[sw_to - 1]][i[sw_from]]
#                         added_cost4 = VRPLibReader.distmat[i[sw_to + 1]][i[sw_from]]
#                     chcost = added_cost1 + added_cost2 + added_cost3 + added_cost4 - minus_cost1 - minus_cost2 - minus_cost3 - minus_cost4
#                     if chcost < 0:
#                         temp = i[sw_from]
#                         i[sw_from] = i[sw_to]
#                         i[sw_to] = temp
#
#     return path
#
#
# def draw_path(path):
#     color = ['r', 'k', 'y', 'c', 'b', 'g', 'm', 'dodgerblue', 'gold', 'peru', 'darkolivegreen', 'indigo', 'lime',
#              'deeppink']
#     plt.xlim(0, 100)
#     plt.ylim(0, 100)
#     for i in path:
#         c = random.choice(color)
#         for j in range(0, len(i) - 1):
#             plt.plot((VRPLibReader.site[i[j]][0], VRPLibReader.site[i[j + 1]][0]),
#                      (VRPLibReader.site[i[j]][1], VRPLibReader.site[i[j + 1]][1]), c, marker='.')
#     plt.show()
#
#
# def value(a):
#     s = 0
#     for i in a:
#         for j in range(len(i) - 1):
#             s += VRPLibReader.distmat[i[j]][i[j + 1]]
#     return s
#
#
# def inner_insert(path):
#     for i in path:
#         if len(i) > 3:
#             sw_from = random.randint(1, len(i) - 2)
#             sw_to = random.randint(1, len(i) - 2)
#             while sw_from == sw_to:
#                 sw_to = random.randint(1, len(i) - 2)
#             temp = i[sw_from]
#             i.remove(i[sw_from])
#             i.insert(sw_to, temp)
#     return path
#
#
# def or_opt(path):
#     for i in path:
#         if len(i) > 4:
#             for sw_from in range(1, len(i) - 3):
#                 for sw_to in range(1, len(i) - 2):
#                     if sw_from != sw_to and sw_from + 1 != sw_to:
#                         if sw_from < sw_to:
#                             minus_cost1 = VRPLibReader.distmat[i[sw_from - 1]][i[sw_from]]
#                             minus_cost2 = VRPLibReader.distmat[i[sw_from + 1]][i[sw_from + 2]]
#                             minus_cost3 = VRPLibReader.distmat[i[sw_to + 1]][i[sw_to]]
#
#                             added_cost1 = VRPLibReader.distmat[i[sw_from - 1]][i[sw_from + 2]]
#                             added_cost2 = VRPLibReader.distmat[i[sw_from + 1]][i[sw_to]]
#                             added_cost3 = VRPLibReader.distmat[i[sw_to + 1]][i[sw_from]]
#                         else:
#                             minus_cost1 = VRPLibReader.distmat[i[sw_from - 1]][i[sw_from]]
#                             minus_cost2 = VRPLibReader.distmat[i[sw_from + 1]][i[sw_from + 2]]
#                             minus_cost3 = VRPLibReader.distmat[i[sw_to - 1]][i[sw_to]]
#
#                             added_cost1 = VRPLibReader.distmat[i[sw_from - 1]][i[sw_from + 2]]
#                             added_cost2 = VRPLibReader.distmat[i[sw_from + 1]][i[sw_to - 1]]
#                             added_cost3 = VRPLibReader.distmat[i[sw_to]][i[sw_from]]
#                         chcost = added_cost1 + added_cost2 + added_cost3 - minus_cost1 - minus_cost2 - minus_cost3
#                         if chcost < 0:
#                             temp1 = i[sw_from]
#                             temp2 = i[sw_from + 1]
#                             i.remove(temp1)
#                             i.remove(temp2)
#                             if sw_to > sw_from:
#                                 i.insert(sw_to - 1, temp2)
#                                 i.insert(sw_to, temp1)
#                             else:
#                                 i.insert(sw_to, temp1)
#                                 i.insert(sw_to, temp2)
#
#     return path
#
#
# def exchange(path):
#     capacity = VRPLibReader.capacity
#     things = VRPLibReader.things
#     for i in range(0, len(path) - 1):
#         i_w = 0
#         for a in path[i]:
#             i_w += things[a]
#         for j in range(i + 1, len(path)):
#             j_w = 0
#             for a in path[j]:
#                 j_w += things[a]
#                 if i_w > capacity or j_w > capacity:
#                     print('ex')
#             for sw_from in range(1, len(path[i]) - 2):
#                 for sw_to in range(1, len(path[j]) - 2):
#                     minus_cost1 = VRPLibReader.distmat[path[i][sw_from - 1]][path[i][sw_from]]
#                     minus_cost2 = VRPLibReader.distmat[path[i][sw_from]][path[i][sw_from + 1]]
#                     minus_cost3 = VRPLibReader.distmat[path[j][sw_to - 1]][path[j][sw_to]]
#                     minus_cost4 = VRPLibReader.distmat[path[j][sw_to]][path[j][sw_to + 1]]
#                     added_cost1 = VRPLibReader.distmat[path[i][sw_from - 1]][path[j][sw_to]]
#                     added_cost2 = VRPLibReader.distmat[path[i][sw_from + 1]][path[j][sw_to]]
#                     added_cost3 = VRPLibReader.distmat[path[j][sw_to - 1]][path[i][sw_from]]
#                     added_cost4 = VRPLibReader.distmat[path[j][sw_to + 1]][path[i][sw_from]]
#                     chcost = added_cost1 + added_cost2 + added_cost3 + added_cost4 - minus_cost1 - minus_cost2 - minus_cost3 - minus_cost4
#                     if chcost <= 0:
#                         if i_w - things[path[i][sw_from]] + things[path[j][sw_to]] <= capacity and j_w + \
#                                 things[path[i][sw_from]] - things[path[j][sw_to]] <= capacity:
#                             temp = path[i][sw_from]
#                             path[i][sw_from] = path[j][sw_to]
#                             path[j][sw_to] = temp
#
#     return path
#
#
# p = [[0, 15, 8, 35, 2, 23, 34, 14, 28, 0],
#      [0, 16, 11, 24, 27, 25, 5, 20, 0],
#      [0, 21, 22, 32, 18, 33, 29, 30, 17, 13, 1, 0],
#      [0, 12, 31, 19, 4, 3, 6, 9, 0],
#      [0, 26, 7, 10, 0]]
# # print(p)
# # draw_path(p)
# # print(value(p))
# # or_opt(p)
# # print(value(p))
# # draw_path(p)

word=open(input('请输入文件名：')+'.txt')
connet=word.readline()
a=[]
st='aaa:'
while connet:
    if connet.__contains__(st):
        a.append(connet.lstrip(st))
print(sum(a)/len(a))