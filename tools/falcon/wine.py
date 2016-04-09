import urllib
from numpy import genfromtxt
from os import remove
import halcon
from time import time
from sys import exit
from sys import argv
import cPickle as pickle
import os
import shutil

if len(argv)>1:
	query_object_index = int(argv[1])
	number_of_results = int(argv[2])
	output_filename = str(argv[3])
else:
	query_object_index = 1
	number_of_results = 10
	output_filename = 'output'

output_directory = os.getcwd() + os.sep + "results"
if not os.path.exists(output_directory):
	os.makedirs(output_directory)

print '''
This example uses the wine dataset from

Machine Learning Repository
Center for Machine Learning and Intelligent Systems
http://archive.ics.uci.edu/ml/datasets/Wine
'''

url = 'http://archive.ics.uci.edu/ml/machine-learning-databases/wine/wine.data'
filename = 'data.csv'
urllib.urlretrieve( url, filename )
data = genfromtxt( filename, delimiter=',' )

print "I will use the first three feature vectors as my query wine set"
query_wines = []
query_wines.append(['wine' + str(query_object_index), 1, data[query_object_index]])

print "\nAnd I will use the rest of the feature vectors to find the most similar images"
dataset = []
counter = 0
for datum in data:
	dataset.append([ 'wine' + str(counter), 1, datum ])
	counter = counter + 1

t = time()
[iids, scores] = halcon.search.query( query_wines, dataset, metric='cityblock', normalization='standard' )
t = time() - t
print "Elapsed time: " + str(t) + " seconds\n"

#icaoberg: i will only display the top ten results
if number_of_results > len(iids):
	number_of_results = len(iids)

iids = iids[0:number_of_results]
scores = scores[0:number_of_results]

workspace = {}
workspace['iids'] = iids
workspace['scores'] = scores
workspace['query'] = query_wines
workspace['dataset'] = dataset
pickle.dump( workspace, open( output_directory + os.sep + "workspace.pkl", "w" ) )
cmd = 'cp ' + filename + ' ' + output_directory
os.system(cmd)
shutil.make_archive( output_filename, "zip", output_directory )
cmd = 'mv ' + output_filename + '.zip ' + output_filename
os.system(cmd)

print "The query object is " + str(query_wines[0][0]) + "\n"
#icaoberg: just in case people do not have the tabulate package
try:
	from tabulate import tabulate
	rank = 0
	table = []

	for index in range(len(iids)):
		table.append([str(rank), str(iids[index]), str(scores[index])])
		rank = rank + 1

	print tabulate(table, tablefmt="fancy_grid", headers=["Ranking","Identifier", "Score"])
except:
	print "rank\tiid\t\tscore"

	rank = 0
	for iid, score in zip(iids,scores):
		print str(rank) + "\t" + str(iid) + "\t\t" + str(score)
		rank = rank + 1

remove(filename)
