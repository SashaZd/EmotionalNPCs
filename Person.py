import random
import names
import itertools
from configs import *
from collections import defaultdict
from collections import Counter
import itertools


from Relationship import Relationship
from Knowledge import Knowledge
from Discussion import Discussion


# from Event import *

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

		self.birthdate = world.current_date # set in the birth event
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

		# Sexually active at the age 18 
		self.flag_sexually_active = False
		# self.partner = None
		self.spouse = None
		self.children = []

		# Stores a list of Relationship objects, per person interacted with
		# current_relationships = relationships currently in progress 
		# past_relationships = if the person stops meeting this person, then after a set time, we demote them
		# Future goal: consider how to renew past relationship? Need to track that, but future goal.
		self.current_relationships = {}
		self.past_relationships = {}

		# Academic details 
		# ToDo: Represent the knowledge or degree topic? If related to society topic it could 
		#  		represent an increase in the confidence of the topic 
		self.flag_education = False  # if the person is too old, or not interested in school, don't check
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

		# Knowledge: (fact numbers set) 
		# Eg. science: [1,4,19,20]
		self.knowledge = Knowledge()


	
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


		if self.town == self.world.towns['Area 51']:
			return

		# print "Otherwise here.... ", self.town
		# Check if age is old enough for sexual partners
		if not self.flag_sexually_active and self.age > 18: 
			self.flag_sexually_active = True

		if self.spouse and not self.pregnant and not self.spouse.pregnant: 
			self.consider_having_baby()

		# if self.pregnant and self.world.current_date >= self.conception_date: 
		# 	self.have_baby()

		# Education Loops
		if self.age > 5 and self.age <= 17:  # 17 because we've not simulated universities yet
			self.flag_education = True
		else:
			self.flag_education = False

		if self.flag_education: 
			if self.age > 5 and self.age <= 17: 
				self.enroll_in_school()

			if self.flag_activate_school and self.age > 17: 
				self.unenroll_from_school()
		
		

		# if self.spouse and self.gender=="female" and not self.pregnant: 
		# 	# homosexual couple, toss coin to see who gets pregnant? 
		# 	# can be changed later
		# 	if self.spouse.gender == "female" and not self.spouse.pregnant: 
		# 		# should you get pregnant 
		# 		if random.random() < 0.5: 
					
		# 				self.pregnant_in_marriage()
		# 	else: 


	##################################################
	# Everything to do with Marriage and Babies
	##################################################

	@property
	def pregnant(self):
		if self.gender == "female": 
			return self.__pregnant
		else: 
			return False

	@pregnant.setter
	def pregnant(self, pregnant):
		if self.gender == "female":
			self.__pregnant = pregnant

	def have_baby(self):
		old = len(self.children)
		from Event import Birth
		born = Birth(self.world, self, self.spouse)
		self.pregnant = False
		current_date = self.world.current_date

		self.world.conception_dates[(current_date.day, current_date.month)].remove(self)

		self.children.append(born.baby)
		born.baby.add_to_census()
		new = len(self.children)

		# born.birthdate = birthdate

	def get_pregnant(self):
		self.pregnant = True
		# print self.world.current_date, self, " is pregnant"

		conception_date = self.world.current_date 
		conception_date = conception_date.replace(days=270)
		self.world.conception_dates[(conception_date.day, conception_date.month)].append(self)

		journal_message = "Announcement - We're pregnant! ", self.name, self.spouse.name
		self.journal.append(journal_message)
		self.spouse.journal.append(journal_message)	
		
	def consider_having_baby(self):
		""" Some probability of having a baby 
		"""
		if self.children: 
			n_kids = len([child for child in self.children if self in child.parents and self.spouse in child.parents])
		else:
			n_kids = 0

		probability_of_a_child = 0.35 / (n_kids + 1)

		# print self, "Thinking about a baby", probability_of_a_child

		# Decided to have a child
		if random.random() < probability_of_a_child: 
			if self.gender == "female":
				self.get_pregnant()

			elif self.spouse.gender == "female":
				self.spouse.get_pregnant()
			
			else:
				print "Want to adopt, but no such feature in game yet"

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
		if self.town.schools:
			chosen_school = random.choice(self.town.schools)
			chosen_school.enroll_student(self)
			self.current_school = chosen_school
		
		else: 
			print "%s district has no school to enroll in. Relocate?"%(self.town)

	def unenroll_from_school(self):
		self.flag_activate_school = False
		self.current_school.unenroll_student(self)
		self.past_schools.append(self.current_school)
		self.current_school = None


	##################################################
	# Everything to do with Addressses and Locations 
	##################################################
	
	# To Do
	def relocate_home(self, town=None, house_number=None, with_household=[]):
		"""Relocation of Home
			Used to change the location of the Person's home 
			If the actual address changes - compare house_number and city only? 
			@param tuple address : (house_number, city)
			@param Person[] with_household : True (household moving with person) | False (moving out alone)
		""" 

		# If moving to another house in the same town
		# if town == self.town and house_number != self.house_number: 
		# 	clear


		# self.past_addresses.append("%s, %s"%(self.house_number, self.town.name))

		# if address != self.address: 
		# 	self.past_addresses.append(self.current_home)
		
		# if self.town != town:
		# 	town.find_unoccupied_home()

		pass



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
		
		group_to_interact_with = [person for person in group if person != self]

		for person in group_to_interact_with: 
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


	def initiate_group_discussion(self, group):

		if random.random() < 0.05:
			count = Counter(list(itertools.chain.from_iterable([person.knowledge.facts.keys() for person in group])))

			# What facts are the most common
			common_max = max(count.values())
			(chosen_topic_of_discussion, frequency) = random.choice([fact for fact in count.most_common(common_max)])
			# print "Discussion of %s: Known to %s/%s people"%(chosen_topic_of_discussion, frequency, len(group))

			group_opinions = []
			for person in group: 
				if chosen_topic_of_discussion in person.knowledge.facts:
					group_opinions.append({
						'person': person, 
						'opinion': person.knowledge.facts[chosen_topic_of_discussion].get_opinion()
					})

			discussion = Discussion(group_opinions)

			# Randomly simulate the duration of the conversation. 
			# The longer the duration, the more the opinions and attitudes of the group may change 
			discussion_duration = random.randint(1,10)

			for minute in range(discussion_duration):
				discussion.discuss()

			for talker in discussion.group: 
				conversationalists = [person.name for person in group if( (person.id != talker['person'].id) and (person.name != talker['person'].name))]
				if len(conversationalists) > 1: 
					talkers = ''.join(conversationalists[:-1]), "and", conversationalists[-1]
				else:
					talkers = ''.join(conversationalists)

				journal_message = "I met %s. We discussed %s for %s minutes."%(''.join(talkers), chosen_topic_of_discussion, discussion_duration)
				person.journal.append(journal_message)
				person = talker['person']
				opinions = talker['opinion']
				changed_mind = person.knowledge.facts[chosen_topic_of_discussion].update_opinion_after_discussion(opinions)

				if changed_mind: 
					journal_message = "I changed my opinions about %s after the discussion."%(chosen_topic_of_discussion)
					person.journal.append(journal_message)
					print "For Demo check: ", person.census_index-1, person.name, chosen_topic_of_discussion


	
	##################################################
	# Opinions and Attitudes
	##################################################

	# def add_fact_to_knowledge(self, fact):
	# 	if fact not in self.knowledge.


	# def update_personal_representation_for_topic(self, topic):
	# 	tot_num_facts = len(self.knowledge[topic]['facts'])
	# 	avg_attitudes = sum([fact['attitude'] for fact in self.knowledge[topic]['facts']])/tot_num_facts
	# 	avg_opinions = sum([fact['opinion'] for fact in self.knowledge[topic]['facts']])/tot_num_facts

	# 	self.knowledge[topic]['representative_opinion'] = round(avg_opinions,2)
	# 	self.knowledge[topic]['representative_attitude'] = round(avg_attitudes,2)
	# 	self.knowledge[topic]['representative_unc'] = round(abs(avg_opinions - avg_attitudes),2)


	# def add_opinion_and_attitude(self, topic, fact, opinion_and_attitude):
	# 	if topic not in self.knowledge: 
	# 		self.knowledge[topic] = {
	# 			'facts': [],
	# 			'representative_opinion': None,
	# 			'representative_attitude': None,
	# 			'representative_unc': None
	# 		}

	# 	self.knowledge[topic]['facts'].append(opinion_and_attitude)
	# 	self.update_personal_representation_for_topic(topic)

		# Example -- 
		# 'democrat': {
		# 	'democrat_0': {
		# 		'attitude': -0.42,
		# 		'opinion': -0.81,
		# 		'pri_thr': 0.5,
		# 		'pub_thr': 0.6,
		# 		'unc': 0.39
		# 	}
	 	# }
		# self.knowledge[topic] = {
		# 	'individual_facts' 
		# }
		# [fact] = opinion_and_attitude
		



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

	def add_to_census(self):
		self.__class__.living_population.append(self)
		self.census_index = len(self.__class__.living_population)
		self.world.birthdays = [self.birthdate.day, self.birthdate.month, self]


	def __str__(self):
		return "%s"%(self.name)

	def __repr__(self):
		return "%s"%(self.name)

	# def __unicode__(self):
	# 	return "%s"%(self.name)










