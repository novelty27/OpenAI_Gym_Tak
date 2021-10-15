class Moves:

	def __init__(self):
		self.moves = {}

	def buildMoves(self, input):
	    x = 1
	    output=[]
	    if(input in self.moves):
	        return self.moves[input]
	    elif (input[1] == 1):
	        while(input[0]-x >= 1):
	            output.append(str(input[0]-x))
	            x = x + 1
	        self.moves[input] = output
	    else:
	        while(input[0]-x >= input[1]):
	            output += [[input[0]-x, [(input[0]-x, input[1]-1)]]]
	            x = x + 1
	        self.moves[input] = output

	def getMoves(self, input):
	    if (input not in self.moves):
	        self.buildMoves(input)
	        return self.getMoves(input)
	    pulledValue = self.moves[input]
	    if (input[1] == 1 ):
	        return self.moves[input]
	    else:
	        output = []
	        for i in pulledValue:
	            recurse = self.getMoves(i[1][0])
	            for j in recurse:
	                output.append(str(i[0]) + '.' + str(j))
	        return output