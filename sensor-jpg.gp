# gnplot only works on UTC
# to get the value "-5" for your TZ, use 
# date +%z
set xtics 3600
set grid ytics
set ytics 100
set format y "%g"
set y2tics 0 +10
set ytics nomirror
set xdata time
set timefmt "%s"
set format x "%H:%M"
set datafile separator ","

set title "24 hours local time"
set xlabel "Time"
set ylabel "CO2 VOC"
set y2label "temp humid PM1 PM2.5 PM10"

set key outside
set key center
set key bottom
set key autotitle columnheader
set key horizontal

set style line 2 linetype 1 linewidth 2 linecolor rgb '#0000ff"
set style line 3 linetype 1 linewidth 2 linecolor rgb '#008000"
set style line 4 linetype 1 linewidth 2 linecolor rgb '#ff0000"
set style line 5 linetype 1 linewidth 2 linecolor rgb '#ffa500"
set style line 6 linetype 1 linewidth 2 linecolor rgb '#000000"
set style line 7 linetype 1 linewidth 2 linecolor rgb '#808080"
set style line 8 linetype 1 linewidth 2 linecolor rgb '#d3d3d3"


#time,temp,humid,CO2,tVOC,PM1.0,PM2.5,PM10.0

plot "all.log" using ($1+(-5*3600)):4 with linespoints linestyle 4, \
     "all.log" using ($1+(-5*3600)):5 with linespoints linestyle 5, \
     "all.log" using ($1+(-5*3600)):2 with linespoints linestyle 2 axis x1y2, \
     "all.log" using ($1+(-5*3600)):3 with linespoints linestyle 3 axis x1y2, \
     "all.log" using ($1+(-5*3600)):6 with linespoints linestyle 6 axis x1y2, \
     "all.log" using ($1+(-5*3600)):7 with linespoints linestyle 7 axis x1y2, \
     "all.log" using ($1+(-5*3600)):8 with linespoints linestyle 8 axis x1y2
#set output
#set terminal jpeg size 1920,1080 color enhanced "Helvetica" 20
set terminal jpeg size 1920,1080
set output "output.jpg"
#     "all.log" using ($1+(-5*3600)):4 with linespoints linestyle 1,\
#     "all.log" using ($1+(-5*3600)):5  with linespoints linestyle 2,\
