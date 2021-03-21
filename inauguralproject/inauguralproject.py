# import relevant packages
import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt


#utility function 
def u_func(h, m, r, pbar, taug, taup, epsilon, phi):
  """
  Housing CRRA function 
  
   Variables
  h : house true value
  m : Amount of cash on hand
  r : interest rate
  pbar : tax bracket cutoff 
  taug : standard house tax
  taup : progressive house tax
  epsilon : undercut factor
  phi : Good old
  """
  u = (m-(r*h+taug*h*epsilon+taup*max(h*epsilon-pbar,0)))**(1-phi)*(h)**phi
  return u   
# scalar optimizer function
def u_optimiser(m, r, pbar, taug, taup, epsilon, phi):
    """ 
    Optimizises with respect to utility
    """
    def objective(h, m, r, pbar, taug, taup, epsilon, phi):
        return(-u_func(h=h, m=m, r=r, pbar=pbar, taug=taug, taup=taup, epsilon=epsilon, phi=phi))  
    sol = optimize.minimize_scalar(objective, args =(m, r, pbar, taug, taup, epsilon, phi))

    """
    h_star = optimal housing
    """ 
    h_star=sol.x
    return h_star



#Function for plotting two figures
def two_figures(x_left, y_left, title_left, xlabel_left, ylabel_left, x_right, y_right, title_right, xlabel_right, ylabel_right):
    """
    plots two figures side by side.

    Inputs: 
    Divided between left and right inputs for the respective plots.
    x_left and y_left are the data which makes up the left plot and x_right and y_right does the same for the right side plot.
    The rest of the inputs are self explanetory desripters.

    Output: 
    Two plots side by side.
    """
    # initialise figure
    fig = plt.figure(figsize=(10,4))
    # b. left plot
    ax_left = fig.add_subplot(1,2,1)
    ax_left.plot(x_left,y_left)

    ax_left.set_title(title_left)
    ax_left.set_xlabel(xlabel_left)
    ax_left.set_ylabel(ylabel_left)

    # c. right plot
    ax_right = fig.add_subplot(1,2,2)

    ax_right.plot(x_right, y_right)

    ax_right.set_title(title_right)
    ax_right.set_xlabel(xlabel_right)
    ax_right.set_ylabel(ylabel_right)

#Tax function
def tax(seed,size,mean,sigma,pbar=3.0,taug=0.012,taup=0.004,epsilon=0.5,phi=0.3,r=0.03):
    """
    A function for calculating the total tax revenue

    Inputs:
    seed: seed number
    size: number of random draws
    mean: The mean of the lognormal distribution
    sigma: Standard deviation for the distribution
    
    Optimisation variables:
    pbar : tax bracket cutoff 
    taug : standard house tax
    taup : progressive house tax
    epsilon: undercut factor
    Phi: Good old

    output:
    Total tax revenue
    """
    #Draw a random m value from the lognormal distribution.
    np.random.seed(seed)
    m_i = np.random.lognormal(mean=mean,sigma=sigma,size=size)

    #Solve the optimization problem for each individual and the tax from it to 'tax'.
    tax = 0

    for i, m_i in enumerate (m_i):        
        hc_i = u_optimiser(m_i,r,pbar,taug,taup,epsilon,phi)
        tax_i = taug*hc_i[0]+taup*max(hc_i[0]-pbar,0)
        tax += tax_i
    
    return tax

#Tax function2
def tax_new(h,pbar=3.0,taug=0.012,taup=0.004,epsilon=0.5):
    """
    A function for calculating the total tax revenue

    Inputs:
    pbar : tax bracket cutoff 
    taug : standard house tax
    taup : progressive house tax
    epsilon: undercut factor
    
    output:
    Total tax revenue
    """

    #Solve the optimization problem for each individual and the tax from it to 'tax'.
    tax = taug*h*epsilon+taup*max(h*epsilon-pbar,0)
    return tax