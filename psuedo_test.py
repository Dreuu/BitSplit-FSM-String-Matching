def count(d):
	return sum([count(v)+1 if len(v) > 0 else 1 for v in d.values()])
	
def count_nodes(pats):
	prefixes = [{}]*8
	
	for pat in pats:
		for char_idx in range(len(pat)):
			char_bits = bin(int.from_bytes(pat[char_idx].encode(), 'big'))
			char_bits = str(char_bits)[2:]
			if len(char_bits) < 8:
				char_bits = '0'*(8-len(char_bits)) + char_bits
			for bit_idx in range(8):
				cur_char = char_bits[bit_idx]
				if char_idx == 0:
					if cur_char not in prefixes[bit_idx]:
						prefixes[bit_idx][cur_char] = {}
						continue
				dict = prefixes[bit_idx]
				for i in range(char_idx):
					dict = dict[cur_char]
				if cur_char not in dict:
					dict[cur_char] = {}
	
	#[print(bin(int.from_bytes(pat.encode(), 'big'))) for pat in pats]
	#print(prefixes)
	[print(x) for x in prefixes]
	
	return sum([count(x) for x in prefixes])
	
def used(groups, x):
	for group in groups:
		if x in group:
			return True
	return False

def correlation(group, string):
	new_group = group + [string]
	
	ns_group = count_nodes(group)
	ns_string = count_nodes([string])
	ns_new_group = count_nodes(new_group)
	
	#print((ns_group + ns_string) / ns_new_group)
	
	return (ns_group + ns_string) / ns_new_group

def str_grp(strings, num_groups):
	n = len(strings)
	
	groups = [[strings[0]]]
	
	#Seed Selection and Correlation Estimation Phase
	for i in range(1, num_groups):
		correlation_vector = [list()]*len(strings)
		for j in range(len(strings)):
			correlation_vector[j] = max([correlation(x,strings[j]) for x in groups[:i]])
		groups.append([strings[correlation_vector.index(min(correlation_vector))]])
		
	#print(groups)
	
	
	#Seed Growing Phase
	for _ in range(n-num_groups):
		corr_diffs = [0]*len(strings)
		for i in range(len(strings)):
			if not used(groups, strings[i]):
				correlations = [correlation(group, strings[i]) for group in groups]
				correlations.sort()
				corr_diffs[i] = correlations[-1] - correlations[-2]
		most_difference_idx = corr_diffs.index(max(corr_diffs))		
		correlations = [correlation(group, strings[most_difference_idx]) for group in groups]
		groups[correlations.index(max(correlations))].append(strings[most_difference_idx])
		
	return groups
	
	
if __name__=='__main__':
	#groups = str_grp(['me', 'him', 'he', 'his'], 2)
	groups = str_grp(['me', 'him', 'he', 'his', 'dog', 'cat'], 2)
	
	print(count_nodes(groups))
	
	for group in groups:
		print(group)
		print(count_nodes(group))
		print()
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	