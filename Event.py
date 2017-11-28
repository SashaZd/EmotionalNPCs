import itertools
from Person import Person
import random
from configs import * 
import names

class Event(object):
	"""parent class for all the Events
		Currently just has a date and a id associated. 
		Later can add the potential to create/allow new events based on rules? 
		Preconditions? Postconditions? 
	"""

	e_id = itertools.count().next

	def __init__(self, date, owner=None):
		super(Event, self).__init__()
		self.id = Event.e_id()
		self.date = date


	def set_owner(self, owner):
		self.owner = owner


	def add_to_journal(self, owner, message):
		owner.journal.append("%s - %s "%(self.date.format('DD-MM-YYYY'), message))
				

class Birth(Event):
	"""docstring for Birth"""
	def __init__(self, world, mother=None, father=None):
		super(Birth, self).__init__(world.current_date)
		self.world = world
		self.baby = Person(world, self)
		self.baby.father = father
		self.baby.mother = mother
		self.date = self.world.current_date
		self.gender = None

		self._set_baby_name()
		self.set_sexual_preference()
		self.set_inherited_attr()

		parent_message = ""

		if mother: 
			self.baby.birth_location = mother.town
			self.baby.town = mother.town
			parent_message.append("My mother is %s."%(self.baby.mother.name))

		else:
			self.baby.birth_location = self.world.towns['Area 51']
			self.baby.town = self.world.towns['Area 51']
			# print self.baby.town

		if father: 
			parent_message.append("My father is %s"%(self.baby.father.name))
		
		self.baby.town.add_citizen(self.baby)


		

		if not mother and not father: 
			parent_message = "I had no parents."

		# else: 
			# if mother: 
				
			# if father:
				
		birth_journal_entry = "I was born in %s. %s"%(self.baby.birth_location, parent_message)
		self.add_to_journal(self.baby, birth_journal_entry)
		self.baby.events.append(self)
		
		if mother: 
			self.add_to_journal(mother, "Had child with %s. Decided to name baby, %s"%(self.baby.father.name, self.baby.name))
			self.mother.events.append(self)
		if father: 
			self.add_to_journal(father, "Had child with %s. Decided to name baby, %s"%(self.baby.mother.name, self.baby.name))
			self.father.events.append(self)



	# Birthdate: if unknown, set to current date
	@property
	def birthdate(self):
		return self.baby.birthdate

	@birthdate.setter
	def birthdate(self, birthdate=None):
		if hasattr(self, 'birthdate'):
			if birthdate != self.baby.birthdate: # changing the year to age? 
				self.baby.birthdate = birthdate
		elif birthdate: 
			self.baby.birthdate = birthdate		# take the date from the simulation? 

		self.baby.age = abs(self.baby.birthdate - self.world.current_date).days/365
		self.date = birthdate


	# Everything reg. the Name

	def _set_baby_name(self):
		self.first_name = None
		self.last_name = None

	# Last Name
	@property
	def last_name(self):
		return self.baby.last_name


	@last_name.setter
	def last_name(self, last_name=None):
		""" Initializing a last name
		If given a last name, assume marriage/birth/etc and assign it to the sim
		If there are no parents, choose random last name, otherwise take the last name of the parents
		Uses Trey Hunner's Random Name Generator: http://treyhunner.com/2013/02/random-name-generator/
		""" 
		if not hasattr(self.baby, 'last_name'): 
			if self.baby.father: 
				self.baby.last_name = self.baby.father.last_name
			elif self.baby.mother: 
				self.baby.last_name = self.baby.mother.last_name
			else:
				self.baby.last_name = names.get_last_name()


	# First Name
	@property
	def first_name(self):
		return self.baby.first_name

	@first_name.setter
	def first_name(self, first_name=None):
		""" Initializing a last name
		If no name from before, then assign a name from the random name generator 
		If changing your name, then add to known aliases
		Uses Trey Hunner's Random Name Generator: http://treyhunner.com/2013/02/random-name-generator/
		""" 
		# if not hasattr(self.baby, 'first_name'): 
		if not first_name: 
			self.baby.first_name = names.get_first_name(gender=self.baby.gender)
		else:
			self.baby.first_name = first_name
		


	# Everything reg. Gender
	@property
	def gender(self):
		return self.baby.gender

	@gender.setter
	def gender(self, gender=None):
		"""allows the gender to be set only during birth"""
		if not hasattr(self.baby, 'gender') or self.baby.gender == None: 
			self.baby.gender = random.choice(POSSIBLE_GENDERS)
		
		# 	self.baby.gender = self.baby.gender


	# Inherited attributes during birth
	# Includes physical attributes from the parents (if they exist) or random (if they don't)
	# In our case that could also include knowledge of topics/rules? Maybe introduce these at a later age? Unsure?
	# May need to define topics with age limits? On when they are discussed? 
	# Otherwise we may get 5yr olds debating the death penalty during kindergarten
	def set_inherited_attr(self):
		"""Inherited Physical Characteristics
		Setting inherited physical, or other characteristics
		"""
		pass


	def set_sexual_preference(self):
		"""Setting Sexual Preferences: Randomly at the moment
		Using the statistics from Wikipedia's Demographics of Sexual Orientation: https://en.wikipedia.org/wiki/Demographics_of_sexual_orientation
		Demographics from the United States used....
		Thought: Eventually, could change the statistics based on regional preferences? 
		"""
		chance = random.random()
		if chance <= 0.017: 
			self.baby.sexual_preference = 'homosexual'
		elif chance <= 0.035: 
			self.baby.sexual_preference = 'bisexual'
		else: 
			self.baby.sexual_preference = 'heterosexual'


