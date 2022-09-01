#! /usr/bin/env python

'''
Extracts all ancestry tracts for sample of 200 individuals
from .trees file. Outputs as .csv

Assumes 2 source populations and
1 diploid ancestor per source population.

usage: localancestry_alltracts.py /full/path/to/infile.trees
'''

import msprime, pyslim
import numpy as np
import pandas as pd
import sys
import re

def dumpTracts(samples, anc_start, anc_end):
	'''
	Returns EdgeTable mapping P1 or P2 ancestry across all chromosomes
	'''
	tablecoll = ts.tables
	ancestor_map = tablecoll.map_ancestors(samples, range(anc_start, anc_end))
	return ancestor_map

def getChildTracts(child, EdgeTable):
	'''
	Returns array of tract starts and ends for one chromosome
	'''
	indices = np.argwhere(EdgeTable.child==child)
	child_arr =[]
	for index in indices:
		child_arr.append([EdgeTable[int(index)].left, EdgeTable[int(index)].right])
		child_arr.sort(key = lambda x: x[0])
	return child_arr

def getMergedTracts(child_arr):
	'''
	Returns merged tracts for one chromosome
	'''
	tracts = []
	start = -1
	max = -1
	for i in range(len(child_arr)):
		t = child_arr[i]
		if t[0] > max:
			if i != 0:
				tracts.append([start, max])
			max = t[1]
			start = t[0]
		else:
			if t[1] >= max:
				max = t[1]
	if max != -1 and [start,max] not in tracts:
		tracts.append([start,max])
	return tracts

def getCompleteChildTracts(child_arr1, child_arr2, child):
	'''
	Returns merged tracts for one chromosome and both ancestries
	'''
	for anc in [1,2]:
		if anc == 1:
			for i in child_arr1:
				i.append(anc)
				i.append(child)
		if anc == 2:
			for i in child_arr2:
				i.append(anc)
				i.append(child)
	try:
		merged_child = np.concatenate((child_arr1, child_arr2))
		merged_child = merged_child[np.lexsort((merged_child[:,2], merged_child[:,3],merged_child[:,1], merged_child[:,0]))].astype('int32')
	except ValueError:
		if not child_arr1:
			merged_child=child_arr2
		elif not child_arr2:
			merged_child=child_arr1
	return merged_child

#read in trees file
infile = sys.argv[1]
outfile = re.search("(.*).trees", infile).group(1)

ts = pyslim.load(infile).simplify()

#sample 200 random chromosomes
sample_high = ts.num_samples

rng = np.random.default_rng()
samples = rng.choice(range(4, sample_high), size=200, replace=False)

#get EdgeTable with ancestry tracts
#for each ancestral population
anc_map1 = dumpTracts(samples, 0, 2)
anc_map2 = dumpTracts(samples, 2, 4)

#get sorted & merged tracts for each sample
for child in samples:
	child_tracts1 = getMergedTracts(getChildTracts(child, anc_map1))
	child_tracts2 = getMergedTracts(getChildTracts(child, anc_map2))
	merged_tracts = getCompleteChildTracts(child_tracts1, child_tracts2, child)
	try:
		total_tracts = np.concatenate((total_tracts, merged_tracts))
	except NameError:
		total_tracts = merged_tracts

#output txt file
ancestor_map_df = pd.DataFrame(total_tracts, columns = ["start_bp", "end_bp", "ancID", "childID"])


#convert to integer
ancestor_map_df = ancestor_map_df[:].astype("int64")

outname = f"{outfile}_alltracts.txt"

#save to csv file
ancestor_map_df.to_csv(outname, index = False, sep="\t")
