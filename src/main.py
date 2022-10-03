import sqlite3
import json 
import sys

def partition_by_week():
	with sqlite3.connect('warehouse.db') as con:
		cursor = con.cursor()
		weeks = cursor.execute('select Id, PostId, VoteTypeId, CreationDate, strftime(\'%W\', CreationDate) wnumber from test_table')
		return list(weeks)

def week_count():
	with sqlite3.connect('warehouse.db') as con:
		cursor = con.cursor()
		count = cursor.execute("select count(*) from (select distinct(strftime(\'%W\', CreationDate)) wnumber from test_table)")
		return list(count)

def vote_count_per_week():
	with sqlite3.connect('warehouse.db') as con:
		cursor = con.cursor()
		vote = cursor.execute("select count(CreationDate) as Date from test_table group by strftime(\'%W\', CreationDate)")
		return list(vote)

def average():
	with sqlite3.connect('warehouse.db') as con:
		cursor = con.cursor()
		yearavr = cursor.execute("select tl1.yvotes/tl2.total_weeks from (select count(CreationDate) as yvotes from test_table)tl1, (select count(*) as total_weeks from (select distinct(strftime(\'%W\', CreationDate)) as wnumber from test_table))tl2")
		return list(yearavr)


# Variables section #
weekcount = week_count()
weekcount = [int(i) for i in weekcount[0]]
weeklyvote = zip(*vote_count_per_week())
weeklyvote = list(weeklyvote)
weeklyvote = [int(i) for i in weeklyvote[0]]

comaverage = average()
comaverage = [int(i) for i in comaverage[0]]
comperminus = [0.8*i for i in comaverage]
comperminus = comperminus[0]
comperminus = int(comperminus)
comperplus = [1.2*i for i in comaverage]
comperplus = comperplus[0]
comperplus = int(comperplus)


def non_outliers():
	norm = []
	for i in weeklyvote:
		if comperplus[0] > i > comperminus[0]:
			norm.append(i)
	return list(norm)

def outliers():
	norm = []
	for i in weeklyvote:
		if comperminus[0] > i:
			norm.append(i)
		if comperplus[0] < i:
			norm.append(i)
	return list(norm)


def outliers_date():
	with sqlite3.connect('warehouse.db') as con:
		cursor = con.cursor()
		vote = cursor.execute("select CreationDate, count(CreationDate) as vcount from test_table group by strftime(\'%W\', CreationDate)")
		vote = list(vote)	
	norm = []
	for i,j in vote:
		if comperminus[0] > j:
			norm.append(i)
		if comperplus[0] < j:
			norm.append(i)
	return list(norm)


def total_outliers():
	with sqlite3.connect('warehouse.db') as con:
		cursor = con.cursor()
		w = cursor.execute("select Id, PostId, VoteTypeId, CreationDate, count(CreationDate) as vcount from test_table group by strftime(\'%W\', CreationDate) order by CreationDate")
		#return list(w)
		items = list(w)
		# return list(items)
		number_of_outliers = 0
		for idx, i in enumerate(items):
			votes_this_week = i[-1]
			votes_last_week = 0
			if idx > 0:
				votes_last_week = items[idx-1][-2]
				if votes_this_week >= comperplus or votes_this_week <= comperminus:
					if not votes_last_week >= comperplus or votes_last_week <= comperminus:
						number_of_outliers = number_of_outliers + 1
            # print(votes_this_week)
		return number_of_outliers	
		
def final_solution():
	with sqlite3.connect('warehouse.db') as con:
		cursor = con.cursor()
		w = cursor.execute("select strftime(\'%Y\', CreationDate) as year, strftime(\'%W\', CreationDate) as wnumber, count(CreationDate) as vcount from test_table group by strftime(\'%W\', CreationDate) order by CreationDate")
		#return list(w)
		items = list(w)
		# return list(items)
		ds = []
		for idx, i in enumerate(items):
			votes_this_week = i[-1]
			votes_last_week = 0
			if idx > 0:
				votes_last_week = items[idx-1][-1]
				if votes_this_week >= comperplus or votes_this_week <= comperminus:
					if not votes_last_week >= comperplus or votes_last_week <= comperminus:
						ds.append(i)
            # print(votes_this_week)
		return list(ds)	

		



#print(partition_by_week())
#print(week_count())
#print(vote_count_per_week())
#print(average())

#print(weekcount)
#print(weeklyvote)
#print(comperminus)
#print(comperplus)
#print(comaverage)

#print(non_outliers())
#print(outliers())
#print(outliers_date())

print(total_outliers())
print(final_solution())












# # The following code is purely illustrative
# try:
#     with open(sys.argv[1]) as votes_in:
#          for line in votes_in:
#             print(json.loads(line))
#             break
# except FileNotFoundError:
#     print("Please download the dataset using 'make fetch_data'")
