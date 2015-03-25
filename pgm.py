import networkx as nx
import random

def wash_words(word_ls):
    word_map = {}
    curr_idx = 0
    for word in word_ls:
        if word not in word_map:
            word_map[word] = curr_idx
            curr_idx += 1
    return [word_map[word] for word in word_ls], word_map

def word_net(corpus_ls):
    """
    Takes a list of numbers
    Do the number map if you want the words back
    In this case, usually don't want the words back
    """
    bigrams = zip(corpus_ls, corpus_ls[1:])
    net = nx.Graph()
    net.add_edges_from(bigrams)
    return net

def select_net(net, p=0.9):
    new_net = nx.Graph()
    edge_list = net.edges()
    new_net_edges = []
    for edge in edge_list:
        if random.random() < p:
            new_net_edges.append(edge)
    new_net.add_edges_from(new_net_edges)
    return new_net

def pgm(net, seeds):
    pass
    """
    a = b = seeds
    z = []
    t = 0
    while a - z:
        t += 1
        #randomly select a pair p from the previous a - z and add one mark to all neighbor pair of p
        b_delta = [] #set of all neighboring pairs of p whose mark counter has reached threshhold r at time t
        a_delta = filter(has_no_conflicting_pair, b_delta)#is a subset of b_delta; order the pairs
        z = z union p
        b = b union b_delta
        a = a union a_delta
    return t, a
    """


if __name__ == "__main__":
    with open("corpus.txt", "r") as corpus_file:
        total_corpus = corpus_file.read().split()
        washed, word_map = wash_words(total_corpus)
        net = word_net(washed)
        src_net = select_net(net)
        tgt_net = select_net(net)
