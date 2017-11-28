import simpy
import arrow
import random
from configs import *
from collections import defaultdict
import itertools

from Person import Person
from Organization import *
from Event import *
from Town import *
from Knowledge import *


class World(object):		# the sim will run for 50 years by default
	"""docstring for World"""
	current_date = arrow.get('%s-%s-%s'%(START_SIM_DATE[0],START_SIM_DATE[1],START_SIM_DATE[2]))

	def __init__(self, until_year=10):
		super(World, self).__init__()
		
		# Populations 
		self.living_population = Person.living_population
		self.organizations = Organization.current_organizations
		# self.deceased_population = []
		self.person_id = 0
		self.birthdays = None
		self.conception_dates = defaultdict(list)
		# Time 
		self.until_year=until_year

		self.towns = {}
		self.setup_world()

	
	def setup_world(self):
		""" Setup initial locations, organizations, etc of the world """
		
		# # currently a city, needs to be extended further
		# self.locations = {key:{
		# 	'schools':[], 'universities':[], 'hospitals':[]
		# } for key in LOCATIONS}

		# Citizens will be compulsarily affiliated with a geographic location
		# Other groups are optional. But if you leave one location, you must move to another
		for location_name in LOCATIONS: 
			town = Town(location_name, self)
			self.towns[location_name] = town


		# Area 51 - Will be the default town
		# If a person leaves the simulation entirely (eg. dies, or gets kidnapped by aliens, 
		# then we move them to Area 51)
		self.towns["Area 51"] = Town("Area 51", self)
		self.towns["Area 51"].area_51_setup()

		self.initilize_knowledge()

		


	def do_things(self):
		born = []
		while True: # self.env.now <= self.until_year:
			World.current_date = World.current_date.replace(days=1)
			day, month = World.current_date.day, World.current_date.month
			weekday = World.current_date.weekday() # returns day of the week, 0-6 0=Monday

			self.age_living_population(day, month)
			self.conceive_babies(day, month)

			if weekday < 4: 
				self.go_to_school()

			yield self.env.timeout(1)


	def conceive_babies(self, day, month):
		if (day,month) in self.conception_dates:
			for mother in self.conception_dates[(day,month)]: 
				mother.have_baby()


	def go_to_school(self):
		for school in self.organizations['school']:
			for student in school.current_members: 
				student.simple_interaction(school.current_members, 'classmate_school')

		# for org in self.organizations:
		# 	if org.type == 'school': 
				# for student in org.current_members: 
				# 	student.simple_interaction(org.current_members, 'classmate_school')


		# Only return children who just turned old enough to start attending school - i.e. no school assigned yet
		# Assign these children to a currently existing school in their area
		# for loc in self.locations.keys():
		#     for school in self.locations[loc]['school']:
		#         for student in school.current_members: 
		#             student.simple_interaction(school.current_members)

		# pass
		


	# Bad iterations!! Should have a link to the Organization.all or something and then iterate through that.
	# 	# ToDo: If school in area is full_capacity, then move family? 
	# 	# pass
	# 	pass
		
	def age_living_population(self, day, month):
		if hasattr(self, 'birthdays'):
			if (day, month) in self.birthdays.keys(): 
				# print "Aging: ", len(self.birthdays[(day,month)]), " children"
				for npc in self.birthdays[(day,month)]:
					npc.do_age()


	@property
	def birthdays(self):
		# if not hasattr(self, 'birthdays'): 
		# 	self.__birthdays = defaultdict(list)
		return self.__birthdays


	@birthdays.setter
	def birthdays(self, new_birth=None):
		if new_birth: 
			[day, month, baby] = new_birth
			if not hasattr(self, 'birthdays'): 
				self.__birthdays = defaultdict(list)
			
			self.__birthdays[(day, month)].append(baby)


	
		


	# @property
	# def schools(self):
	# 	schools = []
		# for loc in [location for location in self.locations.keys()]:
		# 	for school in self.locations[loc]['school']:
	# 			print school

	@property
	def random_location(self):
		return self.towns[random.choice(LOCATIONS)]


	def initilize_knowledge(self):
		self.knowledge = Knowledge()


	# Sample with replacement
	def sample_wr(self, population, _choose=random.choice):
		while True: yield _choose(population)


	def simulate_time(self):

		# until = 365*self.until_year
		# while until > 0: 
		# 	self.do_things()
		# 	until -= 1
		print "Simulating %s years"%(self.until_year)
		self.env = simpy.Environment()
		self.env.process(self.do_things())
		self.env.run(until=365*self.until_year) 


	





