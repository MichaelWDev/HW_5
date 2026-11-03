# Michael Woodyard
# CSE 2050 - 01
# 10/31/2026
# Ballot Boxes


import math
import sys


def ballot_boxes():
	# get the inputs from the sys.stdin
	input = sys.stdin.read().split()

	# if the input is missing, stop the program
	if not input:
		return


	# get the n_cities, and k_ballot_boxes
	n_cities = int(input[0])
	k_ballot_boxes = int(input[1])


	# get all of the populations of the n_cities
	n_city_populations = [int(x) for x in input[2 : 2 + n_cities]]

	# use binary search to get the maximum capacity
	lowest_capacity = 1
	highest_capacity = max(n_city_populations)

	answer = highest_capacity


	# while the lowest is less than or equal to the highest capacity
	while lowest_capacity <= highest_capacity:
		middle = (lowest_capacity + highest_capacity) // 2

		# check the total amount of boxes needed if the max capacity per the box is the middle
		total_boxes = 0

		# for people in n_city_populations, add them to the middle
		for people in n_city_populations:
			total_boxes += (people + middle - 1) // middle


		# adjust the boundaries of the binary search
		if total_boxes <= k_ballot_boxes:
			# the middle number is correct, so save it to a variable and try the smaller capacity
			answer = middle

			highest_capacity = middle - 1

		else:
			# the middle is too small, so try the larger capacity
			lowest_capacity = middle + 1


	# print the answer
	print(answer)
	