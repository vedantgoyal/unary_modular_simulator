#  Define classes for Connector, Logic Circuit, Gate
from connector import *
from basic_blocks import *
from collections import deque

BIT_LENGTH = 5

class Adder(LC):
	def __init__(self,name):
		LC.__init__(self, name)
		self.A = Connector(self, 'A')
		self.B = Connector(self, 'B')
		self.Clk = Connector(self, 'Clk', activates=1)
		self.Out = Connector(self, 'Out')
		self.Reset = Connector(self, 'Reset')
		self.O1 = Or("O1")
		self.O2 = Or("O2")
		self.A1 = And("A1")
		self.Mux1 = Multiplexer("Mux1")
		self.Mem1 = Dmem("Mem1")
		self.A.connect([self.O1.A, self.A1.A])
		self.B.connect([self.O1.B, self.A1.B])
		self.O1.Out.connect(self.Mux1.A)
		self.A1.Out.connect([self.Mux1.B, self.O2.A])
		self.Mem1.Q.connect([self.Mux1.C, self.O2.B])
		self.O2.Out.connect([self.Mem1.D])
		self.Clk.connect(self.Mem1.Clk)
		self.Mux1.Out.connect(self.Out)
		self.O2.B.set(0)
		self.Reset.value=0;										#Revisit
	
	def evaluate(self):
		if self.Reset.value==1:
			self.O2.B.set(0)
		#print("Q is {0}".format(M1.Q.value))

class Repeater(LC):
	def __init__(self,name):
		LC.__init__(self, name)
		self.A = Connector(self, 'A')
		self.B = Connector(self, 'B')
		self.Clk = Connector(self,'Clk', activates=1)
		self.AO = Connector(self, 'AO')
		self.BO = Connector(self, 'BO')
		self.Reset = Connector(self, 'Reset')
		self.items_A = []
		self.items_B = []
		self.direction = "expand"
		
	def evaluate(self):
		if self.Reset.value==1:
			self.items_A = []
			self.items_B = []
			self.direction = "expand"
			
		if self.direction == "expand":
			self.AO.set(self.A.value)
			self.BO.set(self.B.value)
			self.items_A.append(self.A.value)
			self.items_B.append(self.B.value)
			if len(self.items_A) == BIT_LENGTH:
				self.direction = "shrink"
		else:
			self.AO.set(self.items_A.pop(0))
			self.BO.set(self.items_B.pop(0))
			if len(self.items_A) == 0:
				self.direction = "expand"
				
class Aligner(LC):
	def __init__(self,name):
		LC.__init__(self, name)
		self.A = Connector(self, 'A')
		self.B = Connector(self, 'B')
		self.Clk = Connector(self,'Clk', activates=1)
		self.AO = Connector(self, 'AO')
		self.BO = Connector(self, 'BO')
		self.Reset = Connector(self, 'Reset', activates=1)
		self.items_A = []
		self.items_B = []
		self.direction = "expand"
		
	def evaluate(self):
		if self.Reset.value==1:
			self.items_A = []
			self.items_B = []
			self.direction = "expand"
			
		if self.direction == "expand":
			self.AO.set(0)
			self.BO.set(0)
			if self.A.value==0:						# for A we do left align of 1
				self.items_A.append(0)
			if self.A.value==1:
				self.items_A = [1] + self.items_A
			if self.B.value==0:						# for B we do right align of 1
				self.items_B = [0] + self.items_B
			if self.B.value==1:
				self.items_B.append(1)
			if len(self.items_A) == BIT_LENGTH:
				self.direction = "shrink"
		else:
			self.AO.set(self.items_A.pop())
			self.BO.set(self.items_B.pop())
			if len(self.items_A) == 0:
				self.direction = "expand"



