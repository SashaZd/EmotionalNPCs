
import random
from configs import TOPICS
# from configs import SCHOOL_SUBJECTS

# 'science': {'num_facts':20, 'tags':['vaccination', 'abortion', 'health']},

class Knowledge(object):
	"""docstring for Facts"""
	def __init__(self, topics, world=False):

		# if world: 
		# 	self.knowledge = self.initialize_world_knowledge()
		# else:
			self.knowledge = self.initialize_knowledge(topics)
		# self.associate_facts()


	# def inherit_avg_biases_opinion(self, opinions):
	# 	""" Inherit average opinions from the given list
	# 	Used for children to inherit the average of their parent's opinions on a topic 
	# 	"""
	# 	avg_attitude = [opinion['attitude'] for opinion in opinions]
	# 	return avg_attitude


	def create_random_opinion(self):
		""" Init Random Opinion to Start
		Different from having no opinion, 
			or inheriting the biases of the people who first introduce the topic to you  
			This is for facts that are introduced to you in school (perhaps) 
			or that you don't get from any other person (i.e. the internet when you're doing a random search)
		"""
		attitude = round(random.uniform(-1.0, 1.0), 2)
		opinion = round(random.uniform(attitude-0.5, attitude+0.5), 2)
		opinion = -1.0 if opinion < -1.0 else opinion
		opinion = 1.0 if opinion > 1.0 else opinion
		unc = round(abs(attitude - opinion), 2)
		pub_thr = 0.6
		pri_thr = round(random.uniform(0.0, 1.0), 2)

		return {
			'attitude': attitude,
			'opinion': opinion,
			'unc': unc,
			'pub_thr': pub_thr,
			'pri_thr': pri_thr,
		}

	# def function(self):
	# 	pass


	# def associate_facts(self):
	# 	for subject in SCHOOL_SUBJECTS: 
	# 		facts = random.shuffle(range(subject['num_facts']))
	# 		tags = subject['tags']

	##################################################
	# For the world knowledge - Everything that we know, including new facts/topics introduced
	##################################################

	def initialize_knowledge(self, topics):
		# topics = {}
		for topic_name, topic_information in topics.items():
			topic = Topic(topic_name, topic_information)

	# def initialize_knowledge(self):
	# 	for topic_name, topic_information in TOPICS.items():
	# 		topic = Topic(topic_name, topic_information)


		# for topic, information in TOPICS.items(): 
		# 	facts = ["%s_%s"%(topic, info) for info in range(information['num_facts'])]
		# 	topics[topic] = facts
		# return topics


# Config file
# 'democrat': {
	# 'tags': ['politics', 'social science'], 
	# 'num_facts': 15 },

class Topic(object):
	"""docstring for Topic"""
	def __init__(self, name, information=None):
		self.name = name
		self.tags = information['tags'] if 'tags' in information else []
		self.facts = ["%s_%s"%(topic, info) for info in range(information['num_facts'])] if 'num_facts' in information else []


class Fact(object):
	"""docstring for Fact"""
	def __init__(self, name, opinion=None):
		super(Fact, self).__init__()
		self.name = name
		self.opinion = opinion
		



class Opinion(object):
	"""docstring for Fact"""
	def __init__(self, arg):
		# super(Fact, self).__init__()
		# self.arg = arg

		pass
		



