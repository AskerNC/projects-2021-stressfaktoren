# import relevant packages
import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt


#utility function 
def u_func(p_h, m, r, pbar, taug, taup, epsilon, phi):
  """
  Housing CRRA function 
  
   Variables
  p_h : house true value
  m : Amount of cash on hand
  r : interest rate
  pbar : tax bracket cutoff 
  taug : standard house tax
  taup : progressive house tax
  epsilon : undercut factor
  phi : Good old
  """
  u = (m-r*p_h-taug*p_h*epsilon-taup*max(p_h*epsilon-pbar,0))**(1-phi)*p_h**phi
  return u   

# scalar optimizer function
def u_optimiser(m, r, pbar, taug, taup, epsilon, phi):
    """ 
    Optimizises with respect to utility
    """
    def objective(p_h, m, r, pbar, taug, taup, epsilon, phi):
        return(-u_func(p_h=p_h, m=m, r=r, pbar=pbar, taug=taug, taup=taup, epsilon=epsilon, phi=phi))  

    sol = optimize.minimize_scalar(objective,k, method='bounded',bounds=(0,m) args =(m, r, pbar, taug, taup, epsilon, phi))
    
    """
    h_star = optimal housing
    c_star = optimal consumption
    u_star = optimal utility
    """ 
    h_star=sol.x
    c_star=m-r*h_star-taug*h_star*epsilon-taup*max(h_star*epsilon-pbar,0)
    u_star=u_func(p_h=h_star, m=m, r=r, pbar=pbar, taug=taug, taup=taup, epsilon=epsilon, phi=phi)
    return h_star, c_star, u_star

 
