import random
import names
from configs import *

class Person(object):
	"""docstring for Person"""
	def __init__(self, id):
		# super(Person, self).__init__()
		
		self.id = id		# person_id sent from the simulation
		self.age = 0		# increments every year 
		self.gender = random.choice(POSSIBLE_GENDERS)
		
		self.parents = None

		self.first_name = self.set_first_name() 
		self.last_name = self.set_last_name()

		self.alias = set()



	def set_first_name(self):
		""" Give random first name based on gender 
			Uses Trey Hunner's Random Name Generator: http://treyhunner.com/2013/02/random-name-generator/ 
		"""
		return names.get_first_name(gender=self.gender)


	def set_last_name(self, last_name=None):
		""" Initializing a last name
		If given a last name, assume marriage/birth/etc and assign it to the sim
		If there are no parents, choose random last name, otherwise take the last name of the parents
		Uses Trey Hunner's Random Name Generator: http://treyhunner.com/2013/02/random-name-generator/
		""" 
		if not last_name: 
			if not self.parents: 
				# If there aren't any parents, start a new family, choose random last name
				return names.get_last_name()
			else:
				# If the child has parents, then take the last name from the parents
				return self.parents[0].get_last_name()
		else:
			# Already have a previous last name, so add old name to aliases for this person
			if self.last_name: 
				self.alias.add(self.get_full_name())
			return last_name

	def get_full_name(self):
		return "%s %s"%(self.first_name, self.last_name)


	def __str__(self):
		person = """\n id: %s,\n age: %s,\n gender: %s,\n name: %s,\n parents: %s
			"""%(self.id, self.age, self.gender, self.get_full_name(), self.parents)
		return person





