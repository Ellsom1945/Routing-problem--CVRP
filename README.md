# Routing-problem--CVRP

---

# 项目准备阶段

## 准备相关论文，设计准备数据集，最终决定采用[CVRPLIB](http://vrp.atd-lab.inf.puc-rio.br/index.php/en/)上的标准数据集作为实验用数据。



# 项目第一阶段

## 参考论文用各种元启发式算法求解CVRP问题

### 采取的算法主要有：

### [贪心](https://github.com/Ellsom1945/Routing-problem--CVRP/blob/main/Greedy.py)、[遗传](https://github.com/Ellsom1945/route-project/blob/master/%E9%81%97%E4%BC%A0%E7%AE%97%E6%B3%95/%E4%BB%A3%E7%A0%81%E5%AE%9E%E7%8E%B01)、[蚁群](https://github.com/Ellsom1945/route-project/blob/master/%E8%9A%81%E7%BE%A4%E7%AE%97%E6%B3%95/%E4%BB%A3%E7%A0%81%E5%AE%9E%E7%8E%B02)、[禁忌](https://github.com/Ellsom1945/Routing-problem--CVRP/blob/main/H_Hy_Men/TABU.py)、[粒子群](https://github.com/Ellsom1945/route-project/blob/master/%E7%B2%92%E5%AD%90%E7%BE%A4/%E4%BB%A3%E7%A0%81%E5%AE%9E%E7%8E%B02)

### 在实验前期出现的问题主要有：

* 遗传和粒子群算法由于参数过多，时间复杂度高，且收敛不稳定

* 贪心策略设计过于简单，效果很一般，但好在时间复杂度低

* 禁忌在前期的表现最优，其原因在于该算法的设计原理是找初始解的局部最优解，搜索域相较于整个解空间要小很多，其次选用贪心的结果作为初始解，部分问题的最优解特征与贪心的结果路径特征较为一致，导致在项目前期贪心+禁忌的组合效果一直最好

### 第一阶段的项目效果可参考[表格](https://github.com/Ellsom1945/Routing-problem--CVRP/tree/main/%E6%95%B0%E6%8D%AE%E6%AF%94%E8%BE%83)

# 项目第二阶段

## 项目第二阶段采取针对不同的算法进行优化，并加入一些其他种类的算法作为尝试

### 采取的算法主要有：

### [改进粒子群](https://github.com/Ellsom1945/Routing-problem--CVRP/blob/main/pso.py)、[遗传-退火](https://github.com/Ellsom1945/Routing-problem--CVRP/blob/main/H_Hy_Men/GASA.py)、[快速贪心](https://github.com/Ellsom1945/Routing-problem--CVRP/blob/main/H_Hy_Men/IMGR.py)、[改进蚁群](https://github.com/Ellsom1945/Routing-problem--CVRP/blob/main/%E8%9A%81%E7%BE%A41.py)、[粒子群-禁忌](https://github.com/Ellsom1945/Routing-problem--CVRP/blob/main/pso.py)、[Google-ortools](https://github.com/Ellsom1945/Routing-problem--CVRP/blob/main/ort.py)

###  这阶段的各个算法的问题主要有：

* 改进粒子群在时间复杂度和效果和上次比都有很大提升，但当数量级达到10<sup>3</sup>的时候，时间还是很不理想

* 遗传-退火

* 快速贪心主要采用了[KD-Tree](https://zh.wikipedia.org/wiki/K-d%E6%A0%91)+最小堆的，主要算法思想就是利用KD-Tree来聚类，再利用最小堆，以边为操作对象，拼出若干条路径，**这个算法的思路是我觉得现阶段最合理的，先聚类再分别解决每条路径**，首先时间复杂度很低，用于解决较大数量级问题是个不错的选择，其次，这个算法的思想也很合理，比较符合现代物流分层的设计方式，可惜实现的时候技术欠佳，未能达到该算法的本来效果

* 改进蚁群主要是加入了负反馈机制，效果比原先的蚁群算法是要好上不少，但这类元启发算法仍存在参数多时间复杂度高这一问题

* 粒子群-禁忌就是在改进粒子群的基础上加一个局部搜索得到

* ortools 是利用Google的开源框架[ortools](https://developers.google.cn/optimization/)实现的，ortools是一套约束问题、线性规划、图形算法工具包，这套算法其实已经足够优秀，**这套工具包已经足够优秀，在规模处于10<sup>3</sup>以内的问题基本都能输出最优解，而且时间足够优秀**，但由于算法都是利用的内置的足够优秀的模型求解该问题，而且由于底层互相引用过于复杂，导致我花了很长时间都
  未能成功了解该模型的求解流程，且我们的项目目标是构建超启发式算法，无奈只能放弃这个完美答案，**但如果要真正求解该类问题，这个工具包一定是我首选的方法**

###  第二阶段的项目效果可参考[表格](https://github.com/Ellsom1945/Routing-problem--CVRP/tree/main/%E6%95%B0%E6%8D%AE%E6%AF%94%E8%BE%83)

# 项目第三阶段


## 着手搭建超启发式算法








