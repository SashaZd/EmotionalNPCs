import string
from Topics import *

class Attitude(object):
	""" What a person might think toward the topic"""
	def __init__(self, topic, affinity=None, owner = None):
		super(Attitude, self).__init__()
		self.owner = owner
		self.topic = topic
		self.affinity = None
		self.confidence = None
		self.knowledge = 0


	# def change_affinity(self,change_value):
	# 	self.affinity += change_value

	@property
	def affinity(self):
		return self.__affinity

	@affinity.setter
	def affinity(self, new_value):
		"""Change affinity toward a topic during a discussion """
		# if hasattr(self, 'affinity'):
		if not hasattr(self,'affinity'):
			self.__affinity = None

		if not new_value or not isinstance(new_value, float):
			pass
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

	# def change_confidence(self,change_value):
	# 	self.confidence += change_value

	@property
	def confidence(self):
		return self.__confidence

	@confidence.setter
	def confidence(self, new_value):
		"""Change confidence toward a topic during a discussion """
		if not hasattr(self,'confidence'):
			self.__confidence = None

		if not new_value or not isinstance(new_value, float):
			pass
		elif new_value < 0: 
			self.__confidence = 0

		elif new_value > 1:
			self.__confidence = 1.0

		else:
			self.__confidence = new_value

	@property
	def knowledge(self):
		return self.__knowledge

	@knowledge.setter
	def knowledge(self, new_value):
		"""Change knowledge """
		if not hasattr(self,'knowledge'):
			self.__knowledge = 0
		
		# Increasing the amount of knowledge on a topci
		# Currently it's an integer amount, could be replaced by facts/evidence/etc as a list later
		self.__knowledge = new_value


	def add_knowledge(self,change_value):
		self.knowledge += change_value

	# def set_starting_attitude(self,affinity_value,confidence_value,knowing):
	# 	"""Need to assign the basic value based on which society a person belongs"""
	# 	self.affinity = affinity_value
	# 	self.confidence = confidence_value
	# 	self.knowledge = knowing