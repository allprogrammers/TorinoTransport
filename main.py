# tram consist of
# name, list of stops
# dictionary of trams
class TramClass:

	TramsDict = {}

	def __init__(self,name):
		TramClass.TramsDict[name] = self
		self.name = name
		self.route = []

	def AddAliasGroupIndexToRoute(self,index):
		self.route.append(index)

	@staticmethod
	def MakeIDOfGroupOfAliasesIDOfNodes():
		pass

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
	def UpdateTramRoutes(ListOfGroups):

		First = ListOfGroups[0]
		for TramName in TramClass.TramsDict:
			for i in range(0,len(TramClass.TramsDict[TramName].route)):
				if TramClass.TramsDict[TramName].route[i] in ListOfGroups:
					TramClass.TramsDict[TramName].route[i] = First

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
			AliasClass.UpdateTramRoutes(ListOfFoundGroupIndex)
			IndexToReturn = FirstGroupIndex

		return IndexToReturn

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

			TramClass.TramsDict[names[j]].AddAliasGroupIndexToRoute(AliasGroupIndex)

def main():
	ReadFile("dataM2.csv")

	

if __name__ == "__main__":
	main()
