from configs import *
import random
import itertools
from Knowledge import Knowledge
from collections import defaultdict

class Organization(object):
	"""docstring for Organization
	"""
	o_id = itertools.count().next
	current_organizations = defaultdict(list)
	past_organizations = defaultdict(list)

	def __init__(self, name, type=None, location=None, founding_date=None):
		super(Organization, self).__init__()
		# self.arg = arg

		# if name: 
		# 	self.name = name
		# else:
		# 	self.assign_name()
		self.name = name
		self.type = type
		self.founding_date = founding_date
		self.terminate_date = None

		if location: 
			self.location = location
		else:
			self.location = random.choice(LOCATIONS)

		self.current_members = set()
		self.past_members = set()
		self.days_of_meet = [0,1,2,3,4]  # Python dates start on Monday=0
		
		# self.employees = []

		self.knowledge = Knowledge()
		self.__class__.current_organizations[self.type].append(self)

		"""
		TODO: leave and join?
		"""

	def assign_name(self,newname):
		self.name = newname


	def add_member(self, person):
		self.current_members.add(person)


	def remove_member(self, person):
		if person in self.current_members: 
			self.past_members.add(person)
			self.current_members.remove(person)


	def calculate_avg_opinion(self, topic):
		# if topic in self.topics_of_interest: 
		# 	# for member in self.current_members: 
		# 	# 	pass
		# 	print "To Do"

		# else:
		# 	print "No opinion"
		pass


	def __str__(self):
		return "%s"%(self.name)

	def __repr__(self):
		return "%s"%(self.name)

	def __unicode__(self):
		return "%s"%(self.name)

	""" TODO: add members to past_member when they leave"""


class School(Organization):
	"""Local schools
	Currently there's only 2 schools, can change that in the world later. 
	Allows for simulation of people interacting growing up. 
	"""

	def __init__(self, name, location=None, founding_date=None):
		super(School, self).__init__(name, 'school', location, founding_date)
		# self.type = 'school'
		self.subjects = {}

		# self.subjects = self.set_subjects_taught()

	def set_subjects_taught(self, topics):
		"""Subjects taught by this school
			Will be used to decide how much knowledge about a topic a person has
			Can be used to form opinions
		""" 
		topics_chosen = random.sample(topics, random.choice(range(4, len(topics))))
		for topic in topics_chosen: 
			self.knowledge.add_topic(topic)
		
		
	def enroll_student(self, student):
		self.add_member(student)


	def unenroll_student(self, student):
		self.remove_member(student)


	def all_members_simulate_interaction(self):
		# Updates relationship

		if len(self.current_members) > 1: 
			for student in self.current_members:
				student.simple_interaction(self.current_members, 'classmate_school')



	def teach_fact(self):
		fact = self.knowledge.get_random_fact()
		
		# Currently assuming that teachers don't already have opinions 
		if fact.opinion == None: 
			fact.generate_random_opinion()

		for student in self.current_members: 
			student.knowledge.gain_knowledge(fact)
			# print "Teaching %s: %s"%(student.name, fact)

			

class University(Organization):
	""" Grad schools
	"""
	def __init__(self,name):
		super(University, self).__init__(name)
		self.days_of_meet = [0,1,2,3,4,5]
		pass


class Company(Organization):

	""" Company
	"""
	def __init__(self,name):
		super(Company, self).__init__(name)
		pass


class Club(Organization):

	""" Interest Clubs
	"""
	def __init__(self, name, topics_of_interest=[]):
		super(Club, self).__init__(name)

		# Example: "sci-fi", "doctor who", "baking", etc
		self.topics_of_interest = topics_of_interest

		pass


class Hospital(Organization): 
	"""
		For babies to be born in 
	""" 
	def __init__(self, name, location, founding_date=None):
		super(Hospital, self).__init__(name, 'hospital', location, founding_date)
		pass




