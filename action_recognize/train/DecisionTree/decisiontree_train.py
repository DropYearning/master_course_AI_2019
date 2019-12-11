# 作者：马言悦
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import tensorflow as tf
from sklearn import preprocessing  # one-hot-encoding
import matplotlib.pyplot as plt  # plot
from sklearn.model_selection import train_test_split # 划分数据集
from sklearn.tree import DecisionTreeClassifier  # 决策树
from sklearn.externals import joblib  # 导出sklearn模型
from sklearn import metrics # 评估模型
from sklearn.metrics import confusion_matrix # 混淆矩阵

# 绘制混淆矩阵
def plot_Matrix(cm, classes, title=None, cmap=plt.cm.Blues):
    plt.rc('font', family='Times New Roman', size='8')  # 设置字体样式、大小
    # 按行进行归一化
    cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    print("Normalized confusion matrix")
    str_cm = cm.astype(np.str).tolist()
    for row in str_cm:
        print('\t'.join(row))
    # 占比1%以下的单元格，设为0，防止在最后的颜色中体现出来
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            if int(cm[i, j] * 100 + 0.5) == 0:
                cm[i, j] = 0
    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    # ax.figure.colorbar(im, ax=ax) # 侧边的颜色条带
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='Actual',
           xlabel='Predicted')
    # 通过绘制格网，模拟每个单元格的边框
    ax.set_xticks(np.arange(cm.shape[1] + 1) - .5, minor=True)
    ax.set_yticks(np.arange(cm.shape[0] + 1) - .5, minor=True)
    ax.grid(which="minor", color="gray", linestyle='-', linewidth=0.2)
    ax.tick_params(which="minor", bottom=False, left=False)
    # 将x轴上的lables旋转45度
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")
    # 标注百分比信息
    fmt = 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            if int(cm[i, j] * 100 + 0.5) > 0:
                ax.text(j, i, format(int(cm[i, j] * 100 + 0.5), fmt) + '%',
                        ha="center", va="center",
                        color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    plt.savefig('cm.png', dpi=300)
    plt.show()

# 准备数据
df = pd.read_csv('output_normalized_cmu.csv', header=0)
seed = 42
# x为36维特征
x = df.loc[:, :'17_y'].astype(float)
# y为动作种类（标签）
y = df.loc[:,['type_index'] ]
# 将动作类别字段转换为one-hot-encoding
encoder =  preprocessing.LabelBinarizer()
dummy_y = encoder.fit_transform(y)
labels_name = ['Stand', 'Wave', 'Flap', 'Squat', 'Bowling']
# 划分数据集
x_temp,x_test,y_temp,y_test = train_test_split(x, dummy_y, test_size=0.2, random_state=seed) # 第一次划分，划分出20%为测试集：x_test, y_test
x_train, x_validation, y_train, y_validation = train_test_split(x_temp, y_temp, test_size=0.25, random_state=seed) # 第二次划分，划分出60%的训练集和20%的验证集
print('训练集大小:', len(x_train),  '验证集大小:', len(x_validation),  '测试集大小:', len(x_test))
# 初始化决策树模型
tree = DecisionTreeClassifier(random_state=seed)
# 在训练集上训练
tree.fit(x_train, y_train)
# 在验证集上调整模型
print("Evaluation on validation data: accuracy = %0.3f%% \n"  % ( tree.score(x_validation, y_validation) * 100) )
# 在测试集上检验模型
print("Evaluation on test data: accuracy = %0.3f%% \n"  % ( tree.score(x_test, y_test) * 100) )
# 评估模型
y_pred = encoder.inverse_transform(tree.predict(x_test))
y_true = encoder.inverse_transform(y_test)
print(metrics.classification_report(y_true, y_pred, digits=4, target_names=labels_name))
# 混淆矩阵
cm = confusion_matrix(y_true, y_pred)
print(cm)
plot_Matrix(cm, labels_name, "Decision Tree Confusion Matrix")
# 导出sklearn模型
joblib.dump(tree, "decision_tree_model.m")