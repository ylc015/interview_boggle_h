#quantcast test
#author Yik Lun Chan
# 2/5/2016
import sys

#used by build_tries to see if a word exists
FIN = 'fin'
TOP = 'top'
L_TOP = 'left_top'
L_BOT = 'left_bottom'
BOT = 'bottom'
R_TOP = 'right_top'
R_BOT = 'right_bottom'
NO_EDGE = 'no_edge'

#customized queue class
class Queue(object):

	def __init__(self):
		self.q = []

	def get(self):
		if len(self.q) < 1:
			return None
		else:
			value = self.q[0]
			self.q = self.q[1:]
			return value

	def pop(self):
		if len(self.q) == 0:
			return None
		return self.q[0]

	def put(self, data):
		self.q.append(data)

	def empty(self):

		return len(self.q) == 0


	def tail(self):
		if len(self.q) == 0:
			return None
		return self.q[-1]

	def size(self):
		return len(self.q)

	def toString(self):
		
		print "queue: *********"
		for obj in self.q:
			print obj.toString()
		print "****************"

#cell class to present
#
#		         top
#		         ___
# right_top     /   \ left_top
# right_bottom	\___/ left_bottom
#               bottom
class Cell(object):

	#this class present a cell

	def __init__(self, value):


		self.value 			= value
		self.top 			= None	
		self.left_top 		= None
		self.left_bottom 	= None
		self.bottom			= None
		self.right_bottom   = None
		self.right_top		= None

		#used for DFS
		self.visited		= False
		self.isPrefix		= False

	def is_edge_full(self, is_first):

		if self.top is None: return False
		if self.left_top is None : return False
		if self.left_bottom is None: return False
		if self.bottom is None: return False
		if self.right_bottom is None: return False

		#this is a special case where the cell is the head of the loop
		#		__
		#	   / a\__
		#	   \__/  \
		#	   /  \  /
		# like cell a
		if self.right_top is None and not is_first: return False

		return True

	#find next availabe edge
	def next_edge(self):

		#to handle the presendence of top and right top
		if self.top is None and self.left_top is None: return TOP
		elif self.left_top is None: return L_TOP
		elif self.left_bottom is None: return L_BOT
		elif self.bottom is None: return BOT
		elif self.right_bottom is None: return R_BOT
		elif self.right_top is None: return R_TOP
		elif self.top is None: return TOP
		else: return NO_EDGE

	def next_cw_edge(self, tag):

		if tag == TOP:
			return L_TOP
		elif tag == L_TOP:
			return L_BOT
		elif tag == L_BOT:
			return BOT
		elif tag == BOT:
			return R_BOT
		elif tag == R_BOT:
			return R_TOP
		elif tag == R_TOP:
			return TOP

	#add cell to this cell
	def set_adj_edge(self, other, tag):

		#find an available edge
		next_edge = ''

		if tag != '':
			next_edge = tag
		else:
			next_edge = self.next_edge()

		if next_edge == TOP:
			self.top = other
			other.bottom = self

			#check neighbors
			if self.right_top is not None:
				other.right_bottom = self.right_top
				self.right_top.left_top = other
			if self.left_top is not None:
				other.left_bottom = self.left_top
				self.left_top.right_top = other

		elif next_edge == L_TOP:
			self.left_top = other
			other.right_bottom = self

			if self.top is not None:
				other.right_top = self.top
				self.top.left_bottom = other
			if self.left_bottom is not None:
				other.bottom = self.left_bottom
				self.left_bottom.top = other
		elif next_edge == L_BOT:
			self.left_bottom = other
			other.right_top = self

			if self.left_top is not None:
				other.top = self.left_top
				self.left_top.bottom = other
			if self.bottom is not None:
				other.right_bottom = self.bottom
				self.bottom.left_top = other
		elif next_edge == BOT:
			self.bottom = other
			other.top = self

			if self.left_bottom is not None:
				other.left_top = self.left_bottom
				self.left_bottom.right_bottom = other
			if self.right_bottom is not None:
				other.right_top = self.right_bottom
				self.right_bottom.left_bottom = other

		elif next_edge == R_BOT:
			self.right_bottom = other
			other.left_top = self

			if self.bottom is not None:
				other.left_bottom = self.bottom
				self.bottom.right_top = other
			if self.right_top is not None:
				other.top = self.right_top
				self.right_top.bottom = other
		elif next_edge == R_TOP:
			self.right_top = other
			other.left_bottom = self

			if self.right_bottom is not None:
				other.bottom = self.right_bottom
				self.right_bottom.top = other
			if self.top is not None:
				other.left_top = self.top
				self.top.right_bottom = other

		return next_edge



	def toString(self):

		top = '' 
		left_top = ''
		left_bottom = ''
		bottom = ''
		right_bottom = ''
		right_top  = ''

		if self.top is None:
			top = '?' 
		else: 
			top = self.top.value

		if self.left_top is None:
			left_top = '?'
		else:
			left_top = self.left_top.value

		if self.left_bottom is None:
			left_bottom = '?'
		else:
			left_bottom = self.left_bottom.value

		if self.bottom is None:
			bottom = '?'
		else:
			bottom = self.bottom.value

		if self.right_bottom is None:
			right_bottom = '?'
		else:
			right_bottom = self.right_bottom.value

		if self.right_top is None:
			right_top = '?'
		else:
			right_top = self.right_top.value

		print "-----"
		print "  %s  "	% (top)
		print "%s %s %s" % (right_top, self.value, left_top)
		print "%s    %s" % (right_bottom, left_bottom)
		print "  %s  " % (bottom)
		print "-----"

	def __str__(self):

		return self.value



