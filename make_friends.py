import numpy as np
import random
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation

def calculate_p(adjacent_matrix, v_matrix, beta):         # adjacent_matrix: n x n;    v_matrix: n x v_number;   beta: 1 x L 
    n = adjacent_matrix.shape[0]
    v_number = v_matrix.shape[1]
    p_martrix = np.zeros((n,n))
    f_temp = np.zeros((1,n))
    for i in range(n):
        f_temp = calculate_f(i, adjacent_matrix, v_matrix, beta)      
        p_martrix[i,:] = f_temp[0]/sum(f_temp[0])
    return p_martrix



def calculate_f(i, adjacent_matrix, v_matrix, beta):
    f_temp = np.zeros((1,adjacent_matrix.shape[0]))
    for j in range(adjacent_matrix.shape[0]):
        if i==j: continue
        temp_adjacent_matrix = adjacent_matrix
        if temp_adjacent_matrix[i,j]==0: temp_adjacent_matrix[i,j]=1     #改变连边
        else:                            temp_adjacent_matrix[i,j]=0

        s0 = Density_effect(i, temp_adjacent_matrix)
        s1 = Reciprocity_effect(i, temp_adjacent_matrix)
        s2 = Covariate_related_popularity(i, temp_adjacent_matrix, v_matrix, 0)
        f_temp[0,j] = beta[0,0]*s0 + beta[0,1]*s1 + beta[0,2]*s2
    return np.exp(f_temp)


def Density_effect(i, adjacent_matrix):  #密度效应
    s = np.sum(adjacent_matrix[i])
    return s

def Reciprocity_effect(i, adjacent_matrix): #互惠效应
    s = 0
    for j in range(adjacent_matrix.shape[0]):
        s += adjacent_matrix[i,j]*adjacent_matrix[j,i]
    return s

def Covariate_related_popularity(i, adjacent_matrix, v_matrix, v): #协变量相关的追捧效应  v为协变量索引
    s = np.dot(adjacent_matrix[i,:],(v_matrix[:,v]))
    return s

if __name__ == "__main__":
    node_num = 35
    T=200

    link_mat = np.zeros((node_num,node_num))
    node_dict  = {'id':0,'money':0,'major':0,'something_else':0}
    all_node_list = []
    features_mat = np.zeros((node_num,len(node_dict)-1))
    for i in range(node_num):
        node_dict['id'] = i
        node_dict['money'] = random.random()
        node_dict['money'] = random.random()
        node_dict['something_else'] = random.random()
        all_node_list.append(node_dict)
        features_mat[i] =  np.array([node_dict['money'],node_dict['money'],node_dict['something_else']])


    beta=np.mat([[1,2,3]])

    G = nx.DiGraph()
    G.add_nodes_from(list(range(node_num)))

    #pos = nx.spring_layout(G)
    pos=nx.shell_layout(G)
    #动态图
    #plt.ion()
    plt.axis('off')  

    for t in range(100):
        plt.clf()
        #pos = nx.spring_layout(G)
        link_p=calculate_p(link_mat, features_mat, beta)# 生成一个均匀分布的整数随机数
        current_node = random.randint(0, node_num-1)
        node_j = np.random.choice(node_num, p=link_p[current_node,:])
        if G.has_edge(current_node,node_j):
            G.remove_edge(current_node,node_j)
            link_mat[current_node,node_j]=0
        else:
            G.add_edge(current_node,node_j)
            link_mat[current_node,node_j]=1
            
        nx.draw_networkx_nodes(G, pos, node_size=100)
        nx.draw_networkx_edges(G, pos, width=0.3,edge_color='gray')
        nx.draw_networkx_labels(G, pos, font_color='black', font_size=10) 
            
        #plt.pause(0.1)
        image_name = (3-len(str(t+1))) * '0' + str(t+1)
        plt.title('t='+str(t+1))
        plt.savefig("./image/"+image_name+".png")
    
    #plt.pause(0.5)
    plt.clf() 
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=120)
    nx.draw_networkx_edges(G, pos, width=0.5,edge_color='gray')
    nx.draw_networkx_labels(G, pos, font_color='black', font_size=10) 
    #plt.ioff()
    plt.title('t='+str(t+1))
    plt.savefig("./image/"+image_name+".png")
    plt.show()
