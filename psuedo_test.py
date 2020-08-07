import math

def count(d):
	return sum([count(v)+1 if len(v) > 0 else 1 for v in d.values()])
	
def calculate_mem(num_nodes, pats):
	memory_requirements = []
	for nodes in num_nodes:
		memory_requirement = 2 * math.ceil(math.log2(nodes))
		memory_requirement += len(pats)
		memory_requirement *= nodes
		memory_requirements.append(memory_requirement)
	return memory_requirements
	
def count_nodes(pats):
	prefixes = [dict() for _ in range(8)]
	node_counts = [0]*8
	
	for pat_idx in range(len(pats)):
		char_bit_arr = []
		for char_idx in range(len(pats[pat_idx])):
			char_bits = bin(int.from_bytes(pats[pat_idx][char_idx].encode(), 'big'))
			char_bits = str(char_bits)[2:]
			if len(char_bits) < 8:
				char_bits = '0'*(8-len(char_bits)) + char_bits
			char_bit_arr.append(char_bits)
			for bit_idx in range(8):
				cur_char = char_bits[bit_idx]
				if char_idx == 0:
					if cur_char not in prefixes[bit_idx]:
						prefixes[bit_idx][cur_char] = dict()
						node_counts[bit_idx] += 1
						continue
						
				t_dict = prefixes[bit_idx]
				for i in range(char_idx):
					t_dict = t_dict[char_bit_arr[i][bit_idx]]
				if cur_char not in t_dict:
					t_dict[cur_char] = dict()
					node_counts[bit_idx] += 1
	
	#[[print(str(bin(int.from_bytes(char.encode(), 'big')))[2:]) for char in pat] for pat in pats]
	#[print(x) for x in prefixes]
	
	#num_nodes = [count(x) for x in prefixes]
	#print(num_nodes)
	#print(node_counts)
	
	return node_counts
	
def used(groups, x):
	for group in groups:
		if x in group:
			return True
	return False

def correlation(group, string, ns_group, ns_string):
	new_group = group + [string]
	
	ns_new_group = sum(count_nodes(new_group))
	
	return (ns_group + ns_string) / ns_new_group

def str_grp(strings, num_groups):
	n = len(strings)
	ns_strings = [sum(count_nodes([string])) for string in strings]
	
	print()
	print('Processing',n,'strings')
	print()
	
	print('-'*60)
	print('Starting Seed Selection and Correlation Estimation Phase')
	print('-'*60)
	
	groups = [[strings[0]]]
	ns_groups = [ns_strings[1]]
	print('Group 1 of',num_groups)
	
	#Seed Selection and Correlation Estimation Phase
	for i in range(1, num_groups):
		correlation_vector = [list()]*len(strings)
		for j in range(len(strings)):
			correlation_vector[j] = max([correlation(groups[x],strings[j], ns_groups[x], ns_strings[j]) for x in range(len(groups[:i]))])
		groups.append([strings[correlation_vector.index(min(correlation_vector))]])
		ns_groups.append(ns_strings[correlation_vector.index(min(correlation_vector))])
		print('Group',i+1,'of',num_groups)
	print()
		
	#print(groups)
	
	
	print('-'*60)
	print('Starting Seed Growing Phase')
	print('-'*60)
	
	#Seed Growing Phase
	for idx in range(n-num_groups):
		corr_diffs = [0]*len(strings)
		for i in range(len(strings)):
			if not used(groups, strings[i]):
				correlations = [correlation(group[x], strings[i], ns_groups[x], ns_strings[i]) for x in range(len(groups))]
				correlations.sort()
				corr_diffs[i] = correlations[-1] - correlations[-2]
		if max(corr_diffs) != 0:
			most_difference_idx = corr_diffs.index(max(corr_diffs))		
			correlations = [correlation(groups[x], strings[most_difference_idx], ns_groups[x], ns_strings[most_difference_idx]) for x in range(len(groups))]
			groups[correlations.index(max(correlations))].append(strings[most_difference_idx])
			ns_groups[correlations.index(max(correlations))] = count_nodes(groups[correlations.index(max(correlations))])
		else:
			for i in range(len(strings)):
				if not used(groups, strings[i]):
					correlations = [correlation(group, strings[i], ns_groups[x], ns_strings[i]) for x in range(len(groups))]
					groups[correlations.index(max(correlations))].append(string)
					ns_groups[correlations.index(max(correlations))] = count_nodes(groups[correlations.index(max(correlations))])
		print('String',idx+1,'of',n-num_groups)
	print()
		
	return groups
	
	
if __name__=='__main__':
	patterns = ["neck","private","busy","inch","changing","health","subject","unhappy","area","balloon","scientific","ring","silly","top","clearly","solution","itself","court","small","on","slow","mouse","below","season","foot","difference","handsome","related","when","practical","sand","spin","afraid","proper","trade","interest","including","till","fairly","wood","must","brother","gate","color","is","camera","blow","came","mark","butter","keep","colony","force","cotton","trap","terrible","salt","grade","enough","gave","activity","rate","firm","term","difficulty","pattern","syllable","forest","pipe","except","horn","temperature","paint","mix","pack","judge","design","art","rule","however","command","went","stone","his","dear","action","properly","divide","beauty","similar","save","direct","strong","necessary","detail","usually","over","built","pound"]
	
	with open('snort-rule-strings.txt', 'r') as f:
		patterns = f.read().split('\n')
		
	groups = str_grp(patterns, 128)
	
	
	print('-'*60)
	print('All words no groups')
	print()
	print(*patterns)
	print('-'*60)
	
	num_nodes = count_nodes(patterns)
	print(sum(num_nodes),'nodes required')
	print(sum(calculate_mem(num_nodes, patterns)),'bits required')
	print()
	print()
	
	total_memory = 0
	for group_idx in range(len(groups)):
		print('-'*60)
		print('Group',group_idx+1)
		print(*groups[group_idx])
		print('-'*60)
		num_nodes =count_nodes(groups[group_idx])
		print(sum(num_nodes),'nodes required')
		memory = sum(calculate_mem(num_nodes, groups[group_idx]))
		total_memory += memory
		print(memory,'bits required')
		print()
		print()
	
	print('Total bits required =',total_memory)
	print()
	print()
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	