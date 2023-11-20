import numpy as np
import random
import matplotlib.pyplot as plt
import copy
import math



# 我们全部使用矩阵运算
def transforEveryTrick(lambda_,m1_arr,m2_arr):
    pair_num = len(m1_arr)
    trans_random = np.random.random(pair_num)
    #print((m1_arr+m2_arr))
    return (1-lambda_) * (trans_random*(m1_arr+m2_arr)-m1_arr)

def tradeEveryTrick(m_arr):
    m_arr_temp = copy.deepcopy(m_arr)
    np.random.shuffle(m_arr_temp) 
    m1_arr =  m_arr_temp[:int(len(m_arr)/2)]
    m2_arr = m_arr_temp[int(len(m_arr)/2):]
    return (m1_arr,m2_arr)

def pFunction(m_arr,T):
    return (1.0/T) * np.exp(-m_arr/T)

def statistics(m_arr,interval=100,max=4):
    x_arr = np.arange(0, max, 1.0/interval)
    num_arr = np.zeros(interval*max)
    for x in m_arr:
        temp_num = math.floor(x / (1.0/interval))
        num_arr[temp_num] += 1
    return (x_arr,num_arr)

if __name__ == "__main__":
    angents_num = 200
    lambda_ = 0.5

    #worth_array = np.random.randint(100,20000,size=angents_num)
    worth_array = np.ones(angents_num)
    T = sum(worth_array)/angents_num
    for t in range(50000):
        #先分组
        m1_t,m2_t = tradeEveryTrick(worth_array)
        #预先算出来交易量
        trans_one = transforEveryTrick(lambda_=lambda_,m1_arr=m1_t,m2_arr=m2_t)
        m1_t += trans_one
        m2_t -= trans_one
        worth_array = np.concatenate((m1_t,m2_t))
    #print(worth_array)
    #worth_array.sort()
    #print()
    x,y = statistics(worth_array,max=math.ceil(worth_array.max()))
    #画统计直方图
    
    #plt.plot(x,pFunction(y,T=T))
    plt.plot(x,y)
    plt.show()