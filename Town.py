import random
from configs import *
from Organization import * 
from Event import *
from collections import defaultdict

class Town(object):
	"""docstring for Town"""
	t_id = itertools.count().next
	# citizens = []
	

	def __init__(self, name, world):
		# super(Town, self).__init__()
		self.name = name
		self.world = world
		self.founding_date = self.world.current_date
		# self.current_date = self.world.current_date

		# Locations in the Town
		self.schools = []
		self.universities = []
		self.hospitals = []
		self.citizens = []
		

		# Every home in the town
		# { house_num(int) : {occupied: True/False, family_name: String}}
		# build_home constructs a new home when needed, and returns it 
		self.build_home = itertools.count().next
		self.homes = defaultdict(dict)

		# If this is Area 51, then set up initial settler population here. 
		# People will relocate from this location to other towns based on demand for schools, etc 
		# If they die (or are kidnapped by aliens) they move back here.
		if self.name == "Area 51": 
			pass

		else: 
			self.add_hospital() 	# Need a hospital, or the babies won't be born?
			self.init_school_system()


		# self.world.towns[self.name] = self


	@property
	def current_date(self):
		return self.world.current_date

	@current_date.setter
	def current_date(self, value=None):
		# if hasattr(self, 'current_date')
		return self.world.current_date


	#########################

	def find_unoccupied_home(self):
		"""Find home to relocate to
		If there are no unoccupied homes in town, build one
		For new families moving into town, or children moving out of parent's homes, etc
		Todo: Don't build if town population limits have been reached? Very stretchy goal
		""" 
		empty_homes = [house_num for (house_num, occupation_details) in self.homes.items() if occupation_details['occupied']==False]

		# If there aren't any empty homes, build one
		if not empty_homes: 
			house_num = self.build_home()
			self.homes[house_num] = {'occupied':False, 'family':None}
		else: 
			house_num = random.choice(empty_homes)

		return house_num


	def add_citizen(self, person, house_num=None):
		"""A new citizen moves into this town
		Maybe for a job/school? 
		""" 
		# ToDo: Need to add birthdays for the person into the town instead of the world
		if not house_num: 
			house_num = self.find_unoccupied_home()

		self.citizens.append(person)
		self.homes[house_num]['occupied'] = True
		self.homes[house_num]['family'] = person.last_name


	def remove_citizen(self, person):
		# Move them out of the house so it's available for other people

		if self.name != "Area 51":
			self.homes[person.house_num]['occupied'] = False
			self.homes[person.house_num]['family'] = None
		self.citizens.remove(person)


	#################


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


	@property
	def random_citizen(self):
		return random.choice(self.citizens)


	##################################################
	# If the town is Area 51
	##################################################

	def area_51_setup(self):
		if self.name != "Area 51": 
			raise ValueError("There is only one Area 51")
			return 

		start = TheBeginning(self.world)


	










