import numpy as np
##for not using X windows
import matplotlib
matplotlib.use('Agg')
###
import matplotlib.pyplot as plt


with open('out2.csv', 'r') as myfile:
    #market=myfile.read().replace('\n', ' ')
    market=myfile.read().splitlines()

with open('out3.csv', 'r') as myfile:
    #profit=myfile.read().replace('\n', ' ')
    #profit=myfile.read().splitlines()
    profit = map(float, myfile)

with open('out4.csv', 'r') as myfile:
    #profit=myfile.read().replace('\n', ' ')
    #profit=myfile.read().splitlines()
    count = map(int, myfile)

index = np.arange(len(market))
n_groups=len(index)
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.35
opacity = 0.4
rects1 = ax.bar(index, profit, bar_width, alpha=opacity, color='b',label='Profit')
rects2 = ax.bar(index + bar_width, count, bar_width, alpha=opacity, color='r',label='Trades')
ax.set_xlabel("Markets", fontsize=15)
ax.set_ylabel("Profit", fontsize=15 )
ax.set_title("Cryptocurrencies chart")
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(market, fontsize=10, rotation=90)
ax.legend()
fig.tight_layout()
plt.grid(True)
plt.savefig('/var/www/cgi-bin/crypto_results2.png', bbox_inches='tight')
plt.savefig('/root/PycharmProjects/cryptobot/webinterface/static/crypto_results2.png', bbox_inches='tight')
plt.show()





