

from configs import TOPICS
from configs import SCHOOL_SUBJECTS

# 'science': {'num_facts':20, 'tags':['vaccination', 'abortion', 'health']},

class Knowledge(object):
	"""docstring for Facts"""
	def __init__(self):
		self.topics = self.get_topics()
		# self.associate_facts()

	def get_topics(self):
		topics = {}
		for topic, tag in TOPICS.items(): 
			topics[topic] = tag
		return topics


	# def associate_facts(self):
	# 	for subject in SCHOOL_SUBJECTS: 
	# 		facts = range(subject['num_facts'])
	# 		num_tags = subject['tags']
			


		


class Topics(object):
	def __init__(self, name=None):
		self.name = name