class FullAdder(LC):					#Gives Output After BIT_LENGTH cycles
	def __init__(self,name):
		LC.__init__(self, name)
		self.A = Connector(self, 'A')
		self.B = Connector(self, 'B')
		self.Clk = Connector(self, 'Clk', activates=1)
		self.Out = Connector(self, 'Out')
		self.Reset = Connector(self, 'Reset')
		self.Rep1 = Repeater("Rep1")
		self.Add1 = Adder("Add1")
		self.Alg1 = Aligner("Alg1")
		self.A.connect(self.Alg1.A)
		self.B.connect(self.Alg1.B)
		self.Alg1.AO.connect(self.Rep1.A)
		self.Alg1.BO.connect(self.Rep1.B)
		self.Clk.connect([self.Alg1.Clk, self.Rep1.Clk, self.Add1.Clk])
		self.Rep1.AO.connect(self.Add1.A)
		self.Rep1.BO.connect(self.Add1.B)
		self.Add1.Out.connect(self.Out)
		self.Reset.connect = [self.Alg1.Reset,self.Rep1.Reset,self.Add1.Reset]
		self.counter=0
		
	def evaluate(self):	
		if self.Reset.value==1:
			self.counter=0
		elif self.counter==BIT_LENGTH:
			self.Rep1.Reset.set(1)
			self.Add1.Reset.set(1)
		else:
			self.Reset.set(0)
			self.Rep1.Reset.set(0)
			self.Add1.Reset.set(0)
		self.counter+=1;
		

class InverseOld(LC):			#Gives inverse after INV_BOUND cycles
	def __init__(self,name, INV_BOUND):
		LC.__init__(self, name)
		self.A = Connector(self, 'A')
		self.Clk = Connector(self, 'Clk', activates=1)
		self.Out = Connector(self, 'Out')
		self.Reset = Connector(self, 'Reset')
		self.items_A = []
		self.status = "reading"
		self.Out.set(0)
		self.counter = 0
		self.INV_BOUND = INV_BOUND
		
	def evaluate(self):
		self.counter+=1
		if self.Reset.value==1:
			print("Inv was reset")
			self.inverse = None;
			self.status = "reading"
			self.counter = 0
			self.Out.set(0)
			self.Reset.set(0)
		else:
			if self.status =="reading":
				if len(self.items_A)<BIT_LENGTH:
					self.items_A.append(self.A.value)
				else:
					self.inverse = calc_inv(self.items_A)
					self.status = "waiting"
			elif self.status =="waiting":
				if self.counter==self.INV_BOUND:
					self.status = "popping"
			elif self.status =="popping":
				if len(self.inverse)>0:
					self.Out.set(self.inverse.pop())
				else:
					self.Out.set(0)
					self.Reset.set(1)						

class Inverse(LC):			#Gives multiplied after 5*BIT_LENGTH cycles
	def __init__(self,name,INV_BOUND):
		LC.__init__(self, name)
		self.A = Connector(self, 'A',activates=1)
		self.Clk = Connector(self, 'Clk', activates=1)
		self.Out = Connector(self, 'Out')
		self.Reset = Connector(self, 'Reset', activates=1)
		self.items_A = []
		self.Out.set(0)
		self.counter = 0
		self.INV_BOUND = INV_BOUND
		
	def evaluate(self):
		if self.Reset.value==1:
			print("Inv was reset")
			self.inverse = None;
			self.counter = 0
			self.Out.set(0)
			#print("counter ",self.counter)
		else:
			self.counter+=1
			if self.counter<=BIT_LENGTH:
				if len(self.items_A)<BIT_LENGTH:
					print("reading",self.A.value,self.counter)
					self.items_A.append(self.A.value)
					if self.counter==BIT_LENGTH:
						print("Feeding number",self.items_A,self.counter)
						self.answer = calc_inv(self.items_A)
						print("Found answer",self.answer,self.counter)
			elif self.counter <=INV_BOUND:
				self.Out.set(0)
				print("waiting",self.counter)
			elif self.counter>INV_BOUND and self.counter<=INV_BOUND+BIT_LENGTH:
				print("popping",self.answer[-1],"--",self.counter)
				print("popping",self.name,self.answer,self.counter)
				self.Out.set(self.answer.pop())
		
		
