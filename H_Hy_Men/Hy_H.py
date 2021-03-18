import datetime

import tensorflow as tf
import numpy as np
import random
from collections import deque
import matplotlib.pyplot as plt
import copy

from H_Hy_Men import SA, TABU, Sp, GASA, VRPLibReader

GAMMA = 0.8  # 在更新Q函数时的折损参数
OBSERVE = 800
EXPLORE = 2000
FINAL_EPSILON = 0.0
INITIAL_EPSILON = 0.5
REPLAY_MEMORY = 800
BATCH_SIZE = 600


def one_two(path):
    tem = []
    temps = []
    for i in path:
        if (i != 0):
            tem.append(i)
        else:
            a = []
            for j in tem:
                a.append(j)
            if len(a) > 0:
                temps.append(a)
            tem.clear()
    for i in temps:
        i.append(0)
        i.insert(0, 0)
    return temps


def two_one(path):
    return [col for row in path for col in row]


class BrainDQN:

    def __init__(self, actions):

        self.replayMemory = deque()  # replayMemory是一个双向进出的队列
        self.timeStep = 0
        self.epsilon = INITIAL_EPSILON
        self.recording = EXPLORE
        self.sensor_dim = 1
        self.actions = actions
        self.hidden1 = 256
        self.hidden2 = 256
        self.hidden3 = 512

        self.createQNetwork()

    def createQNetwork(self):  # 以tf的方式搭建graph，然后完成初始化，这里的步骤只是在create，并没有开始跑

        W_fc1 = self.weight_variable([self.sensor_dim, self.hidden1])
        b_fc1 = self.bias_variable([self.hidden1])

        W_fc2 = self.weight_variable([self.hidden1, self.hidden2])
        b_fc2 = self.bias_variable([self.hidden2])

        W_fc3 = self.weight_variable([self.hidden2, self.hidden3])
        b_fc3 = self.bias_variable([self.hidden3])

        W_fc4 = self.weight_variable([self.hidden3, self.actions])
        b_fc4 = self.bias_variable([self.actions])  # 设置Q网络的权重

        self.stateInput = tf.compat.v1.placeholder("float", [None, self.sensor_dim])
        # placeholder和feed_dic是一对相互搭配使用的函数，前者申请了一个必要的空间来放置需要的数据。后者则实时输入数据

        h_fc1 = tf.nn.relu(tf.matmul(self.stateInput, W_fc1) + b_fc1)
        h_fc2 = tf.nn.relu(tf.matmul(h_fc1, W_fc2) + b_fc2)
        h_fc3 = tf.nn.tanh(tf.matmul(h_fc2, W_fc3) + b_fc3)  # 前面是在赋初始值，现在便把这个网络的隐藏层搭建好了

        self.QValue = tf.matmul(h_fc3, W_fc4) + b_fc4  # 现在是确定了输出值，输出值是QValue

        self.actionInput = tf.compat.v1.placeholder("float", [None, self.actions])
        self.yInput = tf.compat.v1.placeholder("float", [None])
        Q_action = tf.compat.v1.reduce_sum(tf.multiply(self.QValue, self.actionInput),
                                           reduction_indices=1)  # reduce_sum函数求和，后面的reduction_indices代表了求和的维度
        self.cost = tf.reduce_mean(tf.square(self.yInput - Q_action))
        self.trainStep = tf.compat.v1.train.AdamOptimizer(learning_rate=10 ** -5).minimize(
            self.cost)  # 攒够数据调参的时候，使用的就是这个地方的Adam函数，learning_rate定义的是学习率，后面的minimize是指明了优化的变量是self.cost???那么在这里，调谁的参？

        self.session = tf.compat.v1.InteractiveSession()
        self.session.run(tf.compat.v1.global_variables_initializer())  # 初始化语句

    def trainQNetwork(self):  # 数据攒够了以后，就开始调用这个部分来训练q网络，没有输入的参数，故直接调用。返回值是self.loss，这里已经开始跑这个程序了
        minibatch = random.sample(self.replayMemory,
                                  BATCH_SIZE)  # 随机地从replayMemory中取出BATCH_SIZE的数据，minibatch是一个BATCH_SIZE的数组，这里还没有对replayMemory进行赋值
        state_batch = [data[0] for data in minibatch]
        action_batch = [data[1] for data in minibatch]
        reward_batch = [data[2] for data in minibatch]
        nextState_batch = [data[3] for data in minibatch]

        y_batch = []
        QValue_batch = self.QValue.eval(feed_dict={self.stateInput: nextState_batch})
        for i in range(0, BATCH_SIZE):
            y_batch.append(reward_batch[i] + GAMMA * np.max(QValue_batch[i]))

        _, self.loss = self.session.run([self.trainStep, self.cost], feed_dict={
            self.yInput: y_batch,
            self.actionInput: action_batch,
            self.stateInput: state_batch
        })
        return self.loss

    def setPerception(self, nextObservation, action, reward):
        loss = 0
        newState = nextObservation
        self.replayMemory.append((self.currentState, action, reward, newState))
        if len(self.replayMemory) > REPLAY_MEMORY:
            self.replayMemory.popleft()
        if self.timeStep > OBSERVE:
            loss = self.trainQNetwork()
        self.currentState = newState
        self.timeStep += 1
        return loss

    def getAction(self):  # Q网络已经生成结果，此时便是要决定是选择Q网络的输出结果还是按照某种概率去探索新的世界：得到当前时刻应该采取的动作
        QValue = self.QValue.eval(feed_dict={self.stateInput: [self.currentState]})
        action = np.zeros(self.actions)
        if 0.75 < self.currentState[0] < 1.25:
            if random.random() <= self.epsilon:
                action_index = random.choice([2, 3, 4, 6, 7, 8,
                                              9])  # rando.randrange函数返回递增集合中的一个随机数，这里的action_index相当于从action许用的下标中随机选中了一个，然后在下面的语句action[action_index]中调用
                action[action_index] = 1  # action集中某个元素被置为1表示选用这个集合中的这个元素作为当前的动作
            else:
                temp = copy.deepcopy(QValue)
                temp[0][0] = -99999999
                temp[0][1] = -99999999
                temp[0][5] = -99999999
                temp[0][10] = -99999999
                action_index = np.argmax(temp)
                action[action_index] = 1
        else:
            if random.random() <= self.epsilon:
                action_index = random.randrange(
                    self.actions)  # rando.randrange函数返回递增集合中的一个随机数，这里的action_index相当于从action许用的下标中随机选中了一个，然后在下面的语句action[action_index]中调用
                action[action_index] = 1  # action集中某个元素被置为1表示选用这个集合中的这个元素作为当前的动作
            else:
                action_index = np.argmax(QValue)  # 这时选用Q网络输出值中最大值作为当前的动作
                action[action_index] = 1

        if self.epsilon > FINAL_EPSILON and self.timeStep > OBSERVE:
            self.epsilon -= (INITIAL_EPSILON - FINAL_EPSILON) / EXPLORE  # 根据步骤来更新epsilon
            self.recording = self.recording - 1  # 迭代的次数加一。换言之，每次迭代都需要调用这个getaction函数一次，迭代标志就是在这里改变的。

        return action, self.recording  # 返回action表（本质上就是告知了应该选择哪个动作，然后再参照这个动作和环境进行互动）和剩余迭代次数。

    def getAction_test(self, observation):  # 这里是所有的迭代次数已经完成，把agent投放到了环境当中实打实地去进行工作时的调用
        QValue = self.QValue.eval(feed_dict={self.stateInput: [observation]})
        action = np.zeros(self.actions)
        action_index = np.argmax(QValue)  # 这里不再采用贪心算法，直接采用q网络输出值中的最好动作即可
        action[action_index] = 1

        return action

    def setInitState(self, observation):  # 把观察到的情况输入到这个函数中作为当前时间的状态值，然后参与到上面replayMemory的工作中去。
        self.currentState = observation

    def weight_variable(self, shape):  # 和下面的bias_variable一样，都是在createQnetwork时使用的辅助函数，需要调用TF包中的相关函数
        initial = tf.compat.v1.truncated_normal(shape)
        return tf.Variable(initial)

    def bias_variable(self, shape):
        initial = tf.constant(0.01, shape=shape)
        return tf.Variable(initial)


