import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt1
import matplotlib.cm as cm
import copy
import time
class Cluster:
    def __init__(self,points,mean):
        self.points = np.array(points)
        self.mean = np.array(mean)
        #self.mean += self.points

    def calculateMean(self):
        a = [0.,0.]
        self.mean = np.array(a)
        for p in self.points:
            self.mean += p
            #self.mean[1] = self.mean[1] + p[1]
        if len(self.points)==0:
            self.mean /= 1.0
        else:
            self.mean /= float(len(self.points))

    def calculateShift(self):
        oldMean = copy.deepcopy(self.mean)
        self.calculateMean()
        return getDistance(oldMean,self.mean)


    def calculateLoss(self):
        loss = 0
        for p in self.points:
            loss += getDistance(p,self.mean)
        return loss


def getDistance(d1, d2):
    diff = d1 - d2
    return np.sqrt(diff.T.dot(diff))


def plotClusters(clusters):
    plt.cla()
    colors = iter(cm.rainbow(np.linspace(0, 1, len(clusters) * 2)))
    for c in clusters:
        x = []
        y = []
        for p in c.points:
            x.append(p[0])
            y.append(p[1])
        plt.scatter(x,y , color=next(colors))
        plt.scatter(c.mean[0],c.mean[1],color = next(colors))
    plt.draw()
    plt.show()
    plt.pause(1)


def plotError(iter, error):
    plt1.xlabel('iterations')
    plt1.ylabel('squared-error')
    plt1.plot(iter, error, '-')
    plt1.show()


def kMeans(data,k,r,epselon = 0.1):
    losses = []
    for i in range(r):
        initial = random.sample(data, k)
        clusters = [Cluster(p,p) for p in initial]
        #clusters = [Cluster(data[m], data[m]) for m in range(k)]
        iterations = 0
        done = False
        error = []
        iter = []
        plt.ion()
        plt.show()
        while not done:
            iterations += 1
            list = [[] for i in range(k)]
            for d in data:
                min = getDistance(d,clusters[0].mean)
                index = 0
                for j in range(k):
                    dist = getDistance(d,clusters[j].mean)
                    if dist < min:
                        min = dist
                        index = j
                list[index].append(np.array(d))
                maxShift = 0
            loss = 0
            for j in range(k):
                clusters[j].points = list[j]
                shift = clusters[j].calculateShift()
                loss += clusters[j].calculateLoss()

                if shift > maxShift:
                    maxShift = shift
            error.append(loss)
            iter.append(iterations)
            print "Iterations....",iterations
            print maxShift
            if maxShift < epselon:
                print "Coverged after... %d iterations" %iterations
                done = True
            plotClusters(clusters)
            #time.sleep(1)
        plt.ioff()
        plt.show()
        plotError(iter,error)
        return clusters


if __name__ == "__main__":
    data1 = pd.read_csv("dataset1.csv",delim_whitespace=True).values
    print data1[0][1]
    x = []
    y = []
    for d in data1:
        x.append(d[0])
        y.append(d[1])
    #plt.scatter(x,y)
    #plt.show()
    data = np.column_stack([x,y])
    #print data
    #print data[:,0]
    data = np.array(data)
    #print data[:,0]
    kMeans(data,2,1,0.001)
