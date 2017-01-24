import numpy as np
import random
import copy

'''----------------Object------------------'''
class Order(object):
    def __init__(self, id, times):
        self.id = id;
        self.times = times;
    pass;
'''--------------------------'''

class Ant(object):
    def __init__(self, orderCount, pherno, orders):
        self.orderCount = orderCount;
        self.pherno = pherno;
        self.orders = orders;

    def search(self):
        iter = 1000;#iteration for 1000 times
        result = 100000;
        while iter > 0:
            orders = copy.deepcopy(self.orders);
            temp = random.randint(0, self.orderCount-1);
            finalRes = [copy.deepcopy(orders[temp])];
            orders[temp] = 0;
            while (self.orderCount != len(finalRes)):
                p = self.pherno[temp];
                totalRate = 0;
                for i in range (0, len(p)):
                    if orders[i] != 0 and temp != i:
                        totalRate += p[i];
                        pass;
                    pass;
                ran = random.uniform(0, 1) * totalRate;
                num = 0;
                for i in range (0, len(p)):
                    if orders[i] != 0 and temp != i:
                        num += p[i];
                        if num >= ran:
                            temp = i;
                            break;
                            pass;
                        pass;
                    pass;
                finalRes.append(copy.deepcopy(orders[temp]));
                orders[temp] = 0;
                pass;
            timeCost = timeCal(finalRes);

            if (timeCost < result):
                result = timeCost;
                result_order = copy.deepcopy(finalRes);
                pass;
            self.updatePher(result, finalRes, self.pherno);
            iter -= 1;
            pass;
        return result_order;
        pass;

    def updatePher(self, performance, res, pherno):
        updatePara = 1;
        for i in range(0, len(res)-1):
            o1 = res[i];
            o2 = res[i+1];
            id1 = o1.id;
            id2 = o2.id;
            temp1 = pherno[id1];
            temp = temp1[id2] + (updatePara / performance) * (updatePara / performance);
            temp1[id2] = temp;
            pass;
        pass;
'''----------------Object------------------'''



'''-----------DB---------------------'''
'''this is fake DB
    the first int is id, the second arr is the time cost for each process'''
order_0 = Order(0, [2, 6, 1]);
order_1 = Order(1, [8, 2, 1]);
order_2 = Order(2, [2, 1, 1]);
order_3 = Order(3, [3, 4, 3]);
order_4 = Order(4, [6, 3, 5]);
orders = [order_0, order_1, order_2, order_3, order_4];
'''-----------DB---------------------'''

'''******************utiles******************'''

'''order the orders by process time'''
def orderByProcessTime(orders, interval):
    if interval == 0:
        return sorted(orders, key=lambda order: order.times[0]);
    else:
        return sorted(orders, key=lambda order: order.times[0], reverse=1);
    pass;
'''-----------------------------------------'''

'''time calculator
    it is used to calculate the time
    and to print the result'''
def timeCal(orders):
    res = [];
    shift = 0;
    for i in range(0, len(orders[0].times)):
        finishedMa = [];
        temp = 0;
        if 0 == shift:
            for j in range(0, len(orders)):
                temp += orders[j].times[shift]
                finishedMa.append(temp);
        else:
            for j in range(0, len(orders)):
                order = orders[j];
                last = res[shift-1];
                temp = max(temp+order.times[shift], last[j]+order.times[shift]);
                finishedMa.append(temp);
        res.append(finishedMa);
        shift += 1;
    print(res);
    result = res[len(res)-1];
    return result[len(result)-1];
pass;
'''-----------------------------------------'''
'''******************utiles******************'''


'''---------------solutions----------------'''

'''shorest first process time
    order the orders by the first process time'''
def sfp(orders):
    res = orderByProcessTime(orders, 0);
    return timeCal(res);
    pass;
'''-------------------------------'''

'''firt in first out method'''
def FIFO(orders):
    return timeCal(orders);
    pass;
'''-------------------------------'''

'''this is Johnson solution without other alghorithm'''
def johnson(orders):
    firstarr = [];
    secondarr = [];
    for i in range(0,len(orders)):
        if orders[i].times[0] <= orders[0].times[1]:
            firstarr.append(orders[i]);
        else:
            secondarr.append(orders[i]);
    r1 = orderByProcessTime(firstarr, 0);
    r2 = orderByProcessTime(secondarr, 1);
    res = [];
    for i in range(0, len(r1)):
        res.append(r1[i]);
    for i in range(0, len(r2)):
        res.append(r2[i]);
    return timeCal(res);
pass;
'''-------------------------------'''

'''this is Ant Colony Solution'''
def aco(orders):
    orderCount = len(orders);
    pherno = np.ones((orderCount, orderCount));
    ant = Ant(orderCount, pherno, orders);
    res = ant.search();
    timeCal(res);

print(aco(orders));
FIFO(orders);
johnson(orders);
sfp(orders);