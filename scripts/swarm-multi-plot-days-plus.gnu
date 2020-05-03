# 2018-07-13 bdekoz
# expect directories hour/day/week with media-title-hours.csv, etc inside.

set datafile separator ','
set border 0
#set tmargin at screen 0.05
#set bmargin at screen 0.05
#set rmargin at screen 0.05
#set lmargin at screen 0.05

# TERMINAL
#set terminal svg size 2112,1632 fname 'Apercu'
set terminal svg size 2160,1656 fname 'Apercu'
#set terminal svg size 2112,3264 fname 'Source Sans Pro' fsize 22
#set terminal svg size 4224,1632 fname 'Source Sans Pro' fsize 22
#set terminal svg size 4024,1632 fname 'Source Sans Pro' fsize 22
#set terminal svg size 8448,1632 fname 'Source Sans Pro' fsize 22
#set terminal svg size 12672,1632 fname 'Source Sans Pro' fsize 22

# LINE 1
#set style line 1 lc rgb '#FFBBF1' lt 1 lw 2 pt 7 ps 1   # --- pink
set style line 1 lc rgb '#888888' lt 1 lw 2 pt 7 ps 1   # --- pink

# LINE 2
#set style line 2 lc rgb '#FFFF00' lt 1 lw 2 pt 7 ps 1   # --- yellow
set style line 2 lc rgb '#444444' lt 1 lw 2 pt 7 ps 1   # --- yellow

# LINE 3
#set style line 3 lc rgb '#88000000' lt 1 lw 1 pt 3 ps 0.5   # --- black x 50%
set style line 3 lc rgb '#000000' lt 1 lw 1 pt 3 ps 0.5   # --- black

# LINE 4
#set style line 4 lc rgb '#88AAAAAA' lt 1 lw 1 pt 6 ps 0.3   # gray x 50%
set style line 4 lc rgb '#AAAAAA' lt 1 lw 1 pt 6 ps 1   # gray

# LINE 9
#set style line 9 linetype 1 linecolor 1 linewidth 1 ps 1
set style line 9 linewidth 1 linecolor variable pointsize 0.5
#set style line 9 default


set style fill transparent solid 0.5 noborder

# LABELS, FORMATTING, MARGINS
set autoscale y
set ylabel "UNIQUE PEERS" font "Apercu,24" offset -2,0

set decimal locale
set format y "%'g"
set format y "%'.0f"
#set border 3

set lmargin 20
set rmargin 20
set tmargin 20
set bmargin 20

FILES = system("find . -type f -name '*.csv' | sort")
TITLES = system("find . -type f -name '*.csv' | sort | sed -e 's/-days.csv//' -e 's|^\./||' ")

#set key off
set output 'multi-day.svg'

set xtics 1 rotate by 90 right nomirror font "SourceCodePro-Light,9"
set xlabel "DAYS" font "Apercu,24" offset 0,-12
# Scale x range auto (*) or to a fixed number of days (below as 126)
set xrange [0:*]
#set xrange [0:126]

# Start Plotting...
set multiplot

plot for [i=1:words(FILES)] word(FILES,i) u 1:2 with linespoints pointsize 0.75 title word(TITLES,i)

# multi plot with datestamp below duration.
unset ylabel
unset xlabel
unset autoscale y

unset ytics
unset y2tics
unset x2tics

set xtics 1 rotate by 90 right nomirror font "SourceCodePro-Light,9" offset 0,0

# Get dates from one of the *.csv files above (field 6) for label text
# aka use the first one from word(FILES,0)
FILET = system("find . -type f -name '*.csv' | sort | head -1")
print "using file for dates: "
print FILET

#plot 'r4k-days.csv' using 1:2:xticlabels(6)

plot FILET using 1:2:xticlabels(sprintf('%s  %5u', stringcolumn(6), column(1))) notitle

unset multiplot