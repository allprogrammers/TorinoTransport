import networkx as nx

# tram consist of
# name, list of stops
# dictionary of trams
class TramClass:

	TramsDict = {}

	def __init__(self,name):
		TramClass.TramsDict[name] = self
		self.name = name
		self.route = []
		self.timings = []

	@staticmethod
	def AddAliasGroupIndexToRoute(name,index):
		TramClass.TramsDict[name].route.append(index)

	@staticmethod
	def AddTimeToTimings(name,time):
		TramClass.TramsDict[name].timings.append(time)

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

def ReadFile(NodeFile,TimingFile,outputfile):

	f2open = open(NodeFile,"r",encoding="UTF-8-SIG")
	NodeContent = f2open.readlines()
	f2open.close()
	names = NodeContent[0].strip().split(",")

	f2open = open(TimingFile,"r",encoding="UTF-8-SIG")
	TimingContent = f2open.readlines()
	f2open.close()

	for name in names:
		TramClass(name)

	for i in range(1,len(NodeContent)):

		ithListOfGroups = NodeContent[i].strip().split(",")
		ithListOfTimes = TimingContent[i].strip().split(",")
		for j in range(0,len(ithListOfGroups)):
			if ithListOfGroups[j]=="":
				continue

			CurrentListOfAliases = ithListOfGroups[j].strip().split("|")

			AliasGroupIndex = AliasClass.KeepUnionFind(CurrentListOfAliases)

			TramClass.AddAliasGroupIndexToRoute(names[j],AliasGroupIndex)
			TramClass.AddTimeToTimings(names[j],int(ithListOfTimes[j]))


	Groups = set()
	for x in AliasClass.AliasToGroup:
		if x not in NodeClass.NodeIDToNode:
			NodeClass(AliasClass.AliasToGroup[x])

	outputString = ""
	GroupIds = AliasClass.AliasToGroup.values()
	GroupIDToAliases = {}
	for alias in AliasClass.AliasToGroup:
		if AliasClass.AliasToGroup[alias] not in GroupIDToAliases:
			GroupIDToAliases[AliasClass.AliasToGroup[alias]]=[]
		GroupIDToAliases[AliasClass.AliasToGroup[alias]].append(alias)

	# for key in GroupIDToAliases:
	# 	outputString += f"{key},{[x for x in GroupIDToAliases[key]]}\n"
	#
	# Afile = open(aliasfilename,"w")
	# Afile.write(outputString)
	# Afile.close()

	G = nx.Graph()
	G.add_nodes_from(NodeClass.NodeIDToNode.values())
	for Tram in TramClass.TramsDict.values():
		for i in range(0,len(Tram.route)-1):
			FirstNode = NodeClass.NodeIDToNode[Tram.route[i]]
			SecondNode = NodeClass.NodeIDToNode[Tram.route[i+1]]
			if G.has_edge(FirstNode,SecondNode) and G[FirstNode][SecondNode]['weight']>Tram.timings[i+1]:
				continue
			else:
				G.add_edge(FirstNode,SecondNode,weight=Tram.timings[i+1])

	resp = nx.betweenness_centrality(G)
	output = ""
	for k in resp:
		out1 = ""
		for als in GroupIDToAliases[k.ID]:
			out1 += als+"|"
		out1 = out1[:-1]
		output += out1 + f",{resp[k]}\n"
	outputfile = open(outputfile,"w")
	outputfile.write(output)
	outputfile.close()


def main():

	ReadFile("trams.csv","alltimings.csv","outTimingM2.csv")
	return


if __name__ == "__main__":
	main()
