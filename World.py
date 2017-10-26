import simpy
import arrow
import random
from collections import defaultdict
from Person import Person


class World(object):		# the sim will run for 50 years by default
	"""docstring for World"""

	def __init__(self, until_year=5):
		super(World, self).__init__()
		
		# Populations 
		self.living_population = []
		self.deceased_population = []
		self.person_id = 0

		# Time 
		self.until_year=until_year


	def do_things(self, sim):
		born = []
		sim_date = arrow.get('1990-01-01T00:00:00')
		while(True):
			sim_date = sim_date.replace(days=1)

			# Do things here with some probability based on sim_date
			if random.random() <= 0.01:
				baby = Person()
				self.birthdays = [sim_date.day, sim_date.month, baby.name]
				born.append(baby)

			if sim_date.month==12 and sim_date.day == 31: 
				print "Year: ", sim_date.format('YYYY'), " | Children born: ", len(born)
				for child in born: 
					print child
				self.living_population.extend(born)
				born = []
			
			yield sim.timeout(1)


	@property
	def birthdays(self):
		return self.__birthdays

	@birthdays.setter
	def birthdays(self, new_birth):
		[day, month, baby] = new_birth
		if not hasattr(self, 'birthdays'): 
			self.__birthdays = defaultdict(list)
		
		self.__birthdays[(day, month)].append(baby)


	def simulate_time(self):
		start = arrow.get('2017-01-01T00:00:00')
		env = simpy.Environment()
		env.process(self.do_things(env))
		env.run(until=365*self.until_year)





