import csv
import matplotlib.pyplot as plt
import numpy as np

qualified_qbs = set()
five_star_qbs = set()
four_star_qbs = set()
three_star_qbs = set()
two_star_qbs = set()

D1_SCHOOLS = 335
YEARS = 2013 - 2000
QBS_PER_YEAR = .8
non_nfl = []
nfl = []

def conditional_nfl_prob(qb_set, type_string):
	n = len(qb_set)
	
	n_in_nfl = len(qb_set&qualified_qbs)
	non_nfl.append(n - n_in_nfl)
	nfl.append(n_in_nfl)
	odds = 0 if n_in_nfl == 0 else n_in_nfl/n
	print("number of " + type_string + "s:\t" + str(n))
	print("number of " + type_string + "s successful in nfl:\t" + str(n_in_nfl))
	print("P(nfl success | " + type_string +") = " + str(odds))
#get set of nfl qbs from 2000 on with >=1000 attempts and >=70 passer rating
with open('./qualified_qbs.csv') as csvfile:
	reader = csv.reader(csvfile)
	for qb in reader:
		qualified_qbs.add(qb[0])

with open('./cfb_recruits.csv') as csvfile:
	reader = csv.reader(csvfile)
	for qb in reader:
		star = qb[2]
		if star == '5':
			five_star_qbs.add(qb[0])
		if star == '4':
			four_star_qbs.add(qb[0])
		if star == '3':
			three_star_qbs.add(qb[0])
		if star == '2':
			two_star_qbs.add(qb[0])

for s in five_star_qbs & qualified_qbs:
	print(s)
print("number of successful nfl qbs 2002-:\t" + str(len(qualified_qbs)))

total_college_qbs = D1_SCHOOLS * QBS_PER_YEAR * YEARS - len(five_star_qbs) - len(four_star_qbs) - len(three_star_qbs)
non_nfl_college = total_college_qbs - len(qualified_qbs - five_star_qbs - four_star_qbs - three_star_qbs)
print(1- non_nfl_college/total_college_qbs)
nfl.append(len(qualified_qbs))
non_nfl.append(non_nfl_college)

#conditional_nfl_prob(two_star_qbs, "two star qb")
conditional_nfl_prob(three_star_qbs, "three star qb")
conditional_nfl_prob(four_star_qbs, "four star qb")
conditional_nfl_prob(five_star_qbs, "five star qb")



N = 4

ind = np.arange(2,N+2)    # the x locations for the groups
width = 0.5       # the width of the bars: can also be len(x) sequence

fig = plt.figure()
ax  = fig.add_subplot(111)
# the first argument is the margin of the x-axis, the second of the y-axis
ax.margins(0.04, 0)  

p1 = ax.bar(ind, nfl, width, color = "red")
p2 = ax.bar(ind, non_nfl, width, bottom = nfl)


plt.ylabel('Players')
plt.title('NFL QB Success By Star Rating (Recruited 2000-2013)')
plt.xticks(ind+width/2, ('Non Recruit College', '3 Star QBs', '4 Star QBs', '5 Star QBs'))
#plt.xticks(ind+width/2, ('3 Star QBs', '4 Star QBs', '5 Star QBs'))
plt.yticks(np.arange(0, 4000, 500))
plt.legend((p1[0], p2[0]), ('Success in NFL', 'No Success in NFL'))

plt.show()





