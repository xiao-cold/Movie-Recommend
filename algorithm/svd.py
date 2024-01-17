# 导入所需的模块和库
import os
import time

import pandas as pd
from surprise import SVD, Reader, Dataset
from surprise.dump import dump, load
from surprise.model_selection import cross_validate, train_test_split
from mydb import Movie, Ratings

# 训练好的模型
MODEL_PATH = './algorithm/model/svd_model_1p5M.joblib'


class RecModel:
    def __init__(self, db, model_path=MODEL_PATH):
        self.db = db
        self.data = None
        self.trainset = None
        self.testset = None
        self.model = None
        self.model_path = model_path
        self.movie_title_dict = None
        # 直接加载模型
        if os.path.exists(self.model_path):
            self.preprocess()
            self.model = load(self.model_path)[1]
        # 模型不存在，则先进行数据预处理，再训练模型
        else:
            self.preprocess(full_process=True)
            self.train()
            self.evaluate()

    def preprocess(self, full_process=False):
        """数据预处理"""
        if full_process:
            # 使用 SQLAlchemy 从数据库获取评分数据
            ratings_query = self.db.session.query(Ratings).with_entities(Ratings.userId, Ratings.movieId,
                                                                         Ratings.rating, Ratings.timestamp)
            self.data = pd.read_sql(ratings_query.statement, self.db.engine)

            # # 使用 SQLAlchemy 从数据库获取电影信息
            # movies_query = self.db.session.query(Movie).with_entities(Movie.movieId, Movie.title)
            # md_links_cn_new3_title = pd.read_sql(movies_query.statement, self.db.engine)

            # # 选取包含title的电影
            # data = data[data['movieId'].isin(md_links_cn_new3_title['movieId'])]
            # # 截取前10K个用户的评分数据
            # data = data[data['userId'] <= 10000]
            print("数据集的大小为：{}".format(self.data.shape))
            # 统计数据集中的用户数量和电影数量
            n_users = self.data['userId'].unique().shape[0]
            n_movies = self.data['movieId'].unique().shape[0]
            print('用户数量 ： ' + str(n_users) + ' | 物品数量： ' + str(n_movies))
            # # 将评分数据保存到数据库中
            # data.to_sql('ratings_10k', self.db.engine, if_exists='replace', index=False)
            # 使用 SQLAlchemy 从数据库获取电影标题并转换为以电影ID为索引的字典
            movies_query = self.db.session.query(Movie).with_entities(Movie.movieId, Movie.title)
            movie_title_df = pd.read_sql(movies_query.statement, self.db.engine)
            self.movie_title_dict = dict(zip(movie_title_df['movieId'], movie_title_df['title']))

        else:
            # 使用 SQLAlchemy 从数据库获取电影标题并转换为以电影ID为索引的字典
            movies_query = self.db.session.query(Movie).with_entities(Movie.movieId, Movie.title)
            movie_title_df = pd.read_sql(movies_query.statement, self.db.engine)
            self.movie_title_dict = dict(zip(movie_title_df['movieId'], movie_title_df['title']))

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
        dump(file_name=self.model_path, algo=model, verbose=1)
        self.testset = testset
        self.model = model

    def retrain_model(self, new_ratings):
        # 将新评分添加到数据集
        new_data = pd.DataFrame(new_ratings, columns=['user', 'item', 'rating'])
        self.data = pd.concat([self.data, new_data])

        # 重新训练模型
        reader = Reader(rating_scale=(0.5, 5))
        data = Dataset.load_from_df(self.data[['user', 'item', 'rating']], reader)
        trainset = data.build_full_trainset()
        self.model = SVD()
        self.model.fit(trainset)

        # 保存新的训练时间戳
        self.save_training_timestamp()

    def save_training_timestamp(self):
        timestamp = time.time()
        with open('model_last_trained.txt', 'w') as f:
            f.write(str(timestamp))

    def get_last_training_timestamp(self):
        if os.path.exists('model_last_trained.txt'):
            with open('model_last_trained.txt', 'r') as f:
                return float(f.read())
        return None

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
        """
        # 在构建推荐列表时包含 movieId, title 和预测评分
        recommendations = []
        for movie_id in self.movie_title_dict.keys():  # 遍历所有电影
            prediction = self.model.predict(user_id, movie_id)
            movie_title = self.movie_title_dict[movie_id]
            recommendations.append((movie_id, movie_title, round(prediction.est, 2)))

        # 根据评分排序并返回 top N
        recommendations.sort(key=lambda x: x[2], reverse=True)
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
