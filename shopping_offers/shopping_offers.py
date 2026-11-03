# Michael Woodyard
# CSE 2050 - 01
# 11/02/2026
# Shopping Offers

# -------------------------------------------------------------------------------------------------------------
	# H05.pdf:
	# The input starts with a singe integer s, that is the number of special offers.
	# We have at most 99 special offers in the input.

	# The following s lines describes a special offer using several integers.

	# The first integer n, (1 ≤n ≤5), gives the number of products that are offered.

	# The subsequent n pairs of integers c and k indicate that k items (1 ≤k ≤5)
	# with product code c, (1 ≤c ≤999) are part of the offer.

	# The last number p on the line stands for the reduced price (1 ≤p ≤9999).
	# The reduced price of an offer is less than the sum of the regular prices.

	# The following line contains the number b, (0 ≤b ≤5), of different kinds of products to be purchased.
	# Each of the following b lines contains three values: c, k, and p.
	#		The value c is the (unique) product code (1 ≤c ≤999).
	#		The value k indicates how many items of this product are to be purchased (1 ≤k ≤5).
	# 		The value p is the regular price per item (1 ≤p ≤999).

	# At most 25 items can be in the basket.

	# Output a single integer, that is the lowest possible price to be paid for the purchases.
# -------------------------------------------------------------------------------------------------------------

import sys

# I'm re-trying modular methods this time. I keep forgetting that it exists (oops)

# parses the input and returns the values given
def parse_input():

	# gets the input
	input = sys.stdin.read().split()

	# index to keep track of where i am, inside the input, starting at 0
	if not input:
		return None, None, None, None

	# the starting input index
	input_index = 0

	# number of offers
	number_of_special_offers = int(input[input_index])

	# increment the index by 1 after parsing the first input
	input_index += 1

	# add each offer into a list, [offer_items, reduced_price]
	raw_offers = []

	# loop through the number of special offers
	for _ in range(number_of_special_offers):
		# how many items are in the current offer
		number_of_items_in_offer = int(input[input_index])

		# increment the input_index again
		input_index += 1

		# list of the products offered, [product_code, product_quantity]
		offer_items = []

		# loop through the number of items in the current offer
		for _ in range(number_of_items_in_offer):
			# gets the item code
			item_code = int(input[input_index])

			# get the item_quantity at input_index + 1
			item_quantity = int(input[input_index + 1])

			# append [item_code, item_quantity] to offer_items
			offer_items.append([item_code, item_quantity])

			# increment the input index by two since i gathered two more inputs
			input_index += 2

		# price of the offer
		reduced_price = int(input[input_index])

		# increment the index again
		input_index += 1

		# append the [offer_items, reduced_price] to raw_offers
		raw_offers.append([offer_items, reduced_price])


	# -----------------------------------------------------------

	# get the number of items needed to be bought
	number_of_products = int(input[input_index])

	input_index += 1

	# dictionary to map all of the product codes to index into
	product_code_index_dict = {}

	# list of the quantity of products needed
	quantity_needed = []

	# list of the normal prices
	normal_prices = []

	# loop through the number num_products and gets getting the product_code, product_quantity, and normal_prices
	for index in range(number_of_products):
		product_code = int(input[input_index])
		quantity = int(input[input_index + 1])
		price = int(input[input_index + 2])

		# increment the index by 3 since we gathered 3 inputs
		input_index += 3

		# add the indexed product_code into the product_code_index dictionary
		product_code_index_dict[product_code] = index

		# add the quantity to the quantity_needed list
		quantity_needed.append(quantity)

		# add the price to the normal_prices list
		normal_prices.append(price)


	# -----------------------------------------------------------


	# now to finally format the offers from the raw_offers list

	# this will store the offers that get formatted
	offers_formatted = []


	# loop through the raw_offers list, with their offer_items and raw_offers
	for offer_items, price in raw_offers:
		# counts the offers, indexed at 0, multiplied by number_of_products
		offer_counts = [0] * number_of_products

		# boolean that sets the offer to valid
		offer_is_valid = True


		# loop through offer_items, with their code and quantity
		for product_code, quantity in offer_items:
			if product_code in product_code_index_dict:

				# stores the item indexed inside the code_to_index dictionary, with product_code as the index
				item_index = product_code_index_dict[product_code]

				# sets the offer_counts, at item_index, equal to the quantity
				offer_counts[item_index] = quantity

			# otherwise, if an offer has an item not needed, then skip it
			else:
				# set the offer validity to false
				offer_is_valid = False

				break


		# check if valid_offer is true
		if offer_is_valid:
			# since the offer is valid, appends [offer_counts, price] to offers_formatted
			offers_formatted.append([offer_counts, price])


	# finally, return the quantity_needed, normal_prices, offers_formatted, and number_of_products
	return quantity_needed, normal_prices, offers_formatted, number_of_products


