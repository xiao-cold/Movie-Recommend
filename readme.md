# 电影推荐系统

## *0x00 简介*

    本项目是一个基于用户/物品的协同过滤，SVD隐语义模型的推荐系统。
    使用的数据集是MovieLens 25M Dataset
    项目使用的技术栈是：Python + Flask + MySQL

## *0x01 热门推荐*

    采用了 IMDB 网站的评分权重计算公式： $$wr = \frac{v}{v+m} * R + \frac{m}{v+m} * C$$
    其中：
    - v: 电影的评分人数
    - m: 最小评分人数
    - R: 电影的平均评分
    - C: 所有电影的平均评分
    
    本项目中，m 取值为电影评分人数的 90% 分位数，C 取值为所有电影的平均评分。

## *0x02 协同过滤*

    本项目中，协同过滤分为两种：
    - 基于用户的协同过滤
    - 基于物品的协同过滤
    
    两种协同过滤的计算方式都是一样的，只是计算的对象不同。
    本项目中，计算的对象是用户对电影的评分，计算方式是余弦相似度。

## *0x03 SVD 隐语义模型*

    本项目中，使用的是 SVD++ 隐语义模型，计算方式是：
    $$\hat{r}_{ui} = \mu + b_u + b_i + q_i^T(p_u + |I_u|^{-\frac{1}{2}}\sum_{j \in I_u}y_j)$$
    其中：
    - $\mu$ 是所有电影的平均评分
    - $b_u$ 是用户 u 的评分偏差
    - $b_i$ 是电影 i 的评分偏差
    - $q_i$ 是电影 i 的隐向量
    - $p_u$ 是用户 u 的隐向量
    - $y_j$ 是电影 j 的隐向量
    - $I_u$ 是用户 u 评分过的电影集合

