#You live in a row house, one of 36 like it on your side of the block. A disaster strikes, and the city has to be evacuated. Two years later, with everyone gone for good, the worst-maintained row house on your side of the block, battered by the elements for too long, collapses. Within two years, any row house neighboring the collapsed one also collapses — as does the second-worst-maintained home on the block, if it wasn’t next to the worst-maintained one.
#This contagion continues: Every two years, any row house next to one that’s already collapsed also becomes rubble, and houses continue to collapse in order of how badly maintained they are — the third-worst-maintained house falls in the third round, the fourth-worst-maintained in the fourth round, and so on, assuming they were still standing at the start of that round. (The maintenance rankings are set at the moment the city is evacuated and don’t change from round to round.) Assuming a random distribution of poorly maintained homes, what’s the longest your home can remain standing? What’s the fewest number of years it will take for all 36 row houses to collapse?
#Extra credit: How does either answer change for N rowhouses?
import math as math
import numpy as np
import random as rand
N = 36 #number of houses
maint = [i+1 for i in range(N)] #creates a list of houses in order of quality of maintenance (1 is worst maintined)
print("maint = " + str(maint))
print(len(maint)) #debug
for i in range(0, N): #randomizes the list
	rando_index = rand.randint(0, N-1)
	rando_value = maint[rando_index]
	maint[rando_index] = maint[i]
	maint[i] = rando_value
print("maint = " + str(maint)) #debug
# print(maint[N-1])
# print(len(maint))
# print(max(maint))
year = 0 #the year
maint_prev = maint.copy()
my_house_index = rand.randint(0, N-1) #picks a random number as my house
print("my house is the %s worst maintained house" %maint[my_house_index])
while maint[my_house_index] > 0: #simulates demolition of houses
	for i in range(0, N):
		if i == 0:
			if maint_prev[i+1] == 0:
				maint[i] = 0
			elif maint[i] > 0:
				maint[i] = maint[i] -1
		elif i > 0 and i < N - 1:
			if maint_prev[i-1] == 0:
				maint[i] = 0
			elif maint_prev[i+1] == 0:
				maint[i] = 0
			elif maint[i] > 0:
				maint[i] = maint[i] -1
		else:
			if maint_prev[i-1] == 0:
				maint[i] = 0
			elif maint[i] > 0:
				maint[i] = maint[i] -1
	year = year + 2
	# print("two years ago the block looked like " +str(maint_prev))
	maint_prev = maint.copy()
	print("the year is %s and the block looks like %s" %(year, maint))
print("the block now looks like: " + str(maint))
print(maint[my_house_index])
print("my house lasted %s years" %year)