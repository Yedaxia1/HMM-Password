
import numpy as np

import scipy.stats


start_probability = {}


transition_probability = {

}


states= list()
# Helps visualize the steps of Viterbi.
def print_dptable(V):
    s = "    " + " ".join(("%7d" % i) for i in range(len(V))) + "\n"
    for y in V[0]:
        s += "%.5s: " % y
        s += " ".join("%.7s" % ("%f" % v[y]) for v in V)
        s += "\n"
    print(s)


def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    path = {}

    # Initialize base cases (t == 0)
    for y in states:
        if y not in start_p:
            start_p[y]=0
        startpy=start_p[y]
        emity=emit_p[y]
        obs0=obs[0]
        if obs0 not in emity:
            emity[obs0]=0
        emitYo=emity[obs0]
        V[0][y] = startpy* emitYo
        path[y] = [y]

    # alternative Python 2.7+ initialization syntax
    # V = [{y:(start_p[y] * emit_p[y][obs[0]]) for y in states}]
    # path = {y:[y] for y in states}

    # Run Viterbi for t > 0
    for t in range(1, len(obs)):
        V.append({})
        newpath = {}

        for y in states:
            prob=-1
            state=''
            for y0 in states:
                if y0 not in trans_p:
                    trans_p[y0]={}
                tpy0=trans_p[y0]
                if y not in tpy0:
                    tpy0[y]=0
                tpy0y=tpy0[y]
                obst=obs[t]
                if y not in emit_p:
                    emit_p[y]=0

                empy=emit_p[y]
                if obst not in empy:
                    empy[obst]=0
                epyo=empy[obst]
                vyy=V[t - 1][y0]
                (thisProb, thisState) = (vyy* tpy0y * epyo, y0)
                if thisProb>prob:
                    prob=thisProb
                    state=thisState

            V[t][y] = prob
            pathstate=path[state]
            newpath[y] = pathstate+ [y]

        # Don't need to remember the old paths
        path = newpath

    #print_dptable(V)
    """
    TODO 求前N个概率最大要改这里
    """

    #(prob, state) = max((V[t][y], y) for y in states)
    #return (prob, path[state])

    vresult = dict()
    prlist = list()
    for y in states:
        vresult[V[t][y]] = path[y]
        prlist.append(V[t][y])

    prlist.sort(reverse=True)

    rresult = dict()
    for i in range(10):
        rresult[prlist[i]] = vresult[prlist[i]]

    return rresult

import os

class Pair:
    def __init__(self, text, duration):
        self.text=text
        self.duration=duration
    text: str
    duration: int

def pullTextFromPhone():
    os.system("adb pull /sdcard/Android/data/com.jk.antirecal1/files/record")
    return
def contentToPair():
    stringPairList=list()
    f= open("record.txt",'r')
    lines= f.readlines()
    for x in range(0,len(lines),2):
        pairList=list()
        text=lines[x].replace("\n","")
        internal=lines[x+1].replace("\n","")
        internal_list=internal.split(",")
        isLegal=len(text)-1== len(internal_list)
        if(isLegal):
            for cursor in range(0, len(internal_list)):
                textPair: str= text[cursor:cursor+2]
                pair= Pair(textPair,internal_list[cursor])
                pairList.append(pair)
            stringPairList.append(pairList)
    f.close()
    return stringPairList



def normalize(content_pair_list):


   for content_pair in content_pair_list:
       pair_size = len(content_pair)
       total_duration = 0
       for pair in content_pair:
           total_duration = total_duration + int(pair.duration)
       for pair in content_pair:
           pair.duration = pair_size * int(pair.duration) / total_duration
   return content_pair_list


def get_propbility_from_duration(duration, pair):
    duration_list=[]
    normlize_pair_list=normalize(contentToPair())




