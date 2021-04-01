# tram consist of
# name, list of stops
# dictionary of trams
class Tram:

	TramsDict = {}

	def __init__(self,name):
		Tram.TramsDict[name] = self
		self.name = name
		self.route = []

	def AddIDOfGroupOfAliasesToRoute(self,groupofaliases):
		self.route.append(groupofaliases)

	@staticmethod
	def MakeIDOfGroupOfAliasesIDOfNodes():
		pass

class GroupOfAliases():

	GroupsOfAliasesAsList = []
	ID = 0

	def __init__(self,aliases):
		self.id = GroupOfAliases.ID
		self.aliases = set(aliases)
		GroupOfAliases.GroupsOfAliasesAsList.append(self)

		GroupOfAliases.ID += 1

	def HasAliasesInCommonWith(self,other):
		return len(self.aliases.intersection(other.aliases))

	def GroupUnion(self,other):
		self.aliases = self.aliases.union(other.aliases)
		return self

# Node consist of
# name, aliases, neighbours

class Node:

	AliasesDict = {}

	NodesDict = {}

	def __init__(self,id,aliases):
		self.id = id
		self.aliases = set(aliases)
		for alias in aliases:
			Node.AliasesDict[alias] = self

		Node.NodesDict[self.id] = self

def MergeAndReplace(i,j):
	GroupAtI = GroupOfAliases.GroupsOfAliasesAsList[i]
	GroupAtJ = GroupOfAliases.GroupsOfAliasesAsList[j]
	MergedGroup = GroupAtI.GroupUnion(GroupAtJ)

	GroupOfAliases.GroupsOfAliasesAsList[i] = MergedGroup
	GroupOfAliases.GroupsOfAliasesAsList[j] = MergedGroup


def CondenseAllGroupsOfAliases():
	GroupsOfAliasesAsList = GroupOfAliases.GroupsOfAliasesAsList

	print(len(GroupsOfAliasesAsList))

	for i in range(0,len(GroupsOfAliasesAsList)):
		GroupOfAliases1 = GroupsOfAliasesAsList[i]
		for j in range(1,len(GroupsOfAliasesAsList)):
			#print(f"{i}\t{j}")
			GroupOfAliases2 = GroupsOfAliasesAsList[j]
			if GroupOfAliases1.HasAliasesInCommonWith(GroupOfAliases2)==0:
				continue
			MergeAndReplace(i,j)

def AssignNodesToGroupsOfAliases():
	SetOfGroupsOfAliases = set(GroupOfAliases.GroupsOfAliasesAsList)
	for Group in SetOfGroupsOfAliases:
		Node(Group.id,Group.aliases)
	Tram.MakeIDOfGroupOfAliasesIDOfNodes()#Does Nothing

def ReadFile(filename):
	f2open = open(filename,"r",encoding="UTF-8-SIG")
	filecontent = f2open.readlines()
	#print(filecontent)
	f2open.close()
	names = filecontent[0].strip().split(",")
	for name in names:
		Tram(name)
	for i in range(1,len(filecontent)):
		ithListOfGroups = filecontent[i].strip().split(",")
		for j in range(0,len(ithListOfGroups)):
			CurrentListOfAliases = ithListOfGroups[j].strip().split("|")

			CurrentGroupOfAliases = GroupOfAliases(CurrentListOfAliases)
			Tram.TramsDict[names[j]].AddIDOfGroupOfAliasesToRoute(CurrentGroupOfAliases.ID)

	CondenseAllGroupsOfAliases()
	AssignNodesToGroupsOfAliases()


def main():
	ReadFile("dataM2.csv")

	print(len(Tram.TramsDict.values()))
	# for tram in Tram.TramsDict.values():
	# 	print(tram.name)

	print(len(Node.NodesDict.values()))
	# for node in Node.NodesDict.values():
	# 	print(node.id)

if __name__ == "__main__":
	main()
