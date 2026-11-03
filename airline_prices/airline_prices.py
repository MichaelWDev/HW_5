# Michael Woodyard
# CSE 2050 - 01
# 11/02/2026
# Airline Prices

# -------------------------------------------------------------------------------------------------------------
	# The first line of the input contains two integers:
	#		n : the number of seats left
	# 		w : the number of weeks left before the flight (0 < m ≤300, 0 ≤w ≤52).
	# 			The next w + 1 lines give the estimates for 2 weeks
	# 						w − 1 weeks, ... , down to 0 weeks (last week) before the flight.

	# Each of these lines starts with an integer k, (0 < k ≤100)
	#		k : the number of different prices to consider that week

	# This is followed by integers:
	# 		0 < p1 < p2 < ... < pk < 1000, giving the prices in dollars.

	# Finally, this is followed by k additional integers:
	# 		s1, ... , sk, (0 ≤si ≤n) indicating the number of tickets that will be sold for the corresponding prices.

	# On the first line, print the maximum total revenue the airline can obtain from ticket sales, from:
	#		1) The current week to the time of the flight
	# 		2) The next w lines should contain the optimal price for w weeks before the flight,
	# 				w − 1 weeks before the flight, and so on up to the week of the flight (week 0)
	# 
	# 		3) If there are multiple sets of ticket prices achieving this maximum:
	# 				Choose the smallest ticket price for the corresponding week.
# -------------------------------------------------------------------------------------------------------------


import sys


# gets the input, and returns the parsed input
def parse_input():

	input = sys.stdin.read().split()

	# if the input is missing, stop the program
	if not input:
		return None, None, None

	# -----------------------------------------------------------

	# index to keep track of where i am, inside the input, starting at 0
	input_index = 0

	# get the n seats (total number of seats)
	total_number_of_seats = int(input[input_index])

	# get the w weeks (total number of weeks), + 1 to the input index
	total_number_of_weeks = int(input[input_index + 1])

	# increment the input_index by 2, since i got 2 inputs so far
	input_index += 2

	# list that will store the price options per week ([price_1, demand_1])
	price_options_per_week = []

	# loop to the total_number_of_weeks + 1
	for _ in range(total_number_of_weeks + 1):

		# number of different prices per week
		number_of_different_prices_per_week = int(input[input_index])

		# increment the input_index again, by 1
		input_index += 1

		# stores the prices in dollar amount, using a for loop
		prices_in_dollars = [
			int(prices) for prices in input[
				input_index : input_index + number_of_different_prices_per_week
			]
		]

		# increment the input_index again, now by the number_of_different_prices_per_week
		input_index += number_of_different_prices_per_week

		# stores the number of tickets sold for each flight
		number_of_tickets_sold = [
			int(tickets_sold) for tickets_sold in input[
				input_index : input_index + number_of_different_prices_per_week
			]
		]

		# same increment as the previous increment above
		input_index += number_of_different_prices_per_week

		# list that will be used to store (price, tickets_sold) pairs
		airline_options = []

		# loop to the range of number_of_different_prices_per_week
		for index in range(number_of_different_prices_per_week):
			airline_options.append((prices_in_dollars[index], number_of_tickets_sold[index]))

		# append the airline_options list into the price_options_per_week list
		price_options_per_week.append(airline_options)


	# -----------------------------------------------------------


	# finally, return the total_number_of_seats, total_number_of_weeks, and the price_options_per_week
	return total_number_of_seats, total_number_of_weeks, price_options_per_week

# parse_input() is done!


# -----------------------------------------------------------


# now to calculate the maximum revenue and keep track of the optimal prices

# im going to reuse the memoization technique for this as well, just like i did in shopping_offers.py

