from configs import *
import random


class Organization(object):
	"""docstring for Organization
	"""
	o_id = itertools.count().next
	current_organizations = []
	past_organizations = []

	def __init__(self, name=None):
		super(Organization, self).__init__()
		# self.arg = arg

		if name: 
			self.name = name
		else:
			self.assign_name()

		self.location = random.choice(LOCATIONS)  # Currently 4 locations are possible. 
		self.current_members = set()
		self.past_members = set()
		self.days_of_meet = [0,1,2,3,4]  # Python dates start on Monday=0
		self.terminate_date = None
		self.employee = []

		self.__class__.current_organizations.append(self)

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

	def __init__(self, name):
		super(School, self).__init__(name)
		
		self.type = 'school'
		
	def enroll_student(self, student):
		self.add_member(student)

	def unenroll_student(self, student):
		self.remove_member(student)
			

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
	def __init__(self,name):
		super(Club, self).__init__(name)
		pass