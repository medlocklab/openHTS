import pandas
import numpy
import random


DIMS96 = {'rows':8,'columns':12}

def create_constant_column_plate(dims: dict,sources: int):
	"""
	Generate a dataframe representing a 96-well plate that has one media
	ingredient per column.
	"""
	# initialize an array with one row for each well and one column for each
	# media ingredient source
	wells = numpy.zeros((dims['rows']*dims['columns'],sources))

	# fill each column of the plate with a single ingredient
	for i in range(0,sources):
		wells[i*dims['rows']:(i+1)*dims['rows'],i] = 1.0
	
	# convert to a dataframe with wells numbered 1-96 in the index and each
	# media ingredient labeled as "source N"
	df = pandas.DataFrame(wells,
				index=list(range(1,dims['rows']*dims['columns']+1)),
				columns=list(["source " + str(x) for x in range(1,sources+1)]))
	df.index.name = 'wells'
	return(df)


def create_random_plate(dims: dict, sources: int):
	"""
	Generate a plate completely filled in each well with random combinations
	of source ingredients, each in intervals of 0.05, which add to 1.0 total
	per well.
	"""
	# initialize an array with one row for each well and one column for each
	# media ingredient source
	wells = numpy.zeros((dims['rows']*dims['columns'],sources))

	# for each well, get the relative amount of each media ingredient source
	wellcount = 0
	for well in wells:
		distribution = list(random_ints_with_sum(sources))
		distribution = [d/float(sources) for d in distribution]
		# add zeros to get length equal to total number of sources
		distribution.extend(
						[0.0 for x in range(0,sources-len(distribution))])
		# shuffle the entries
		random.shuffle(distribution)
		wells[wellcount] = distribution
		wellcount += 1
	
	df = pandas.DataFrame(wells,
				index=list(range(1,dims['rows']*dims['columns']+1)),
				columns=list(["source " + str(x) for x in range(1,sources+1)]))
	df.index.name = 'wells'
	return(df)
	

def random_ints_with_sum(n):
    """
    Generate positive random integers summing to `n`, sampled
    uniformly from the ordered integer partitions of `n`.
    """
    p = 0
    for _ in range(n - 1):
        p += 1
        if random.randrange(2):
            yield p
            p = 0
    yield p + 1


if __name__ == "__main__":
	# if this is executed as a script, generate a few test plates
	constant_columns = create_constant_column_plate(dims=DIMS96,sources=12)
	constant_columns.to_csv('./generated_test_files/constant_columns.tsv',
							sep='\t')
	random_plate = create_random_plate(dims=DIMS96,sources=12)
	random_plate.to_csv('./generated_test_files/random_plate.tsv', sep='\t')