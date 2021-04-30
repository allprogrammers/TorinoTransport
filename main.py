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

	def add_neighbour(neighbour):
		self.neighbours.add(neighbour)


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
		Groups.add(AliasClass.AliasToGroup[x])
	print(len(Groups))

def main():

	ReadFile("dataM2.csv")





if __name__ == "__main__":
	main()
