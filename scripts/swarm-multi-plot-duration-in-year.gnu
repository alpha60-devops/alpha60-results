# 2024-05-11 bdekoz

# precondition:
# expect directories hour/day/week with media-title-hours.csv, etc inside.

# invoke:
# gnuplot -c swarm-multi-plot-duration-in-year.gnu week 2024

# NB: have to manually toggle day/week below

duration=ARG1
yearstamp=ARG2
print "invoked as: ", ARG0, duration, yearstamp

OFILE=system("echo 'multi-'" . duration . "-in-year-" . yearstamp . ".svg")
set output OFILE
print "outputfile: ", OFILE

set datafile separator ','

set border 0

# Margins as 5% of screen size
#set tmargin at screen 0.05
#set bmargin at screen 0.05
#set rmargin at screen 0.05
#set lmargin at screen 0.05

# Margins as 30 x times of one character
set lmargin 30
set rmargin 30
set tmargin 30
set bmargin 40

# TERMINAL
# width, height in pixels

# Eng C base size in pixels...
# 122 days and 1 x so...
#set terminal svg size 2160,1656 fname 'Apercu'
# 244 days and 2 x so...
#set terminal svg size 4320,1656 fname 'Apercu'
#set terminal svg size 4224,1632 fname 'Apercu'
# 365 days and 3 x above size, so...
#set terminal svg size 6480,1656 fname 'Apercu'

# 4K base size in pixels
set terminal svg size 3840,2160 fname 'Apercu'

#set terminal svg size 2112,1632 fname 'Apercu'
#set terminal svg size 2112,3264 fname 'Source Sans Pro' fsize 22
#set terminal svg size 4224,1632 fname 'Source Sans Pro' fsize 22
#set terminal svg size 4024,1632 fname 'Source Sans Pro' fsize 22
#set terminal svg size 8448,1632 fname 'Source Sans Pro' fsize 22
#set terminal svg size 12672,1632 fname 'Source Sans Pro' fsize 22

# LINE 1
#set style line 1 lc rgb '#FFBBF1' lt 1 lw 2 pt 7 ps 1   # --- pink
set style line 1 lc rgb '#888888' lt 6 lw 8 pt 7 ps 1   # --- pink

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
set style line 9 linewidth 1 linecolor variable pointsize 2
#set style line 9 default


set style fill transparent solid 0.5 noborder
set decimal locale

# LABELS, FORMATTING, MARGINS
#set autoscale y
set yrange [0:125000]
#set yrange [0:650000]
set ylabel "UNIQUE PEERS" font "Apercu,44" offset -12,0

set format y "%'g"
set format y "%'.0f"
set ytics font "SourceCodePro-Light,20"

#set border 3

FILES = system("find . -type f -name '*.csv' | sort")
#TITLES = system("find . -type f -name '*.csv' | sort | sed -e 's/-days.csv//' -e 's|^\./||' ")
TITLES = system("find . -type f -name '*.csv' | sort | sed -e 's/-weeks.csv//' -e 's|^\./||' ")

#set key off

set xtics 1 rotate by 90 right nomirror font "SourceCodePro-Light,20"
XLABELTXT=system("echo ''" . duration . "S IN " . yearstamp . " | tr '[a-z]' '[A-Z]'")
set xlabel XLABELTXT font "Apercu,44" offset 0,-24, char 0 right

# Scale x range auto (*) ...
#set xrange [0:*]

# Scale x range to a fixed number of days or weeks in a year.
#set xrange [0:365]
set xrange [0:53]

# Start Plotting...
set multiplot

plot for [i=1:words(FILES)] word(FILES,i) u 1:2 with linespoints pointsize 2 title word(TITLES,i)

# multi plot with datestamp below duration.
unset ylabel
unset xlabel
unset autoscale y

unset ytics
unset y2tics
unset x2tics

# effective type size in points is 6
set xtics 1 rotate by 90 right nomirror font "SourceCodePro-Light,20" offset 0,0

# Get dates from one of the *.csv files above (field 6) for label text
# aka use the first one from word(FILES,0)
FILET = system("find . -type f -name '*.csv' | sort | head -1")
print "using file for dates: ", FILET

plot FILET using 1:2:xticlabels(sprintf('%s  %6.3u', stringcolumn(6), column(1))) notitle

unset multiplot