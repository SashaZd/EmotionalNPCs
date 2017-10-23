
class Organization(object):
	"""docstring for Organization
	"""

	def __init__(self, name,type):
		super(Organization, self).__init__()
		# self.arg = arg

		if name: 
			self.name = name
		else:
			self.assign_name()

		self.type = type
		self.current_member = []
		self.past_member = []

		if self.type == "gradschool":
			self.days_of_meet = [1,2,3,4,5,6,7]
		else:
			self.days_of_meet = [1,2,3,4,5]

		if self.type == "work":
			self.employee = []
			"""
			TODO: leave and join?
			"""


	def __str__(self):
		return self.name

	def assign_name(self,newname):
		self.name = newname

	def add_member(self,person):
		self.current_member.append(person)


	""" TODO: add members to past_member when they leave"""


		
