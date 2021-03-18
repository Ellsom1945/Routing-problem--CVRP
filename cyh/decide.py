import torch
import torch.nn as nn
import torch.nn.functional as F
import matplotlib.pyplot as plt
import numpy as np
from cyh.change_path import *
from cyh.value_function import *
from cyh.VRPLibReader2 import *
from cyh.SA import *
from cyh.GASA import *
from cyh.oropt import *


def achieve(i, tpath, rm):
    if i == 0:
        return list(chpa1(tpath))
    elif i == 1:
        return list(chpa2(tpath))
    elif i == 2:
        return list(chpa3(tpath))
    elif i == 3:
        return list(chpa4(tpath))
    elif i == 4:
        sa = SA(100, 0.1, 0.9, 100)
        tpath, b = sa.SA_solver(rm.distmat, rm.things, rm.capacity, tpath)
        return list(tpath)
    elif i == 5:
        gasa = GASA(100, 0.1, 0.9, 100, 100, 0.1, 20)
        tpath, b = gasa.GASA_solver(rm.distmat, rm.things, rm.capacity, tpath)
        return list(tpath)
    else:
        return list(oropt(tpath, rm.n - 1, rm.distmat, rm.capacity, rm.things))


def Init(f, distmat, weight, things, n, p, pb):
    for i in range(len(p)):
        tl = list(range(1, n))
        random.shuffle(tl)
        p[i] = np.array(tl).copy()
        vi = value_function(distmat, p[i], weight, things)
        if vi < f:
            f = vi
            pb = list(p[i])
    return list(pb), f


# Hyper Parameters
BATCH_SIZE = 32
LR = 0.01  # learning rate
EPSILON = 0.9  # greedy policy
GAMMA = 0.9  # reward discount
TARGET_REPLACE_ITER = 100  # target update frequency
MEMORY_CAPACITY = 2000
N_ACTIONS = 6
N_STATES = 1


# ENV_A_SHAPE = 0 if isinstance(env.action_space.sample(), int) else env.action_space.sample().shape     # to confirm the shape

class Net(nn.Module):
    def __init__(self, ):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(N_STATES, 10)
        self.fc1.weight.data.normal_(0, 0.1)  # initialization
        self.out = nn.Linear(10, N_ACTIONS)
        self.out.weight.data.normal_(0, 0.1)  # initialization

    def forward(self, x):
        x = self.fc1(x)
        x = F.relu(x)
        actions_value = self.out(x)
        return actions_value


class DQN(object):
    def __init__(self):
        self.eval_net, self.target_net = Net(), Net()

        self.learn_step_counter = 0  # for target updating
        self.memory_counter = 0  # for storing memory
        self.memory = np.zeros((MEMORY_CAPACITY, N_STATES * 2 + 2))  # initialize memory
        self.optimizer = torch.optim.Adam(self.eval_net.parameters(), lr=LR)
        self.loss_func = nn.MSELoss()

    def choose_action(self, x):
        x = torch.unsqueeze(torch.FloatTensor(x), 0)
        # input only one sample
        if np.random.uniform() < EPSILON:  # greedy
            actions_value = self.eval_net.forward(x)
            action = torch.max(actions_value, 1)[1][0].data.numpy()
            # action = action[0] if ENV_A_SHAPE == 0 else action.reshape(ENV_A_SHAPE)  # return the argmax index
        else:  # random
            action = np.random.randint(0, N_ACTIONS)
            # action = action if ENV_A_SHAPE == 0 else action.reshape(ENV_A_SHAPE)
        return action

    def store_transition(self, s, a, r, s_):
        transition = np.hstack((s, [a, r], s_))
        # replace the old memory with new memory
        index = self.memory_counter % MEMORY_CAPACITY
        self.memory[index, :] = transition
        self.memory_counter += 1

    def learn(self):
        # target parameter update
        if self.learn_step_counter % TARGET_REPLACE_ITER == 0:
            self.target_net.load_state_dict(self.eval_net.state_dict())
        self.learn_step_counter += 1

        # sample batch transitions
        sample_index = np.random.choice(MEMORY_CAPACITY, BATCH_SIZE)
        b_memory = self.memory[sample_index, :]
        b_s = torch.FloatTensor(b_memory[:, :N_STATES])
        b_a = torch.LongTensor(b_memory[:, N_STATES:N_STATES + 1].astype(int))
        b_r = torch.FloatTensor(b_memory[:, N_STATES + 1:N_STATES + 2])
        b_s_ = torch.FloatTensor(b_memory[:, -N_STATES:])

        # q_eval w.r.t the action in experience
        q_eval = self.eval_net(b_s).gather(1, b_a)  # shape (batch, 1)
        q_next = self.target_net(b_s_).detach()  # detach from graph, don't backpropagate
        q_target = b_r + GAMMA * q_next.max(1)[0].view(BATCH_SIZE, 1)  # shape (batch, 1)
        loss = self.loss_func(q_eval, q_target)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()


dqn = DQN()
rm = readmessage("C://Users//ellsom//PycharmProjects//test//data//A//A-n32-k5.vrp")
rm.rdmessage()
pb = np.zeros((10, 31)).astype(int)
bestpath = list(range(1, 32))
fb = value_function(rm.distmat, bestpath, rm.capacity, rm.things)
bestpath, fb = Init(fb, rm.distmat, rm.capacity, rm.things, 32, pb, bestpath)
s = [fb]
print(s)
Watch = []
for i_episode in range(1000):
    while True:
        a = dqn.choose_action(s)
        # take action
        bestpath = achieve(a, bestpath, rm)
        s_ = [value_function(rm.distmat, list(bestpath), rm.capacity, rm.things)]
        Watch.append(s_)
        if s_[0] < s[0]:
            r = 1
            done = 1
            s = s_
        elif s_[0] == s[0]:
            r = 0
            done = 1
        else:
            r = -1
            done = 0

        # modify the reward
        dqn.store_transition(s, a, r, s_)

        if dqn.memory_counter > MEMORY_CAPACITY:
            dqn.learn()

        if done:
            break
    print(s)
plt.plot(Watch)
plt.show()