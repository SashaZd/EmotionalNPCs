from configs import STARTING_SOCIETIES
from Attitude import Attitude

class Society(object):
	"""docstring for Society"""
	def __init__(self):
		super(Society, self).__init__()
		self.arg = arg
		self.current_members = []  # current:bool, join_date, leave_date=None, member:Person
		self.attitudes = {}

	def add_member(self, person):
		member = {
			'join_date': person.world.current_date,
			'leave_date':　None, 
			'member': person 
		}
		self.current_members.append(member)

	def remove_member(self, person):
		print "To Do if needed"
		pass
	
	def add_attitude(self,topic,affinity):
		if topic in self.attitudes.keys():
			print "Topic already exists"

		else: 
			attitude = Attitude(topic, affinity, self)
			self.attitudes.append(Attitude)

	def send_newsletter(self):
		# give the person thought if they don't know something, change their thought if they already have the attitude in the certain topics
		print 'ToDo later'




society = Society(STARTING_SOCIETIES[0])


