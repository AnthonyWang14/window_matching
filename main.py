import numpy as np
from samp import *
from graph import *
from max_matching import *
from batch import *
import time

class OnlineMatching:

    def __init__(self, graph = None, T = 1000) -> None:
        self.G = graph
        self.T = T
        # self.d = d


    def gene_sequence(self):
        seq = []
        quit_time = []
        for t in range(self.T):
            seq_one, quit_one = self.G.gene_an_arrival()
            seq.append(seq_one)
            quit_time.append(quit_one)
        return seq, quit_time


    def test_matching_valid(self, algo, matching, reward, seq, quit_time):
        if algo == 'OFF':
            return 
        matched_list = [0 for i in seq]
        r = 0
        for m in matching:
            ind_i = m[0]
            ind_j = m[1]
            match_time = m[2]
            if matched_list[ind_i] > 0:
                print(ind_i, 'is matched twice', algo)
                break
            if matched_list[ind_j] > 0:
                print(ind_j, 'is matched twice', algo)
                break
            if (match_time-ind_i)>quit_time[ind_i] or (match_time-ind_j)>quit_time[ind_j]:
                print('error quit time', algo)
                break
            matched_list[ind_i] = 1
            matched_list[ind_j] = 1
            u = seq[m[0]]
            v = seq[m[1]]
            r += self.G.weights[u][v]
        if np.abs((r-reward)) > 1e-5:
            print('error reward', algo)
        return

    def run_test(self, algo_list = ['OFF'], test_num = 1):
        reward_list_dict = {}
        algo_result = {}
        algo_mean = {}
        run_time = {}
        for algo in algo_list:
            algo_result[algo] = []
            run_time[algo] = 0
        for k in range(test_num):
            seq, quit_time = self.gene_sequence()
            # print(quit_time)
            for algo in algo_list:
                start = time.time()
                reward = 0
                matching = []
                print('run', algo)

                if algo == 'SAMP':
                    samp = Samp(graph=self.G, seq=seq, quit_time=quit_time, gamma = 1)
                    reward = samp.eval()
                    matching = samp.matching
                
                if algo == 'BATCH_MEAN':
                    batch_mean_match = BatchMatching(graph=self.G, seq=seq, quit_time=quit_time, batch_type='MEAN')
                    reward = batch_mean_match.eval()
                    matching = batch_mean_match.matching

                if algo == 'BATCH_MIN':
                    batch_min_match = BatchMatching(graph=self.G, seq=seq, quit_time=quit_time, batch_type='MIN')
                    reward = batch_min_match.eval()
                    matching = batch_min_match.matching
                    print(matching)

                if algo == 'OFF':
                    alive = [1 for i in range(len(seq))]
                    max_match = MaxMatching(graph=self.G, seq=seq, quit_time=quit_time, alive=alive)
                    reward = max_match.eval()
                    matching = max_match.matching

                algo_result[algo].append(reward)
                run_time[algo] += time.time() - start
                # print(algo, matching)
                self.test_matching_valid(algo, matching, reward, seq, quit_time)

        for algo in algo_list:
            algo_mean[algo] = np.mean(algo_result[algo])
        for algo in algo_list:
            print(algo, algo_mean[algo]/algo_mean['OFF'])
        # print(algo_result)
        print('run time', run_time)
        return(algo_result)


if __name__ == '__main__':
    np.random.seed(0)
    g = Graph(type_number = 30, weights = None)
    # g.show_details()
    # d = 10
    T = 2000
    # g.extend(d)
    # print(g.weights, g.rates, g.N)
    online_match = OnlineMatching(g, T=T)
    online_match.run_test(algo_list=['SAMP', 'BATCH_MIN', 'BATCH_MEAN', 'OFF'], test_num=2)