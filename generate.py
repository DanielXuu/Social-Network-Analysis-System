import networkx
import pymysql
import operator
import matplotlib.pyplot as plt
import json

def generate(lst):
    db = pymysql.connect(host='***', user='***', password='***', database='***')

    cursor = db.cursor()


    # str_lst = ','.join([str(item) for item in lst])

    cursor.execute("SELECT CONCAT(TRIM(Demographic.resident_fname),' ',TRIM(Demographic.resident_lname)) AS Source,\
                          TRIM(CONCAT(TRIM(Network.network_fname),' ',TRIM(Network.network_lname))) AS Target,\
                          SUM(Network.network_weight) AS Weight\
                          FROM Demographic, Network\
                          WHERE Demographic.survey_id = Network.survey_id AND Demographic.block_id IN (%s)\
                          GROUP BY Source, Target" % lst)  
    data = cursor.fetchall()

    # for row in data :
    #     print(row[0], row[1])
        
    cursor.close()
    db.close()

    edges = []
    for row in data:
        edges.append((row[0], row[1], max(0, float(row[2]))))

    node_name = []
    for i in data :
        node_name.append(i[0])
        node_name.append(i[1])
    node_name = set(node_name)

    G = networkx.DiGraph()
    G.add_nodes_from(node_name)
    G.add_weighted_edges_from(edges)
    #print(networkx.info(G))
    temp = {}
    for each in networkx.info(G).split('\n')[2:]:
        temp[each.split(':')[0]] = float(each.split(':')[1])

    density = networkx.density(G)
    #print("Network density:", density)

    degree_dict = dict(G.degree(G.nodes()))
    networkx.set_node_attributes(G, degree_dict, 'degree')
    sorted_degree = sorted(degree_dict.items(), key=operator.itemgetter(1), reverse=True)

    inDegree_dict = dict(G.in_degree(G.nodes()))
    inDegree_dict
    networkx.set_node_attributes(G, inDegree_dict, 'inDegree')
    sorted_inDegree = sorted(inDegree_dict.items(), key=operator.itemgetter(1), reverse=True)

    outDegree_dict = dict(G.out_degree(G.nodes()))
    outDegree_dict
    networkx.set_node_attributes(G, outDegree_dict, 'outDegree')
    sorted_outDegree = sorted(outDegree_dict.items(), key=operator.itemgetter(1), reverse=True)

    betweenness_dict = networkx.betweenness_centrality(G) # Run betweenness centrality
    networkx.set_node_attributes(G, betweenness_dict, 'betweenness')
    sorted_betweenness = sorted(betweenness_dict.items(), key=operator.itemgetter(1), reverse=True)

    ret =  {}
    for each in edges:
        if each[0] not in ret:
            ret[each[0]] = 0
        
    for each in edges:
        if each[1] not in ret:
            ret[each[1]] = each[2]
        else:
            ret[each[1]] += each[2]
    
    networkx.set_node_attributes(G, ret, 'weighted_indegree')

    sorted_nodeSize = sorted(ret.items(), key=operator.itemgetter(1), reverse=True)

    
    output = networkx.readwrite.json_graph.node_link_data(G)
    output['density'] = density
    output.update(temp)

    return output


if __name__ == "__main__":
    print(generate())
    print(type(json.dumps(generate())))
