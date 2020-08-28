import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk
import pandas as p
from matplotlib.backends.backend_gtk3agg import FigureCanvas  # or gtk3cairo.
import datetime
from numpy.random import random
from matplotlib.figure import Figure
import common

def datatemplate(col,cell,model,itr,unused):
    cell.set_property("text",common.format_indian_cr(model.get(itr,unused)[0]))

class DataManager(Gtk.Window):
    c=p.read_csv('tn-cag-maintable.csv')
    columns=['Rev','Tax','GST','Stamp','Land','Sales,Trade','Excise','Share of Union Tax','Other',
                'Non-Tax Rev',
                'Grants',
                'CapRec','CR-Recoveries','CR-Other','Borrowing',
                'Total Inflow',
                'RevEx',
                'Expenditure','Interest','Salaries','Pension','Subsidy',
                'Investments','Capex','sal',
                "Sector Wise Expenditure",
                "General Sector","GS-Revenue","GS-Capital",
                "Social Sector","SS-Revenue","SS-Capital",
                "Economic Sector","ES-Revenue","ES-Capital","ES-Grants",
                'Total Expenditure',#'RevEx+CapEx',
                "Loans Disbursed",'RevDef','FiscalDef','PrimaryDef','Year','Month']
    c.columns=columns
    #c=c.drop([7,9,14]) # drop estimate rows month = 9999 and row for 2019 March which falls under fy 2018
    c.sort_values(['Year','Month'],inplace=True,ascending=False)
    view=['Year','Month','Total Inflow','Total Expenditure','Borrowing','Interest']
    data=c[view].to_numpy()
    num_cols=len(view)

    def __init__(self):
        super().__init__()
        self.set_default_size(600, 600)
        self.connect('destroy', lambda win: Gtk.main_quit())

        self.set_title('TN Monthly Finances')
        self.set_border_width(8)

        vbox = Gtk.VBox(homogeneous=False, spacing=8)
        self.add(vbox)

        label = Gtk.Label(label='Click a row to plot the data')

        vbox.pack_start(label, False, False, 0)

        sw = Gtk.ScrolledWindow()
        sw.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        sw.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        vbox.pack_start(sw, True, True, 0)

        model = self.create_model()

        self.treeview = Gtk.TreeView(model=model)
        self.treeview.set_property('activate-on-single-click',True)


        # Matplotlib stuff
        fig = Figure(figsize=(6, 4))

        self.canvas = FigureCanvas(fig)  # a Gtk.DrawingArea
        vbox.pack_start(self.canvas, True, True, 0)
        ax = fig.add_subplot(111)
        ax.set_xticks([i for i in range(self.num_cols-2)])
        ax.set_xticklabels(self.view[2:])
        self.line, = ax.plot(self.data[0, 2:], 'go')  # plot the first row

        self.treeview.connect('row-activated', self.plot_row)
        sw.add(self.treeview)

        self.add_columns()

        self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK |
                        Gdk.EventMask.KEY_PRESS_MASK |
                        Gdk.EventMask.KEY_RELEASE_MASK)

    def plot_row(self, treeview, path, view_column):
        ind, = path  # get the index into data
        points = self.data[ind, 2:]
        self.line.set_ydata(points)
        self.canvas.draw()

    def add_columns(self):
        for i in range(self.num_cols):
            r=Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(self.view[i], r, text=i)
            if i >=2:
                column.set_cell_data_func(r,datatemplate,i)
            self.treeview.append_column(column)

    def create_model(self):
        types = [str,str] + [float] * (self.num_cols-2)
        #print(types)
        store = Gtk.ListStore(*types)
        for row in self.data:
            tmp=[str(int(row[0])), str(int(row[1]))]
            if tmp[1] == '9999':
                tmp[1]='Estimate'
            else:
                tmp[1]=datetime.datetime.strptime(tmp[1],"%m").strftime("%b")
            tmp.extend(row[2:])
            store.append(tuple(tmp))
        return store


manager = DataManager()
manager.show_all()
Gtk.main()