class GameState:  # 环境生成模拟器
    def __init__(self, path, fit):
        self.dist = VRPLibReader.distmat
        self.dimension = VRPLibReader.n
        self.capacity = VRPLibReader.capacity
        self.path_best = path
        self.fit_best = fit
        self.current_path = path
        self.current_fit = fit
        self.state = 0

    def value(self, a):
        s = 0
        for i in a:
            for j in range(len(i) - 1):
                s += self.dist[i[j]][i[j + 1]]
        return s

    def frame_step(self, input_actions, path):  # 此处action应为一维数组
        a = np.flatnonzero(input_actions)[0]
        fit = self.value(path)
        self.current_path, next_fit = self.takeaction(a, path)
        self.current_fit = next_fit
        if a < 2:
            observation = [(fit - next_fit) / fit + 1]
        elif a > 7:
            observation = [(fit - next_fit) / fit + 2]
        else:
            observation = [(fit - next_fit) / fit + 1]
        if fit > next_fit:
            reward = 1
        elif fit == next_fit:
            reward = 0
        else:
            reward = -1
        return observation, reward

    def opt(self, path):
        MAXCOUNT = 100

        def calPathDist(indexList):
            sum = 0.0
            for i in range(1, len(indexList)):
                sum += self.dist[indexList[i]][indexList[i - 1]]
            return sum
            # path1长度比path2短则返回true

        def pathCompare(path1, path2):
            if calPathDist(path1) <= calPathDist(path2):
                return True
            return False

        def generateRandomPath(bestPath):
            a = np.random.randint(len(bestPath))
            while True:
                b = np.random.randint(len(bestPath))
                if np.abs(a - b) > 1:
                    break
            if a > b:
                return b, a, bestPath[b:a + 1]
            else:
                return a, b, bestPath[a:b + 1]

        def reversePath(path):
            rePath = path.copy()
            rePath[1:-1] = rePath[-2:0:-1]
            return rePath

        def updateBestPath(bestPath):
            count = 0
            while count < MAXCOUNT:
                start, end, path = generateRandomPath(bestPath)
                rePath = reversePath(path)
                if pathCompare(path, rePath):
                    count += 1
                    continue
                else:
                    count = 0
                    bestPath[start:end + 1] = rePath

        for i in path:
            if len(i) > 3:
                updateBestPath(i)
        return path

    def swap(self, path):
        for i in path:
            if len(i) > 4:
                for sw_from in range(1, len(i) - 3):
                    for sw_to in range(sw_from + 1, len(i) - 2):
                        if abs(sw_from - sw_to) == 1:
                            sw_to = max(sw_from, sw_to)
                            sw_from = min(sw_from, sw_to)
                            minus_cost1 = self.dist[i[sw_from - 1]][i[sw_from]]
                            minus_cost2 = 0
                            minus_cost3 = 0
                            minus_cost4 = self.dist[i[sw_to]][i[sw_to + 1]]
                            added_cost1 = self.dist[i[sw_from - 1]][i[sw_to]]
                            added_cost2 = 0
                            added_cost3 = 0
                            added_cost4 = self.dist[i[sw_to + 1]][i[sw_from]]
                        else:
                            minus_cost1 = self.dist[i[sw_from - 1]][i[sw_from]]
                            minus_cost2 = self.dist[i[sw_from]][i[sw_from + 1]]
                            minus_cost3 = self.dist[i[sw_to - 1]][i[sw_to]]
                            minus_cost4 = self.dist[i[sw_to]][i[sw_to + 1]]
                            added_cost1 = self.dist[i[sw_from - 1]][i[sw_to]]
                            added_cost2 = self.dist[i[sw_from + 1]][i[sw_to]]
                            added_cost3 = self.dist[i[sw_to - 1]][i[sw_from]]
                            added_cost4 = self.dist[i[sw_to + 1]][i[sw_from]]
                        chcost = added_cost1 + added_cost2 + added_cost3 + added_cost4 - minus_cost1 - minus_cost2 - minus_cost3 - minus_cost4
                        if chcost < 0:
                            temp = i[sw_from]
                            i[sw_from] = i[sw_to]
                            i[sw_to] = temp

        return path

    def exchange(self, path):
        capacity = VRPLibReader.capacity
        things = VRPLibReader.things
        for i in range(0, len(path) - 1):
            i_w = 0
            for a in path[i]:
                i_w += things[a]
            for j in range(i + 1, len(path)):
                j_w = 0
                for a in path[j]:
                    j_w += things[a]
                for sw_from in range(1, len(path[i]) - 2):
                    for sw_to in range(1, len(path[j]) - 2):
                        minus_cost1 = self.dist[path[i][sw_from - 1]][path[i][sw_from]]
                        minus_cost2 = self.dist[path[i][sw_from]][path[i][sw_from + 1]]
                        minus_cost3 = self.dist[path[j][sw_to - 1]][path[j][sw_to]]
                        minus_cost4 = self.dist[path[j][sw_to]][path[j][sw_to + 1]]
                        added_cost1 = self.dist[path[i][sw_from - 1]][path[j][sw_to]]
                        added_cost2 = self.dist[path[i][sw_from + 1]][path[j][sw_to]]
                        added_cost3 = self.dist[path[j][sw_to - 1]][path[i][sw_from]]
                        added_cost4 = self.dist[path[j][sw_to + 1]][path[i][sw_from]]
                        chcost = added_cost1 + added_cost2 + added_cost3 + added_cost4 - minus_cost1 - minus_cost2 - minus_cost3 - minus_cost4
                        if chcost <= 0 and (
                                i_w - things[path[i][sw_from]] + things[path[j][sw_to]]) < capacity and (
                                j_w + things[path[i][sw_from]] -
                                things[path[j][sw_to]]) < capacity:
                            i_w = i_w - things[path[i][sw_from]] + things[path[j][sw_to]]
                            j_w = j_w + things[path[i][sw_from]] - things[path[j][sw_to]]
                            temp = path[i][sw_from]
                            path[i][sw_from] = path[j][sw_to]
                            path[j][sw_to] = temp

                        if i_w > capacity or j_w > capacity:
                            print('ex')

        return path

    def inner_insert(self, path):
        for i in path:
            if len(i) > 3:
                for sw_from in range(1, len(i) - 2):
                    for sw_to in range(1, len(i) - 2):
                        if sw_from != sw_to:
                            if sw_from > sw_to:
                                minus_cost1 = self.dist[i[sw_from - 1]][i[sw_from]]
                                minus_cost2 = self.dist[i[sw_from]][i[sw_from + 1]]
                                minus_cost3 = self.dist[i[sw_to - 1]][i[sw_to]]

                                added_cost1 = self.dist[i[sw_from]][i[sw_to - 1]]
                                added_cost2 = self.dist[i[sw_from]][i[sw_to]]
                                added_cost3 = self.dist[i[sw_from - 1]][i[sw_from + 1]]
                            else:
                                minus_cost1 = self.dist[i[sw_from - 1]][i[sw_from]]
                                minus_cost2 = self.dist[i[sw_from]][i[sw_from + 1]]
                                minus_cost3 = self.dist[i[sw_to + 1]][i[sw_to]]

                                added_cost1 = self.dist[i[sw_from]][i[sw_to + 1]]
                                added_cost2 = self.dist[i[sw_from]][i[sw_to]]
                                added_cost3 = self.dist[i[sw_from - 1]][i[sw_from + 1]]
                            chcost = added_cost1 + added_cost2 + added_cost3 - minus_cost1 - minus_cost2 - minus_cost3
                            if chcost < 0:
                                temp = i[sw_from]
                                i.remove(i[sw_from])
                                i.insert(sw_to, temp)

        return path

    def or_opt(self, path):
        for i in path:
            if len(i) > 4:
                for sw_from in range(1, len(i) - 3):
                    for sw_to in range(1, len(i) - 2):
                        if sw_from != sw_to and sw_from + 1 != sw_to:
                            if sw_from < sw_to:
                                minus_cost1 = self.dist[i[sw_from - 1]][i[sw_from]]
                                minus_cost2 = self.dist[i[sw_from + 1]][i[sw_from + 2]]
                                minus_cost3 = self.dist[i[sw_to + 1]][i[sw_to]]

                                added_cost1 = self.dist[i[sw_from - 1]][i[sw_from + 2]]
                                added_cost2 = self.dist[i[sw_from + 1]][i[sw_to]]
                                added_cost3 = self.dist[i[sw_to + 1]][i[sw_from]]
                            else:
                                minus_cost1 = self.dist[i[sw_from - 1]][i[sw_from]]
                                minus_cost2 = self.dist[i[sw_from + 1]][i[sw_from + 2]]
                                minus_cost3 = self.dist[i[sw_to - 1]][i[sw_to]]

                                added_cost1 = self.dist[i[sw_from - 1]][i[sw_from + 2]]
                                added_cost2 = self.dist[i[sw_from + 1]][i[sw_to - 1]]
                                added_cost3 = self.dist[i[sw_to]][i[sw_from]]
                            chcost = added_cost1 + added_cost2 + added_cost3 - minus_cost1 - minus_cost2 - minus_cost3
                            if chcost < 0:
                                temp1 = i[sw_from]
                                temp2 = i[sw_from + 1]
                                i.remove(temp1)
                                i.remove(temp2)
                                if sw_to > sw_from:
                                    i.insert(sw_to - 1, temp2)
                                    i.insert(sw_to, temp1)
                                else:
                                    i.insert(sw_to, temp1)
                                    i.insert(sw_to, temp2)

        return path

    def opt_c(self, path):
        def generateRandomPath(bestPath):
            a = np.random.randint(len(bestPath))
            while True:
                b = np.random.randint(len(bestPath))
                if np.abs(a - b) > 1:
                    break
            if a > b:
                return b, a, bestPath[b:a + 1]
            else:
                return a, b, bestPath[a:b + 1]

        def reversePath(path):
            rePath = path.copy()
            rePath[1:-1] = rePath[-2:0:-1]
            return rePath

        for i in path:
            if len(i) > 3:
                generateRandomPath(i)
                start, end, t = generateRandomPath(i)
                rePath = reversePath(t)
                i[start:end + 1] = rePath
        return path

    def tabu_solver_c(self, path):
        iterations = 50
        capacity = VRPLibReader.capacity
        things = VRPLibReader.things
        while iterations > 0:
            count = 0
            i = random.randint(0, len(path) - 1)
            j = random.randint(0, len(path) - 1)
            while i == j:
                j = random.randint(0, len(path) - 1)
            i_w, j_w = 0, 0
            for a in path[i]:
                i_w += things[a]
            for a in path[j]:
                j_w += things[a]
            sw_from = random.randint(1, len(path[i]) - 2)
            sw_to = random.randint(1, len(path[j]) - 2)
            while i_w - things[path[i][sw_from]] + things[path[j][sw_to]] > capacity or j_w + things[path[i][sw_from]] - \
                    things[path[j][sw_to]] > capacity:
                if count < 10:
                    sw_from = random.randint(1, len(path[i]) - 2)
                    sw_to = random.randint(1, len(path[j]) - 2)
                else:
                    return path
                count += 1
            temp = path[i][sw_from]
            path[i][sw_from] = path[j][sw_to]
            path[j][sw_to] = temp
            iterations -= 1
        return path

    def inner_insert_c(self, path):
        for i in path:
            if len(i) > 3:
                sw_from = random.randint(1, len(i) - 2)
                sw_to = random.randint(1, len(i) - 2)
                while sw_from == sw_to:
                    sw_to = random.randint(1, len(i) - 2)
                temp = i[sw_from]
                i.remove(i[sw_from])
                i.insert(sw_to, temp)
        return path

    def takeaction(self, action, path):
        fit = self.value(path)
        if action == 0:  # 启发式算子
            oldpath = copy.deepcopy(path)
            gasa = GASA.GASA()
            path = gasa.GASA_solver(path)[0]
            if len(path) > VRPLibReader.carnum:
                path = oldpath
            fit = self.value(path)

        elif action == 1:
            oldpath = copy.deepcopy(path)
            sa = SA.SA()
            path = sa.SA_solver(path)[0]
            if len(path) > VRPLibReader.carnum:
                path = oldpath
            fit = self.value(path)

        elif action == 2:

            path = TABU.tabu_solver(path)
            fit = self.value(path)

        elif action == 3:  # 优化算子

            path = self.opt(path)
            fit = self.value(path)

        elif action == 4:

            path = self.swap(path)
            fit = self.value(path)

        elif action == 5:

            path = self.inner_insert(path)
            fit = self.value(path)

        elif action == 6:

            path = self.exchange(path)
            fit = self.value(path)

        elif action == 7:

            path = self.or_opt(path)
            fit = self.value(path)

        elif action == 8:  # 变异

            path = self.opt_c(path)
            fit = self.value(path)

        elif action == 9:

            path = self.tabu_solver_c(path)
            fit = self.value(path)

        elif action == 10:

            path = self.inner_insert_c(path)
            fit = self.value(path)

        if fit < self.fit_best:
            self.path_best = copy.deepcopy(path)
            self.fit_best = fit
        return path, fit


