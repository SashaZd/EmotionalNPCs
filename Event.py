import itertools
from Person import Person
import random
from configs import * 
import names

class Event(object):
	"""parent class for all the Events
		Currently just has a date and a id associated. 
		Later can add the potential to create/allow new events based on rules? 
		Preconditions? Postconditions? 
	"""

	e_id = itertools.count().next

	def __init__(self, date, owner=None):
		super(Event, self).__init__()
		self.id = Event.e_id()
		self.date = date


	def set_owner(self, owner):
		self.owner = owner


	def add_to_journal(self, owner, message):
		owner.journal.append("%s - %s "%(self.date.format('DD-MM-YYYY'), message))
		
		

class Birth(Event):
	"""docstring for Birth"""
	def __init__(self, world, mother=None, father=None):
		super(Birth, self).__init__(world.current_date)
		self.baby = Person(world, self)
		self.baby.father = father
		self.baby.mother = mother
		self.gender = None
		parent_message = ""

		if mother: 
			self.baby.birth_location = mother.city
			self.baby.city = mother.city
			parent_message.append("My mother is %s."%(self.baby.mother.name))

		if father: 
			parent_message.append("My father is %s"%(self.baby.father.name))

		else:
			self.baby.birth_location = random.choice(LOCATIONS)
			self.baby.city = self.baby.birth_location


		self._set_baby_name()
		self.set_sexual_preference()
		self.set_inherited_attr()

		if not mother and not father: 
			parent_message = "I had no parents."

		# else: 
			# if mother: 
				
			# if father:
				

		self.add_to_journal(self.baby, "I was born in %s. %s"%(self.baby.birth_location, parent_message))
		
		if mother: 
			self.add_to_journal(mother, "Had child with %s. Decided to name baby, %s"%(self.baby.father.name, self.baby.name))
		if father: 
			self.add_to_journal(father, "Had child with %s. Decided to name baby, %s"%(self.baby.mother.name, self.baby.name))



	# Birthdate: if unknown, set to current date
	@property
	def birthdate(self):
		return self.baby.__birthdate

	@birthdate.setter
	def birthdate(self, birthdate=None):
		if hasattr(self, 'birthdate'):
			if birthdate[2] != self.baby.__birthdate[2]: # changing the year to age? 
				self.baby.__birthdate[2] = birthdate[2]
		elif birthdate: 
			self.baby.__birthdate = birthdate		# take the date from the simulation? 


	# Everything reg. the Name

	def _set_baby_name(self):
		self.first_name = None
		self.last_name = None

	# Last Name
	@property
	def last_name(self):
		return self.baby.last_name


	@last_name.setter
	def last_name(self, last_name=None):
		""" Initializing a last name
		If given a last name, assume marriage/birth/etc and assign it to the sim
		If there are no parents, choose random last name, otherwise take the last name of the parents
		Uses Trey Hunner's Random Name Generator: http://treyhunner.com/2013/02/random-name-generator/
		""" 
		if not hasattr(self.baby, 'last_name'): 
			if self.baby.father: 
				self.baby.last_name = self.baby.father.last_name
			elif self.baby.mother: 
				self.baby.last_name = self.baby.mother.last_name
			else:
				self.baby.last_name = names.get_last_name()

	# First Name
	@property
	def first_name(self):
		return self.baby.first_name

	@first_name.setter
	def first_name(self, first_name=None):
		""" Initializing a last name
		If no name from before, then assign a name from the random name generator 
		If changing your name, then add to known aliases
		Uses Trey Hunner's Random Name Generator: http://treyhunner.com/2013/02/random-name-generator/
		""" 
		# if not hasattr(self.baby, 'first_name'): 
		if not first_name: 
			self.baby.first_name = names.get_first_name(gender=self.baby.gender)
		else:
			self.baby.first_name = first_name
		


	# Everything reg. Gender
	@property
	def gender(self):
		return self.baby.gender

	@gender.setter
	def gender(self, gender=None):
		"""allows the gender to be set only during birth"""
		if not hasattr(self.baby, 'gender'): 
			self.baby.gender = random.choice(POSSIBLE_GENDERS)
		
		# 	self.baby.gender = self.baby.gender


	# Inherited attributes during birth
	# Includes physical attributes from the parents (if they exist) or random (if they don't)
	# In our case that could also include knowledge of topics/rules? Maybe introduce these at a later age? Unsure?
	# May need to define topics with age limits? On when they are discussed? 
	# Otherwise we may get 5yr olds debating the death penalty during kindergarten
	def set_inherited_attr(self):
		"""Inherited Physical Characteristics
		Setting inherited physical, or other characteristics
		"""
		pass


	def set_sexual_preference(self):
		"""Setting Sexual Preferences: Randomly at the moment
		Using the statistics from Wikipedia's Demographics of Sexual Orientation: https://en.wikipedia.org/wiki/Demographics_of_sexual_orientation
		Demographics from the United States used....
		Thought: Eventually, could change the statistics based on regional preferences? 
		"""
		chance = random.random()
		if chance <= 0.017: 
			self.baby.sexual_preference = 'homosexual'
		elif chance <= 0.035: 
			self.baby.sexual_preference = 'bisexual'
		else: 
			self.baby.sexual_preference = 'herosexual'



		
		

	








