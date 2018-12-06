def map_groups(groups):
    
    """
    Create dictionary with addresses as dictionary keys, and list of groups (lists) where the
    address appears as the dictionary values. 
        {'1asghdhfghdghd56':[1],
         '1hgjjhr67hfnfbfg':[2,3],
         ...
         }
    """
    
    mapping = {}
    for group in groups:
        for address in group:
            mapping[address] = []
    for group in groups:    
        for address in group:
            if groups.index(group) not in mapping[address]:
                mapping[address].append(groups.index(group))
    return mapping

def get_cluster_mapping(mapping):
    
    """
    Mapping of the group number to the list of addresses that appear in the group
        {1:['1fhmykck', '1azkoypri'],
         2:['1fpplrkk'],
         ...
         }
    """
    
    cluster_mapping = {}
    for k, v in mapping.items():
        if k == 'N/A':
            pass
        else:
            for el in v:
                cluster_mapping[el] = []

    for k, v in mapping.items():
        if k == 'N/A':
            pass
        else:  
            for el in v:
                cluster_mapping[el].append(k)

    return cluster_mapping

def to_merge(mapping):
    
    """
    Temporary clusters is a list of lists of groups that have non-empty intersections with each other, or,
    in other words, that have to be merged later
        {cluster_1:[address_1, address_2], [address_2, address_3, address_4], [address_3, address_5, address_6],
         cluster_2:[address_7, address_8], [address_8, address_9],
         cluster_3:[address_10, address_11],
         ...
         }
    """

    temp_clusters = []
    for k, v in mapping.items():
        to_merge = []
        count = 0

        if temp_clusters == []:
            temp_clusters.append(v)

        for cl in temp_clusters:
            intersection = intersect(v, cl)
            if intersection != []:
                to_merge.append(merge_lists(v,cl))
                temp_clusters.remove(cl)
                count += 1

        if count == 0:
            temp_clusters.append(v)

        flat_cluster = [item for sublist in to_merge for item in sublist]
        flat_cluster = list(set(flat_cluster))
        if flat_cluster not in temp_clusters:
            temp_clusters.append(flat_cluster)
            
    return temp_clusters

def merge_lists(list_1, list_2):
    """Create a list that contains all elements from both lists"""
    return [el for el in list_1 if el not in list_2]+[el for el in list_2 if el not in list_1]+\
    [el for el in list_1 if el in list_1 and el in list_2]

def cluster_groups(groups_to_merge, cluster_mapping):
    
    """
    A function that creates a dictionary with the first number of the group in the groups to merge as the keys, 
    and the list of addresses belonging to the cluster, as the values.
    
    {(1, 5):[address_1, address_5, address_6],
     (2, 3):[address_2, address_3, address_4],
     ...
     }
    The lists above have no pairwise intersections with each other.
    
    """
    
    clustering = {}
    for t in groups_to_merge:
        key = tuple(t)
        value = [cluster_mapping[el] for el in t]
        if key != ():
            clustering[key[0]] = value

    '''Flatten the lists of addresses belonging to a cluster'''
    for k, v in clustering.items(): 
        clustering[k] = [item for sublist in v for item in sublist]
        clustering[k] = list(set(clustering[k]))
    return clustering

    '''Delete clusters of one address'''
    del_keys = []
    for k, v in clustering.items():
        if len(v) == 1:
            del_keys.append(k)

    for key in del_keys:
        del clustering[key]

def intersect(list_m, list_n):
    """Find the intersection of two lists."""
    return [el for el in list_m if el in list_n]