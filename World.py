import simpy
import arrow
import random
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
		while(True):
			start = arrow.get('2015-01-01T00:00:00')
			sim_date = start.replace(days=sim.now)

			# Do things here with some probability based on sim_date
			if random.random() <= 0.01:
				born.append(Person())

			if sim_date.month==12 and sim_date.day == 31: 
				print "Year: ", sim_date.format('YYYY'), " | Children born: ", len(born)
				for child in born: 
					print child
				self.living_population.extend(born)
				born = []
			
			yield sim.timeout(1)


	def simulate_time(self):
		start = arrow.get('2017-01-01T00:00:00')
		env = simpy.Environment()
		env.process(self.do_things(env))
		env.run(until=365*self.until_year)





