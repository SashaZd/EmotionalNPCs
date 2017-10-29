import random
import names
import itertools
from configs import *

class Person(object):
	"""docstring for Person"""

	# Incremental ID for all persons of this class
	p_id = itertools.count().next
	living_population = []
	deceased_population = []

	def __init__(self, birthdate=None, mother=None, father=None):
		# @param birthdate = (day, month, year)
		# @param Person mother: The birth mother
		# @param Person father: The birth father
		
		self.id = Person.p_id()		# person_id sent from the simulation
		self.gender = None

		# Init properties that change based on the birth of the character from the simulation
		self.mother = mother 
		self.father = father 
		self.birthdate = birthdate 		# Need to add the birth month/day to the world sim to increment age

		self.age = 0		# increments every year 

		# Names and aliases for this person
		# Known aliases, in case of change of name to track family?
		self.aliases = set()
		self.last_name = None
		self.first_name = None

		self.spouse = None

		# Setting inherited physical attributes
		self.set_inherited_physical_attr(mother, father)

		self.__class__.living_population.append(self)


	def do_age(self):
		self.age += 1


	@property
	def gender(self):
		return self.__gender

	@gender.setter
	def gender(self, gender=None):
		"""allows the gender to be set only during birth"""
		if not hasattr(self, 'gender'): 
			self.__gender = random.choice(POSSIBLE_GENDERS)
		else:
			self.__gender = self.__gender


	# Setting the mother
	@property
	def mother(self):
		return self.__mother

	@mother.setter
	def mother(self, mother):
		if hasattr(self, 'mother') and mother: 
		# if not self.__mother and mother: 
			self.__mother = mother
		else: 
			self.__mother = None


	# Setting the father
	@property
	def father(self):
		return self.__father

	@father.setter
	def father(self, father):
		if hasattr(self, 'father') and father: 
		# if not self.__father and father: 
			self.__father = father
		else: 
			self.__father = None


	# Birthdate: if unknown, set to current date
	@property
	def birthdate(self):
		return self.__birthdate

	@birthdate.setter
	def birthdate(self, birthdate=None):
		if hasattr(self, 'birthdate'):
			if birthdate[2] != self.__birthdate[2]: # changing the year to age? 
				self.__birthdate[2] = birthdate[2]
		elif birthdate: 
			self.__birthdate = birthdate		# take the date from the simulation? 
		

	def magic_age(self, age):
		# In case we're introducing a new character of advanced age
		# Could also work for adoption? Not sure? 
		if age in AGE_GROUP.keys():
			new_age = AGE_GROUP[age]

		# Otherwise, the person's been provided with an age, change birthdate accordingly
		elif isinstance(age, int):
			new_age = age 
		
		diff_years = new_age - self.age 
		self.age = new_age
		self.birthdate = [self.birthdate[0], self.birthdate[2], self.birthdate[2]-diff_years]


	# Last Name
	@property
	def last_name(self):
		return self.__last_name

	@last_name.setter
	def last_name(self, last_name=None):
		""" Initializing a last name
		If given a last name, assume marriage/birth/etc and assign it to the sim
		If there are no parents, choose random last name, otherwise take the last name of the parents
		Uses Trey Hunner's Random Name Generator: http://treyhunner.com/2013/02/random-name-generator/
		""" 
		
		if not hasattr(self, 'last_name'): 
			if self.father: 
				self.__last_name = self.father.last_name
			elif self.mother: 
				self.__last_name = self.mother.last_name
			else:
				self.__last_name = names.get_last_name()
		
		# Changing the last name
		elif last_name != self.__last_name: 
			self.aliases.add(self.get_full_name())
			self.__last_name = last_name



	# First Name
	@property
	def first_name(self):
		return self.__first_name

	@first_name.setter
	def first_name(self, first_name=None):
		""" Initializing a last name
		If no name from before, then assign a name from the random name generator 
		If changing your name, then add to known aliases
		Uses Trey Hunner's Random Name Generator: http://treyhunner.com/2013/02/random-name-generator/
		""" 
		if not hasattr(self, 'first_name'): 
			self.__first_name = names.get_first_name(gender=self.gender)
		
		# Changing the first name, add to known aliases
		elif first_name != self.__first_name: 
			self.aliases.add(self.get_full_name())
			self.__first_name = first_name


	def set_first_name(self, first_name=None):
		""" Give random first name based on gender 
			Uses Trey Hunner's Random Name Generator: http://treyhunner.com/2013/02/random-name-generator/ 
		"""
		# If the person already has a name and is changing it, then add it to the aliases
		if first_name: 
			if self.first_name: 
				self.aliases.add(self.get_full_name())
			self.first_name = first_name

		else:
			self.first_name = names.get_first_name(gender=self.gender)


	# Returns the full name
	@property
	def name(self):
		return "%s %s"%(self.__first_name, self.__last_name)


	# Setting inherited physical characteristics
	def set_inherited_physical_attr(self, mother, father):
		pass


	# Testing
	def get_bio(self):
		person = ("%s,"
				"\n  id: %s,"
				"\n  dob: %s,"
				"\n  age: %s,"
				"\n  gender: %s,"
				"\n  mother: %s,"
				"\n  father: %s")%(self.name, self.id, self.birthdate, self.age, self.gender, self.mother, self.father)
		print person


	def __str__(self):
		return "%s"%(self.name)

	def __repr__(self):
		return "%s"%(self.name)

	def __unicode__(self):
		return "%s"%(self.name)







