def valid(bo, pos, num):
	for i in range(len(bo[0])):
		if bo[pos[0]][i] == num and pos[1] != i:
			return False
	for i in range(len(bo)):
		if bo[i][pos[1]] == num and pos[1] != i:
			return False

	
	box_x = pos[1] // 3
	box_y = pos[0] // 3
	
	for i in range(box_y*3, box_y*3 +3):
		for x in range(box_x*3, box_x*3 +3):
			if bo[i][x] == num and (i, x) != pos:
				return False
	
	return True
	


def find_empty(bo):
	for i in range(len(bo)):
		for x in range(len(bo[0])):
			if bo[i][x] == 0:
				return (i, x) # row and col

	return None