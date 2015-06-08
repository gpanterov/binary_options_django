import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm


def find_nodes_number(node_number, level):
	if level < 0:
		return 0
	if node_number > level:
		return 0
	elif node_number == 0 and level == 0:
		return 1
	else:
		res = find_nodes_number(node_number, level-1) + find_nodes_number(node_number+1, level-1) + \
											find_nodes_number(node_number-1, level-1)
		return res
fname = "option_probabilities.csv"
df = pd.read_csv(fname, names = ['t', 'i', 'stayprob', 'p'])
df = df[(df['i'] ==7) &( df['stayprob']==0.5)]
y = df['p'].values
y = np.log(y + 1e-5)
x1 = np.sqrt(df['t'].values)
x2 = np.log(df['i'].values)
x3 = df['stayprob'].values
X = np.column_stack((x1, ))



X = sm.add_constant(X)
model = sm.OLS(y, X)
res = model.fit()
#print res.summary()


yhat = res.fittedvalues
#for level in range(3,16):
#	result = [level]
#	for nodes_number in range(level+1):
#		result.append(find_nodes_number(nodes_number, level))
#	
#	print result



f = open(fname, 'r')

content1 = {}
content2 = {}
content3 = {}


p = 0.8
i = 2
for line in f:
	data = line.strip().split(',')
	if int(data[1].strip()) == i:
		if float(data[2].strip()) == p:
			content1[int(data[0].strip())] = float(data[3])
		
	elif int(data[1].strip()) == i:
		if float(data[2].strip()) == p:
			content2[int(data[0].strip())] = float(data[3])

	elif int(data[1].strip())== i:
		if float(data[2].strip()) == p:
			content3[int(data[0].strip())] = float(data[3])

	
	else:
		pass


x = range(i+1,54)
y = [content1[j] for j in x]
y = np.array(y)
x = np.array(x)
x = x - i
dy = y[1:] - y[:-1]
#y = np.sqrt(y)

X = np.column_stack((np.sqrt(x),))

#X = sm.add_constant(X)
model = sm.OLS(y, X)
res = model.fit()
yhat = res.fittedvalues
print res.summary()
#z = [content2[i] for i in x]
#l = [content3[i] for i in x]

#d1 = np.array(z) - np.array(y)
#d2 = np.array(l) - np.array(y)






plt.plot(x,y, 'r')
plt.plot(x,yhat, 'b')
#plt.plot(x,l, 'g')
plt.show()



	
