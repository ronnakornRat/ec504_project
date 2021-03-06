import sys
import time
import json

from GraphAdjList import *
from matrix import *
from Visual import print_network
from scoring_func import score
### default file location
file1_location = "./data/set3_a.txt"
file2_location = "./data/set3_b.txt"

# the location of the file, relative to where we compile the program
# file1_location = "./data/4932.protein.physical.links.v11.0.txt"
# file2_location = "./data/9606.protein.physical.links.v11.0.txt"

if len(sys.argv) > 1:
    if sys.argv[1] == 's':
        if sys.argv[2].isdigit():
            file1_location = "./data/set" + sys.argv[2] + "_a.txt"
            file2_location = "./data/set" + sys.argv[2] + "_b.txt"
        else:
            print("argument after \'s\' need to be digit")
            exit(1)
    elif sys.argv[1] == 'i':
        file1_location = sys.argv[2]
        file2_location = sys.argv[3]
    else:
        print('command ', sys.argv[1], 'is not recogized')
        exit(1)

print("loading graph1 from: ", file1_location)
print("loading graph2 from: ", file2_location)

# making grpah1 and graph2, reading information from the provided file
graph1, graph2, map1, map2 = make_graph(file1_location, file2_location)
print("Making graph: done")


print("graph1: ", (graph1['max_id'] + 1), " vertices")
print("graph2: ", (graph2['max_id'] + 1), " vertices")
# a, b, lambda should be between 0 and 1
a = 1
b = 0 # we don't use biological data for this testing
lamb_da = 0.5


### called the alignment function
start_time = time.time()
result = align(graph1, graph2, a, b, lamb_da)
elapse_time = time.time() - start_time
print("Align time --- %s seconds ---" % (elapse_time))
### result is a dictionary, {id_in_graph1, id_in_graph2}, basically a bunch of matching between i,j

inv_map1 = {v: k for k, v in map1.items()}
inv_map2 = {v: k for k, v in map2.items()}

### remapped the id to the 'protein name'
mapped_result = [(inv_map1[i], inv_map2[j]) for (i,j) in result.items()]
print('Result:')
print(mapped_result)

EC_score, largest_cc = score(result, graph1, graph2)
largest_cc = list(largest_cc)
largest_cc = [inv_map1[item] for item in largest_cc]

print("edge correctness = ", EC_score)
print("largest_cc = ", largest_cc)
print("lengeth largest_cc = ", len(largest_cc))

### ouputing the result
data = {}
data['result'] = mapped_result
data['edge correctness'] = EC_score
data['LCCS'] = largest_cc
data['LCCS_len'] = len(largest_cc)

### change 'data' to the filename we want
save_location = 'result/data.json'
print('Saving result to ', save_location)
### save result into .json file
with open(save_location, 'w') as fp:
    json.dump(data, fp)

### print the 2 compared graph, with color coded
print_network(file1_location, file2_location, mapped_result)