class Multiplier(LC):			#Gives multiplied after 5*BIT_LENGTH cycles
	def __init__(self,name):
		LC.__init__(self, name)
		self.A = Connector(self, 'A')
		self.B = Connector(self, 'B')
		self.Clk = Connector(self, 'Clk', activates=1)
		self.Out = Connector(self, 'Out')
		self.Reset = Connector(self, 'Reset')
		self.items_A = []
		self.items_B = []
		self.Out.set(0)
		self.counter = 0
		
	def evaluate(self):
		if self.Reset.value==1:
			self.counter = 0
			self.items_A = []
			self.items_B = []
			self.Reset.set(0)
			self.Out.set(0)
			#print("counter ",self.counter)
		else:
			self.counter+=1
			if self.counter<=BIT_LENGTH:
				if len(self.items_A)<BIT_LENGTH:
					#print("reading",self.counter)
					self.items_A.append(self.A.value)
					self.items_B.append(self.B.value)
					if self.counter==BIT_LENGTH:
						self.answer = calc_mul(self.items_A,self.items_B)
			elif self.counter <=5*BIT_LENGTH:
				self.Out.set(0)
				#print("waiting",self.counter)
			elif self.counter>5*BIT_LENGTH and self.counter<=6*BIT_LENGTH:
				#print("popping",self.answer[-1],"--",self.counter)
				#print("popping",self.name,self.answer,self.counter)
				self.Out.set(self.answer.pop())
			else:
				#print("Resetting Inverse",self.counter)
				self.Out.set(0)
				self.Reset.set(1)						


def calc_mul(items_A,items_B):
	if len(items_A)!=BIT_LENGTH or len(items_B)!=BIT_LENGTH:
		print("Raise Hell in mul_inv")
	num_A = items_A.count(1)
	num_B = items_B.count(1)
	answer = num_A*num_B
	answer = answer%BIT_LENGTH
	to_ret = [1]*answer + [0]*(BIT_LENGTH-answer)
	return to_ret	


def calc_inv(num_as_list):
	if len(num_as_list)!=BIT_LENGTH:
		print("Raise Hell in calc_inv")
	num = num_as_list.count(1)
	if num ==0:
		return [0]*(BIT_LENGTH)
		#print("Raise Hell in calc_inv, inv of 0?")
	t = 0; r=BIT_LENGTH; newt=1; newr=num;
	while newr!=0:
		q = int(r/newr)
		temp = t
		t = newt
		newt = temp - q*newt
		temp = r
		r = newr
		newr = temp - q*newr
		
	inv = t%BIT_LENGTH
	to_ret = [1]*inv + [0]*(BIT_LENGTH-inv)
	return to_ret
	
def dec_to_unary(num):
	num = num%BIT_LENGTH
	to_ret = [1]*num + [0]*(BIT_LENGTH-num)
	return to_ret

class Cell(LC):
	def __init__(self,name):
		LC.__init__(self, name)
		self.Reg = [0]*BIT_LENGTH
		self.Out1 = Connector(self, 'Out1')
		self.In1 = Connector(self, 'In1')
		self.Clk = Connector(self, 'Clk', activates=1)
		self.Hold = Connector(self, 'Hold')
		self.Release = Connector(self, 'Release')
		self.In1.set(0)
		
	def evaluate(self):
		if self.Hold.value==1 and self.Release.value==1:
			self.Out1.set(self.Reg[-1])
			self.Reg = [self.Reg.pop()] + self.Reg
		elif self.Hold.value==1 and self.Release.value==0:
			self.Out1.set(0)
		elif self.Hold.value==0 and self.Release.value==0:
			self.Out1.set(0)
			self.Reg.pop()
			self.Reg = [self.In1.value] + self.Reg
		elif self.Hold.value==0 and self.Release.value==1:
			self.Out1.set(self.Reg.pop())
			self.Reg = [self.In1.value] + self.Reg
			
