from configs import *
import random


class Organization(object):
	"""docstring for Organization
	"""

	def __init__(self, name=None):
		super(Organization, self).__init__()
		# self.arg = arg

		if name: 
			self.name = name
		else:
			self.assign_name()

		self.location = random.choice(LOCATIONS)  # Currently 4 locations are possible. 
		self.current_member = []
		self.past_member = []
		self.days_of_meet = [1,2,3,4,5]
		self.employee = []
		"""
		TODO: leave and join?
		"""

	def __str__(self):
		return self.name

	def assign_name(self,newname):
		self.name = newname

	def add_member(self,person):
		self.current_member.append(person)

	""" TODO: add members to past_member when they leave"""


class School(Organization):
	"""Local schools
	Currently there's only 2 schools, can change that in the world later. 
	Allows for simulation of people interacting growing up. 
	"""

	def __init__(self, name):
		super(School, self).__init__(name)
		# self.name = None
		pass
			

class GradSchool(Organization):

	""" Grad schools
	"""
	def __init__(self,name):
		super(GradSchool, self).__init__(name)
		self.days_of_meet = [1,2,3,4,5,6,7]
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