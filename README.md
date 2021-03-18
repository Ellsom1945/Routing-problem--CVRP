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

### 第一阶段的项目效果可参考[表格](https://github.com/Ellsom1945/Routing-problem--CVRP/blob/main/10.08%E6%95%B0%E6%8D%AE%E6%AF%94%E8%BE%83_2.xlsx)

# 项目第二阶段

## 项目第二阶段采取针对不同的算法进行优化，并加入一些其他种类的算法作为尝试

### 采取的算法主要有：

### [改进粒子群]()





  