I_BOUND=10
INV_BOUND=10
class Grid(LC):
	def __init__(self,name, GRID_SIZE):
		LC.__init__(self, name)
		self.GRID_SIZE = GRID_SIZE
		self.grid = [[Cell("c{0}{1}".format(i,j)) for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]
		self.Clk = Connector(self, 'Clk', activates=1)
		self.HoldPiv = Connector(self, 'HoldPiv')
		self.ReleasePiv = Connector(self, 'ReleasePiv')
		self.HoldR0 = Connector(self, 'HoldR0')
		self.ReleaseR0 = Connector(self, 'ReleaseR0')
		self.HoldC0 = Connector(self, 'HoldC0')
		self.ReleaseC0 = Connector(self, 'ReleaseC0')
		#self.Eliminate = Connector(self, 'Eliminate')
		self.Inv1 = Inverse("Inv1", I_BOUND)
		self.Mul1 = Multiplier("Mul1")
		self.Mul2 = Multiplier("Mul2")
		self.Not1 = Not("Not1")
		self.FA1 =  FullAdder("FA1")
		self.counter = 0
		
		self.Clk.connect([self.Inv1.Clk,self.Mul1.Clk,self.Mul2.Clk,self.FA1.Clk,]+[self.grid[i][j].Clk for i in range(GRID_SIZE) for j in range(GRID_SIZE)])
		self.grid[0][0].Out1.connect(self.Inv1.A)
		self.Inv1.Out.connect(self.Mul1.A)
		self.grid[0][1].Out1.connect(self.Mul1.B)
		self.grid[1][0].Out1.connect(self.Mul2.A)
		self.Mul1.Out.connect(self.Mul2.B)
		self.Mul2.Out.connect(self.Not1.A)
		self.Not1.Out.connect(self.FA1.A)
		self.grid[1][1].Out1.connect(self.FA1.B)
		self.FA1.Out.connect(self.grid[1][1].In1)
		"""
		self.HoldPiv.connect(self.grid[0][0].Hold)
		self.ReleasePiv.connect(self.grid[0][0].Release)
		self.HoldR0.connect([self.grid[i][0].Hold for i in range(1,self.GRID_SIZE)])
		self.ReleaseR0.connect([self.grid[i][0].Release for i in range(1,self.GRID_SIZE)])
		self.HoldC0.connect([self.grid[0][i].Hold for i in range(1,self.GRID_SIZE)])
		self.ReleaseC0.connect([self.grid[0][i].Release for i in range(1,self.GRID_SIZE)])
		"""
		self.grid[1][0].Hold.set(1)							
		self.grid[1][0].Release.set(0)
		self.grid[0][1].Hold.set(1)
		self.grid[0][1].Release.set(0)
		self.grid[0][0].Hold.set(0)
		self.grid[0][0].Release.set(1)
		
		
	def evaluate(self):
		self.counter+=1
		if self.counter==I_BOUND:
			self.Mul1.Reset.set(1)
			self.grid[0][1].Hold.set(1)
			self.grid[0][1].Release.set(1)
		elif self.counter == (I_BOUND + 5*BIT_LENGTH):
			self.Inv1.Reset.set(1)
			self.Mul2.Reset.set(1)
			self.grid[1][0].Hold.set(1)
			self.grid[1][0].Release.set(1)
		elif self.counter == (I_BOUND + 10*BIT_LENGTH):
			self.FA1.Reset.set(1)
			self.grid[1][1].Hold.set(1)
			self.grid[1][1].Release.set(1)
		elif self.counter == (I_BOUND + 11*BIT_LENGTH):
			self.grid[1][1].Hold.set(0)
			self.grid[1][1].Release.set(0)
		elif self.counter == (I_BOUND + 12*BIT_LENGTH):
			self.grid[1][1].Hold.set(1)
			self.grid[1][1].Release.set(0)
		
	def grid_load(self, to_load):
		for i in range(self.GRID_SIZE):
			for j in range(self.GRID_SIZE):
				self.grid[i][j].Reg = dec_to_unary(to_load[i][j])	
	


