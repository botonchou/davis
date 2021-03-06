#!/usr/bin/env python

# ----------------------------------------------------------------------------
# A Benchmark Dataset and Evaluation Methodology for Video Object Segmentation
#-----------------------------------------------------------------------------
# Copyright (c) 2016 Federico Perazzi
# Licensed under the BSD License [see LICENSE for details]
# Written by Federico Perazzi
# ----------------------------------------------------------------------------

""" Read and display evaluation from HDF5.

EXAMPLE:
	python tools/eval_view.py method.h5

"""


import os
import time
import argparse

import numpy   as np
import os.path as osp

from prettytable import PrettyTable as ptable
from davis.dataset import *
from davis import log

def parse_args():
	"""Parse input arguments."""

	parser = argparse.ArgumentParser(
			description='Read and display evaluation from HDF5.')

	parser.add_argument(dest='input',default=None,type=str,
			help='Path to the HDF5 evaluation file to be displayed.')

	# Parse command-line arguments
	args       = parser.parse_args()
	args.input = osp.abspath(args.input)

	return args

if __name__ == '__main__':

	args = parse_args()

	technique = osp.splitext(osp.basename(args.input))[0]

	db_eval_dict = db_read_eval(technique,raw_eval=False,
			inputdir=osp.dirname(args.input))

	db_benchmark = db_read_benchmark()
	db_sequences = db_read_sequences()


	log.info("Displaying evaluation of: %s"%osp.basename(args.input))

	table = ptable(["Sequence"] + ['J(M)','J(O)','J(D)','F(M)','F(O)','F(D)','T(M)'])

	X = []
	for key,values in db_eval_dict[technique].iteritems():
		X.append(db_eval_dict[technique][key].values())

	X = np.hstack(X)[:,:7]
	for s,row in zip(db_sequences,X):
		table.add_row([s.name]+ ["{: .3f}".format(n) for n in row])

	table.add_row(['Average'] +
			["{: .3f}".format(n) for n in np.nanmean(X,axis=0)])

	print "\n" + str(table) + "\n"

