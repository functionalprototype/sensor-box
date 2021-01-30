set xdata time
set timefmt "%s"
set xtics 3600
set format x "%H:%M"
set datafile separator ","
set title "24 hours EST"
set key autotitle columnheader
plot "all.log" u 1:2, \
     "all.log" u 1:3, \
     "all.log" u 1:4, \
     "all.log" u 1:5
set output
