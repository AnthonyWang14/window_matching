import numpy as np
import random
# from numpy.random import default_rng

# underlying graph
class Graph:
    def __init__(self, type_number = 10, dist_type = 'geometric', density = 1, shift_mean=0,weights = None, rates = None) -> None:
        np.random.seed(0)
        self.N = type_number
        self.density = density
        self.sparsity = 1-2/self.N*self.density
        self.shift_mean = shift_mean
        # print(weights)
        if weights:
            self.weights = weights
        # randomized weights
        else:
            self.gene_weights()

        if rates:
            self.rates = np.array(rates)
        else:
            self.gene_rates()

        self.dist_type = dist_type
        self.gene_quit_dist()
        self.check_lam_dx()
    
    def check_lam_dx(self):
        larger_one_count = 0
        for i in range(self.N):
            if self.mean_quit_time[i]*self.rates[i]>1:
                larger_one_count += 1
        print('larger_one_count', larger_one_count)
        
    def gene_weights(self):
        self.weights = np.random.uniform(0, 1, (self.N, self.N))
        for i in range(self.N):
            for j in range(self.N):
                if j >= i:
                    q = np.random.uniform(0, 1)
                    # only consider sparse when N>5
                    if self.N > 5:
                        if q < self.sparsity:
                            q = 0
                    self.weights[i][j] = q
                    self.weights[j][i] = q

    def gene_rates(self):
        r = np.random.uniform(0, 1, self.N)
        self.rates = np.array([l/np.sum(r) for l in r])

    def gene_quit_dist(self):
        # need define quit_pamameter, mean quit time list
        self.dist_paras = []
        self.mean_quit_time = []

        if self.dist_type == 'geometric':
            # need one parameter p > 0.5
            # self.dist_paras = []
            min_p = 0.5
            for i in range(self.N):
                p = np.random.rand()*(1-min_p)+min_p
                self.dist_paras.append(p)
                self.mean_quit_time.append(1/p)
        
        if self.dist_type == 'shift_geo':
            # need one parameter p > 0.5
            # self.dist_paras = []
            min_p = 0.5
            for i in range(self.N):
                paras = {}
                paras['dev'] = np.random.randint(0,2*self.shift_mean)
                paras['p'] = np.random.rand()*(1-min_p)+min_p
                self.dist_paras.append(paras)
                self.mean_quit_time.append(1/paras['p']+paras['dev'])

        if self.dist_type == 'single':
            for i in range(self.N):
                n = np.random.randint(10, 50)
                self.dist_paras.append(n)
                self.mean_quit_time.append(n)

        if self.dist_type == 'binomial':
            min_p = 0.5
            for i in range(self.N):
                paras = {}
                paras['n'] = np.random.randint(10, 50)
                paras['p'] = np.random.rand()
                # paras['p'] = np.random.rand()*(1-min_p)+min_p
                paras['dev'] = 0
                self.dist_paras.append(paras)
                self.mean_quit_time.append(paras['n']*paras['p']+paras['dev'])

        if self.dist_type == 'poisson':
            for i in range(self.N):
                paras = {}
                paras['lam'] = 10*np.random.rand()
                paras['dev'] = 0
                self.dist_paras.append(paras)
                self.mean_quit_time.append(paras['lam']+paras['dev'])
            
        if self.dist_type == 'uniform':
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

        if self.dist_type == 'geometric':
            p = self.dist_paras[ind]
            # z = np.random.geometric(p)
            return np.random.geometric(p)

        if self.dist_type == 'binomial':
            n = self.dist_paras[ind]['n']
            p = self.dist_paras[ind]['p']
            dev = self.dist_paras[ind]['dev']
            return np.random.binomial(n, p)+dev

        if self.dist_type == 'poisson':
            lam = self.dist_paras[ind]['lam']
            dev = self.dist_paras[ind]['dev']
            return np.random.poisson(lam)+dev

        if self.dist_type == 'shift_geo':
            p = self.dist_paras[ind]['p']
            dev = self.dist_paras[ind]['dev']
            return np.random.geometric(p)+dev

        if self.dist_type == 'single':
            return self.dist_paras[ind]

        if self.dist_type == 'uniform':
            val = self.quit_dist[ind]['value']
            prob = self.quit_dist[ind]['prob']
            q = np.random.random()
            cum_prob = 0
            for x in range(len(val)):
                cum_prob += prob[x]
                if q <= cum_prob+1e-5:
                    break
            return val[x]
    
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



    

    


    
    
