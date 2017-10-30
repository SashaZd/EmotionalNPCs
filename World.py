import simpy
import arrow
import random
from configs import *
from collections import defaultdict
import itertools

from Person import Person
from Organization import School



class World(object):		# the sim will run for 50 years by default
	"""docstring for World"""

	def __init__(self, until_year=40):
		super(World, self).__init__()
		
		# Populations 
		self.living_population = Person.living_population
		# self.deceased_population = []
		self.person_id = 0
		self.birthdays = None
		# Time 
		self.until_year=until_year

		self.setup_world()

	
	def setup_world(self):
		""" Setup initial locations, organizations, etc of the world """
		
	  	# currently a city, needs to be extended further
		self.locations = {key:{
			'school':[], 'university':[]
		} for key in LOCATIONS}

		# For every day of the week, link all currently running organizations that meet on that day
		# self.days_of_week = [key:set() for key in range(0)]

		# Make a list of all schools
		self.make_schools()
		# self.make_universities()

		self.settler_babies() 	# start with 100 people in the town as babies. No parents, inheritence.
								# Their initial interactions will form the basis for relationships

		# actions to perform on various days of week
		# self.days_of_week = defaultdict[list]


	def do_things(self, sim):
		born = []
		sim_date = arrow.get('%s-%s-%s'%(START_SIM_DATE[0],START_SIM_DATE[1],START_SIM_DATE[2]))
		
		while(True):
			sim_date = sim_date.replace(days=1)
			day, month = sim_date.day, sim_date.month
			weekday = sim_date.weekday() # returns day of the week, 0-6 0=Monday
			self.age_living_population(day, month)

			if weekday < 4: 
				self.go_to_school()



			# Do things here with some probability based on sim_date
			# if random.random() <= 0.01:
			# 	baby = Person()
			# 	self.birthdays = [day, month, baby]
			# 	born.append(baby)

			# if sim_date.month==12 and sim_date.day == 31: 
			# 	print "Year: ", sim_date.format('YYYY'), " | Children born: ", len(born)
			# 	self.living_population.extend(born)
			# 	born = []
			
			yield sim.timeout(1)

	def go_to_school(self):

		# Only return children who just turned old enough to start attending school - i.e. no school assigned yet
		# Assign these children to a currently existing school in their area
		for loc in [location for location in self.locations.keys()]:
			for school in self.locations[loc]['school']:
				for student in school.current_members: 
					student.simple_interaction(school.current_members)

	# Bad iterations!! Should have a link to the Organization.all or something and then iterate through that.
	# 	# ToDo: If school in area is full_capacity, then move family? 
	# 	# pass
	# 	pass
		


	def age_living_population(self, day, month):
		if hasattr(self, 'birthdays'):
			if (day, month) in self.birthdays.keys(): 
				for npc in self.birthdays[(day,month)]:
					npc.do_age()


	@property
	def birthdays(self):
		return self.__birthdays

	@birthdays.setter
	def birthdays(self, new_birth=None):
		if new_birth: 
			[day, month, baby] = new_birth
			if not hasattr(self, 'birthdays'): 
				self.__birthdays = defaultdict(list)
			
			self.__birthdays[(day, month)].append(baby)


	def settler_babies(self, num=100):
		# choose random birthdays for the first 100 people in the world
		# they will be parents with some probability for the next generation

		sim_date = arrow.get('%s-%s-%s'%(START_SIM_DATE[0],START_SIM_DATE[1],START_SIM_DATE[2]))
		seed_births = set()
		for day in itertools.islice(self.sample_wr(range(365)),num):
			birth = sim_date.replace(days=day)
			_year = random.choice(range(10))
			birthday = [birth.day, birth.month, birth.year-_year]
			self.make_baby(birthday)

		# # Currently the only babies are the settler ones, so increase their age
		# for baby in Person.living_population: 
		# 	baby.magic_age("SETTLERS")


	def make_baby(self, birthday=None, mother=None, father=None):
		if not birthday: 
			raise ValueError("Baby needs a birthday in World.make_baby()")
			return 

		baby = Person(self, birthday)
		self.birthdays = [birthday[0],birthday[1],baby]
		


	# @property
	# def schools(self):
	# 	schools = []
		# for loc in [location for location in self.locations.keys()]:
		# 	for school in self.locations[loc]['school']:
	# 			print school


	def make_schools(self):
		"""Create Schools in the world
		For every location in the world, add to the default schools at the location
		"""
		num_schools = random.choice(range(len(LOCATIONS), NUM_SCHOOLS_PER_LOCATION*len(LOCATIONS)))
		school_names = random.sample(SCHOOL_NAMES, num_schools)
		
		for each in range(num_schools): 
			school = School(school_names.pop())
			self.locations[school.location]['school'].append(school)
			


	# Sample with replacement
	def sample_wr(self, population, _choose=random.choice):
		while True: yield _choose(population)


	def simulate_time(self):
		start = arrow.get('2017-01-01T00:00:00')
		env = simpy.Environment()
		env.process(self.do_things(env))
		env.run(until=365*self.until_year)





