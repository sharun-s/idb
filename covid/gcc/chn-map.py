import sys
#print("files to process-", len(sys.argv)-1)
import pandas as p
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gp

fig = plt.figure(facecolor="#001f3f")
l2=gp.read_file('../chn-zones.json')
ax3 = fig.add_subplot(111, frameon=False)
l2.plot(ax=ax3, facecolor='#0099dd',edgecolor='blue', alpha=.78,linewidth=0)
ax3.get_xaxis().set_visible(False)
ax3.get_yaxis().set_visible(False)
ax3.set_facecolor("#002f4f")
ax3.set_alpha(0.3)
ax3.spines['bottom'].set_color('white')#'#ccc107')
ax3.spines['top'].set_color('white') 
ax3.spines['right'].set_color('white')
ax3.spines['left'].set_color('white')
l2[l2.Name==sys.argv[1].replace('.csv','')].plot(ax=ax3,facecolor='#ffcc55',edgecolor='blue',alpha=.73, linewidth=0) 
plt.show()