tf.compat.v1.disable_eager_execution()
actions = 11  # 返回数组P的长度，这里的长度是9
SP = []
anslist = Sp.sp
# SP.append([one_two(Greedy.total_cost), [0]])
for i in anslist:
    SP.append([i, [0]])
brain = BrainDQN(actions)  # DQN模拟生成器，需要告知动作空间的个数
com = GameState(SP[0][0], 999999)  # 一个环境模拟生成器
terminal = True
recording = EXPLORE  # 迭代次数标记
Fit = []
FB = []
State = []
while recording > 0:  # 每次迭代都需要执行这个函数段
    # initialization
    print(recording, brain.timeStep)
    if terminal:
        ind_0 = random.choice(SP)
        ind = copy.deepcopy(ind_0)
        action = np.zeros(actions)
        action_index = random.randrange(actions)
        action[action_index] = 1
        observation0, reward0 = com.frame_step(action, ind[0])
        brain.setInitState(ind[1])
        com.current_path = ind[0]
        com.current_fit = com.value(ind[0])
        terminal = False
    # if brain.timeStep < OBSERVE:
    #     action, recording = brain.getAction()  # 每次迭代都按照DQN包中的函数来得到本次迭代选择的action（返回值是一个数组，这个数组里面被赋值为1的action便是本次迭代选择的动作）
    #     nextObservation, reward = com.frame_step(action, com.current_path)
    #     loss = brain.setPerception(nextObservation, action, reward)
    #     FB.append(com.fit_best)
    # else:
    action, recording = brain.getAction()  # 每次迭代都按照DQN包中的函数来得到本次迭代选择的action（返回值是一个数组，这个数组里面被赋值为1的action便是本次迭代选择的动作）
    print(action)
    nextObservation, reward = com.frame_step(action, com.current_path)  # 取得了action列表，我们就要按照和这个action和环境互动了
    loss = brain.setPerception(nextObservation, action, reward)  # 得到本次的loss值
    if com.current_fit < com.fit_best:
        terminal = True
        SP.append([com.current_path, brain.currentState])
    else:
        if random.random() > 0.9:
            terminal = True
            SP.append([com.current_path, brain.currentState])
        else:
            terminal = True
    Fit.append(com.current_fit)
    FB.append(com.fit_best)
    State.append(nextObservation)


def draw_path(path, sites):
    color = ['r', 'k', 'y', 'c', 'b', 'g', 'm', 'dodgerblue', 'gold', 'peru', 'darkolivegreen', 'indigo', 'lime',
             'deeppink']
    plt.xlim(0, 100)
    plt.ylim(0, 100)
    for i in path:
        c = random.choice(color)
        for j in range(0, len(i) - 1):
            plt.plot((sites[i[j]][0], sites[i[j + 1]][0]), (sites[i[j]][1], sites[i[j + 1]][1]), c, marker='.')
    plt.show()


draw_path(com.path_best, VRPLibReader.site)
plt.plot(Fit)
plt.show()
plt.plot(FB)
plt.show()
plt.plot(State)
plt.show()
print(com.fit_best)
print(com.path_best)
print(datetime.datetime.now())
