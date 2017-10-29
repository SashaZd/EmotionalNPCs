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
		self.set_locations()
		self.settler_babies()


	def do_things(self, sim):
		born = []
		sim_date = arrow.get('%s-%s-%s'%(START_SIM_DATE[0],START_SIM_DATE[1],START_SIM_DATE[2]))
		while(True):
			sim_date = sim_date.replace(days=1)
			day, month = sim_date.day, sim_date.month

			self.age_living_population(day, month)

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


	def simulate_time(self):
		start = arrow.get('2017-01-01T00:00:00')
		env = simpy.Environment()
		env.process(self.do_things(env))
		env.run(until=365*self.until_year)


	def settler_babies(self, num=100):
		# choose random birthdays for the first 100 people in the world
		# they will be parents with some probability for the next generation

		sim_date = arrow.get('%s-%s-%s'%(START_SIM_DATE[0],START_SIM_DATE[1],START_SIM_DATE[2]))
		seed_births = set()
		for day in itertools.islice(self.sample_wr(range(365)),num):
			birth = sim_date.replace(days=day)
			_year = random.choice(range(3))
			birthday = [birth.day, birth.month, birth.year-_year]
			self.make_baby(birthday)

		# # Currently the only babies are the settler ones, so increase their age
		# for baby in Person.living_population: 
		# 	baby.magic_age("SETTLERS")


	def make_baby(self, birthday=None, mother=None, father=None):
		if not birthday: 
			raise ValueError("Baby needs a birthday in World.make_baby()")
			return 

		baby = Person(birthday)
		self.birthdays = [birthday[0],birthday[1],baby]


	def set_locations(self):
		self.locations = defaultdict(dict)
		self.make_schools()


	def make_schools(self):
		"""Create Schools in the world
		For every location in the world, add to the default schools at the location
		"""
		num_schools = random.choice(range(len(LOCATIONS), NUM_SCHOOLS_PER_LOCATION*len(LOCATIONS)))
		school_names = random.sample(SCHOOL_NAMES, num_schools)
		
		for each in range(num_schools): 
			school = School(school_names.pop())
			if 'school' in self.locations[school.location]:
				self.locations[school.location]['school'].append(school)
			else:
				self.locations[school.location]['school'] = [school]


	# Sample with replacement
	def sample_wr(self, population, _choose=random.choice):
	    while True: yield _choose(population)





