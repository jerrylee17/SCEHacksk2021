import pprint
import os
import csv
import boto3

s3 = boto3.resource("s3")

from typing import Dict, List

pp = pprint.PrettyPrinter(indent=4)


class WildfireModel:
    def __init__(
        self, default_risk: float, spawned_fires: List[int], gamma: float, wind_map
    ):
        # How easy it is for the fire to spread at every location in the map - R(s)
        self.default_risk = default_risk
        self.fire_map = [self.default_risk] * 10

        # Spawn a fire at location 8
        self.spawned_fires = spawned_fires
        # Put spawned fires into fire map
        for f in self.spawned_fires:
            self.fire_map[f] = 1

        self.gamma = gamma
        self.wind_map = wind_map

        self._max_wind = max(
            [max([v for v in value.values()] + [0]) for value in self.wind_map.values()]
        )

        if self._max_wind >= 1:
            self._standardize_wind_map()


        # Generate negative weights
        self._generate_wind_map_negatives()

        self._invert_wind_map()

        # pp.pprint(self.wind_map)

        # Initial U(s)
        self.utility = [0] * 10

    # Invert wind map
    def _invert_wind_map(self):
        for key, value in self.wind_map.items():
            for k, v in value.items():
                self.wind_map[key][k] *= -1

    # Standardize wind map to highest wind
    def _standardize_wind_map(self):
        for key, value in self.wind_map.items():
            for k, v in value.items():
                if v is not None and v > 0:
                    self.wind_map[key][k] = (
                        0.95 * self.wind_map[key][k] / self._max_wind
                    )

    # Revert the utility values to scale with highest wind
    def _revert_utility_values(self):
        for i in range(len(self.utility)):
            self.utility[i] = round(self.utility[i] * self._max_wind, 5)

    # Generate negatives in wind map
    def _generate_wind_map_negatives(self):
        for key, value in self.wind_map.items():
            for k, v in value.items():
                if v is not None and v > 0:
                    self.wind_map[k][key] = -1 * self.wind_map[key][k]
                    # self.wind_map[k][key] = 0
                # if v < 0:
                #     self.wind_map[key][k] = 0

    # Bellman iteration on node
    def _bellman_iteration_on_node(self, x, u):
        if x in self.spawned_fires:
            return 1
        pathValues = []
        # Iteration on neighbors
        for loc, probability in self.wind_map[x].items():
            if probability is None:
                continue
            pathValues.append(probability * u[loc])
        if len(pathValues) == 0:
            pathValues.append(0)
        utility_value = round(self.fire_map[x] + self.gamma * max(pathValues), 5)
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

        self.remove_negatives()
        print(f'============={i}TH ITERATION=============')
        # Revert utility values
        # if self._max_wind >= 1:
        #     self._revert_utility_values()
        # print(f'============={i}TH ITERATION=============')
        # pp.pprint([(j, val) for j, val in enumerate(self.utility)])
        # print(f'=============SORTED IN ORDER OF RISK=============')
        # pp.pprint(sorted([(j, val) for j, val in enumerate(self.utility)], key=lambda x: x[1], reverse=True))
    def remove_negatives(self):
        for i, x in enumerate(self.utility):
            if x < 0:
                self.utility[i] = 0
            # self.utility[i] = min(self.utility[i] + 0.3, 1)

    def display(self):
        print(f"=============UNSORTED=============")
        pp.pprint([(j, val) for j, val in enumerate(self.utility)])
        print(f"=============SORTED IN ORDER OF RISK=============")
        pp.pprint(
            sorted(
                [(j, val) for j, val in enumerate(self.utility)],
                key=lambda x: x[1],
                reverse=True,
            )
        )

    def to_csv(self, file_path="./tmp/output.csv"):
        with open(file_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            for i, value in enumerate(self.utility):
                writer.writerow([i, value])

    def upload_to_s3(self, file_path="./tmp/output.csv", bucket_name="sce-hacks-arson"):
        s3 = boto3.resource("s3")
        s3.meta.client.upload_file(file_path, bucket_name, os.path.split(file_path)[1])


"""
Assume map looks like this
  0
1 2 3
4 5 6
7 8 9

    - Wind speed needs to be standardized between 0 and 1
"""

"""
Wind map (probabilities)
Negative = wind going out
Positive = wind coming in
For ex: Wind going from 0 --> 2 will be represented like the following
    - 0: {2: -0.9}
    - 2: {0: 0.9}
"""

WIND_PROBABILITY_MAP = {
    0: {2: -0.9},
    1: {2: -0.3, 4: -0.5},
    2: {0: 0.9, 1: 0.3, 3: -0.6, 5: -0.5},
    3: {2: 0.6, 6: -0.5},
    4: {1: 0.5, 5: -0.9, 7: 0.3},
    5: {2: 0.5, 4: 0.9, 6: -0.6, 8: 0.5},
    6: {3: 0.5, 5: 0.6, 9: 0.3},
    7: {4: -0.3, 8: -0.5},
    8: {5: -0.5, 7: 0.5, 9: -0.3},
    9: {6: -0.3, 8: 0.3},
}

WIND_VALUE_MAP = {
    0: {},
    1: {},
    2: {0: 12, 1: 4},
    3: {2: 8},
    4: {1: 7, 7: 4},
    5: {2: 7, 4: 12, 8: 7},
    6: {3: 7, 5: 8, 9: 4},
    7: {},
    8: {7: 7},
    9: {8: 4},
}

# Graph
GRAPH = {
    0: {1, 2, 4, 5, 6, 7, 8},
    1: {0, 2, 8, 9},
    2: {0, 1, 4},
    3: {2, 4},
    4: {0, 2, 3, 5, 6},
    5: {0, 4, 6},
    6: {0, 4, 5, 7},
    7: {0, 6, 8},
    8: {0, 1, 7, 9},
    9: {1, 8},
}

WIND_SIMULATION_1 = {
    0: {1: 18, 8: 25},
    1: {},
    2: {0: 20, 1: 8, 4: 10},
    3: {2: 15, 4: 12},
    4: {0: 12, 2: 4, 5: 4, 6: 2},
    5: {0: 5, 6: 10},
    6: {0: 10},
    7: {0: 11, 6: 8},
    8: {0: 10, 1: 10, 7: 12},
    9: {1: 20, 8: 15},
}

# Southeast breeze
WIND_SIMULATION_2 = {
    0: {6: 4, 7: 5, 8: 11},
    1: {0: 15, 8: 11, 9: 8},
    2: {0: 10, 1: 7, 4: 11},
    3: {2: 10, 4: 12},
    4: {0: 6, 5: 10, 6: 4},
    5: {6: 17},
    6: {7: 15},
    7: {},
    8: {7: 11},
    9: {9: 10},
}

for key, value in WIND_PROBABILITY_MAP.items():
    for k, v in value.items():
        if v is not None and v > 0:
            WIND_PROBABILITY_MAP[key][k] = 14 * WIND_PROBABILITY_MAP[key][k]
        else:
            WIND_PROBABILITY_MAP[key][k] = None

DEFAULT_RISK = 0.02
SPAWNED_FIRES = [0, 3, 9]
GAMMA = 0.8
model = WildfireModel(DEFAULT_RISK, SPAWNED_FIRES, GAMMA, WIND_SIMULATION_2)
model.score()
model.display()
model.to_csv()
# model.upload_to_s3()
