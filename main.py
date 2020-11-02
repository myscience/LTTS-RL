import visualize as vs
import numpy as np
from ltts import LTTS
from env import Reach

# Here we define our model
N, I, O, T = 100, 2, 2, 100;

dt = 1 / T;
tau_m = 2. * dt;
tau_s = 2. * dt;
tau_ro = 5. * dt;
beta_s  = np.exp (-dt / tau_s);
beta_ro = np.exp (-dt / tau_ro);
sigma_teach = 4.;
sigma_input = 6.;
offT = 1;
dv = 1 / 5.;
alpha = .1;
alpha_rout = .1;
Vo = -4;
h = -4;
s_inh = 20;

# Here we build the dictionary of the simulation parameters
par = {'tau_m' : tau_m, 'tau_s' : tau_s, 'tau_ro' : tau_ro, 'beta_ro' : beta_ro,
	   'dv' : dv, 'alpha' : alpha, 'Vo' : Vo, 'h' : h, 's_inh' : s_inh,
	   'N' : N, 'T' : T, 'dt' : dt, 'offT' : offT, 'alpha_rout' : alpha_rout,
	   'sigma_input' : sigma_input, 'sigma_teach' : sigma_teach};

# Here we define target and initial position
targ1 = np.array ((.9, 0.8));
targ2 = np.array ((.2, 0.6));
init = np.array ((0.5, 0.5));

# Here we init the environment
env = Reach (max_T = T, targ = targ1, init = init);

# Here we init our model
ltts = LTTS ((N, I, O, T), par);

# Based on this information we compute the expert trajectory input-output and
# produce a network behaviour to clone
steps = 80;

expert1 = env.build_expert (targ1, init, steps = steps, T = T, offT = offT);
expert2 = env.build_expert (targ2, init, steps = steps, T = T, offT = offT);

targ1, inp1 = ltts.implement (expert1);
targ2, inp2 = ltts.implement (expert2);

# out += np.random.uniform (-0.05, 0.05, size = out.shape);

# Here we clone this behaviour
ltts.clone ((expert1, expert2), (targ1, targ2), epochs = 500);

# Here we test the resulting behaviour
S_gen, action = ltts.compute (inp1);
vs.cloning_plot ((targ1, expert1[1]), (S_gen, action), save = 'test-raster.jpeg');

# Here we move the target
# targ /= 1.1

obv = init
for t in range (T - 1):
	action = ltts.step (obv, t);
	obv, r, done, agent = env.step (action / steps);

	fig = env.render ();
	# fig.savefig ('test.jpeg');
