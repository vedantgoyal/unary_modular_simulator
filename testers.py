from connector import *
from basic_blocks import *
from advanced_components import *
from collections import deque


def TestAdder(a,b):
	a.extend(a)
	b.extend(b)
	if len(a)<20:
		a = [0]*(20-len(a)) + a
	if len(b)<20:
		b = [0]*(20-len(b)) + b
	
	Add1 = Adder("Add1")
	#Add1.O2.B.set(0)
	Output=[]
	print("ck",list(map(lambda x: x%7, range(20)))[::-1])
	print("a:",a)
	print("b:",b)
	
	for x in range(20):	
		Add1.Clk.set(x)
		Add1.A.set(a.pop())
		Add1.B.set(b.pop())
		Output.append(Add1.Out.value)

	print("  ",Output[::-1])
	
def TestPlex(a,b,c):
	M1 = Multiplexer("M1")
	M1.A.set(a)
	M1.B.set(b)
	M1.C.set(c)
	print("Multiplexer says: {0}".format(M1.D.value))
	
def TestMem(d):
	if len(d)<10:
		d.extend([0]*(10-len(d)))
	print(d)
	M1 = Dmem("M1")
	
	for x in range(10):
		print("Clock cycle change {0}".format(x))
		M1.Clk.set(x)
		M1.D.set(d[x])
		if x==5:
			M1.D.set(0)
		print("Setting D to {0}".format(d[x]))
		
def TestRepeater(a,b):
	if len(a)<12:
		a = [0]*(12-len(a)) + a
	if len(b)<12:
		b = [0]*(12-len(b)) + b
	Rep1 = Repeater("Rep1")
	Output1=[]
	Output2=[]
	print("ck",list(map(lambda x: x%5, range(12)))[::-1])
	print("a:",a)
	print("b:",b)
	
	for x in range(12):
		Rep1.A.set(a.pop())
		Rep1.B.set(b.pop())
		Rep1.Clk.set(x)
		Output1.append(Rep1.AO.value)
		Output2.append(Rep1.BO.value)
		#if x==3:
		#	Rep1.Reset.set(1)
		#print("Clock cycle change {0}".format(x))
		#print("Setting A={0} and B={1}".format(a[-1],b[-1]))

	print("  ",Output1[::-1])
	print("  ",Output2[::-1])

def TestAligner(a,b):
	if len(a)<12:
		a = [0]*(12-len(a)) + a
	if len(b)<12:
		b = [0]*(12-len(b)) + b
	Ag1 = Aligner("Ag1")
	Output1=[]
	Output2=[]
	print("ck",list(map(lambda x: x%5, range(12)))[::-1])
	print("a:",a)
	print("b:",b)
	
	for x in range(12):
		Ag1.A.set(a.pop())
		Ag1.B.set(b.pop())
		Ag1.Clk.set(x)
		Output1.append(Ag1.AO.value)
		Output2.append(Ag1.BO.value)
		#if x==3:
		#	Rep1.Reset.set(1)
		#print("Clock cycle change {0}".format(x))
		#print("Setting A={0} and B={1}".format(a[-1],b[-1]))

	print("  ",Output1[::-1])
	print("  ",Output2[::-1])
	
def TestFullAdder(a,b,n):
	if len(a)<n:
		a = [0]*(n-len(a)) + a
	if len(b)<n:
		b = [0]*(n-len(b)) + b
	FA1 = FullAdder("FA1")
	FA1.Reset.set(0)
	Output=[]
	print("ck",list(map(lambda x: x%5, range(n)))[::-1])
	print("a:",a)
	print("b:",b)
	
	for x in range(n):
		FA1.A.set(a.pop())
		FA1.B.set(b.pop())
		FA1.Clk.set(x)
		Output.append(FA1.Out.value)
	print("  ",Output[::-1])


