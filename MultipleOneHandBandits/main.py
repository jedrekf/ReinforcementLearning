import numpy as np
import random
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

# bandit with win threshold and payoff
class Bandit:
    def __init__(self, id):
        self.id = id
        self.win_threshold = random.randrange(10, 200)/1000
        self.avg = np.random.rand()
        print("bandit ", self.id)
        print("     win threshold: ", 1 - self.win_threshold)

    def play(self):
        result = np.random.uniform(0, 1)
        if result > self.win_threshold:
            reward = np.random.normal(self.avg, 1)
            # make minimum reward like this
            if reward < 0.01:
                return 0.01
            else:
                return reward
        else:
            return 0


class Agent:
    def __init__(self, env, epsilon, rand_tries_max):
        self.env = env
        self.rand_tries_max = rand_tries_max # how many tries should be random at first to determine the best bandit
        self.avg_reward = np.zeros(len(env.bandits)) #array of average rewards for given bandit id
        self.total_reward = np.zeros(len(env.bandits)) # total rewards for given bandits
        self.expected_reward = np.zeros(len(env.bandits)) # maybe just avg or maybe calculate some change in values
        self.b_i = np.zeros(len(env.bandits))  #how many times given bandit was selected
        self.e = epsilon # how often to check other that the best option
        # for a step
        self.i = 0 # iteration number
        self.chosen_id = 0 # current chosen bandit
        self.reward = 0 # reward obtained for chosen bandit
        self.data = dict(total=[], avg=[]) # history of total reward for steps, and averages

    def choose_bandit(self):
        self.i += 1
        if(self.i < self.rand_tries_max):
            # random learning
            self.chosen_id = np.random.choice(env.banditids)
        else:
            # after random learning finished take the best with "(1 - epsilon)" probability
            if(np.random.uniform(0, 1) > (1 - self.e)):
                # if it is a random explore then get the random bandit id that is not the current best one
                self.chosen_id = np.random.choice([x for x in env.banditids if x != np.argmax(self.avg_reward)])
            else:
                # exploit the best option
                self.chosen_id = np.argmax(self.avg_reward)

        self.b_i[self.chosen_id] += 1
        return self.chosen_id

    def update(self, reward):
        # calculate current reward and learn
        self.total_reward[self.chosen_id] += reward
        self.avg_reward[self.chosen_id] = self.total_reward[self.chosen_id] / self.b_i[self.chosen_id]
        self.data['total'].append(sum(self.total_reward))
        self.data['avg'].append(np.max(self.avg_reward))


class Environment:    
    def __init__(self, bandit_count, n_times):
        self.n_times = n_times #max number of actions taken by an agent (steps)
        self.banditids = [x for x in range(bandit_count)] #ids of bandits from 0 to bandit_count
        self.bandits = []
        for i in self.banditids:
            self.bandits.append(Bandit(i)) #init bandits

    def run(self, agent):
        self.total_reward = 0
        agent.i = 0

        # one step within environment: agent takes an action(pull on given bandit) -> reward -> learn
        for i in range(self.n_times):
            # execute a pull on one of the bandits and get a reward 
            bandit_id = agent.choose_bandit()

            # get a random value and check if bigger than the threshold for winning
            reward = self.bandits[bandit_id].play()
            
            # save the reward
            agent.reward = reward
            # agent learns of reward
            agent.update(reward)
            self.total_reward += reward

        return self.total_reward


# run tests
env = Environment(10, 500)
eps = [0.0, 0.1, 0.01]
rand = [30, 30, 30]
totals = []
averages = []
for t in zip(eps, rand):
    agent = Agent(env, t[0], t[1])
    print("eps: ", t[0], "random tries count: ", t[1], "total reward: ", env.run(agent))    
    totals.append(agent.data['total'])
    averages.append(agent.data['avg'])

# plot
plt.figure(1)

for i, ep in enumerate(eps):
    plt.plot(totals[i], label=str(ep))

plt.legend()


plt.figure(2)
for i, ep in enumerate(eps):
    plt.plot(averages[i], label=str(ep))
plt.legend()

plt.show()
