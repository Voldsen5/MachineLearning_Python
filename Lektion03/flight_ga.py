# -*- truncate-lines:t -*-
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 4 10:11:14 2020
@author: Sila
"""
import os
import time
import random
import math
from numpy import inf, isfinite

# Programming Collective Intelligence chapter 5.
# Example with finding optimal flight times.


# Planning a trip for the Glass family. They start in different
# locations all arriving at the same place, meet and then return.
# The task here is to optimize the time they arrive, based on cost and
# waiting time - as stated in the cost function -


people = [('Seymour', 'BOS'),
          ('Franny', 'DAL'),
          ('Zooey', 'CAK'),
          ('Walt', 'MIA'),
          ('Buddy', 'ORD'),
          ('Les', 'OMA')]
# Laguardia
destination = 'LGA'

flights = {}
if (os.path.exists('schedule.txt')):
    file1 = open('schedule.txt', 'r')
    Lines = file1.readlines()
    for line in Lines:
        origin, dest, depart, arrive, price = line.strip().split(',')
        flights.setdefault((origin, dest), [])

        # Add details to the list of possible flights
        flights[(origin, dest)].append((depart, arrive, int(price)))


def getminutes(t):
    x = time.strptime(t, '%H:%M')
    return x[3] * 60 + x[4]


def printschedule(r):
    for d in range(int(len(r) / 2)):
        name = people[d][0]
        origin = people[d][1]
        out = flights[(origin, destination)][int(r[d])]
        ret = flights[(destination, origin)][int(r[d + 1])]
        print('%10s%10s %5s-%5s $%3s %5s-%5s $%3s' % (name, origin,
                                                out[0], out[1], out[2],
                                                ret[0], ret[1], ret[2]))


def schedulecost(sol):
    totalprice = 0
    latestarrival = 0
    earliestdep = 24 * 60

    for d in range(int(len(sol) / 2)):
        # Get the inbound and outbound flights
        origin = people[d][1]
        outbound = flights[(origin, destination)][int(sol[d])]
        returnf = flights[(destination, origin)][int(sol[d + 1])]

        # Total price is the price of all outbound and return flights
        totalprice += outbound[2]
        totalprice += returnf[2]

        # Track the latest arrival and earliest departure
        if latestarrival < getminutes(outbound[1]): latestarrival = getminutes(outbound[1])
        if earliestdep > getminutes(returnf[0]): earliestdep = getminutes(returnf[0])

    # Every person must wait at the airport until the latest person arrives.
    # They also must arrive at the same time and wait for their flights.
    totalwait = 0
    for d in range(int(len(sol) / 2)):
        origin = people[d][1]
        outbound = flights[(origin, destination)][int(sol[d])]
        returnf = flights[(destination, origin)][int(sol[d + 1])]
        totalwait += latestarrival - getminutes(outbound[1])
        totalwait += getminutes(returnf[0]) - earliestdep

        # Does this solution require an extra day of car rental? That'll be $50!
    if latestarrival > earliestdep: totalprice += 50

    return totalprice + totalwait

#Random searching isn’t a very good optimization method, but it makes it easy to
#understand exactly what all the algorithms are trying to do, and it also serves as a
#baseline so you can see if the other algorithms are doing a good job.
def randomoptimize(domain, costf, bestr=None, nRandomAttempts=1000, verbose=False):
    """
    Input:
      bestr: best solution
    """
    best = inf  # best solution function evaluation
    sols_tried = []  # keep track of what inputs we have tried so we don't retry them (this is really only important for small problems)

    # initialize the search starting location:
    if bestr is None: bestr = [float(random.randint(domain[i][0], domain[i][1])) for i in range(len(domain))]

    r = bestr
    for i in range(nRandomAttempts):
        if r in sols_tried: continue
        sols_tried.append(r)

        # Get the cost
        cost = costf(r)

        # Compare it to the best one so far
        if cost < best:
            best = cost
            bestr = r
            if verbose:
                print("New best= %10.6f; sol= %s" % (best, bestr))

        r = [float(random.randint(domain[i][0], domain[i][1])) for i in range(len(domain))]
    return bestr


def hillclimb(domain, costf, sol=None, verbose=False):
    if sol is None: sol = [float(random.randint(domain[i][0], domain[i][1])) for i in
                           range(len(domain))]  # create a random solution
    best = costf(sol)
    if not isfinite(best): return None
    # Main loop
    while 1:
        # Create list of neighboring solutions
        neighbors = []

        for j in range(len(domain)):
            # One away in each direction
            if sol[j] < domain[j][1]:  # can we step one to the right?
                neighbors.append(sol[0:j] + [sol[j] + 1] + sol[j + 1:])
            if sol[j] > domain[j][0]:  # can we step one to the left?
                neighbors.append(sol[0:j] + [sol[j] - 1] + sol[j + 1:])

        # See what the best solution amongst the neighbors is
        current = best
        for j in range(len(neighbors)):
            cost = costf(neighbors[j])
            ###print "Trying neighbors[j]= ", neighbors[j], cost, best
            if cost < best:
                best, sol = cost, neighbors[j]
                if verbose:
                    print("New best= %10.6f; sol= %s" % (best, sol))

        # If there's no improvement, then we've reached the top
        if best == current: break
    return sol


def multiple_start_annealing(domain, costf, num_random_starts=100, T=10000.0, cool=0.95, step=1):
    """
    Runs the routine "annealingoptimize" but starting from multiple random locations.
    """

    all_results = []
    for i in range(num_random_starts):
        vec = [float(random.randint(domain[i][0], domain[i][1])) for i in range(len(domain))]
        res = annealingoptimize(domain, costf, vec=vec, T=10000.0, cool=0.95, step=1)
        all_results.append(res)

    (best_cost, best_sol) = (inf, None)
    for i in range(num_random_starts):
        if costf(all_results[i]) < best_cost:
            best_cost = costf(all_results[i])
            best_sol = all_results[i]

    return best_sol


def annealingoptimize(domain, costf, vec=None, T=10000.0, cool=0.95, step=1):
    # Initialize our solution randomly if one is not provided:
    if vec is None: vec = [float(random.randint(domain[i][0], domain[i][1])) for i in range(len(domain))]

    while T > 0.1:
        # Choose one of the indices
        i = random.randint(0, len(domain) - 1)

        # Choose a direction to change it
        dir = random.randint(-step, step)

        # Create a new list with one of the values changed
        vecb = vec[:]
        vecb[i] += dir
        if vecb[i] < domain[i][0]:
            vecb[i] = domain[i][0]
        elif vecb[i] > domain[i][1]:
            vecb[i] = domain[i][1]

        # Calculate the current cost and the new cost
        ea = costf(vec)
        eb = costf(vecb)
        p = pow(math.e, (-eb - ea) / T)

        # Is it better, or does it make the probability cutoff?
        if (eb < ea or random.random() < p): vec = vecb

        # Decrease the temperature
        T = T * cool
    return vec


def geneticoptimize(domain, costf, vec=None, popsize=50, step=1, mutprob=0.2, elite=0.2, maxiter=10, printbest=False):
    """
    domain  = the valid domain in which we can look for a minimum
              an example would be domain = [(0, 10), (0, 10), (0, 10), (0, 10)] for a four
              dimensional problem where each variable must be between 0 and 10
              inclusive (i.e. 0 and 10 are valid values for solutions)

    costf   = the function we seek to minimize.  costf(vec)

    vec     = an optional initial guess at the minimum value.

    step    = the amount by which we change the value of the i-th component of the vector we mutate
              namely the ith component of the vector vec goes to vec[i]-step or vec[i]+step

    mutprob = the probability of a mutation

    elite   = percentage of the best performer to take from the current popluation to use in
              initializing the next population
    """

    # Mutation Operation
    def mutate(vec):
        i = random.randint(0, len(domain) - 1)
        if random.random() < 0.5:  # we try to decrement the value at vec[i]
            if vec[i] > domain[i][0]:  # we can
                res = vec[0:i] + [vec[i] - step] + vec[i + 1:]
            else:  # we can't
                res = vec[0:i] + [vec[i] + step] + vec[i + 1:]
        else:  # we try to increment the value at vec[i]
            if vec[i] < domain[i][1]:  # we can
                res = vec[0:i] + [vec[i] + step] + vec[i + 1:]
            else:  # we can't
                res = vec[0:i] + [vec[i] - step] + vec[i + 1:]
        return res

        # Crossover Operation

    def crossover(r1, r2):
        lB, uB = 1, max(len(domain) - 1, 1)
        i = random.randint(lB,
                           uB)  # i=0 returns full r1 array; i=len(domain) returns full r2 array (thus we need i>0 and i<len(domain)
        return r1[:i] + r2[i:]

    # Build the initial population (taken randomly)
    if (vec is None):
        pop = []
    else:
        pop = [vec]
    for i in range(popsize - len(pop)):
        vec = [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]
        pop.append(vec)

    # How many winners from each generation?
    topelite = int(elite * popsize)

    (best_score, num_best) = (inf, 0)
    # Main loop
    for i in range(maxiter):
        scores = [(costf(v), v) for v in pop]
        scores.sort()
        ranked = [v for (s, v) in scores]

        # Start with the pure winners
        pop = ranked[0:topelite]

        # Add mutated and bred forms of the winners
        while len(pop) < popsize:
            if random.random() < mutprob:

                # Mutation
                c = random.randint(0, topelite)
                pop.append(mutate(ranked[c]))
            else:

                # Crossover
                c1 = random.randint(0, topelite)
                c2 = random.randint(0, topelite)
                pop.append(crossover(ranked[c1], ranked[c2]))

        if (scores[0][0] < best_score):
            best_score = scores[0][0]
            num_best = 1
        elif (scores[0][0] == best_score):
            num_best += 1  # keep track of the number of times we have seen this value for a minimum
        if (num_best >= 10): break;
        if (printbest):
            print(best_score)

    return scores[0][1]

# Explain setup:
# Below, represents a solution in which Seymour takes the second flight of the day from Boston
# to New York, and the fifth flight back to Boston on the day he returns. Franny
# takes the fourth flight from Dallas to New York, and the third flight back.
s1=[1,4,3,2,7,3,6,3,2,4,5,3]
printschedule(s1)
print('Cost of solution - %', schedulecost(s1))
print("")

print("A random optimize algorithm solution")

#The function takes a couple of parameters. Domain is a list of 2-tuples that specify the
#minimum and maximum values for each variable. The length of the solution is the
#same as the length of this list. In the current example, there are nine outbound flights
#and nine inbound flights for every person, so the domain in the list is (0,8) repeated
#twice for each person.
#The second parameter, costf, is the cost function, which in this example will be
#schedulecost.
domain=[(0,8)]*(len(people)*2)
s2=randomoptimize(domain,schedulecost)
printschedule(s2)
print('Cost of solution - %', schedulecost(s2))

print("")
print("Hill climbing")

# Now try hill climbing
s3=hillclimb(domain,schedulecost)
printschedule(s3)
print('Cost of solution - %', schedulecost(s3))

print("")
print("Genetic Algorithm")

# Now try Genetic Algorithm
s4=geneticoptimize(domain,schedulecost)
printschedule(s4)
print('Cost of solution - %', schedulecost(s4))

print('Cost of solution 1: - %', schedulecost(s1))
print('Cost of solution 2: - %', schedulecost(s2))
print('Cost of solution 3: - %', schedulecost(s3))
print('Cost of solution 4: - %', schedulecost(s4))