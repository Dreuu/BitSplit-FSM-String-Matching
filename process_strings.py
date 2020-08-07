import math
import sys

# Calculates the amount of memory required for an FSM
def calculate_mem(num_nodes, pats):
    memory_requirements = []

    # = (2^1* log(Base 2)(N_S) + W_PMV) * N_S
    # = (2 * log(Base 2)(nodes) + len(pats)) * nodes
    # Summed for 8 parallel FSM networks
    for nodes in num_nodes:
        memory_requirement = 2 * math.ceil(math.log2(nodes))
        memory_requirement += len(pats)
        memory_requirement *= nodes
        memory_requirements.append(memory_requirement)
    return memory_requirements

# Calculates the number of nodes required for an FSM given input strings
def count_nodes(pats):
    prefixes = [dict() for _ in range(8)]
    node_counts = [0]*8
    max_depth = max([len(x) for x in pats])
    node_array0 = [['0']*8 for _ in range(max_depth)]
    node_array1 = [['0']*8 for _ in range(max_depth)]

    for pat_idx in range(len(pats)):
        char_bit_arr = []
        for char_idx in range(len(pats[pat_idx])):
            char_bits = bin(int.from_bytes(
                pats[pat_idx][char_idx].encode(), 'big'))
            char_bits = str(char_bits)[2:]
            if len(char_bits) < 8:
                char_bits = '0'*(8-len(char_bits)) + char_bits
            char_bit_arr.append(char_bits)

            for bit_idx in range(8):
                if char_bits[bit_idx] == '0' and node_array0[char_idx][bit_idx] != '1':
                    node_counts[bit_idx] += 1
                    node_array0[char_idx][bit_idx] = '1'
                if char_bits[bit_idx] == '1' and node_array1[char_idx][bit_idx] != '1':
                    node_counts[bit_idx] += 1
                    node_array1[char_idx][bit_idx] = '1'

    return node_counts

# Checks if string 'x' is in any of the groups within the group list 'groups'
def used(groups, x):
    for group in groups:
        if x in group:
            return True
    return False

# Calculates the correlation between two FSMs based on their
#  individual node requirements vs their joined node requirements
def correlation(group, string, ns_group, ns_string):
    new_group = group + [string]
    ns_new_group = sum(count_nodes(new_group))
    return (ns_group + ns_string) / ns_new_group

# The psuedocode represented within the research paper
# A novel method of creating groups to split strings 
def str_grp(strings, num_groups):
    n = len(strings)
    ns_strings = [sum(count_nodes([string])) for string in strings]

    print()
    print('Processing', n, 'strings')
    print()

    print('-'*60)
    print('Starting Seed Selection and Correlation Estimation Phase')
    print('-'*60)

    groups = [[strings[0]]]
    ns_groups = [ns_strings[1]]
    print('Group 1 of', num_groups, end='\r')

    # Seed Selection and Correlation Estimation Phase
    for i in range(1, num_groups):
        correlation_vector = [list()]*len(strings)
        for j in range(len(strings)):
            correlation_vector[j] = max([correlation(
                groups[x], strings[j], ns_groups[x], ns_strings[j]) for x in range(len(groups[:i]))])
        groups.append(
            [strings[correlation_vector.index(min(correlation_vector))]])
        ns_groups.append(
            ns_strings[correlation_vector.index(min(correlation_vector))])
        print('Group', i+1, 'of', num_groups, end='\r')
    print()
    print()

    print('-'*60)
    print('Starting Seed Growing Phase')
    print('-'*60)

    # Seed Growing Phase
    for idx in range(n-num_groups):
        corr_diffs = [0]*len(strings)
        for i in range(len(strings)):
            if not used(groups, strings[i]):
                correlations = [correlation(
                    groups[x], strings[i], ns_groups[x], ns_strings[i]) for x in range(len(groups))]
                correlations.sort()
                corr_diffs[i] = correlations[-1] - correlations[-2]
        if max(corr_diffs) != 0:
            most_difference_idx = corr_diffs.index(max(corr_diffs))
            correlations = [correlation(groups[x], strings[most_difference_idx],
                                        ns_groups[x], ns_strings[most_difference_idx]) for x in range(len(groups))]
            groups[correlations.index(max(correlations))].append(
                strings[most_difference_idx])
            ns_groups[correlations.index(max(correlations))] = sum(
                count_nodes(groups[correlations.index(max(correlations))]))
        else:
            for i in range(len(strings)):
                if not used(groups, strings[i]):
                    correlations = [correlation(
                        group, strings[i], ns_groups[x], ns_strings[i]) for x in range(len(groups))]
                    groups[correlations.index(
                        max(correlations))].append(string)
                    ns_groups[correlations.index(max(correlations))] = sum(
                        count_nodes(groups[correlations.index(max(correlations))]))
        print('String', idx+1, 'of', n-num_groups, end='\r')
    print()
    print()

    return groups


if __name__ == '__main__':
    # Snort rules strings for use
    # Using all 4000 strings becomes too difficult to process
    with open('snort-rule-strings.txt', 'r') as f:
        patterns = f.read().split('\n')

    string_limit = 128
    num_groups = 16
    if len(sys.argv) > 1:
        string_limit = int(sys.argv[1])
    if len(sys.argv) > 2:
        num_groups = int(sys.argv[2])

    patterns = patterns[:string_limit]
    groups = str_grp(patterns, num_groups)

    # Print memory requirement for all strings without the group splitting, but with bit-split FSMs
    print('-'*60)
    print('All words no groups')
    print()
    print(*patterns)
    print('-'*60)
    num_nodes = count_nodes(patterns)
    print(sum(num_nodes), 'nodes required')
    print(sum(calculate_mem(num_nodes, patterns)), 'bits required')
    print()
    print()

    total_memory = 0
    # Print the memory requirements of each group after group splitting, then print the total memory required
    for group_idx in range(len(groups)):
        print('-'*60)
        print('Group', group_idx+1)
        print(*groups[group_idx])
        print('-'*60)
        num_nodes = count_nodes(groups[group_idx])
        print(sum(num_nodes), 'nodes required')
        memory = sum(calculate_mem(num_nodes, groups[group_idx]))
        total_memory += memory
        print(memory, 'bits required')
        print()
        print()

    print('Total bits required =', total_memory)
    print()
    print()