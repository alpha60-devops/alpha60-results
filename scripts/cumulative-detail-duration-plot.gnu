# 2022-08-10 bdekoz
# expect directories hour/day/week with media-title-hours.csv, etc inside.

reset
set decimal locale
set datafile separator ','
set border 0

# TERMINAL
#set terminal svg size 1080,1080 fname 'Apercu'
#set terminal svg size 1080,1350 fname 'Apercu'
set terminal svg size 1920,1350 fname 'Apercu'
set lmargin 15
set rmargin 15
set tmargin 20
set bmargin 20

# FILES, OUTPUT FILES
#FILES = system("find . -type f -name '*.csv' | sort")
FILECD = "ukr-rus-war-2022-cumulative-detail-by-day.csv"
FILEUD = "ukr-rus-war-2022-days.csv"
outputfilename = sprintf("%s-cumulative-%s.svg", "ukr-rus-cyberwar", "day");
set output outputfilename


# LINE 1
#set style line 1 lc rgb '#888888' lt 1 lw 2 pt 7 ps 1   # --- gray
#set style line 1 lc rgb '#FFBBF1' lt 1 lw 2 pt 1 ps 1   # --- pink
set style line 1 lc rgb '#FF0000' lt 1 lw 2 pt 1 ps 1   # --- red

# LINE 2
#set style line 2 lc rgb '#FFFF00' lt 1 lw 2 pt 7 ps 1   # --- yellow
set style line 2 lc rgb '#444444' lt 1 lw 2 pt 7 ps 1   # --- yellow

# LINE 3
#set style line 3 lc rgb '#88000000' lt 1 lw 1 pt 3 ps 0.5   # --- black x size 50%
set style line 30 lc rgb '#000000' lt 1 lw 1 pt 3 ps 0.75   # --- black
set style line 31 lc rgb '#767676' lt 1 lw 1 pt 7 ps 0.5   # wcag grey
set style line 32 lc rgb '#949494' lt 3 lw 1 pt 7 ps 0.5   # wcag light grey
set style line 33 lc rgb '#969696' lt 3 lw 1 pt 9 ps 1   # --- wcag light light grey

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
set xlabel xlabeltext font "Apercu,16" offset 0,0

# 1 btiha
ylabeltext = "BTIHA"
set ylabel ylabeltext font "Apercu,16" offset -6,0
set size 1,0.33
set origin 0,0
plot for [data in FILECD] data u 1:2 with linespoints ls 1 notitle
unset ylabel
unset xlabel

# 2,3 cumulative upeer/useeds
ylabeltext = "CUMULATIVE PEERS/SEEDS"
set ylabel ylabeltext font "Apercu,16" offset -1,0
set size 1,0.33
set origin 0,0.66
plot FILECD using 1:3 with linespoints ls 30, '' using 1:4 with linespoints ls 32 notitle
unset ylabel

# 3,5 per-day upeer/useeds
ylabeltext = "DAILY PEERS/SEEDS"
set ylabel ylabeltext font "Apercu,16" offset -2,0
set size 1,0.33
set origin 0,0.33
plot FILEUD using 1:2 with linespoints ls 30, '' using 1:3 with linespoints ls 32 notitle
unset ylabel


unset multiplot