class Marriage(Event):
	""" Marriage Event
		Marries two people, and changes their last names (sometimes) accordingly 
		Also adds a marriage event to the person's journal. 
		Can also decide on a child policy during the wedding? 
	""" 
	def __init__(self, date, person, significant_other):
		super(Marriage, self).__init__(date)
		self.person = person
		self.significant_other = significant_other
		self.marriage()
		self.change_last_name()
		self.children_from_this_marriage = []


	def marriage(self):
		"""Get married
		Again, this is an exception case since otherwise many social relationship factors are involved
		""" 
		self.person.update_relationship(self.significant_other, "Spouse")
		self.significant_other.update_relationship(self.person, "Spouse")

		p_journal_message = "Got married to %s."%(self.significant_other.name)
		self.add_to_journal(self.person, p_journal_message)
		s_journal_message = "Got married to %s."%(self.person.name)
		self.add_to_journal(self.significant_other, s_journal_message)
		
		self.person.spouse = self.significant_other
		self.significant_other.spouse = self.person


	def change_last_name(self):
		s_journal_message = ""
		p_journal_message = ""
		# Probability of changing last name
		if random.random() >= 0.295:
			if self.person.gender == 'male': 
				self.significant_other.last_name = self.person.last_name
				s_journal_message = "I took his last name. I'm now %s"%(self.significant_other.last_name)
			elif self.significant_other.gender == 'male': 
				self.person.last_name = self.significant_other.last_name
				p_journal_message = "I took his last name. I'm now %s"%(self.person.last_name)
			else:
				self.significant_other.last_name = self.person.last_name
				s_journal_message = "I took her last name. I'm now %s"%(self.significant_other.last_name)
			
		# This is probably not true. Need to check stats and rules?
		elif random.random() >= 0.295:
			couple = [self.person, self.significant_other]
			random.shuffle(couple)
			new_last_name = "%s-%s"%(couple[0].last_name,couple[1].last_name)
			self.person.last_name = new_last_name
			self.significant_other.last_name = new_last_name
			s_journal_message = "We hyphenated our names! I'm now %s"%(self.significant_other.last_name)
			p_journal_message = "We hyphenated our names! I'm now %s"%(self.person.last_name)
		
		else:
			s_journal_message = "We decided to keep our names."
			p_journal_message = "We decided to keep our names."

		self.add_to_journal(self.person, p_journal_message)
		self.add_to_journal(self.significant_other, s_journal_message)
		self.person.events.append(self)
		self.significant_other.events.append(self)


class TheBeginning(Event):
	"""The start of the world
		Settlers are generated in Area 51. They divide into couples (if at all), and 
		then relocate to another town.
	"""
	def __init__(self, world):
		super(TheBeginning, self).__init__(world.current_date)
		self.world = world
		print "Big Bang!"

		# Makes a seed population of settlers to populate the world with
		self.settler_babies(50)

		# Find partners - not based on affinity at the moment. Totally random
		# Consider it after effects of alien abduction 
		self.random_match_couples()


	def settler_babies(self, num=50):
		"""Initial seed population for the world
		@param int num
			Choose random birthdays for the first people in the world
			They will pair up and then migrate to other cities.
		""" 
		sim_date = self.world.current_date
		for day in itertools.islice(self.world.sample_wr(range(365)),num):
			birth = sim_date.replace(days=day)
			_year = 20 + random.choice(range(10))
			birthdate = sim_date.replace(years=-_year)
			born = Birth(self.world)

			# Change the birthdate of the baby by a few years since he/she is a settler and an adult
			born.birthdate = birthdate


	def random_match_couples(self):
		"""Maybe make settler couples based on some probability
			Unlike the rest of the cases, this is not based on initial interaction.
		"""
		
		while self.world.towns['Area 51'].citizens:
			person = self.world.towns['Area 51'].random_citizen

			matches = [match for match in self.world.towns['Area 51'].citizens if abs(match.age-person.age) <= 5]
			matches.remove(person)

			if person.sexual_preference == 'homosexual': 
				matches = [match for match in matches if match.gender == person.gender]
			elif person.sexual_preference == 'heterosexual': 
				matches = [match for match in matches if match.gender != person.gender]

			if matches and random.random() >= 0.452:
				significant_other = random.choice(matches)
				# choose wedding date?
				sim_date = self.world.current_date
				wedding_date = sim_date.replace(days=random.choice(range(365)))
				marriage = Marriage(wedding_date, person, significant_other)

				# print "Couple! %s and %s"%(person.name, significant_other.name)
				self.random_relocate(person, significant_other)

			else:
				self.random_relocate(person)


	def random_relocate(self, person, significant_other=None):
		"""Choose a random town to relocate to"""
		new_town = self.world.random_location
		
		# Change journal entry
		if not significant_other: 
			person.town.remove_citizen(person)
			new_town.add_citizen(person)
			journal_message = "Moving to %s. (singing) Alone again... naturally."%(new_town.name)
			self.add_to_journal(person, journal_message)
			# print person.name, journal_message

		else:
			house_num = new_town.find_unoccupied_home()
			# self.random_marriage(person, significant_other)
			# print "Moving person: ", person, significant_other, " to house: ", house_num
			person.town.remove_citizen(person)
			significant_other.town.remove_citizen(significant_other)
			new_town.add_citizen(person, house_num)
			new_town.add_citizen(significant_other, house_num)
			journal_message = "This place is spooky. Moving to a new town, %s."%(new_town.name)
			self.add_to_journal(person, journal_message)
			self.add_to_journal(significant_other, journal_message)









