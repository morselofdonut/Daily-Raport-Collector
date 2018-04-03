from sshtunnel import SSHTunnelForwarder
import MySQLdb
import csv
import numpy as np
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import mpld3
import mpld3.plugins as plugins


#collecting data and saving into .txt file
try:

	with SSHTunnelForwarder(('127.0.0.1', 3306),ssh_password='root',ssh_username='root',remote_bind_address=('127.0.0.1', 3306)) as server:
			con = MySQLdb.connect(user='root', passwd='root',db='basic_db', host='127.0.0.1',port=server.local_bind_port,charset='utf8')
			cursor = con.cursor()
			cursor.execute('''select * from table''')
			data = cursor.fetchall()

	with open('datafile.txt', 'a', newline='') as csv_file:
			csv_app = csv.writer(csv_file, delimiter=',')
			csv_app.writerows(data)
			
except MySQLdb.Error:
	continue

#plotting	
plt.switch_backend('agg')

def bytespdate2num(fmt, encoding='utf-8'):
		strconverter = mdates.strpdate2num(fmt)

		def bytesconverter(b):
				s = b.decode(encoding)
				return strconverter(s)

		return bytesconverter


date, value_x,value_y,value_z = np.loadtxt('datafile.txt',delimiter=',',unpack=True,converters={0:bytespdate2num('%Y-%m-%d %H:%M:%S')})

fig = plt.figure(figsize=(19, 15))

#defining function to calculate hourly score
def dynamictitle(x,y):
		if x>=y:
				return (str(x) +' (+' + str(x-y) + ')')
		else:
				return (str(x) +' (' + str(x-y) + ')')

ax1 = plt.subplot2grid((7, 4), (0, 0), rowspan=1, colspan=2)
if len(date)>62:
		plt.title('' +dynamictitle(profitv1[-1], profitv1[-60]),fontsize=18)
else:
		plt.title('' +str(profitv1[-1]), fontsize=18)

ax2 = plt.subplot2grid((7, 4), (0, 2), rowspan=1, colspan=2)
if len(date)>62:
		plt.title('' +dynamictitle(profitv2[-1], profitv2[-60]),fontsize=18)
else:
		plt.title('' +str(profitv2[-1]), fontsize=18)

ax3 = plt.subplot2grid((7, 4), (5, 0), rowspan=1, colspan=2)
if len(date)>62:
		plt.title('' +dynamictitle(trans[-1], trans[-60]),fontsize=18)
else:
		plt.title('' +str(trans[-1]), fontsize=18)


plot1=ax1.plot_date(date, profitv1, 'r-', linewidth=2)
ax1.grid(True)

plot2=ax2.plot_date(date, profitv2, 'b-', linewidth=2)
ax2.grid(True)

plot3=ax3.plot_date(date, trans, 'k-', linewidth=2)
ax3.grid(True)



#adding plugins and functionalities

class TweakToolbar(plugins.PluginBase):
    """Plugin for changing toolbar"""

    JAVASCRIPT = """
    mpld3.register_plugin("tweaktoolbar", TweakToolbar);
    TweakToolbar.prototype = Object.create(mpld3.Plugin.prototype);
    TweakToolbar.prototype.constructor = TweakToolbar;
    function TweakToolbar(fig, props){
        mpld3.Plugin.call(this, fig, props);
    };

    TweakToolbar.prototype.draw = function(){
      // the toolbar svg doesn't exist
      // yet, so first draw it
      this.fig.toolbar.draw();

      // then change the toolbar as desired

      // show toolbar
      this.fig.toolbar.buttonsobj.transition(750).attr("y", 0);
      
      // remove event triggers
      this.fig.canvas
        .on("mouseenter", null)
        .on("mouseleave", null)
        .on("touchenter", null)
        .on("touchstart", null);


      // then remove the draw function,
      // so that it is not called again
      this.fig.toolbar.draw = function() {}
    }
    """
    def __init__(self):
        self.dict_ = {"type": "tweaktoolbar"}
		
class TopToolbar(plugins.PluginBase):
    """Plugin for moving toolbar to top of figure"""

    JAVASCRIPT = """
    mpld3.register_plugin("toptoolbar", TopToolbar);
    TopToolbar.prototype = Object.create(mpld3.Plugin.prototype);
    TopToolbar.prototype.constructor = TopToolbar;
    function TopToolbar(fig, props){
        mpld3.Plugin.call(this, fig, props);
    };

    TopToolbar.prototype.draw = function(){
      // the toolbar svg doesn't exist
      // yet, so first draw it
      this.fig.toolbar.draw();

      // then change the y position to be
      // at the top of the figure
      this.fig.toolbar.toolbar.attr("y", 2);

      // then remove the draw function,
      // so that it is not called again
      this.fig.toolbar.draw = function() {}
    }
    """
    def __init__(self):
        self.dict_ = {"type": "toptoolbar"}

labels=value_z.tolist()
tooltip = mpld3.plugins.PointLabelTooltip(plot1[0], labels=labels,voffset=15)
plugins.connect(plt.gcf(), TopToolbar(),TweakToolbar(),tooltip)

#shaping and saving
plt.subplots_adjust(left=0.05, bottom=0.05, right=0.94, top=0.95, wspace=0.3, hspace=0.3)
mpld3.save_html(fig, "plot_output.html")



