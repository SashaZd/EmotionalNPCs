from math import exp, fabs

class Discussion(object):
	"""docstring for Discussion"""
	def __init__(self, group):
		super(Discussion, self).__init__()
		self.group = group
		self.avg_attitude = 0
		self.avg_opinion = 0
		self.avg_unc = 0
		self.personal_opinion = 0
		self.abc = 0


	@property
	def discuss(self):
		self.avg_attitude = self.group_attitude
		self.avg_opinion  = self.group_opinion
		self.avg_unc      = self.group_unc
		self.update_attitude_opinion
		self.update_unc

		
	


	# find the mean of attitude in the group
	@property
	def group_attitude(self):
		num_of_people = 0
		sum_of_attitude = 0
		for opinions in self.group:
			sum_of_attitude += self.group[num_of_people]['opinions']['attitude']
			num_of_people += 1
		return float(sum_of_attitude/num_of_people)


	# find the mean of attitude in the group
	@property
	def group_opinion(self):
		num_of_people = 0
		sum_of_opinion = 0
		for opinions in self.group:
			sum_of_opinion += self.group[num_of_people]['opinions']['opinion']
			num_of_people += 1
		return float(sum_of_opinion/num_of_people)

	# find the mean of unc in the group
	@property
	def group_unc(self):
		num_of_people = 0
		sum_of_unc = 0
		for opinions in self.group:
			sum_of_unc += self.group[num_of_people]['opinions']['unc']
			num_of_people += 1
		return float(sum_of_unc/num_of_people)

	# calculate fa in public opinion strength
	@property
	def calculate_fa(self):
		num_of_people = 0
		for opinions in self.group:
			num_of_people += 1
		if(num_of_people == 1):
			return 0
		elif(num_of_people == 2):
			return 0.1
		elif(num_of_people == 3):
			return 0.3
		else:
			return 1

	# calculate fb in public opinion strength		
	@property
	def calculate_fb(self):
		x = self.avg_unc
		return (1/(1+exp(24*x-6)))


	# calculate fc in public opinion strength		
	@property
	def calculate_fc(self):
		x = fabs(self.personal_opinion - self.avg_opinion)
		return (1/(1+exp(-12*x+6)))

	# update the attitude & opinion based on unc value
	@property
	def update_attitude_opinion(self):
		num_of_people = 0
		for opinions in self.group:
			# if unc is larger than 0.5, the person will follow the group 
			# update the person's opinion & attitude by the mean of the group
			if(self.group[num_of_people]['opinions']['unc'] >= 0.5):
				self.group[num_of_people]['opinions']['attitude'] = self.avg_attitude
				self.group[num_of_people]['opinions']['opinion'] = self.avg_opinion
			else:
				self.personal_opinion = self.group[num_of_people]['opinions']['opinion']
				f_a = self.calculate_fa
				f_b = self.calculate_fb
				f_c = self.calculate_fc
				public_opinion_strength = (f_a+f_b+f_c)/3
				public_threshhold = 0.6
				th1 = 1 - self.group[num_of_people]['opinions']['unc']
				th2 = 0
				if(th1 < public_threshhold):
					th2 = public_threshhold
				else:
					th2 = th1
				if (public_opinion_strength < th1):
					pass
				elif(public_opinion_strength >= th2):
					attitude_difference = self.group[num_of_people]['opinions']['attitude'] - self.avg_attitude
					self.group[num_of_people]['opinions']['attitude'] += 0.5 * attitude_difference
				else:
					if(self.group[num_of_people]['opinions']['unc'] <= 0.25):
						self.group[num_of_people]['opinions']['attitude'] = self.avg_attitude
						self.group[num_of_people]['opinions']['opinion'] = self.avg_opinion
					else:
						self.group[num_of_people]['opinions']['attitude'] = self.avg_attitude

			num_of_people += 1

	# update the unc value after updating the attitude & opinion
	@property
	def update_unc(self):
		num_of_people = 0
		for opinions in self.group:
			self.group[num_of_people]['opinions']['unc'] = fabs(self.group[num_of_people]['opinions']['attitude']-self.group[num_of_people]['opinions']['opinion']) 
			num_of_people += 1


