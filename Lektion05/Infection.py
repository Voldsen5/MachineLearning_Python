# -*- truncate-lines:t -*-
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 08:45:10 2020
@author: Sila
"""

from modsim import *

init = State(S=89, I=1, R=0)

#To convert from number of people to fractions, we divide through by the total.
init /= sum(init)


def make_system(size, beta, gamma):
    """Make a system object for the SIR model.

    beta: contact rate in days
    gamma: recovery rate in days

    returns: System object
    """
    init = State(S=size, I=1, R=0)
    init /= sum(init)

    t0 = 0
    t_end = 7 * 14

    return System(init=init, t0=t0, t_end=t_end,
                  beta=beta, gamma=gamma)

tc = 3      # time between contacts in days
tr = 100      # recovery time in days

beta = 1 / tc      # contact rate in per day
gamma = 1 / tr     # recovery rate in per day

system = make_system(89, beta, gamma)


def update_func(state, t, system):
    """Update the SIR model.

    state: State with variables S, I, R
    t: time step
    system: System with beta and gamma

    returns: State object
    """
    s, i, r = state

    infected = system.beta * i * s
    recovered = system.gamma * i

    s -= infected
    i += infected - recovered
    r += recovered

    return State(S=s, I=i, R=r)

# To run a single time step, we call it like this:

state = update_func(init, 0, system)


def run_simulation(system, update_func):
    """Runs a simulation of the system.

    Add three Series objects to the System: S, I, R

    system: System object
    update_func: function that updates state
    """
    S = TimeSeries()
    I = TimeSeries()
    R = TimeSeries()

    state = system.init
    t0 = system.t0
    S[t0], I[t0], R[t0] = state

    for t in linrange(system.t0, system.t_end):
        state = update_func(state, t, system)
        S[t + 1], I[t + 1], R[t + 1] = state

    return S, I, R

tc = 3      # time between contacts in days
tr = 4      # recovery time in days

beta = 1 / tc      # contact rate in per day
gamma = 1 / tr     # recovery rate in per day

system = make_system(89, beta, gamma)
S, I, R = run_simulation(system, update_func)


def plot_results(S, I, R):
    """Plot the results of a SIR model.

    S: TimeSeries
    I: TimeSeries
    R: TimeSeries
    """

    plot(S, label='Susceptible')
    plot(I, label='Infected')
    plot(R, label='Recovered')

    decorate(xlabel='Time (days)',
             ylabel='Fraction of population')

    S.plot(color='blue', label='Susceptible')
    I.plot(color='red', label='Infected')
    R.plot(color='green', label='Recovered')

    plt.show()

#plot_results(S, I, R)


tc = 0.75      # time between contacts in days
tr = 7.5      # recovery time in days

beta = 1 / tc      # contact rate in per day
gamma = 1 / tr     # recovery rate in per day

system = make_system(5500000, beta, gamma)
S, I, R = run_simulation(system, update_func)
plot_results(S, I, R)
