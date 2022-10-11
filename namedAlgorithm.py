# -*- codeing = utf-8 -*-
# @Time : 2022/10/8 21:34
# @Author : 朱镕钊
# @File ： namedAlgorithm.py
# @Software : PyCharm
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier

from loadData import *


# 划分特征和标签，是否有来作为标签，其余为特征
def get_label_feature(data):
    df = data.copy()
    label = df["Attended"]
    feature = df.drop("Attended", axis=1)
    return feature, label

# 返回最好的算法
def ACC(train_data, algorithms):
    # 划分特征
    X_train, y_train = get_label_feature(train_data)
    fit_score = 0
    best_algorithm = None
    for algorithm in algorithms:
        algorithm.fit(X_train, y_train)
        y_predict = algorithm.predict(X_train)
        accuracy = accuracy_score(y_train, y_predict)   # 每个模型的准确率
        print(str(algorithm) + "\t" + "acc = %.4f" % accuracy)
        if fit_score < accuracy:
            fit_score = accuracy
            best_algorithm = algorithm
    # 返回准确率最高的算法
    return best_algorithm


def compute_score(test_data, algorithm):
    num_of_Named = 0  # 点名的人数
    num_of_hit = 0  # 命中的人数
    i = 0
    for one_class_attend in test_data:
        i = i + 1
        # 划分特征和标签
        test_data_feature, test_data_label = get_label_feature(one_class_attend)
        # 预测出的标签
        y_predict = algorithm.predict(test_data_feature)
        # 每次点名的人数等于没来的人数，即总人数-预测有来的人数
        num_of_Named += num_students - y_predict.sum()
        # print("num of named = %d" % num_of_Named)
        # 获取没来人的学号
        # argsort 表示返回下标
        named_ids = y_predict.argsort()[:num_students - y_predict.sum()]
        # 如果预测的人刚好没来，则为命中
        num_of_hit += (test_data_label[named_ids] == y_predict[named_ids]).sum()
        # print("num of hit = %d" % num_of_hit)
        # 输出
        if i % 20 == 10:
            print("named_ids of course_" + str(i // 20) + " :")
            print(named_ids)
    # 计算准确率
    accuracy_rate = num_of_hit / num_of_Named
    return accuracy_rate


# 逻辑回归
LR = LogisticRegression(random_state=0, max_iter=5000)
# KNN
KNN = KNeighborsClassifier(n_neighbors=5)
# 高斯贝叶斯
GNB = GaussianNB()
# 随机森林
RFC = RandomForestClassifier()
# 所有要尝试的算法
algorithms = [LR, KNN, GNB, RFC]
# 找到正确率最高的算法
algorithm = ACC(total_data, algorithms)
# 输出E
print("E = %.4f" % compute_score(datalist, algorithm))
