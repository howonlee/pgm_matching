import networkx as nx
import sys
import random
import collections
import itertools
import operator
import cProfile

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

def get_seeds(src_net, tgt_net, num_seeds):
    src_degs = sorted(nx.degree(src_net).items(), key=operator.itemgetter(1), reverse=True)
    tgt_degs = sorted(nx.degree(tgt_net).items(), key=operator.itemgetter(1), reverse=True)
    #ordered_maps = zip(map(operator.itemgetter(0), src_degs), map(operator.itemgetter(0), tgt_degs))
    ordered_maps = zip(map(operator.itemgetter(0), src_degs), map(operator.itemgetter(0), src_degs))
    return list(itertools.islice(ordered_maps, num_seeds))

def pgm(net1, net2, seeds, r): #seeds is a list of tups
    marks = collections.defaultdict(int)
    imp_1 = {} #impossible tails
    imp_2 = {} #impossible heads
    unused = seeds[:]
    used = []
    t = 0
    while unused:
        t += 1
        t2 = 0
        print "t: ", t
        print "number impossibles: ", len(imp_1), len(imp_2)
        print "number unused: ", len(unused)
        curr_pair = unused.pop(random.randint(0,len(unused)-1))
        for neighbor in itertools.product(net1.neighbors(curr_pair[0]), net2.neighbors(curr_pair[1])):
            if imp_1.has_key(neighbor[0]) or imp_2.has_key(neighbor[1]):
                continue
            marks[neighbor] += 1
            t2 += 1
            if t2 % 250000 == 0:
                #this is an awful hack
                break
            if marks[neighbor] > r:
                unused.append(neighbor)
                imp_1[neighbor[0]] = True
                imp_2[neighbor[1]] = True
        used.append(curr_pair)
    return used

def score_easy(pgm_res):
    corrects = len([x for x in pgm_res if x[0] == x[1]])
    print "correct / total: ", corrects, " / ", len(pgm_res)

if __name__ == "__main__":
    with open("corpus.txt", "r") as corpus_file:
        total_corpus = corpus_file.read().split()
        washed, word_map = wash_words(total_corpus)
        net = word_net(washed)
        #net = nx.gnp_random_graph(1000, 0.5)
        src_net = select_net(net)
        tgt_net = select_net(net)
        seeds = get_seeds(src_net, tgt_net, 1000)
        score_easy(pgm(src_net, tgt_net, seeds, 4))
