import pandas as pd
import numpy as np

df = pd.read_csv("./data.csv",encoding="gbk")
df = df.sample(frac=1).reset_index(drop=True)
df = df.drop(['供暖方式', '套内面积','房屋年限','链家编号','房权所属','建筑类型'], axis=1)
df = df[~df['房屋户型'].isin(['车位'])]
df.replace('暂无数据', np.NaN,inplace=True)
df.replace('未知', np.NaN,inplace=True)
df['成交单价'] = df['成交单价'] / 10000
df['区域']=df['区域'].str.split('二手房', expand=True)[0]
df['子区域']=df['子区域'].str.split('二手房', expand=True)[0]
df['建筑面积']=df['建筑面积'].str.split('㎡',expand=True)[0]
df=df.join(df['所在楼层'].str.split("\(共",expand=True)[1].str.replace('层\)',''))
df.rename(columns={1: '楼层数'}, inplace=True)
df['房屋朝向']=df['房屋朝向'].str.replace(' ','')
df['所在楼层'] = df['所在楼层'].str.split("\(共", expand=True)[0]
df['挂牌时间'] = pd.to_datetime(df['挂牌时间'])
df['成交时间'] = pd.to_datetime(df['成交时间'])
df['浏览'].fillna(df['浏览'].median(),inplace=True)
df['产权年限'].fillna('70年', inplace=True)
df[['楼层数','关注', '浏览', '建筑面积', '建成年代']]\
    = df[['楼层数','关注', '浏览', '建筑面积', '建成年代']].apply(pd.to_numeric)
d = df['户型结构'].isna()
d=d[d==True] 
na=df.groupby('楼盘名称')['户型结构'].agg(lambda x: x.mode())
for index in d.index:
	t = na[df.loc[index, '楼盘名称']]
	if type(t) == type(np.array(1)):
		if len(t) > 1:
			t=t[0]
		else:
			t='平层'
	df.loc[index, '户型结构'] = t
d = df['建成年代'].isna()
d=d[d==True] 
na=df.groupby('楼盘名称')['建成年代'].agg(lambda x: x.mode())
for index in d.index:
	t = na[df.loc[index, '楼盘名称']]
	if type(t) == type(np.array(1)):
		if len(t) > 1:
			t=t[0]
		else:
			t='2010'
	df.loc[index,'建成年代']=t
d = df['配备电梯'].isna()
d=d[d==True]
for index in d.index:
	if df.loc[index,'楼层数'] > 10:
		t='有'
	else:
		t ='无'
	df.loc[index,'配备电梯']=t
df.reset_index(drop=True, inplace=True)
print(df.info())
print(df.isnull().sum())
df.to_csv('./beautifuldata.csv',encoding='gbk',index=None)
