# tram consist of
# name, list of stops
# dictionary of trams
class TramClass:

	TramsDict = {}

	def __init__(self,name):
		TramClass.TramsDict[name] = self
		self.name = name
		self.route = []

	@staticmethod
	def AddAliasGroupIndexToRoute(name,index):
		TramClass.TramsDict[name].route.append(index)

	@staticmethod
	def UpdateTramRoutesToFirst(ListOfGroups):

		First = ListOfGroups[0]
		for TramName in TramClass.TramsDict:
			for i in range(0,len(TramClass.TramsDict[TramName].route)):
				if TramClass.TramsDict[TramName].route[i] in ListOfGroups:
					TramClass.TramsDict[TramName].route[i] = First

class AliasClass:

	AliasToGroup = {}
	NextGroupIndex = 0

	@staticmethod
	def AddCurrentAliasesToFirstGroup(ListOfAliases,FirstGroupIndex):

		for alias in ListOfAliases:
			AliasClass.AliasToGroup[alias] = FirstGroupIndex

	@staticmethod
	def UnionGroupsWithFirst(ListOfGroups):

		FirstGroupIndex = ListOfGroups[0]
		for i in range(1,len(ListOfGroups)):
			AllAliases = [k for k,v in AliasClass.AliasToGroup.items()]
			for alias in AllAliases:
				AliasClass.AliasToGroup[alias] = FirstGroupIndex

	@staticmethod
	def KeepUnionFind(ListOfAliases):
		ListOfFoundGroupIndex = []
		for alias in ListOfAliases:
			if alias in AliasClass.AliasToGroup:
				if AliasClass.AliasToGroup[alias] not in ListOfFoundGroupIndex:
					ListOfFoundGroupIndex.append(AliasClass.AliasToGroup[alias])
		IndexToReturn = -1
		if ListOfFoundGroupIndex == []:
			for alias in ListOfAliases:
				AliasClass.AliasToGroup[alias] = AliasClass.NextGroupIndex
			IndexToReturn = AliasClass.NextGroupIndex
			AliasClass.NextGroupIndex += 1

		else:
			FirstGroupIndex = ListOfFoundGroupIndex[0]
			AliasClass.AddCurrentAliasesToFirstGroup(ListOfAliases,FirstGroupIndex)
			AliasClass.UnionGroupsWithFirst(ListOfFoundGroupIndex)
			TramClass.UpdateTramRoutesToFirst(ListOfFoundGroupIndex)
			IndexToReturn = FirstGroupIndex

		return IndexToReturn

class NodeClass:

	NodeIDToNode = {}

	def __init__(self,ID):
		self.ID = ID
		NodeClass.NodeIDToNode[ID] = self

		self.neighbours = set()

		self.visited = False
		self.DistanceFromStart = -1
		self.parent = None

	def add_neighbour(self,neighbour):
		self.neighbours.add(neighbour)

	@staticmethod
	def make_neighbour(first,second):
		first.add_neighbour(second)
		second.add_neighbour(first)

	@staticmethod
	def reset():
		for x in NodeClass.NodeIDToNode:
			NodeClass.NodeIDToNode[x].visited = False
			NodeClass.NodeIDToNode[x].DistanceFromStart = -1
			NodeClass.NodeIDToNode[x].parent = None

	def visit(self):
		self.visited = True

	def setDistance(self,newDistance):
		self.DistanceFromStart = newDistance

	def setParent(self,parentNode):
		self.parent = parentNode

def ReadFile(filename):

	f2open = open(filename,"r",encoding="UTF-8-SIG")
	filecontent = f2open.readlines()
	f2open.close()

	names = filecontent[0].strip().split(",")
	for name in names:
		TramClass(name)

	for i in range(1,len(filecontent)):

		ithListOfGroups = filecontent[i].strip().split(",")
		for j in range(0,len(ithListOfGroups)):
			if ithListOfGroups[j]=="":
				continue

			CurrentListOfAliases = ithListOfGroups[j].strip().split("|")

			AliasGroupIndex = AliasClass.KeepUnionFind(CurrentListOfAliases)

			TramClass.AddAliasGroupIndexToRoute(names[j],AliasGroupIndex)

	Groups = set()
	for x in AliasClass.AliasToGroup:
		if x not in NodeClass.NodeIDToNode:
			NodeClass(AliasClass.AliasToGroup[x])

	for Tram in TramClass.TramsDict.values():
		for i in range(0,len(Tram.route)-1):
			FirstNode = NodeClass.NodeIDToNode[Tram.route[i]]
			SecondNode = NodeClass.NodeIDToNode[Tram.route[i+1]]
			NodeClass.make_neighbour(FirstNode,SecondNode)

def RouteBetween(start,finish):
	start.visit()

	if start==finish:
		return [start]

	neighbours=[node for node in start.neighbours if node.visited==False]

	if neighbours == []:
		return []


	for neighbour in neighbours:
		resp = RouteBetween(neighbour,finish)

		if not resp:
			continue
		return [start]+resp

def ShortestRouteBetween(start,finish):

	ToVisit = [start]
	start.DistanceFromStart = 0
	while ToVisit:
		current = ToVisit.pop(0)
		if current.visited == True:
			continue
		current.visit()
		ToVisit = ToVisit + [node for node in current.neighbours if node.visited == False]
		for node in current.neighbours:
			if node.DistanceFromStart == -1 or node.DistanceFromStart>current.DistanceFromStart+1:
				node.setDistance(current.DistanceFromStart+1)
				node.setParent(current)

		#print([x.ID for x in ToVisit])
	if finish.DistanceFromStart==-1:
		return []

	routeToReturn = []
	last = finish
	while last is not None:
		routeToReturn = [last] + routeToReturn
		last = last.parent

	return routeToReturn

def main():

	ReadFile("dataM2.csv")

	route = ShortestRouteBetween(NodeClass.NodeIDToNode[1],NodeClass.NodeIDToNode[2])
	print([(x.ID,x.DistanceFromStart) for x in route])
	NodeClass.reset()
	




if __name__ == "__main__":
	main()
