# gnplot only works on UTC
# to get the value "-5" for your TZ, use 
# date +%z
set xtics 3600
set format x "%H:%M"
set ytics 100
set grid ytics
set format y "%g"
set xdata time
set timefmt "%s"
set datafile separator ","
set title "VOC PPM 1.0 2.5 10.0
set key autotitle columnheader
plot "all.log" using ($1+(-5*3600)):5, \
     "all.log" using ($1+(-5*3600)):6,\
     "all.log" using ($1+(-5*3600)):7,\
     "all.log" using ($1+(-5*3600)):8
set output
