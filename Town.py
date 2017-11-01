import random
from configs import *
from Organization import * 

class Town(object):
	"""docstring for Town"""
	t_id = itertools.count().next
	towns = []
	citizens = []

	def __init__(self, name, world):
		# super(Town, self).__init__()
		self.name = name
		self.world = world
		self.founding_date = self.world.current_date

		# Locations in the Town
		self.schools = []
		self.universities = []
		self.hospitals = []

		self.homes = {}    	# Every home in the town
							# occupied: True/False 

		self.add_hospital() 	# Need a hospital, or the babies won't be born?
		self.init_school_system()



	def init_school_system(self):
		"""Randomly generate school system. 
			Schools: For now, at least one school per location is generated
			Universities: Todo
		""" 
		for i in range(random.choice(range(1, 2*NUM_SCHOOLS_PER_LOCATION))):
			self.add_school()


	def add_school(self, school_name=None):
		if not school_name: 
			school_name = random.choice(SCHOOL_NAMES)
		school = School(school_name, self.name, self.world.current_date)
		self.schools.append(school)
		

	def add_hospital(self, hospital_name=None):
		if not hospital_name: 
			hospital_name = random.choice(HOSPITAL_NAMES)
		hospital = Hospital(hospital_name, self.name, self.world.current_date) 
		self.hospitals.append(hospital)


