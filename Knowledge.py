from copy import deepcopy
import random
from collections import Counter
import itertools
from Discussion import Discussion


# 'science': {'num_facts':20, 'tags':['vaccination', 'abortion', 'health']},

class Knowledge(object):
	"""docstring for Facts"""
	def __init__(self):
		# self.tags = []
		self.topics = {}
		self.views = {}
		self.facts = {}


	def initiate_group_discussion(self, group):
		if random.random() < 0.05:
			count = Counter(list(itertools.chain.from_iterable([person.knowledge.facts.keys() for person in group])))

			# What facts are the most common
			common_max = max(count.values())
			(chosen_topic_of_discussion, frequency) = random.choice([fact for fact in count.most_common(common_max)])
			print "Discussion of %s: Known to %s/%s people"%(chosen_topic_of_discussion, frequency, len(group))

			group_opinions = []
			for person in group: 
				if chosen_topic_of_discussion in person.knowledge.facts:
					group_opinions.append({
						'person': person, 
						'opinion': person.knowledge.facts[chosen_topic_of_discussion].get_opinion()
					})

			discussion = Discussion(group_opinions)
			


	def gain_knowledge(self, fact):
		topic_name = fact.topic

		if topic_name not in self.topics.keys(): 
			new_topic = Topic(topic_name)
			self.add_topic(new_topic)

		if fact not in self.topics[topic_name].facts and fact not in self.facts: 
			# Never heard this information before. 
			# Currently generates a random opinion of the fact if there's no opinion currently
			# Todo: Add inheritence of parental bias
			new_fact = deepcopy(fact)
			new_fact.generate_random_opinion()
			self.add_fact(new_fact)



		# 	# if not fact.name in self.facts: 
		# 	# 	self.facts[fact.name] = new_fact

		else: 
		# 	# Todo: Need to update the fact/opinion's strength? if you continually learn about it 
		# 	# i.e. opinion is reinforced over and over. Should cause a change 
		# 	# Future update? Or could we just initialize a discussion with 1-2 people accordingly? 
			pass

	
	# Takes Fact instance, and adds it to current knowledge
	def add_fact(self, fact):
		if fact not in self.topics[fact.topic].facts:

			# If hearing of the fact for the first time
			# Currently generates a random opinion
			# Todo: Add parental bias
			if not fact.opinion: 
				fact.generate_random_opinion()

			self.topics[fact.topic].add_fact(fact)
			self.facts[fact.name] = fact
			

	# Takes Topic instance, and adds it to current knowledge
	def add_topic(self, topic):
		if topic.name not in self.topics: 
			self.topics[topic.name] = topic
			
			for fact in topic.facts:
				if fact.name not in self.facts:  
					self.facts[fact.name] = fact
				
				else:
					# Todo: Update existing information?
					pass


	def add_view(self, topic):
		if topic.name not in self.views: 
			self.views[topic.name] = topic
			
			for fact in topic.facts:
				if fact.name not in self.facts:  
					self.facts[fact.name] = fact
				
				else:
					# Todo: Update existing information?
					pass

	
	def get_random_fact(self):
		return random.choice(self.facts.values())
		

	def __str__(self):
		return "%s"%(self.topics)

	def __repr__(self):
		return "%s"%(self.topics)



class Topic(object):
	"""docstring for Topic"""
	def __init__(self, name):
		self.name = name
		self.tags = [] # information['tags'] if 'tags' in information else []
		self.facts = []

		# if information: 
		# 	self.add_facts(information)


	def add_tag(self, tag):
		if tag not in self.tags: 
			self.tags.append(tag)


	def add_fact(self, fact):
		self.add_tag(fact.tag)
		self.facts.append(fact)


	def get_associated_facts_known(self):
		return self.facts


	def __str__(self):
		return "%s(%s facts)"%(self.name, len(self.facts))

	def __repr__(self):
		return "%s(%s facts)"%(self.name, len(self.facts))



class Fact(object):
	"""docstring for Fact"""
	def __init__(self, name, topic, tag, opinion=None):
		super(Fact, self).__init__()
		self.name = name
		self.tag = tag
		self.topic = topic

		# By default self.opinion = None. 
		# i.e. No opinion if you haven't heard of something before
		self.opinion = opinion

	def get_opinion(self):
		return self.opinion.get_opinion()

	def generate_random_opinion(self):
		self.opinion = Opinion()
		self.opinion.generate_random_opinion()

	def __str__(self):
		return "%s --> %s"%(self.name, self.opinion)

	def __repr__(self):
		return "%s --> %s"%(self.name, self.opinion)
		


class Opinion(object):
	"""docstring for Fact"""
	def __init__(self):
		super(Opinion, self).__init__()
		
		self.attitude = None		
		self.opinion = None		
		self.unc = None		
		self.pub_thr = None		
		self.pri_thr = None		


	def generate_random_opinion(self):
		""" Init Random Opinion to Start
		Different from having no opinion, 
			or inheriting the biases of the people who first introduce the topic to you  
			This is for facts that are introduced to you in school (perhaps) 
			or that you don't get from any other person (i.e. the internet when you're doing a random search)
		"""
		self.attitude = round(random.uniform(-1.0, 1.0), 2)
		
		opinion = round(random.uniform(self.attitude-0.5, self.attitude+0.5), 2)
		self.opinion = -1.0 if opinion < -1.0 else opinion
		self.opinion = 1.0 if opinion > 1.0 else opinion
		
		self.unc = round(abs(self.attitude - self.opinion), 2)
		self.pub_thr = 0.6
		self.pri_thr = round(random.uniform(0.0, 1.0), 2)

 
	def get_opinion(self):
		return {
			'attitude': self.attitude,
			'opinion': self.opinion,
			'unc': self.unc,
			'pub_thr': self.pub_thr,
			'pri_thr': self.pri_thr,
		}

	def __str__(self):
		return "attitude: %s | opinion: %s | unc: %s"%(self.attitude, self.opinion, self.unc)

	def __repr__(self):
		return "attitude: %s | opinion: %s | unc: %s"%(self.attitude, self.opinion, self.unc)
		



