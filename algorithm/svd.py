# 导入所需的模块和库
import os
import pandas as pd
from pandas._libs.parsers import QUOTE_NONNUMERIC
from surprise import SVD, Reader, Dataset
from surprise.dump import dump, load
from surprise.model_selection import cross_validate, train_test_split

# 电影信息数据集
ALL_MOVIES_PATH = './data/dataset/all_movies.csv'
# 评分数据集
RATINGS_PATH = './data/dataset/ratings.csv'
# 训练好的模型
MODLE_PATH = './algorithm/model/svd_model_1p5M.joblib'


class RecModel:
    def __init__(self):
        self.data = None
        self.trainset = None
        self.testset = None
        self.model = None
        self.movie_dict = None
        wd = os.getcwd()
        print(wd)
        if os.path.exists(MODLE_PATH):
            self.preprocess()
            self.model = load(MODLE_PATH)[1]
        else:
            self.preprocess(full_process=True)
            self.train()
            self.evaluate()

    def preprocess(self, full_process=False):
        """数据预处理"""
        if full_process:
            # 读取 ml-25m 数据集中的 ratings.csv 的['userId', 'movieId', 'rating']列
            data = pd.read_csv(RATINGS_PATH, usecols=['userId', 'movieId', 'rating'])
            # 已获取title的电影
            md_links_cn_new3_title = pd.read_csv(ALL_MOVIES_PATH, quoting=QUOTE_NONNUMERIC)

            # 选取包含title的电影
            data = data[data['movieId'].isin(md_links_cn_new3_title['movieId'])]
            # 截取前10K个用户的评分数据
            data = data[data['userId'] <= 10000]
            print("数据集的大小为：{}".format(data.shape))
            # 统计数据集中的用户数量和电影数量
            n_users = data['userId'].unique().shape[0]
            n_movies = data['movieId'].unique().shape[0]
            print('用户数量 ： ' + str(n_users) + ' | 物品数量： ' + str(n_movies))
            # 将前10K个用户的共1.49M条评分数据保存到文件中
            data.to_csv(RATINGS_PATH, index=False)
            self.data = data
            self.movie_dict = md_links_cn_new3_title.set_index('movieId')['title'].to_dict()
        else:
            # self.data = pd.read_csv(RATINGS_PATH, usecols=['userId', 'movieId', 'rating'])
            self.movie_dict = pd.read_csv(ALL_MOVIES_PATH).set_index('movieId')['title'].to_dict()

    def train(self):
        """训练 SVD 模型"""
        # 使用 surprise 库中的 Reader 类来读取数据，指定 rating_scale 为 (0.5, 5) 之间的评分
        reader = Reader(rating_scale=(0.5, 5))
        data = Dataset.load_from_df(self.data[['userId', 'movieId', 'rating']], reader)
        # 使用 surprise 库中的 train_test_split 函数来分割数据集
        trainset, testset = train_test_split(data, test_size=0.2)
        # 使用 surprise 库中的 SVD 类来构建和训练 SVD 模型，设置合适的参数
        model = SVD(n_factors=100, lr_all=0.005, reg_all=0.02)
        # 使用 surprise 库中的 cross_validate 函数来评估 SVD 模型的性能，选择合适的评价指标
        print('开始训练模型...')
        cross_validate(model, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)

        # 使用 surprise 库中的 dump 函数来保存 SVD 模型，以便之后的使用
        print('模型训练完成！')
        dump(file_name=MODLE_PATH, algo=model, verbose=1)
        self.testset = testset
        self.model = model

    def get_top_n_recommendations(self, user_id, n=10):
        """
        使用训练的 SVD 模型给出前 n 部电影推荐。

        参数:
        user_id (int): 用户的ID。
        n (int, 可选): 要推荐的电影数量。默认为10。

        返回:
        list: 一个包含前n部推荐电影的列表。每个元素是一个元组，包含电影的ID和预测的评分。

        使用方法:
        1. 创建一个RecModel对象。
        2. 调用此方法，传入用户ID和要推荐的电影数量。

        示例:
        >>> model = RecModel()
        >>> recommendations = model.get_top_n_recommendations(1, 5)
        >>> print(recommendations)
        [(318, 4.5), (296, 4.4), (356, 4.3), (2571, 4.2), (260, 4.1)]
        """
        recommendations = []
        movieid_list = list(self.movie_dict.keys())

        for movie_id in movieid_list:  # 遍历所有电影
            prediction = self.model.predict(user_id, movie_id)
            recommendations.append((movie_id, round(prediction.est, 2)))

        # 根据评分排序
        recommendations.sort(key=lambda x: x[1], reverse=True)

        top_n_recommendations = recommendations[:n]
        return top_n_recommendations

    def evaluate(self):
        # 使用 SVD 模型来对 testset 进行预测
        predictions = self.model.test(self.testset)
        # 使用 surprise 库中的 accuracy 模块来计算预测的准确性，如 RMSE 和 MAE
        from surprise import accuracy
        rmse = accuracy.rmse(predictions)
        mae = accuracy.mae(predictions)
        print('RMSE: {:.2f}, MAE: {:.2f}'.format(rmse, mae))


if __name__ == '__main__':
    SVD = RecModel()
    # rec = SVD.get_top_n_recommendations(1)
    # print(SVD.movie_dict)
