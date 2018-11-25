import numpy as np
import MySQLdb
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


with open('out8.csv', 'r') as myfile:
    market=myfile.read().splitlines()

#with open('out9.csv', 'r') as myfile:
#    signals=map(int, myfile)


with open('out10.csv', 'r') as myfile:
    max_loss_3=map(float, myfile)


with open('out11.csv', 'r') as myfile:
    max_loss_0=map(float, myfile)


with open('out12.csv', 'r') as myfile:
    max_loss_1=map(float, myfile)


with open('out13.csv', 'r') as myfile:
    max_loss_2=map(float, myfile)

with open('out14.csv', 'r') as myfile:
    max_loss_4=map(float, myfile)

with open('out15.csv', 'r') as myfile:
    max_loss_5=map(float, myfile)


with open('out16.csv', 'r') as myfile:
    max_loss_6=map(float, myfile)


with open('out17.csv', 'r') as myfile:
    max_loss_7=map(float, myfile)


with open('out-max.csv', 'r') as myfile:
    max_loss=map(float, myfile)
    max_val= max(max_loss)


data = [max_loss_0, max_loss_1, max_loss_2, max_loss_3, max_loss_4, max_loss_5, max_loss_6, max_loss_7]




#columns = ('BTC-XMR', 'BTC-ETH', 'BTC-XRP', 'BTC-DASH', 'BTC-QTUM')
columns = tuple(market)

#rows = ['%d year' % x for x in (100, 50, 20, 10, 5)]
#rows = ['%d  Signal type' % x for x in signals]
rows = ['%d  Signal type' % x for x in (7, 6, 5, 4, 3, 2, 1, 0)]



values = np.arange(0, int(max_val), 5)
#value_increment = 0

# Get some pastel shades for the colors
colors = plt.cm.BuPu(np.linspace(0, 0.7, len(rows)))
n_rows = len(data)

#index = np.arange(len(columns)) + 0.3
index = np.arange(len(columns))+0.3


bar_width = 1

# Initialize the vertical-offset for the stacked bar chart.
y_offset = np.zeros(len(columns))

# Plot bars and create text labels for the table
cell_text = []
for row in range(n_rows):
    plt.bar(index, data[row], bar_width, bottom=y_offset, color=colors[row])
    y_offset = data[row]
    cell_text.append(['%1.1f' % (x) for x in y_offset])

# Reverse colors and text labels to display the last value at the top.
colors = colors[::-1]
cell_text.reverse()

# Add a table at the bottom of the axes
the_table = plt.table(cellText=cell_text, rowLabels=rows, rowColours=colors, colLabels=columns, loc='bottom')
the_table.auto_set_font_size(False)
the_table.set_fontsize(5)


# Adjust layout to make room for the table:
plt.subplots_adjust(left=0.2, bottom=0.3)

plt.ylabel("Loss in percent's")
plt.yticks(values, ['%d' % val for val in values])
plt.xticks([])
plt.title('Loss profit')

plt.grid(True)
plt.savefig('/var/www/cgi-bin/crypto_results4.png')
plt.savefig('/root/PycharmProjects/cryptobot/webinterface/static/crypto_results4.png')
plt.show()
