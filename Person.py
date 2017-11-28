import random
import names
import itertools
from configs import *
from collections import defaultdict
from Relationship import Relationship

class Person(object):
	"""docstring for Person"""

	# Incremental ID for all persons of this class
	p_id = itertools.count().next
	living_population = []
	deceased_population = []


	def __init__(self, world, birth):
		# @param world = simulation object (currently world.. need to rename?)
		# @param birth = Birth event from the Events.py file 

		self.id = Person.p_id()		# person_id sent from the simulation
		self.journal = []			# journal tracking all events in this Sim's life
		self.world = world

		self.birthdate = None
		self.gender = None

		# Names and aliases for this person
		# Known aliases, in case of change of name during wedding, etc to track family?
		self.aliases = set()
		self.last_name = None
		self.first_name = None

		# Current home_town, and past_addresses_town track where the person has lived before
		# For instance, people may move to find a job, or go to school
		self.house_number = None
		self.town = None
		self.past_addresses = []

		# Location tracks the actual location of the user in the world during a timestep
		self.current_location = None
# 
		# Sexually active at the age 18 
		self.flag_sexually_active = False
		self.partner = None
		self.spouse = None

		# Stores a list of Relationship objects, per person interacted with
		# current_relationships = relationships currently in progress 
		# past_relationships = if the person stops meeting this person, then after a set time, we demote them
		# Future goal: consider how to renew past relationship? Need to track that, but future goal.
		self.current_relationships = {}
		self.past_relationships = {}

		# Academic details 
		# ToDo: Represent the knowledge or degree topic? If related to society topic it could 
		#  		represent an increase in the confidence of the topic 
		self.flag_activate_school = False
		self.school = None
		self.past_schools = []
		self.flag_activate_university = False
		self.university = None
		self.past_universities = None

		self.events = []

		# Age for the person 
		# age is set as a @property. If it changes, it triggers flags in the person.
		self.age = 0		# increments every year 

		self.__class__.living_population.append(self)

	
	##################################################
	# Aging and everything that comes with growing old
	##################################################

	def do_age(self):
		self.age += 1

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


		if not self.town or (self.town == self.world.towns['Area 51']):
			return

		# Check if age is old enough for sexual partners
		if not self.flag_sexually_active and self.age > 18: 
			self.flag_sexually_active = True

		if not self.flag_activate_school and self.age > 5: 
			self.enroll_in_school()

		if self.flag_activate_school and self.age > 17: 
			self.unenroll_from_school()


	##################################################
	# Everything to do with Academia - Schools and Universities 
	##################################################

	# Possibility of enrolling in school -- some may choose not to? 
	# ToDo: Change probability of enrollment occurring from 1 to some percentage chance
	# Future: Could change this per region based on real stats? 
	# ToDo: Need to move this to the events class? 
	def enroll_in_school(self):
		self.flag_activate_school = True

		# If there's a school
		if self.world.locations[self.city]['schools']:
			chosen_school = random.choice(self.world.locations[self.city]['schools'])
			chosen_school.enroll_student(self)
			self.current_school = chosen_school
		
		else: 
			print "%s district has no school to enroll in. Relocate?"%(self.city)


	def unenroll_from_school(self):
		self.flag_activate_school = False
		self.current_school.unenroll_student(self)
		self.past_schools.append(self.current_school)
		self.current_school = None



	##################################################
	# Everything to do with Addressses and Locations 
	##################################################
	
	# To Do
	def relocate_home(self, town=None, with_household=None):
		"""Relocation of Home
			Used to change the location of the Person's home 
			If the actual address changes - compare house_number and city only? 
			@param tuple address : (house_number, city)
			@param Person[] with_household : True (household moving with person) | False (moving out alone)
		""" 
		# if address != self.address: 
		# 	self.past_addresses.append(self.current_home)
		
		if self.town != town:
			town.find_unoccupied_home()



	# @property
	# def town(self):
	# 	# print "Getting town"
	# 	if not hasattr(self, 'town'):
	# 		self.__town = None
	# 	return self.__town
			


	# @town.setter
	# def town(self, town=None):
	# 	print "Setting town"
	# 	""" Initializing a last name
	# 	If given a last name, assume marriage/birth/etc and assign it to the sim
	# 	If there are no parents, choose random last name, otherwise take the last name of the parents
	# 	Uses Trey Hunner's Random Name Generator: http://treyhunner.com/2013/02/random-name-generator/
	# 	""" 
	# 	# if not hasattr(self, 'town'): 
	# 	self.__town = town

		# # Changing the last name
		# elif town and town != self.__town: 
		# 	self.aliases.add(self.name)
		# 	self.__town = town

		

		# else: 
		# 	print "Error! Use the relocate_home method to move independently or with household"

	
	##################################################
	# Everything to do with Names
	##################################################
	@property
	def name(self):
		return "%s %s"%(self.first_name, self.last_name)

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
		if not hasattr(self, 'last_name') and last_name: 
			self.__last_name = last_name

		# Changing the last name
		elif last_name and last_name != self.__last_name: 
			self.aliases.add(self.name)
			self.__last_name = last_name


	@property
	def first_name(self):
		return self.__first_name


	@first_name.setter
	def first_name(self, first_name=None):
		""" Changing existing first name
		If the person already has a name and is changing it, then add it to the aliases
		"""

		if not hasattr(self, 'first_name') and first_name: 
			self.__first_name = first_name

		elif first_name and first_name != self.first_name:
			self.aliases.add(self.name)
			self.__first_name = first_name


	##################################################
	# Relationships with other people 
	##################################################

	def simple_interaction(self, group, relationship_type):
		"""Power up relationship with a person""" 
		for person in group: 
			if person != self: 
				self.update_relationship(person, relationship_type)
			# if person.name not in self.current_relationships: 
			# 	self.current_relationships[person.name] = {
			# 	}
			# else:
			# 	self.current_relationships[person.name] += 1


	def update_relationship(self, other, relationship_type):
		if other in self.current_relationships.keys():
			relationship = self.current_relationships[other]

		# Don't have a relationship with this person
		# Creating a new relationship with this person
		else: 
			relationship = Relationship(self, other)
			self.current_relationships[other] = relationship
		
		relationship.update_relationship(relationship_type, 1)


	@property
	def spouse(self):
		return self.__spouse


	@spouse.setter
	def spouse(self, spouse=None):
		""" Changing existing first name
		If the person already has a name and is changing it, then add it to the aliases
		"""

		if not hasattr(self, 'spouse') and spouse: 
			self.__spouse = spouse

		elif spouse and spouse != self.spouse:
			self.__spouse = spouse
			print "some probability of having a baby"



	##################################################
	# Testing
	##################################################

	def who_is(self):
		# person = ("%s,"
		# 		"\n  id: %s,"
		# 		"\n  dob: %s,"
		# 		"\n  age: %s,"
		# 		"\n  gender: %s,"
		# 		"\n  mother: %s,"
		# 		"\n  father: %s")%(self.name, self.id, self.birthdate, self.age, self.gender, self.mother, self.father)
		# print person
		return self.__dict__


	def __str__(self):
		return "%s"%(self.name)

	def __repr__(self):
		return "%s"%(self.name)

	# def __unicode__(self):
	# 	return "%s"%(self.name)










