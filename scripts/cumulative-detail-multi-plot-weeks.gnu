# 2022-07-31 bdekoz
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
set ylabel "UNIQUE PEERS" font "Apercu,24" offset -1,0

set decimal locale
set format y "%'g"
set format y "%'.0f"
#set border 3

set lmargin 25
set rmargin 15
set tmargin 20
set bmargin 20

FILES = system("find . -type f -name '*.csv' | sort")
TITLES = system("find . -type f -name '*.csv' | sort | sed -e 's/-weeks.csv//' -e 's|^\./||' ")

set xtics 1 rotate by 90 right nomirror font "SourceCodePro-Light,9"

set xlabel "WEEKS" font "Apercu,24" offset 0,-12
set output 'cumulative-multi-week.svg'

set multiplot

#plot for [data in FILES] data u 1:2
#plot for [data in FILES] data u 1:2 w p pt 1 lt rgb 'black' notitle

#plot for [i=1:words(FILES)] word(FILES,i) u 1:2 w p pt 1 title word(TITLES,i)

# pointsize 0.5, 0.75, 1
#plot for [i=1:words(FILES)] word(FILES,i) u 1:2 with linespoints pointsize 0.75 title word(TITLES,i)

plot for [i=1:words(FILES)] word(FILES,i) u 1:3 with linespoints ls 3 title word(TITLES,i)

plot for [i=1:words(FILES)] word(FILES,i) u 1:4 with linespoints ls 4 title word(TITLES,i)




#plot 'multi-weeks.csv' using 1:2 with linespoints ls 1


unset multiplot
