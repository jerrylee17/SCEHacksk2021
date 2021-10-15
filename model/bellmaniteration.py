import pprint
pp = pprint.PrettyPrinter(indent=4)

'''
Assume map looks like this
  0
1 2 3
4 5 6
7 8 9

    - Wind speed needs to be standardized between 0 and 1
'''

'''
Wind map (probabilities)
Negative = wind going out
Positive = wind coming in
For ex: Wind going from 0 --> 2 will be represented like the following
    - 0: {2: -0.9}
    - 2: {0: 0.9}
'''
windMap = {
    0: {2: -0.9},
    1: {2: -0.3, 4: -0.5},
    2: {0: 0.9, 1: 0.3, 3: -0.6, 5: -0.5},
    3: {2: 0.6, 6: -0.5},
    4: {1: 0.5, 5: -0.9, 7: 0.3},
    5: {2: 0.5, 4: 0.9, 6: -0.6, 8: 0.5},
    6: {3: 0.5, 5: 0.6, 9: 0.3},
    7: {4: -0.3, 8: -0.5},
    8: {5: -0.5, 7: 0.5, 9: -0.3},
    9: {6: -0.3, 8: 0.3}
}

# Generate negatives in wind map
def genNegatives(p):
    for key, value in p.items():
        for k, v in value.items():
            if v is not None and v > 0:
                p[k][key] = -1*p[key][k]

genNegatives(windMap)

# How easy it is for the fire to spread at every location in the map - R(s)
default_risk = 0.02
fireMap = [default_risk]*10

# Spawn a fire at location 8
spawnedFire = [0, 8]
# Put spawned fires into fire map
for f in spawnedFire:
    fireMap[f] = 1

# Gamma
G = 0.8

def fireBellmanIteration(x, u):
    if x in spawnedFire:
        return 1
    pathValues = []
    # Iteration on neighbors
    for loc, probability in windMap[x].items():
        if probability is None:
            continue
        pathValues.append(probability*u[loc])
    if len(pathValues) == 0:
        pathValues.append(0)
    Us = round(
        fireMap[x] + G * max(pathValues),
        5
    )
    return Us

def fireBellman():
    # Initial U(s)
    fire = [0]*10

    # 100 iterations at most to reach equilibrium
    for i in range(100):
        tmp = fire.copy()
        for x in range(len(fire)):
            tmp[x] = fireBellmanIteration(x, fire)
        if fire == tmp:
            break
        fire = tmp
    print(f'============={i}TH ITERATION=============')
    pp.pprint([(j, val) for j, val in enumerate(fire)])
    print(f'=============SORTED IN ORDER OF RISK=============')
    pp.pprint(sorted([(j, val) for j, val in enumerate(fire)], key=lambda x: x[1], reverse=True))

fireBellman()
