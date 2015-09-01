from matplotlib.widgets import Slider
from pylab import *

def f(S, Gmax, Km):
    s1 = Gmax*S  #G_max
    e1 = S + Km #K_m
    return divide(s1,e1)

S=arange(0,100,0.1)

ax = subplot(111)
subplots_adjust(left=0.15, bottom=0.25)
l, = plot(f(S, 1.0, 1.0))
grid(False)
title('Playing with sliders')
xlabel('time')
ylabel('concentration')

axcolor = 'lightgoldenrodyellow'
axGmax = axes([0.15, 0.1, 0.65, 0.03], axisbg=axcolor)
axKm = axes([0.15, 0.15, 0.65, 0.03], axisbg=axcolor)

sGmax = Slider(axGmax, 'Gmax', 0.1, 3.0, valinit=1)
sKm = Slider(axKm, 'Km', 0.01, 1.0, valinit=1)

def update(val):
    l.set_ydata(f(S, sGmax.val, sKm.val))

sGmax.on_changed(update)
sKm.on_changed(update)

show()