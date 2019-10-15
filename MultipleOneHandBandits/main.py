import numpy as np


# bandit with win threshold and payoff
class Bandit:
    def __init__(self, id):
        self.id = id
        self.win_threshold = np.random.rand()
        self.reward = np.random.randint(1,100)
        print("bandit ", self.id)
        print("     win prob: ", 1 - self.win_threshold)
        print("     win reward: ", self.reward)


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

    def choose_bandit(self):
        self.i += 1
        if(self.i < self.rand_tries_max):
            # random learning
            self.chosen_id = np.random.choice(range(self.env.bandit_count))
        else:
            # after random learning finished take the best with "(1 - epsilon)" probability, or random
            if(np.random.uniform(0, 1) > (1 - self.e)):
                self.chosen_id = np.random.choice(range(self.env.bandit_count))
            else:
                # exploit the best option
                self.chosen_id = np.argmax(self.avg_reward)

        self.b_i[self.chosen_id] += 1
        print("chose bandit " + str(self.chosen_id))
        return self.chosen_id

    def update(self, reward):
        # calculate current reward and learn
        self.total_reward[self.chosen_id] += reward
        self.avg_reward[self.chosen_id] = self.total_reward[self.chosen_id] / self.b_i[self.chosen_id]


class Environment:
    
    def __init__(self, bandit_count, n_times):
        self.n_times = n_times #max number of actions taken by an agent (steps)
        self.bandit_count = bandit_count # num of bandits
        self.bandits = []
        for i in range(bandit_count):
            self.bandits.append(Bandit(i)) #init bandits

    def run(self, agent):
        self.total_reward = 0
        agent.i = 0

        # one step within environment: agent takes an action(pull on given bandit) -> reward -> learn
        for i in range(self.n_times):
            # execute a pull on one of the bandits and get a reward 
            bandit_id = agent.choose_bandit()
            # get a random value and check if bigger than the threshold for winning
            bandit_result  = np.random.uniform(0, 1) 
            chosen_bandit = self.bandits[bandit_id]
            if(bandit_result > chosen_bandit.win_threshold):
                reward = chosen_bandit.reward
            else:
                reward = 0
            # save the reward
            agent.reward = reward
            # agent learns of reward
            agent.update(reward)
            self.total_reward += reward
            

        print("total reward: ", self.total_reward)
        return self.total_reward


env = Environment(10, 2000)
# epsilon determines with what probability to check other options that the current best one
agent = Agent(env, 0.05, 400)
env.run(agent)
