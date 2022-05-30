import pandas as pd
from bokeh.plotting import figure
from bokeh.io import output_file, show, export_svgs
from bokeh.plotting import ColumnDataSource

POINTS = 1000
df = pd.read_csv('coords.csv', header=None, names=['lat', 'lon'])
print(df.head(), df.shape)
df1 = df.groupby(pd.qcut(df.index, POINTS, labels=False)).mean()
print(df1.head(), df1.shape)
source = ColumnDataSource(df1)
y_size_in_degrees = df1.lat.max() - df1.lat.min()
x_size_in_degrees = df1.lon.max() - df1.lon.min()
yscale = 110989  # length 1 degree of lon
xscale = (91290 + 91290 + 90165) / 3  # length 1 degree of lat

yx = y_size_in_degrees * yscale / (x_size_in_degrees * xscale)

p = figure(x_axis_label='lon',
           y_axis_label='lat',
           plot_width=1200, plot_height=int(1200*yx))
p.xaxis.visible = False
p.xgrid.visible = False
p.yaxis.visible = False
p.ygrid.visible = False

# Add patches to figure p with line_color=white for x and y
p.patch('lon', 'lat', source=source)
p.output_backend = "svg"
export_svgs(p, filename=f"plot{POINTS}.svg")

# Specify the name of the output file and show the result
output_file(f'crete{POINTS}.html')
show(p)