def observation_to_state(duration):
    max_prob=0
    guess_pair='error'
    pair_list=[]
    prob_list=list()

    for alphabet1 in range(97,123):
        for alphabet2 in range(97, 123):
            pair=chr(alphabet1)+chr(alphabet2)
            pair_list.append(pair)
    for pair in pair_list:
        prob=get_propbility_from_duration(duration,pair)
        if prob>max_prob:
            max_prob=prob
            guess_pair=pair
    return guess_pair



'''
生成模型
'''
def init_viterbi():
    stringPairList=contentToPair()



    for stringPair in stringPairList:
        last_state=""
        for cursor in range(0, len(stringPair)):
            pair:Pair=stringPair[cursor]

            if last_state!="":
                if last_state not in transition_probability:
                    transition_probability[last_state]=dict()
                currentTransDict = transition_probability[last_state]
                if pair.text not in currentTransDict:
                    currentTransDict[pair.text]=0
                currentTransDict[pair.text]=currentTransDict[pair.text]+1




            if pair.text not in states:
                states.append(pair.text)

            if(cursor==0):
                if pair.text not in start_probability:
                    start_probability[pair.text]=0
                start_probability[pair.text]=start_probability[pair.text]+1

            last_state=pair.text

    '''
    for mypari in transition_probability.keys():
        currentTransDict = transition_probability[mypari]
        count=0
        sum=0

        #计算总数
        for statew in currentTransDict:
            sum+=currentTransDict[statew]
            count+=1

        tail = mypari[1]

        for i in range(10):
            if (tail+str(i)) not in currentTransDict:
                currentTransDict[tail+str(i)]=sum/10

        for  transition_probability_state in transition_probability.keys():
            transition_probability_val_dict=transition_probability[transition_probability_state]
            total=0
            for transition_probability_val in transition_probability_val_dict.keys():
                total=total+transition_probability_val_dict[transition_probability_val]
            for transition_probability_val in transition_probability_val_dict.keys():
                transition_probability_val_dict[transition_probability_val]=transition_probability_val_dict[transition_probability_val]/total
        '''

    return

"""
根据输入值生成emission_probability矩阵
用content_pair生成 状态对应观测值 的概率 函数
observations 带进去生成矩阵
"""
def create_emission_probability(content_pairs,observations):

    state_to_observation_dict=dict()

    # TODO 本函数内加入归一化处理

    for content_pair in content_pairs:
        for pair in content_pair:
            if pair.text in state_to_observation_dict.keys():
                observation_set=state_to_observation_dict[pair.text]
                observation_set.append(pair.duration)
            else:
                 state_to_observation_dict[pair.text]=list()
                 state_to_observation_dict[pair.text].append(pair.duration)


    emission_probability = dict()
    for state in state_to_observation_dict.keys():
        emission_probability[state]=dict()
        observation_set = state_to_observation_dict[state]

        observation_set=set(map(int,observation_set))
        mymean = np.mean(list(observation_set))
        standard_deviation=np.std(list(observation_set))
        if standard_deviation==0:
            standard_deviation=1 #TODO 这里可能要考虑下合适的值.
        normal_dist_model= scipy.stats.norm(mymean,standard_deviation)

        for observation in observations:
            state_prob= normal_dist_model.pdf(int(observation))
            emission_probability[state][observation]=state_prob

    return  emission_probability









def printstate():
    print(transition_probability)
    print(emission_probability)
    print(observations)
    print(states)
    print(start_probability)

#时间序列乘2函数
def double_observations(observations):
    for i in range(5):
        observations[i]*=2;

    return observations;

init_viterbi()
#072365
#540635

#observations = ('339','418','199',384','519','317','619','650','299')  # 339,418,199,384,519,317,619,650,299
observations = [151,200,201,198,227]

#时间序列乘2函数
#observations = double_observations(observations);

observations=list(map(str, observations ))
# printstate()
emission_probability = create_emission_probability(contentToPair(),observations)
result=dict()
result=viterbi(observations, states, start_probability, transition_probability, emission_probability)
for r in result.keys():
    print(r)
    print(result[r])

