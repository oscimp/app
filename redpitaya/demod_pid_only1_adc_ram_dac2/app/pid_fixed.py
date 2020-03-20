class PIDfixed(object):

	def __init__(self, kp=0, ki=0, sp=0, osp=0, imax=10**999, omax=10**999, oscale=12):

#	kp, ki: proprtional and integral parameters
#	sp: setpoint
#	osp: output setpoint (output bias)
#	imax: integrator maximum value
#	omax: output range is [-omax, +omax]
#	oscale: output scaling, output is devided by 2**oscale

		self.kp = kp
		self.ki = ki
		self.sp = sp
		self.osp = osp
		self.imax = imax
		self.omax = omax
		self.oscale = oscale
		self.un = 0
		self._inv_out = 1
		self._int_en = True
		self._reset_state = False
		self._sum = 0

	def compute(self, y0):
		eps = self.sp - y0
		if self._int_en is True:
			sum_ = min(self.imax, max(-self.imax, self._sum + eps))
		else:
			sum_ = 0
		vn = (self.kp * eps +  self.ki * sum_) >> self.oscale
		vn += self.osp
		self.un = min(self.omax, max(-self.omax, vn)) * self._inv_out
		self._sum = sum_ + self.un - vn # Anti windup
		return self.un

	@property
	def integrator(self):
		return self._sum

	def invert_out(self, state=True):
#        	Just invert output...
		if state is True:
			self._inv_out = -1
		else:
			self._inv_out = 1

	def enable_int(self, state=True):
		if state is True:
			self._int_en = True
		else:
			self._int_en = False
			self.reset(True)

	def reset(self, state):
		self._sum = 0
