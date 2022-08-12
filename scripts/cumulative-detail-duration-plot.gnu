# 2022-08-10 bdekoz
# expect directories hour/day/week with media-title-hours.csv, etc inside.

reset
set decimal locale
set datafile separator ','
set border 0

# TERMINAL
set terminal svg size 1920,1080 fname 'Apercu'
set lmargin 15
set rmargin 15
set tmargin 20
set bmargin 20

# FILES, OUTPUT FILES
#FILES = system("find . -type f -name '*.csv' | sort")
FILES = "ukr-rus-war-2022-cumulative-detail-by-day.csv"
outputfilename = sprintf("%s-cumulative-%s.svg", "ukr-rus-cyberwar", "day");
set output outputfilename


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
set format y "%'g"
set format y "%'.0f"
set autoscale y
set xtics 1 rotate by 90 right nomirror font "SourceCodePro-Light,9"

# PLOT
#
# A note about
# set origin (xorigin),(yorigin)
#
# A box of length one, 0,0 is the lower left.
#
#             (1,1)
#    (0,0)
#
# set multiplot
# output two graphs in 2 rows 1 col
#set multiplot layout 2,1 upwards
set size 1,1
set multiplot
unset key

xlabeltext = "DAYS"
set xlabel xlabeltext font "Apercu,24" offset 0,-2

# 1 btiha
ylabeltext = "BTIHA"
set ylabel ylabeltext font "Apercu,24" offset -6,0
set size 1,0.5
set origin 0,0
plot for [data in FILES] data u 1:2 with linespoints ls 3 notitle
unset ylabel
#unset autoscale y

# 2,3 upeer/useeds
ylabeltext = "UNIQUE PEERS"
set ylabel ylabeltext font "Apercu,24" offset -6,0
set size 1,0.5
set origin 0,0.5
plot for [data in FILES] data u 1:3:4 with linespoints ls 4 notitle
#plot for [data in FILES] data u 1:4 with linespoints ls 5 notitle


unset multiplot
