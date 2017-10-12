from connector import *

class LC:
    # Logic Circuits have names and an evaluation function defined in child
    # classes. They will also contain a set of inputs and outputs.
    def __init__(self, name):
        self.name = name

    def evaluate(self):
        return


class Not(LC):         # Inverter. Input A. Output B.
    def __init__(self, name):
        LC.__init__(self, name)
        self.A = Connector(self, 'A', activates=1)
        self.Out = Connector(self, 'Out')

    def evaluate(self):
        self.Out.set(not self.A.value)


class Gate2(LC):         # two input gates. Inputs A and B. Output C.
    def __init__(self, name):
        LC.__init__(self, name)
        self.A = Connector(self, 'A', activates=1)
        self.B = Connector(self, 'B', activates=1)
        self.Out = Connector(self, 'Out')


class And(Gate2):       # two input AND Gate
    def __init__(self, name):
        Gate2.__init__(self, name)

    def evaluate(self):
        self.Out.set(self.A.value and self.B.value)


class Or(Gate2):         # two input OR gate.
    def __init__(self, name):
        Gate2.__init__(self, name)

    def evaluate(self):
        self.Out.set(self.A.value or self.B.value)

class Xor(Gate2):
    def __init__(self, name):
        Gate2.__init__(self, name)
        self.A1 = And("A1")  # See circuit drawing to follow connections
        self.A2 = And("A2")
        self.I1 = Not("I1")
        self.I2 = Not("I2")
        self.O1 = Or("O1")
        self.A.connect([self.A1.A, self.I2.A])
        self.B.connect([self.I1.A, self.A2.A])
        self.I1.B.connect([self.A1.B])
        self.I2.B.connect([self.A2.B])
        self.A1.Out.connect([self.O1.A])
        self.A2.Out.connect([self.O1.B])
        self.O1.Out.connect([self.Out])
        
class Multiplexer(LC):
	def __init__(self,name):
		LC.__init__(self, name)
		self.A = Connector(self, 'A', activates=1)
		self.B = Connector(self, 'B', activates=1)
		self.C = Connector(self, 'C', activates=1)
		self.Out = Connector(self, 'Out')
		
	def evaluate(self):
		if self.C.value == 0:
			self.Out.set(self.A.value)
		elif self.C.value ==1:
			self.Out.set(self.B.value)
		else:
			self.Out.set(None)
			
class Dmem(LC):
	def __init__(self,name):
		LC.__init__(self, name)
		self.D = Connector(self, 'D')
		self.Clk = Connector(self, 'Clk', activates=1)
		self.Q = Connector(self, 'Q')
		self.Q_bar = Connector(self, 'Q_bar')
		
	def evaluate(self):
		self.Q.set(self.D.value)
		self.Q_bar.set(not self.D.value)        
