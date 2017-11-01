

# class Configs(object):
# 	"""docstring for Configs"""
# 	def __init__(self, arg):
# 		super(Configs, self).__init__()
# 		self.arg = arg
		


TOPICS = [
	# Politics 			- DEMOCRAT --> REPUBLICAN 
	# Death Penalty		- Pro ---> Anti 

	# HOMOSEXUALITY 	- PRO ---> ANTI 
	# VACCINATIONS 		- PRO ---> ANTI
	# Abortion			- PRO ---> ANTI 
	{'tag' : 'health',   'name' : 'vaccination'},   
	{'tag' : 'health',   'name' : 'abortion'},     
	{'tag' : 'politics', 'name' : 'death penalty'}  
]

STARTING_SOCIETIES = [
	{'democrat':0.2, 'vaccinations':0.2, 'abortion': None,'death penalty':0.9}, # Society #1
	{'democrat':0.3, 'vaccinations':0.8, 'abortion':0.2,'death penalty':0.1}, # Society #2
	{'democrat':0.9, 'vaccinations':0.5, 'abortion':0.9,'death penalty':0.4}  # Society #3
]

START_SIM_DATE = (1990,01,01)

POSSIBLE_GENDERS = [
	'male', 'female'
]

AGE_GROUP = {
	'YOUNG': 5,
	'ADULT': 21,
	'SETTLERS': 25
}

AGE_FIRST_SCHOOL = 5

LOCATIONS = [
	'Raleigh', 
	'Atlanta',
	'Pittsburgh', 
	'New York',
	'San Francisco'
]

NUM_SCHOOLS_PER_LOCATION = 3

SCHOOL_NAMES = [
	'Allington Primary School',
	'Amherst School',
	'The Anthony Roper Primary School',
	'Ashford Oaks Community Primary School',
	'Barham CofE Primary School',
	'Barming Primary School',
	'Barn End Centre',
	'Barton Junior School',
	'Bean Primary School',
	'Beauherne Community School',
	"Brunswick House Primary School",
	"Canterbury Road Primary School",
	"Canterbury St Peter's Methodist Primary School",
	"Capel Primary School",
	"Capel-le-Ferne Primary School",
	"Cecil Road Primary School",
	"Challenger Centre",
	"Chantry Primary School",
	"Cheriton Primary School",
	"Chevening St Botolph's CofE Primary School",
	"Chiddingstone CofE Primary School",
	"Chilham St Mary's CofE Primary School",
	"Chilton Primary School",
	"Colliers Green CofE Primary School",
	"Coxheath Primary School",
	"Cranbrook CofE Primary School"
	"Crockham Hill CofE Primary",
	"Culverstone Green Primary School",
	"Dame Janet Infant School",
	"Dame Janet Junior School",
	"Darenth Community Primary School",
	"The Discovery School",
	"Ditton CofE Junior School",
	"Downs View Infants School",
]


HOSPITAL_NAMES = [
	'Citrus Medical Center',
	'Clemency Medical Clinic',
	'Silver Birch Community Hospital',
	'Grand Mountain Hospital Center',
	'Golden Valley Hospital',
	'Fairbanks Clinic',
	'Horizon Medical Clinic',
	'Grand Mountain Community Hospital',
	'Featherfall Hospital Center',
	'Green Hill Hospital',
	'Pine Valley Hospital',
	'Sapphire Lake Medical Clinic',
	'Rosewood Medical Clinic',
	'Wellness Medical Clinic',
	'Pioneer Clinic',
	'Spring Forest Hospital',
	'Freeman Clinic',
	'Castle Hospital',
	'Tranquility Hospital',
	'Hill Crest Hospital Center',
	'Silver Pine Clinic',
	'Summer Springs Hospital',
	'Lakeside Clinic',
	'Fairmont Medical Center',
	'Progress Medical Clinic',
	'Oak Valley Community Hospital',
	'Rose Medical Center',
	'Mountain View General Hospital',
	'Silver Wing Hospital Center',
	'Griffin Hospital Center'
]



