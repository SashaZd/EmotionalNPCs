import string
from Topics import *

class Attitude(object):
	""" What a person might think toward the topic"""
	def __init__(self, person = None, topic = None):
		super(Attitude, self).__init__()
		self.person = person
		self.topic = topic
		self.affinity = None
		self.confidence = None
		self.knowledge = False


	def do_affinity(self,change_value):
		if change_value:


		if self.affinity == None:
			self.affinity = None
		if self.affinity+change_value<=0.0:
			self.affinity = 0.0
		elif self.affinity+change_value>=1.0:
			self.affinity = 1.0
		else:
			self.affinity += change_value

	@property
	def affinity(self):
		return self.__affinity

	@affinity.setter
	def affinity(self, new_value):
		"""Change affinity toward a topic during a discussion """
		# if hasattr(self, 'affinity'):
		if not new_value:
			self.__affinity = None
		elif new_value < 0: 
			self.__affinity = 0

		elif new_value > 1:
			self.__affinity = 1.0

		else:
			self.__affinity = new_value

		# self.__affinity = new_value
		# else:
		# if change_value and isinstance(change_value, float):
		# 	self.__affinity = change_value
		# else: 
		# 	self.__affinity = None

	def do_confidence(self,change_value):
		if self.confidence == None:
			self.confidence = None
		if self.confidence+change_value<=0.0:
			self.confidence = 0.0
		elif self.confidence+change_value>=1.0:
			self.confidence = 1.0
		else:
			self.confidence += change_value

	@property
	def confidence(self):
		return self.__confidence

	@confidence.setter
	def confidence(self, confidence):
		"""Change confidence toward a topic during a discussion """
		if isinstance(confidence, float):
			self.__confidence = confidence

	@property
	def knowledge(self):
		return self.__knowledge

	@knowledge.setter
	def knowledge(self, knowledge):
		"""Change knowledge """
		if isinstance(knowledge, bool):
			self.__knowledge = knowledge

	def do_knowledge(self):
		self.knowledge = True

	def set_starting_attitude(self,affinity_value,confidence_value,knowing):
		"""Need to assign the basic value based on which society a person belongs"""
		self.affinity = affinity_value
		self.confidence = confidence_value
		self.knowledge = knowing