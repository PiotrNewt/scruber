# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

x = [0.01, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3]

stadium1 = [0, 0, 0, 1/102, 0, 2/168 ,1/68]
country1 = [1, 1, 23/27, 38/42, 47/54, 54/69, 21/27]
league1 = [1/3, 2/3, 5/9, 1/4, 7/15, 8/21, 3/8]
team1 = [5/9, 7/9, 28/45, 87/135, 96/180, 125/225, 139/270]
player1 = [151/177, 706/876, 1342/1752, 1926/2628, 2464/3504, 2771/4380, 3285/5256]

stadium2 = [0, 1/18, 0, 2/102, 0, 0, 1/68]
country2 = [1, 1, 23/27, 38/42, 47/54, 54/69, 21/27]
league2 = [1/3, 1, 2/3, 7/12, 9/15, 15/21, 14/24]
team2 = [1, 13/15, 37/45, 111/135, 133/180, 165/225, 181/270]
player2 = [167/177, 785/876, 1517/1752, 2175/2628, 2764/3504, 3240/4380, 3675/5256]

def sublineChart(table_name,r1,r2):
    # new graph
    plt.figure()
    plt.plot(x,r1,'r--',label='s-' + table_name)
    plt.plot(x,r2,'b--',label='m-' + table_name)
    plt.plot(x,r1,'ro--',x,r2,'bx--')
    plt.xlabel('dirty rate')
    plt.ylabel('repair rate')
    plt.legend()

def lineChart():
    # stadium
    sublineChart('stadium', stadium1, stadium2)

    # country
    sublineChart('country', country1, country2)

    # league
    sublineChart('league', league1, league2)

    # team
    sublineChart('team', team1, team2)

    # player
    sublineChart('player', player1, player2)

    plt.show()


# Histogram
def histogram():
    def subHisto(table_name,r1,r2):
        # new graph
        plt.figure()

        def fixO(r):
            for i in range(len(r)):
                if r[i] == 0:
                    r[i] = 0.001

        fixO(r1)
        fixO(r2)

        x_list = ['0.01', '0.05', '0.1', '0.15', '0.2', '0.25', '0.3']
        ticky = [0,0,0,0,0,0,0]
        xh = list(range(len(r1)))
        total_width, n = 0.6, 2
        width = total_width / n
        plt.bar(xh, r1, width=width, label='s-' + table_name,fc = 'r')

        a = []
        for i in range(len(xh)):
            a.append(xh[i] + width/2)
        plt.bar(a, ticky, width=0,tick_label = x_list,fc = 'b')

        for i in range(len(xh)):
            xh[i] = xh[i] + width

        plt.bar(xh, r2, width=width, label='m-' + table_name,fc = 'b')

        plt.xlabel('dirty rate')
        plt.ylabel('repair rate')
        plt.legend()

    # stadium
    subHisto('stadium', stadium1, stadium2)

    # country
    subHisto('country', country1, country2)

    # league
    subHisto('league', league1, league2)

    # team
    subHisto('team', team1, team2)

    # player
    subHisto('player', player1, player2)

    plt.show()


#----
lineChart()
histogram()