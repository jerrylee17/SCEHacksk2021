import pprint
from typing import Dict, List
pp = pprint.PrettyPrinter(indent=4)

class WildfireModel:

    def __init__(self, default_risk : float, spawned_fires: List[int], gamma: float, wind_map):
        # How easy it is for the fire to spread at every location in the map - R(s)
        self.default_risk = default_risk
        self.fire_map = [self.default_risk]*10

        # Spawn a fire at location 8
        self.spawned_fires = spawned_fires
        # Put spawned fires into fire map
        for f in self.spawned_fires:
            self.fire_map[f] = 1

        self.gamma = gamma
        self.wind_map = wind_map
        
        self.max_wind = max([
            max([v for v in value.values()]) for value in self.wind_map.values()
        ])
        print(self.max_wind)
        self._standardize_wind_map()

        # Generate negative weights
        self._generate_wind_map_negatives()

        # Initial U(s)
        self.utility = [0]*10

    # Standardize wind map to highest wind
    def _standardize_wind_map(self):
        pass

    # Revert wind map
    def _revert_wind_map(self):
        pass

    # Generate negatives in wind map
    def _generate_wind_map_negatives(self):
        for key, value in self.wind_map.items():
            for k, v in value.items():
                if v is not None and v > 0:
                    self.wind_map[k][key] = -1*self.wind_map[key][k]

    # Bellman iteration on node
    def _bellman_iteration_on_node(self, x, u):
        if x in self.spawned_fires:
            return 1
        pathValues = []
        # Iteration on neighbors
        for loc, probability in self.wind_map[x].items():
            if probability is None:
                continue
            pathValues.append(probability*u[loc])
        if len(pathValues) == 0:
            pathValues.append(0)
        utility_value = round(
            self.fire_map[x] + self.gamma * max(pathValues),
            5
        )
        return utility_value

    # Start off bellman iteration
    def score(self):

        # 100 iterations at most to reach equilibrium
        for i in range(100):
            tmp = self.utility.copy()
            for x in range(len(self.utility)):
                tmp[x] = self._bellman_iteration_on_node(x, self.utility)
            if self.utility == tmp:
                break
            self.utility = tmp
        # print(f'============={i}TH ITERATION=============')
        # pp.pprint([(j, val) for j, val in enumerate(self.utility)])
        # print(f'=============SORTED IN ORDER OF RISK=============')
        # pp.pprint(sorted([(j, val) for j, val in enumerate(self.utility)], key=lambda x: x[1], reverse=True))

    def display(self):
        print(f'=============UNSORTED=============')
        pp.pprint([(j, val) for j, val in enumerate(self.utility)])
        print(f'=============SORTED IN ORDER OF RISK=============')
        pp.pprint(sorted([(j, val) for j, val in enumerate(self.utility)], key=lambda x: x[1], reverse=True))


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
WIND_MAP = {
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

DEFAULT_RISK = 0.02
SPAWNED_FIRES = [0,8]
GAMMA = 0.8
model = WildfireModel(DEFAULT_RISK, SPAWNED_FIRES, GAMMA, WIND_MAP)
model.score()
model.display()