def build_prefixes_words(data):

	prefixes = set()

	words = []

	for word in data:

		words.append(word)

		prefix = ''

		for letter in word:

			prefix += letter

			prefixes.add(prefix)

	return words, prefixes



# build the honeycomb map
def build_comb(data):

	#first number is always the number of layers
	layers = 1

	#this will be the heart cell of the comb
	head = Cell(data[1])


	#this is list that stores all the cells
	cells = []
	cells.append(head)

	#old candidates
	old_can = Queue()

	
	#holding candidates for next round
	temp_q = Queue()

	for letters in data[2:]:

		candidates = Queue()


		#this indicates whether all the cells has been put on the comb
		loop_closed = False

		#push all cells into a queue
		for letter in letters:
			cell = Cell(letter)
			candidates.put(cell)
			temp_q.put(cell)


		#to indicate if this is the first cell of the loop
		is_first = True

		# we need to avoid base case
		if layers == 1:
			is_first = False

		while not loop_closed:



			#head is the cell that we want to connect our new candidates(cell) with
			#we would append new cells to head until its full
			#however, there is one base case where head is the first node of the cycle.
			while not head.is_edge_full(is_first):

				next_cell = None

				if candidates.empty():
					loop_closed = True

					break

				else:
					next_cell = candidates.get()	
				
				head.set_adj_edge(next_cell, '')


			
			#fetch next head from old candidates
			if old_can.empty():
				loop_closed = True

				#now we need to connect the last cell of the loop to the first cell
				# the direction is always right bottom
				temp_q.pop().set_adj_edge(next_cell, R_BOT)

				#update old candidates info
				while not temp_q.empty():
					cell = temp_q.get()
					old_can.put(cell)
					cells.append(cell)

				if not old_can.empty():
					head = old_can.get()

					
			else:
				#choose next head
				head = old_can.get()

			if is_first: is_first = False

		layers += 1

	return cells



#perform dfs to find words given a starting point
def findwords(start_cell, words, prefixes):

	stack = [ start_cell ]

	str = ''

	result = []

	counter = 0

	while stack:

		current_cell = stack.pop()

		#set as a delimited to indicate that all neight of this node has
		#been visited, strip off the last element of the string
		# for instance, S->T->D->K->F where DKF is the neighthours of cell T
		# the stack should maintain the form [S,T,D,K,F] where T isPrefix is set to false
		# once we have visted cell, D, k, F. we should strip 'T' from the str and start
		# from string 'S' again
		if current_cell.isPrefix:

			current_cell.isPrefix = False

			str = str[:-1]

			continue

		str += current_cell.value

		current_cell.visited = True


		if str in words:

			result.append(str)

		if str in prefixes:

			current_cell.isPrefix = True

			stack.append(current_cell)

			if current_cell.top is not None and not current_cell.top.visited:

				stack.append(current_cell.top)


			if current_cell.left_top is not None and not current_cell.left_top.visited:

				stack.append(current_cell.left_top)


			if current_cell.left_bottom is not None and not current_cell.left_bottom.visited:

				stack.append(current_cell.left_bottom)


			if current_cell.bottom is not None and not current_cell.bottom.visited:

				stack.append(current_cell.bottom)


			if current_cell.right_bottom is not None and not current_cell.right_bottom.visited:

				stack.append(current_cell.right_bottom)


			if current_cell.right_top is not None and not current_cell.right_top.visited:

				stack.append(current_cell.right_top)


		else:

			current_cell.visited = False

			str = str[:-1]

		test = ''

		for cell in stack:

			test += cell.value


	return result



def findAllwords(cells, words, prefixes):

	result = []

	for cell in cells:


		result += findwords(cell, words, prefixes)


		# reset all node to unvisited
		for cell in cells:

			cell.visited = False


	return result


def main(argv):

	#read both files from terminal
	honey_txt = []
	with open(argv[0], "r") as ins:
		for line in ins:
			honey_txt.append(line.strip('\n'))



	dictionary = []
	with open(argv[1], "r") as ins:
		for line in ins:
			dictionary.append(line.strip('\n'))


	cells = build_comb(honey_txt)

	words, prefixes = build_prefixes_words(dictionary)

	result = findAllwords(cells, words, prefixes)

	result = set(result)

	for word in sorted(result):

		print word
	
	

if __name__ == "__main__":
	main(sys.argv[1:])