def TestMultiplier(a,b,n):
	if len(a)<n:
		a = [0]*(n-len(a)) + a
	if len(b)<n:
		b = [0]*(n-len(b)) + b
	Mul1 = Multiplier("Mul1")
	Output=[]
	print("ck",list(map(lambda x: x%5, range(n)))[::-1])
	print("a:",a)
	print("b:",b)
	for x in range(n):
		Mul1.A.set(a.pop())
		Mul1.B.set(b.pop())
		Mul1.Clk.set(x)
		Output.append(Mul1.Out.value)
	print("  ",Output[::-1])
	
	
def TestInverse(a,n,INV_BOUND):
	if len(a)<n:
		a = [0]*(n-len(a)) + a
	In1 = Inverse("In1",INV_BOUND)
	Output1=[]
	Output2=[]
	print("ck",list(map(lambda x: x%5+1, range(n)))[::-1])
	print("a:",a)
	for x in range(n):
		In1.A.set(a.pop())
		In1.Clk.set(x)
		Output1.append(In1.A.value)
		Output2.append(In1.Out.value)
	print("  ",Output1[::-1])
	print("  ",Output2[::-1])
	
def TestCell(a,n):
	if len(a)<n:
		a = [0]*(n-len(a)) + a
	Cel1 = Cell("Cel1")
	Output=[]
	print("ck",list(map(lambda x: x%5+1, range(n)))[::-1])
	print("a:",a)
	Cel1.Hold.set(0)
	Cel1.Release.set(0)
	print(Cel1.Reg, "should not hold and not release")
	for x in range(5):
		Cel1.In1.set(a.pop())
		Cel1.Clk.set(x)
		Output.append(Cel1.Out1.value)
	Cel1.Hold.set(1)
	Cel1.Release.set(0)
	print(Cel1.Reg, "should hold but not release")
	for x in range(5):
		Cel1.In1.set(a.pop())
		Cel1.Clk.set(x)
		Output.append(Cel1.Out1.value)
	Cel1.Hold.set(1)
	Cel1.Release.set(1)
	print(Cel1.Reg, "should hold but also release")
	for x in range(5):
		Cel1.In1.set(a.pop())
		Cel1.Clk.set(x)
		Output.append(Cel1.Out1.value)
	print(Cel1.Reg, "should not hold and release")
	Cel1.Hold.set(0)
	Cel1.Release.set(1)
	for x in range(5):
		Cel1.In1.set(a.pop())
		Cel1.Clk.set(x)
		Output.append(Cel1.Out1.value)
	print(Cel1.Reg)
	print("  ",Output[::-1])

def TestGrid(n):
	G1 = Grid("G1",3)
	G1.grid_load([[2,1,0],[3,2,1],[0,1,3]])
	Output1 =[]
	Output2 =[]
	print("ck",list(map(lambda x: x+1, range(n)))[::-1])

	print(G1.grid[0][0].Reg,G1.grid[0][1].Reg,G1.grid[1][1].Reg, "")
	for x in range(80):
		print("clk",x)
		G1.Clk.set(x)
		if x>=0 and x<20:
			Output1.append(G1.Inv1.A.value)
			Output2.append(G1.Inv1.Out.value)
	print(G1.grid[0][0].Reg,G1.grid[0][1].Reg,G1.grid[1][1].Reg, "")
	print(list(map(lambda x: x%5+1, range(20)))[::-1])
	print(Output1[::-1])
	print(Output2[::-1])

TestGrid(35)
#TestCell([1,0,0,1,0,1,0,1,1,0],20)
#TestMultiplier([1,1,1,0,0],[1,1,1,1,0],35)
#TestInverse([1,1,0,0,0],20,10)
#TestFullAdder([1,0,0,1,1],[1,1,1,1,0],20)
#TestAligner([0,0,1,0,0],[1,0,1,0,1])
#TestRepeater([0,0,0,0,1],[1,1,1,0,0])
#TestAdder([0,0,0,1,1,1,1],[1,1,0,0,0,0,0])