# recursive function using memoization, that will calculate the max revenue and track the optimal prices
def calculate_maximum_revenue_and_track_optimal_prices(
		week_index,
		seats_left,
		total_number_of_weeks,
		price_options_per_week,
		memoization
	):

	# first, check if there are no weeks left, or no seats are left
	# if week_index is greater than total_number_of_weeks, return 0 and an empty list
	if week_index > total_number_of_weeks:
		return 0, []


	# using a tuple like i did in the last program as a key for the memoization dictionary
	# it'll store (week_index, seats_left)
	current_state = (week_index, seats_left)


	if current_state in memoization:
		return memoization[current_state]


	# -----------------------------------------------------------


	# create a new variable, maximum_revenue, starting at -1
	maximum_revenue = -1

	# list that will be used to track the optimal_prices
	optimal_prices = []

	# options for the current week, from price_options_per_week with the week_index
	options_for_current_week = price_options_per_week[week_index]


	# loop that goes through the price of each ticket, and demand (option) for the current week
	for price_of_each_ticket, demand in options_for_current_week:

		# number of tickets sold, which is limited by the remaining seats, using min():
			# With a single iterable argument, return its smallest item
			# The default keyword-only argument specifies an object to return if the provided iterable is empty
			# With two or more positional arguments, return the smallest argument (from vscode)
		tickets_sold = min(seats_left, demand)

		# calculates the revenue of this week, multiplying the number of tickets sold by the price
		revenue_for_this_week = tickets_sold * price_of_each_ticket

		# now to recursively call for the remaining weeks
		# future revenue AND future prices uses the method, and will include in the call:
			# week_index + 1 (increment the index first)
			# seats_left, subtracted by tickets_sold to get the remaining seats
			# total_number_of_weeks
			# price_options_per_week
			# and the memoization
		future_revenue, future_prices = calculate_maximum_revenue_and_track_optimal_prices(
			week_index + 1,
			seats_left - tickets_sold,
			total_number_of_weeks,
			price_options_per_week,
			memoization
		)

		# calculates the total revenue expected, which is done by adding revenue_for_this_week and future_revenue together
		total_revenue_expected = revenue_for_this_week + future_revenue


		# now to check if the total_revenue_expected is greater than the maximum_revenue
		if total_revenue_expected > maximum_revenue:
			# if the total_revenue_expected is greater than the maximum_revenue, set the maximum to the total expected
			maximum_revenue = total_revenue_expected

			# and add the price_of_each_ticket and future_prices together, put it into the optimal_prices list
			optimal_prices = [price_of_each_ticket] + future_prices

		# else if the total_revenue_expected is equal to the maximum_revenue, then choose the lowest ticket price for the week
		elif total_revenue_expected == maximum_revenue:
			# if there is no optimal_price, or the price_of_each_ticket is greater than the optimal_price at index 0
			if not optimal_prices or price_of_each_ticket < optimal_prices[0]:

				# set the maximum_revenue to the total_revenue_expected
				maximum_revenue = total_revenue_expected

				# and add the price_of_each_ticket and future_prices together, put it into the optimal_prices list
				optimal_prices = [price_of_each_ticket] + future_prices


	# finally, store the maximum_revenue variable, and optimal_prices list into the memoization at the index current_state
	memoization[current_state] = (maximum_revenue, optimal_prices)

	# and return the maximum_revenue and optimal_prices
	return maximum_revenue, optimal_prices


# calculate_maximum_revenue_and_track_optimal_prices() is done!


# -----------------------------------------------------------


# now for the main function!!


def airline_prices():

	# parses the input, using the parse_input() function i made, and assigns them to variables
	total_number_of_seats, total_number_of_weeks, price_options_per_week = parse_input()


	# check if the input is missing, if it is then stop the program
	if total_number_of_seats is None:
		return


	# initializes the memoization dictionary
	memoization = {}

	# calculates the maximum revenue and optimal prices,
	# using my calculate_maximum_revenue_and_track_optimal_prices() method
	# assigns them to maximum_revenue and optimal_prices
	maximum_revenue, optimal_prices = calculate_maximum_revenue_and_track_optimal_prices(
		0,
		total_number_of_seats,
		total_number_of_weeks,
		price_options_per_week,
		memoization
	)


	# now to print the maximum revenue first
	print(maximum_revenue)


	# then, print each optimal price in the optimal_prices list on the following lines
	# a for loop will do this perfectlyyy
	for optimal_price in optimal_prices:
		# for every new line, print the optimal_price
		print(optimal_price)


airline_prices()

