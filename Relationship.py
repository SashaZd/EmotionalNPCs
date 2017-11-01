
from collections import defaultdict

class Relationship(object):
	"""docstring for Relationship"""
	def __init__(self, owner, other):
		super(Relationship, self).__init__()
		self.owner = owner
		self.other = other
		self.relationships = defaultdict(dict)
		# print "New Relationship: ", owner.id, other.id


	def update_relationship(self, relationship_type, by_charge=1):
		"""Charging the relationship
		Currently all relationship_types charge with a value of 365
		Every 365 times you interact with a person, the strength of your relationship goes up by one.
		""" 
		if relationship_type not in self.relationships.keys(): 
			self.relationships[relationship_type] = {
				'charge': 1, 
				'relationship': 1
			}

		else: 
			self.relationships[relationship_type]['charge'] += by_charge
			
			if self.relationships[relationship_type]['charge'] >= 365: 
				self.relationships[relationship_type]['relationship'] += int(self.relationships[relationship_type]['charge']/365)
				self.relationships[relationship_type]['charge'] = (self.relationships[relationship_type]['charge']%365)



	def __str__(self):
		rel_str = ""
		for rel_type, val in self.relationships.items(): 
			rel_str += "(%s) - %s\n"%(rel_type, val['relationship'])
		return rel_str
		# return """%s"""%(self.other.name, self.relationships)

	def __repr__(self):
		rel_str = ""
		for rel_type, val in self.relationships.items(): 
			rel_str += "(%s) - %s\n"%(rel_type, val['relationship'])
		return rel_str
		# return """Relationship: %s and %s
		# 	%s"""%(self.other.name, self.relationships)


		# self.where_they_first_met = owner.location  # true since 
		






