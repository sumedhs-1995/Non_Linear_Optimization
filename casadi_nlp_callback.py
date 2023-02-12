from casadi import *

class constraint1(Callback):
  def __init__(self, name, opts={}):
    Callback.__init__(self)
    self.construct(name, opts)

  # Number of inputs and outputs
  def get_n_in(self): return 1
  def get_n_out(self): return 1

  # Initialize the object
  def init(self):
     print('initializing object')

  # Evaluate numerically
  def eval(self, arg):
    a = horzsplit(arg[0],[0,1,2])
    X = a[0]
    Y = a[1]
    Z = (1-X)**2-Y
    return [Z]

# Instantiate the Callback (make sure to keep a reference to it!)
con = constraint1('constraint1', {"enable_fd":True})



x = MX.sym('x')
y = MX.sym('y')
z = MX.sym('z')
f = x**2+100*z**2
g = z + con(horzcat(x,y))

nlp = {}                 # NLP declaration
nlp['x']= vertcat(x,y,z) # decision vars
nlp['f'] = f             # objective
nlp['g'] = g             # constraints

# Create solver instance
F = nlpsol('F','ipopt',nlp);

# Solve the problem using a guess
F(x0=[2.5,3.0,0.75],ubg=0,lbg=0)
