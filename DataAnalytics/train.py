import random 
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from pylab import mpl
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.ensemble._forest import RandomForestRegressor
mpl.rcParams['font.sans-serif'] = ['STZhongsong']
mpl.rcParams['axes.unicode_minus'] = False
df = pd.read_csv("./beautifuldata.csv", encoding="gbk")


h=['经度','纬度','成交价','房屋户型','所在楼层','建筑面积','户型结构','房屋朝向','建成年代','装修情况','梯户比例','产权年限','配备电梯','房屋用途','楼层数']
df=df[h]
for col in df.columns:
	if str(df[col].dtype) == 'object':
		df_group = df.groupby(col)
		lt = list(df_group.groups.keys())
		tm=random.randint(1,99)
		for k in lt:
			df.loc[df[col]==k,col]=lt.index(k) + tm

X = df.drop(['成交价'],axis=1) 
y = df['成交价']
xtrain, xtest, ytrain, ytest = train_test_split(X, y, test_size=0.2, random_state=0)


def train(began,end,step=1):
	scores = []
	for i in range(began,end,step):
		rf = RandomForestRegressor(n_estimators=i,random_state=10)
		score = cross_val_score(rf,xtrain,ytrain,cv=10).mean()
		scores.append(score)
		print('决策树数量为：%d,score为：%s'%(i,score))
	return scores
ss=train(1,102,10)
temp = ((ss.index(max(ss))) * 10)+1
print('=========================')
last = train(temp - 5, temp + 5)
print('决策树数量为%d时，score值最大' %(temp-5+last.index(max(last))))
model = RandomForestRegressor(n_estimators=temp-5+last.index(max(last)),random_state=10)
model.fit(xtrain, ytrain)
score = model.score(xtest, ytest)
result = model.predict(xtest)
plt.figure(figsize=(16,9))
plt.plot(np.arange(len(result)), ytest, "go-", label="训练集")
plt.plot(np.arange(len(result)), result, "ro-", label="测试集")
plt.title(f"method:---score:{score}")
plt.legend(loc="best")
plt.show()
