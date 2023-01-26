#
# Perform a series of coin flips and keep a record of the running total
# Heads increments the total, Tails decrements it.
# For each series record the number of times each positive value is reached before a negative
# before a negative value, and vice versa.
#
# e.g. How many times was a total of +5 reached before -5? Or -10 before +3?
#
# Record the results in a 2 dimensional table where each cell is a bin containing
# a count of win/loss (+/-) occurances for a given pair of values.
#
# e.g. +5 was reached before -5 in 3 series, and -5 was reached before +5 in 6 series.
#      The value in the bin at (5, 5) is -3.
#
# 'Wins' (positive values) are y-coordinate values
# 'Losses' (negative values) are x-coordinate values
# 
# 3  1  2 -3
# 2 -2 -3  4
# 1  2 -1  1
#    1  2  3 (negative totals)
#
# In the table above, the total count reached -2 before it reached 2
# three more times than 2 was reached before -2
#
# During each series, a preliminary table is generated to track which min/max pairs are reached first.
# If the first roll is a heads, then the total is 1, and 1 occurred before any negative value.
# So the entire horizontal row (y=1) is filled in with ones.
# If the next roll is tails, then the count is now zero again and there is no 'first occurance'
# Then the next roll is tails, the count is -1, and so -1 occurred before any positive number except 1.
# The entire column (x=1) is filled with -1, except for (1,1) which already has a 1 in it.
# When the series is complete, the premliminary table is summed with the tracking table.
#






import random, statistics, sys

RANDOM_SEED     = 314
N_TRIALS        = 2
FLIPS_PER_TRIAL = 100
ROWS            = FLIPS_PER_TRIAL // 2  # arbitrary big number, should not be exceeded
COLS            = FLIPS_PER_TRIAL // 2

def flip():
    '''Return +1 if heads, -1 if tails.'''
    if random.randint(0,1): return +1
    else:                   return -1

def printTable(table):
    for row in range(ROWS-1, 0, -1): # y values
        print ()
        for col in range(1, COLS): # x values
            print ("%3d" % table[col][row], end='')
    print ()


#
# Main
#

#random.seed(RANDOM_SEED)

for t in range(N_TRIALS):
    total = 0
    tmax = 0
    tmin = 0
    series_table = [[0 for col in range(COLS)] for row in range(ROWS)] # initialize table
    for f in range(FLIPS_PER_TRIAL):
        total += flip()
        if total > tmax:
            # new positive max value, fill row in series table
            tmax = total
            for col in range(COLS):
                if series_table[col][tmax] == 0:
                    series_table[col][tmax] = 1
        if total < tmin:
            # new negative max value, fill col in series table
            tmin = total
            tmin_abs = abs(tmin)
            for row in range(ROWS):
                if series_table[tmin_abs][row] == 0:
                    series_table[tmin_abs][row] = -1

    printTable(series_table)


