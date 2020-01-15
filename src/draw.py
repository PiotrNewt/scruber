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

'''
plt.figure()
l1=plt.plot(x,stadium1,'r--',label='s-stadium')
l2=plt.plot(x,country1,'g--',label='s-country')
l3=plt.plot(x,league1,'b--',label='s-league')
l4=plt.plot(x,team1,'k--',label='s-team')
l5=plt.plot(x,player1,'y--',label='s-player')

l11=plt.plot(x,stadium2,'r--',label='m-stadium')
l12=plt.plot(x,country2,'g--',label='m-country')
l13=plt.plot(x,league2,'b--',label='m-league')
l14=plt.plot(x,team2,'k--',label='m-team')
l15=plt.plot(x,player2,'y--',label='m-player')

plt.plot(x,stadium1,'ro--',x,country1,'go--',x,league1,'bo--',x,team1,'ko--',x,player1,'yo--')
plt.plot(x,stadium2,'r^--',x,country2,'g^--',x,league2,'b^--',x,team2,'k^--',x,player2,'y^--')

# plt.ylim(0,1)
plt.title('repair results')
plt.xlabel('dirty rate')
plt.ylabel('repair rate')
plt.legend()
'''

def lineChart():
    # for single one
    plt.figure()
    ax1 = plt.subplot(2,3,1)
    ax2 = plt.subplot(2,3,2)
    ax3 = plt.subplot(2,3,4)
    ax4 = plt.subplot(2,3,5)
    ax5 = plt.subplot(2,3,6)

    # stadium
    plt.sca(ax1)
    plt.plot(x,stadium1,'r--',label='s-stadium')
    plt.plot(x,stadium2,'b--',label='m-stadium')
    plt.plot(x,stadium1,'ro--',x,stadium2,'bx--')
    plt.xlabel('dirty rate')
    plt.ylabel('repair rate')
    plt.legend()

    # country
    plt.sca(ax2)
    plt.plot(x,country1,'r--',label='s-country')
    plt.plot(x,country2,'b--',label='m-country')
    plt.plot(x,country1,'ro--',x,country2,'bx--')
    plt.xlabel('dirty rate')
    plt.ylabel('repair rate')
    plt.legend()

    # league
    plt.sca(ax3)
    plt.plot(x,league1,'r--',label='s-league')
    plt.plot(x,league2,'b--',label='m-league')
    plt.plot(x,league1,'ro--',x,league2,'bx--')
    plt.xlabel('dirty rate')
    plt.ylabel('repair rate')
    plt.legend()

    # team
    plt.sca(ax4)
    plt.plot(x,team1,'r--',label='s-team')
    plt.plot(x,team2,'b--',label='m-team')
    plt.plot(x,team1,'ro--',x,team2,'bx--')
    plt.xlabel('dirty rate')
    plt.ylabel('repair rate')
    plt.legend()

    # player
    plt.sca(ax5)
    plt.plot(x,player1,'r--',label='s-player')
    plt.plot(x,player2,'b--',label='m-player')
    plt.plot(x,player1,'ro--',x,player2,'bx--')
    plt.xlabel('dirty rate')
    plt.ylabel('repair rate')
    plt.legend()

    plt.show()


# Histogram
def histogram():
    def subHisto(table_name,r1,r2):
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
        # plt.bar(xh, r2, width=width, label='m-' + table_name,tick_label = x_list,fc = 'b')

        # plt.ylim(0,1.05)
        plt.xlabel('dirty rate')
        plt.ylabel('repair rate')
        plt.legend()

    plt.figure()
    h1 = plt.subplot(2,3,1)
    h2 = plt.subplot(2,3,2)
    h3 = plt.subplot(2,3,4)
    h4 = plt.subplot(2,3,5)
    h5 = plt.subplot(2,3,6)

    # stadium
    plt.sca(h1)
    subHisto('stadium', stadium1, stadium2)

    # country
    plt.sca(h2)
    subHisto('country', country1, country2)

    # league
    plt.sca(h3)
    subHisto('league', league1, league2)

    # team
    plt.sca(h4)
    subHisto('team', team1, team2)

    # player
    plt.sca(h5)
    subHisto('player', player1, player2)

    plt.show()


#----
lineChart()
histogram()