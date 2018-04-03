from sshtunnel import SSHTunnelForwarder
import MySQLdb
import csv
import numpy as np
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import mpld3
import mpld3.plugins as plugins
import os

#collecting data and saving into .txt files based on id
with SSHTunnelForwarder(('127.0.0.1', 3306),ssh_password='root',ssh_username='root',remote_bind_address=('127.0.0.1', 3306)) as server:
	con = MySQLdb.connect(user='root', passwd='root',db='basic_db', host='127.0.0.1',port=server.local_bind_port,charset='utf8')
	cursor = con.cursor()
    cursor.execute( '''select id from bot_id''')
    bots = cursor.fetchall()

id_list=[x for x, in bots]
for i in id_list:
	cursor = con.cursor()
    cursor.execute( '''select * from table where bot_id ='''+str(i)+''') * ''')
    data = cursor.fetchall()

    with open('%s.txt' % i, 'a', newline='') as csv_file:
    	csv_app = csv.writer(csv_file, delimiter=',')
    	csv_app.writerows(data)

mpl.rcParams['font.size'] = 15
plt.switch_backend('agg')

def bytespdate2num(fmt, encoding='utf-8'):
	strconverter = mdates.strpdate2num(fmt)

    def bytesconverter(b):
    	s = b.decode(encoding)
    	return strconverter(s)
    	return bytesconverter

#providing dynamic sizing depending on number of ids
z=len(id_list)
while z%2==1:
        z=z+1
else:
        h=z*6.25
fig = plt.figure(figsize=(19,h))

        
if len(id_list)%2==0:
        v=len(list)*2
else:
        v=len(list)*2+1

p=0
q=0
#plotting
for id in list:
	if os.stat('%s.txt' % id).st_size != 0:
		date, botid, i, a, d, c,date2,inv2,acc2,dec2,can2 = np.loadtxt('%s.txt' % id, delimiter=',',unpack=True, converters={0: bytespdate2num('%Y-%m-%d %H:%M:%S'),6: bytespdate2num('%Y-%m-%d %H:%M:%S')})
		id2=id
		id = plt.subplot2grid((v, 2), (p, 0), rowspan=1, colspan=2)
        plt.title(str(id2),fontsize=18)
        axes=plt.gca()
        axes.set_ylim([-5,119])

		id.plot_date(date, i, 'r', linewidth=2, label='% invalid')
        id.plot_date(date, a, 'g', linewidth=2, label='% accepted')
        id.plot_date(date, d, 'b', linewidth=2, label='% declined')
        id.plot_date(date, c, 'k', linewidth=2, label='% cancelled')
        id.grid(True)
        if p==0:
        	plt.legend(loc='upper center',bbox_to_anchor=(0.5, 1.02),ncol=4,fancybox=True,prop={'size':13}, borderaxespad=0.)
            p= p+1
mpl.rcParams['font.size'] = 20

for id in list:
	if os.stat('%s.txt' % id).st_size != 0:
		date, botid, i, a, d, c,date2,inv2,acc2,dec2,can2 = np.loadtxt('%s.txt' % id, delimiter=',',unpack=True, converters={0: bytespdate2num('%Y-%m-%d %H:%M:%S'),6: bytespdate2num('%Y-%m-%d %H:%M:%S')})
        id2=id
        id = plt.subplot2grid((v, 2), (p, q), rowspan=2, colspan=1)
        plt.title(str(id2),fontsize=18)
        slices=[int(inv2[-1]),int(acc2[-1]),int(dec2[-1]),int(can2[-1])]
        colrs=['r','g','b','k']
        lbl= [int(inv2[-1]),int(acc2[-1]),int(dec2[-1]),int(can2[-1])]
        id.pie(slices,colors=colrs, labels=lbl,labeldistance=1.05)
        id.grid(True)
        id.axis('equal')
        if p==0:
        	plt.legend(loc='upper center',bbox_to_anchor=(0.5, 1.02),ncol=4,fancybox=True,prop={'size':13}, borderaxespad=0.)
        if q==0:
        	q=q+1
        else:
        	q=0
        	p=p+2
#shaping and saving                                       
plt.subplots_adjust(left=0.05, bottom=0.05, right=0.94, top=0.99, wspace=0.1, hspace=0.4)
mpld3.save_html(fig,'daily-stats-graph.html')
