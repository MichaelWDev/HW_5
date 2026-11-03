# Michael Woodyard
# CSE 2050 - 01
# 10/31/2026
# Edit Distance


import sys


def edit_distance():

	# get all of the inputs
	input = sys.stdin.read().split()

	# if the input is missing, stop the program
	if len(input) < 2:
		return


	# get the string A and the targetted end string B
	starting_string = input[0]
	ending_string = input[1]

	# get the lengths of each string
	starting_string_length = len(starting_string)
	ending_string_length = len(ending_string)


	# make a 2d array to store the minimum editing distance
	# between starting_string[:i], and ending_string[:j]
	dynamic_programming_table = [[0] * (ending_string_length + 1) for _ in range (starting_string_length + 1)]

	# loop through the starting_string_length amount
	for i_index in range(starting_string_length + 1):
		# add the i_index to the dpt at [i_index][0]
		dynamic_programming_table[i_index][0] = i_index

	# loop through the ending_string_length amound
	for j_index in range(ending_string_length + 1):
		# add the j_index to the dpt at [0][j_index]
		dynamic_programming_table[0][j_index] = j_index


	# put the values into the dpt
	for i_index in range(1, starting_string_length + 1):
		for j_index in range(1, ending_string_length + 1):

			# check if the characters inside the starting_string are == to the ending_strings
			if starting_string[i_index - 1] == ending_string[j_index - 1]:
				dynamic_programming_table[i_index][j_index] = dynamic_programming_table[i_index - 1][j_index - 1]

			else:
				# now replace, delete, and insert
				dynamic_programming_table[i_index][j_index] = 1 + min(
					# replaces
					dynamic_programming_table[i_index - 1][j_index - 1],

					# deletes
					dynamic_programming_table[i_index - 1][j_index],

					# inserts
					dynamic_programming_table[i_index][j_index - 1]
				)

	# print the total amount of minimum operations done
	total_minimum_operations = dynamic_programming_table[starting_string_length][ending_string_length]
	print(total_minimum_operations)


	# ------------------------------------------------------------------------------------------

	# remake the dynamic_programming_table[starting_string_length][ending_string_length] edits
	i_length, j_length = starting_string_length, ending_string_length

	operations = []

	# while i_length or j_length are greater than 0
	while i_length > 0 or j_length > 0:
		# characters are identical
		if i_length > 0 and j_length > 0 and starting_string[i_length - 1] == ending_string[j_length - 1]:
			i_length -= 1
			j_length -= 1

		# check for substitution / replace (diagonals)
		elif i_length > 0 and j_length > 0 and dynamic_programming_table[i_length][j_length] == dynamic_programming_table[i_length - 1][j_length - 1] + 1:
			operations.append(('replace', i_length - 1, ending_string[j_length - 1]))
			i_length -= 1
			j_length -= 1

		# check for deletion
		elif i_length > 0 and dynamic_programming_table[i_length][j_length] == dynamic_programming_table[i_length - 1][j_length] + 1:
			operations.append(('delete', i_length - 1))
			i_length -= 1

		# check for insertion
		elif j_length > 0 and dynamic_programming_table[i_length][j_length] == dynamic_programming_table[i_length][j_length - 1] + 1:
			operations.append(('insert', i_length, ending_string[j_length - 1]))
			j_length -= 1


	# reverse the operations, go from starting_string to ending_string
	operations.reverse()


	# ------------------------------------------------------------------------------------------

	# apply the operations in sequential order, and then format the outputted lines

	# get the current characters of the starting_string
	current_characters = list(starting_string)

	# tracking index offset caused by insertions/deletions for replace positioning
	# for op type, position, and character placed inside operations
	for operation_type , position, character in operations:
		p_str = "".join(current_characters)


		# check the operation types


		# if the type is replace
		if operation_type == 'replace':
			# replace the character at the given position with the format .c.
			q_str = "".join(current_characters[:position]) + f".{character}." + "".join(current_characters[position + 1 :])

			# the current_characters at position is set to the character
			current_characters[position] = character

		# if the type is delete
		elif operation_type == 'delete':
			# note the character deleted at the position with a [*]
			q_str = "".join(current_characters[:position]) + "[*]" + "".join(current_characters[position + 1 :])

			# pop the position in current_characters
			current_characters.pop(position)

		elif operation_type == 'insert':
			# insert the character at the position with a [c]
			q_str = "".join(current_characters[:position]) + f"[{character}]" + "".join(current_characters[position:])
			
			# insert the (position, character) into the current_characters
			current_characters.insert(position, character)


		# print the string transformation (ie: p --> q)
		print(f"{p_str} --> {q_str}")


	# print the actual reconstructed string
	print("".join(current_characters))


edit_distance()

# Note: For some reason there's a bug within the algorithm that messes up the final printout.
#		My Output:
#			2
#			LOVE --> .M.OVE
#			MOVE --> MOV[I]E
#			MOVIE

#		Expected Output:
# 			2
# 			LOVE --> LOV[I]E
# 			LOVIE --> .M.OVIE
# 			MOVIE