
import random
from configs import TOPICS
# from configs import SCHOOL_SUBJECTS

# 'science': {'num_facts':20, 'tags':['vaccination', 'abortion', 'health']},

class Knowledge(object):
	"""docstring for Facts"""
	def __init__(self):
		self.biases = self.get_topics()
		# self.associate_facts()

	def get_topics(self):
		topics = {}
		for topic, information in TOPICS.items(): 
			facts = ["%s_%s"%(topic, info) for info in range(information['num_facts'])]
			topics[topic] = facts
		return topics


	def create_original_opinion(self):
	    attitude = round(random.uniform(-1.0, 1.0), 2)
	    opinion = round(random.uniform(attitude-0.5, attitude+0.5), 2)
	    opinion = -1.0 if opinion < -1.0 else opinion
	    opinion = 1.0 if opinion > 1.0 else opinion
	    unc = abs(attitude - opinion)
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





		


class Topics(object):
	def __init__(self, name=None):
		self.name = name