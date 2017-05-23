import numpy as np

def pprint(board):
	print '\n\n'
	new_string = ['','','']
	for a in range(3):
		for b in range(3):
			if board[a][b] == 0:
				new_string[a] += ' -'
			elif board[a][b] == 1:
				new_string[a] += ' x'
			elif board[a][b] == 2:
				new_string[a] += ' o'
	for line in new_string:
		print '   ',line
	print '\n\n\n\n'


# Return [1,2] for player win. Return 0 for tie. Return -1 for unfinished
def winstate(board):
	all_lines = []
	for a in xrange(3):
		all_lines.append(board[a,:])
		all_lines.append(board[:,a])
	all_lines.append(np.array([board[2,0],board[1,1],board[0,2]]))
	all_lines.append(np.array([board[0,0],board[1,1],board[2,2]]))

	# Return choose ( [1,2] )
	for b in all_lines:
		if len(set(b))==1 and 0 not in b:
			return b[0]

	# Return (-1) for unfinished
	if 0 in board:
		return -1

	# Return (0) for tie
	return 0

# Find legal moves on the board
def legal_moves(board):
	legal = []
	for a in range(len(board)):
		for b in range(len(board)):
			if board[a][b]==0:
				legal.append([a,b])
	return legal

# Adds a player's move to the board
def add_move(initial_board,move,player):
	board = np.copy(initial_board)
	a, b = move[0],move[1]
	board[a][b] = player
	return board

# Returns a score for winning positions.
# Speed counts.
def score(winner,depth):
	if winner == 1:
		return 10 - depth
	elif winner == 2:
		return depth - 10
	elif winner == 0:
		return 0
	else:
		return None

# Returns a node's score - min score or max score depending
def check_node(board,player,depth,decide=False):
	depth += 1
	winner = winstate(board)
	if winner >= 0:
		return score(winner,depth)
	elif winner < 0: # else:
		legal = legal_moves(board)
		new_boards = []
		scores = []
		new_player = player % 2 + 1
		for a in legal:
			new_boards.append(add_move(board,a,player))
		for b in new_boards:
			scores.append(check_node(b,new_player,depth))
		mx, max_index = max( (scores[i],i) for i in xrange(len(scores)))
		mn, min_index = min( (scores[i],i) for i in xrange(len(scores)))
		if player == 1:
			if decide:
				return legal[max_index]
			return mx
		elif player == 2:
			if decide:
				return legal[min_index]
			return mn

print '\n\n   T-I-C\n   T-A-C\n   T-O-E\n\n\n     by ben\n\n\n'
new_board = np.zeros((3,3)).astype(int)



# For player/computer gameplay
first = raw_input('   Would you like to go first? (y/n) : ')
while first not in ['y','n']:
	if first not in ['y','n']:
		print '   Try again.'

pprint(new_board)

if first == 'n':
	computer_move = check_node(new_board,2,0,decide=True)
	new_board = add_move(new_board,computer_move,1)
	print '\n   COMP MOVE:'
	pprint(new_board)

while True:
	text = input('\n   Please enter your move in form 0,0:   ')
	human_move = [text[0],text[1]]
	new_board = add_move(new_board,human_move,1)
	if winstate(new_board) >= 0:
		break
	print '\n   YOUR MOVE:'
	pprint(new_board)


	computer_move = check_node(new_board,2,0,decide=True)
	new_board = add_move(new_board,computer_move,2)
	print '\n   COMP MOVE:'
	pprint(new_board)
	if winstate(new_board) >= 0:
		break

endgame = winstate(new_board)

if endgame == 0:
	print "\n   The game is of the cat!"
elif endgame == 1:
	print '   You win!'
elif endgame == 2:
	print '   Computer wins!'

