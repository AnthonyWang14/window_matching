from graph import *

class GreedyMatching:
    
    def __init__(self, graph, seq, quit_time) -> None:
        self.G = graph
        self.seq = seq
        self.quit_time = quit_time

    