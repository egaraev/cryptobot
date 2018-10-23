import numpy as np
##for not using X windows
import matplotlib
matplotlib.use('Agg')
###
import matplotlib.pyplot as plt


with open('out5.csv', 'r') as myfile:
    #market=myfile.read().replace('\n', ' ')
    market=myfile.read().splitlines()

with open('out6.csv', 'r') as myfile:
    #profit=myfile.read().replace('\n', ' ')
    #profit=myfile.read().splitlines()
    profit = map(float, myfile)

with open('out7.csv', 'r') as myfile:
    #profit=myfile.read().replace('\n', ' ')
    #profit=myfile.read().splitlines()
    count = map(int, myfile)

index = np.arange(len(market))
n_groups=len(index)
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.35
opacity = 0.4
rects1 = ax.bar(index, profit, bar_width, alpha=opacity, color='g',label='AI predictions')
rects2 = ax.bar(index + bar_width, count, bar_width, alpha=opacity, color='r',label='Trades')
ax.set_xlabel("Markets", fontsize=15)
ax.set_ylabel("AI successfull predictions", fontsize=15 )
ax.set_title("AI chart")
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(market, fontsize=10, rotation=90)
ax.legend()
fig.tight_layout()
plt.grid(True)
plt.savefig('/var/www/cgi-bin/crypto_results3.png')
plt.savefig('/root/PycharmProjects/cryptobot/webinterface/static/crypto_results3.png')
plt.show()





