import random
import names
from configs import *

class Person(object):
	"""docstring for Person"""
	def __init__(self, birth=None):
		# super(Person, self).__init__()
		
		self.id = id		# person_id sent from the simulation
		self.gender = None

		# Init properties that change based on the birth of the character from the simulation
		self.mother = birth 
		self.father = birth 
		self.age = 0		# increments every year 
		self.birthday = birth
		self.last_name = None
		self.first_name = None

		# Known aliases, in case of change of name to track family?
		self.aliases = set()


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
	def mother(self, birth=None):
		if birth: 
			self.__mother = birth.mother 
		else: 
			self.__mother = None


	# Setting the father
	@property
	def father(self):
		return self.__father

	@father.setter
	def father(self, birth=None):
		if birth: 
			self.__father = birth.father 
		else: 
			self.__father = None


	# Birthday: if unknown, set to current date
	@property
	def birthdate(self):
		return self.__birthdate

	@birthdate.setter
	def birthdate(self, birth=None, stage=None):
		if birth: 
			self.__birthdate = birth.birthdate 		# take the date from the simulation? 
		else: 
			self.__birthdate = None

		# In case we're introducing a new character of advanced age
		# Could also work for adoption? Not sure? 
		if stage == "Adult": 
			self.age = 21
			self.__birthdate.replace(days=-365*AGE['ADULT'])
		elif stage == "Young": 
			self.age = 5
			self.__birthdate.replace(days=-365*AGE['YOUNG'])


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


	# Testing
	def __str__(self):
		return self.name
		# person = """\n id: %s,\n age: %s,\n gender: %s,\n name: %s,\n mother: %s,\n father: %s
		# 	"""%(self.id, self.age, self.gender, self.name, self.mother, self.father)
		# return person








