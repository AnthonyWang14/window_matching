import numpy as np
import random

# underlying graph
class Graph:
    def __init__(self, type_number = 10, weights = None, rates = None, quit_dist = None) -> None:
        np.random.seed(0)
        self.N = type_number
        # print(weights)
        if weights:
            self.weights = weights
        # randomized weights
        else:
            self.gene_weights()

        if rates:
            self.rates = rates
        else:
            self.gene_rates()

        if quit_dist:
            self.quit_dist = quit_dist
            self.mean_quit_time = []
            for i in range(len(self.quit_dist)):
                self.mean_quit_time.append(int((self.quit_dist['value'][-1]+self.quit_dist['value'][0])/2))
        else:
            self.gene_quit_dist()
    
    def gene_weights(self):
        self.weights = np.random.uniform(0, 1, (self.N, self.N))
        for i in range(self.N):
            for j in range(self.N):
                if j >= i:
                    q = np.random.uniform(0, 1)
                    if q < 0.95:
                        q = 0
                    self.weights[i][j] = q
                    self.weights[j][i] = q

    def gene_rates(self):
        # identical
        # self.rates = [1./self.N for i in range(self.N)]
        # uniform distribution
        r = np.random.uniform(0, 1, self.N)
        self.rates = [l/np.sum(r) for l in r]

    def gene_quit_dist(self):
        d_min = 5
        d_max = 20
        d_range = 2
        self.mean_quit_time = []
        self.quit_dist = []
        for i in range(self.N):
            realized_mean = random.randint(d_min, d_max)
            realized_range = random.randint(0, d_range)
            quit_value = list(range(realized_mean-realized_range, realized_mean+realized_range+1))
            quit_prob = [1/len(quit_value) for i in range(len(quit_value))]
            self.quit_dist.append({'value': quit_value, 'prob': quit_prob})
            self.mean_quit_time.append(realized_mean)
        print(self.quit_dist)
    
    def gene_quit_time(self, ind):
        val = self.quit_dist[ind]['value']
        prob = self.quit_dist[ind]['prob']
        q = np.random.random()
        cum_prob = 0
        for ind in range(len(val)):
            cum_prob += prob[ind]
            if q <= cum_prob+1e-5:
                break
        return val[ind]
    
    def gene_an_arrival(self):
        q = np.random.random()
        cum_prob = 0
        # print('q', q)
        for ind in range(self.N):
            cum_prob += self.rates[ind]
            # print(ind, cum_prob)
            if q <= cum_prob+1e-5:
                qt = self.gene_quit_time(ind)
                return ind, qt        
        
    def show_details(self):
        print('weights')
        print(self.weights)
        print('*'*100)
        print('rates')
        print(self.rates)

    def extend(self, d):
        extend_type = []
        extend_rates = []
        for i in range(len(self.rates)):
            k = int(self.rates[i]*d)
            # print(k)
            for j in range(k):
                extend_type.append(i)
                extend_rates.append(1/d)
            if (self.rates[i]-k/d > 1e-5):
                extend_type.append(i)
                extend_rates.append(self.rates[i]-k/d)
        extend_N = len(extend_type)
        extend_weights = np.random.uniform(0, 1, (extend_N, extend_N))
        for i in range(extend_N):
            for j in range(extend_N):
                extend_weights[i][j] = self.weights[extend_type[i]][extend_type[j]]
        self.rates = extend_rates
        self.weights = extend_weights
        self.N = extend_N
        pass

if __name__ == '__main__':
    g = Graph()
    print(g.weights, g.rates)



    

    


    
    
