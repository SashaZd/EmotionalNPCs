import string
from Topics import *

class Attitude(object):
	""" What a person might think toward the topic"""
	 def __init__(self, person, topic):
	 self.person = person
	 self.topic = topic
	 self.affinity = None
	 self.confidence = None
	 self.knowledge = False


	 def do_affinity(self,change_value):

		self.affinity += change_value

	@property
	def affinity(self):
		return self.__affinity

	@affinity.setter
	def affinity(self, affinity):
		if isinstance(affinity, float):
			self.__affinity = affinity