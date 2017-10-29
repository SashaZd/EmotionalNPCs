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

		self.current_location = None
		self.prior_locations = []

		# Names and aliases for this person
		# Known aliases, in case of change of name to track family?
		self.aliases = set()
		self.last_name = None
		self.first_name = None

		self.sexually_active = False
		self.sexual_preference = self.set_sexual_preference()
		self.spouse = None

		self.age = 0		# increments every year 

		# Setting inherited physical attributes
		self.set_inherited_attr(mother, father)

		self.__class__.living_population.append(self)


	@property
	def age(self):
		return self.__age

	@age.setter
	def age(self, age):
		"""Aging the person a year at a time. 
		
		@property age will allow for changes in flags... 
		Eg. allowing for school, work, sexually active behaviour, etc
		"""
		if isinstance(age, int):
			self.__age = age

		# Check if age is old enough for sexual partners
		if not self.sexually_active and self.age > 18: 
			self.sexually_active = True

	def do_age(self):
		self.age += 1


 
	def set_inherited_attr(self, mother, father):
		"""Inherited Physical Characteristics
		Setting inherited physical, or other characteristics
		"""
		# if self.mother: 
		# 	self.current_location = self.mother.current_location
		pass


	@property
	def current_location(self):
		return self.__current_location

	@current_location.setter
	def current_location(self, new_location):
		if not hasattr(self, "current_location"):
			if self.mother: 
				self.__current_location = self.mother.current_location
			elif self.father: 
				self.__current_location = self.father.current_location
			else:
				self.__current_location = random.choice(LOCATIONS)
		
		elif new_location: 
			self.prior_locations.append(self.__current_location)
			self.__current_location = new_location


	def choose_sexual_partner(self):
		pass


	def set_sexual_preference(self):
		"""Setting Sexual Preferences: Randomly at the moment
		Using the statistics from Wikipedia's Demographics of Sexual Orientation: https://en.wikipedia.org/wiki/Demographics_of_sexual_orientation
		Demographics from the United States used....
		Thought: Eventually, could change the statistics based on regional preferences? 
		"""
		chance = random.random()
		if chance <= 0.017: 
			self.sexual_preference = 'homosexual'
		elif chance <= 0.035: 
			self.sexual_preference = 'bisexual'
		else: 
			self.sexual_preference = 'herosexual'



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










