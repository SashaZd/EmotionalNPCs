
class Organization(object):
	"""docstring for Organization
	"""

	def __init__(self, name=None):
		super(Organization, self).__init__()
		# self.arg = arg

		if name: 
			self.name = name
		else:
			self.assign_name()


	def __str__(self):
		return self.name


	def assign_name(self):
		self.name = "Unknown"


	def doSomething(self):
		self.dosomething = "Nothing"
		print self.dosomething
		print "another222222"

		
