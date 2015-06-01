import numpy as np
import random
import statsmodels.api as sm
import matplotlib.pyplot as plt
import time

# Params

Nsim = 50000
fname = "option_probabilities.csv"

def simulate(Nstep, stayprob):
	uprob = (1. - stayprob) / 2
	res = 0
	for i in range(Nstep):
		z = random.random()
		if z <= uprob:
			res -= 1
		elif z > uprob and z <= (uprob + stayprob):
			pass
		else:
			res += 1
	return res



 
def sim2(Nsim, Nstep, stayprob, i):
	res = []
	for j in range(Nsim):
		res.append(simulate(Nstep, stayprob))		
	res = np.array(res)
	return 1. * len(np.where(res > i)[0]) / len(res)


for Nstep in range(48, 100):
	for i in range(1, 21):
		if Nstep > i:
			t = time.time()

			for s in range(1, 99):	
				stayprob = float(s) / 100.
				res = sim2(Nsim, Nstep, stayprob, i)
				line_to_append = "%s, %s, %s, %s\n" %(Nstep, i, stayprob, res)
				with open(fname, 'a') as f:
					f.write(line_to_append)

			print Nstep, i, time.time() - t
			
