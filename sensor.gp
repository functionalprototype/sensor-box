# gnplot only works on UTC
# to get the value "-5" for your TZ, use 
# date +%z
set xtics 3600
set grid ytics
set ytics 100
set format y "%g"
set xdata time
set timefmt "%s"
set format x "%H:%M"
set datafile separator ","
set title "24 hours local time"
set key autotitle columnheader

#set style line 1 linetype 1 linewidth 2 linecolor rgb '#ff0000'
#set style line 2 linetype 1 linewidth 2 linecolor rgb '#00ff00"

plot "all.log" using ($1+(-5*3600)):2, \
     "all.log" using ($1+(-5*3600)):3, \
     "all.log" using ($1+(-5*3600)):4, \
     "all.log" using ($1+(-5*3600)):5, \
     "all.log" using ($1+(-5*3600)):6, \
     "all.log" using ($1+(-5*3600)):7, \
     "all.log" using ($1+(-5*3600)):8
set output
#     "all.log" using ($1+(-5*3600)):4 with linespoints linestyle 1,\
#     "all.log" using ($1+(-5*3600)):5  with linespoints linestyle 2,\