# parse_input() completed


# -----------------------------------------------------------


# memoization (which i just learned) is a type of caching for program performance
# it stores computed results for future retrieval


# recursive function that finds the minimum costs, using memoization
def minimum_cost(current_needs, normal_prices, offers_formatted, memoization):

	# converts the current_needs into a tuple, so i can use it as a dictionary key
	current_needs_tuple = tuple(current_needs)

	# uses the current_needs_tuple to check if the minimum cost was already calculated in the memoization
	if current_needs_tuple in memoization:
		return memoization[current_needs_tuple]


	# will be used to calculate the cost of buying all remaining items at the normal prices
	normal_prices_total_cost = 0

	# loop to the length of current_needs
	for index in range(len(current_needs)):
		# calculates the normal_prices_total_cost, using current_needs[index] multiplied by the normal_prices[index]
		normal_prices_total_cost += current_needs[index] * normal_prices[index]


	# -----------------------------------------------------------

	# now to apply each special offer


	# loop through offers_formatted, getting offer_counts and offer_price
	for offer_counts, offer_price in offers_formatted:

		# check if the offer can be used, wont go past the current_needs
		offer_can_be_used = True

		# loop to the length of current_needs
		for index in range(len(current_needs)):

			# checks if the offer_counts at the index is greater than the current_needs[index]
			if offer_counts[index] > current_needs[index]:

				# since offer_counts[index] is greater than the current_needs[index], set offer_can_be_used to false
				offer_can_be_used = False

				break



		# since the offer is valid, ill apply it and recursively call the function
		if offer_can_be_used:

			# list that stores the new quantities needed
			new_needs = []

			# loop to the length of current_needs
			for index in range(len(current_needs)):

				# appends the calculated new_needs, subtracting the offer_counts[index] from current_needs[index]
				new_needs.append(current_needs[index] - offer_counts[index])


			# recursively calls the remaining needs and additionally the offer_price
			cost_with_offer = offer_price + minimum_cost(new_needs, normal_prices, offers_formatted, memoization)


			# keeps track of the minimum costs found
			# if the cost_with_offer is less than the normal_prices_total_cost, set the normal_prices_total_cost equal to the cost_with_offer
			if cost_with_offer < normal_prices_total_cost:
				normal_prices_total_cost = cost_with_offer


	# now to finally save the result in the memoization's dictionary, and return the normal_prices_total_cost
	memoization[current_needs_tuple] = normal_prices_total_cost

	return normal_prices_total_cost


# -----------------------------------------------------------


# lastly, the main method that will print the calculated_minimum_cost, using the inputs


# main method!!
def shopping_offers():

	# uses the method above, parse_input(), to get all the inputs
	# parse_input() returns the variables: quantity_needed, normal_prices, offers_formatted, number_of_products
	# sets those variables here = to those variables returned
	quantity_needed, normal_prices, offers_formatted, number_of_products = parse_input()


	# if the quantity_needed is None (0), then stop shopping_offers()
	if quantity_needed is None:
		return

	# initializes the memoization dictionary that i made earlier
	memoization = {}

	# calculate the minimum cost, using the minimum_cost() function i made earlier
	# calls the function using quantity_needed, normal_prices, offers_formatted, and memoization
	calculated_minimum_cost = minimum_cost(quantity_needed, normal_prices, offers_formatted, memoization)


	# print the calculated_minimum_cost
	print(calculated_minimum_cost)


shopping_offers()


# prints 14!!!!