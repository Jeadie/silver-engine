# silver-engine
Financial based scripts and web apps based off content learnt in MATH3090 at UQ. 

## Current tools
- Stochastic binomial yield curve lattices
- Discount cashflow valuation tools for debt and equity instruments

## Stochastic binomial yield curve lattices
This tool calculates both spot and forward yield curves for the given future time period. The tool is discrete that uses a forward lattice model. 

The tool has the following features: 
  - Customisable probability functions (with respect to the time period and previous probability and yield) for binomial steps.
  - Customisable yield (both up/down) functions both with respect to the time period and previous yield. 
  
  To run, simply define the required functions above and on instantiation the model will use back propogation to calculate the spot yields and in turn forward yields. 
  
  ``` python
  
  yield_up = lambda t, y: y + 0.01
  yield_down = lambda t, y: y - 0.01
  p_func = lambda t, y, p: 0.7
  time_intervals = 5; 
  initial_spot_yield = 0.03; 
  
  rates = ForwardYieldLattice(time_intervals, initial_spot_yield, yield_up_func=yield_up, 
                                                                  yield_down_func=yield_down,
                                                                  prob_func=p_func)
                                                                  
  y_0_4 = lattice.get_spot_rate(4)
  y_2_4 = lattice.calculate_forward_yields(2,4)
  ```


## Discount cashflow valuation tools for debt and equity instruments
This tool is still in development but will be able to value a combination of financial instruments at varying discount rates and time periods. With a base abstract representation of an instrument, a factory will provide concrete implementations of securities such as ordinary/preferential shares, annuities and other cashflow instruments. 
