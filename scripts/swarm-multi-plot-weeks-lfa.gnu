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

# gnuplot
# linestyle
# pointstyle : available point symbols

# pointstyle 2
# outline/fill square, pt(4/5)
# outline/fill circle, pt(6,7)
# outline/fill top tri, pt(8,9)
# outline/fill down tri, pt(10,11)
# outline/fill diamond, pt(12,13)
# pt 2 x, pt 3 plusx

# dashtype '.', '-', '...' aka dt

# pointstyle 4
# pt 196, 39, 118, 45 # fill square white square moves CW
# pt 199, 56, 127, 125 # outline diamond square fill 0/3/6/9 CW
# pt 57, 135, 129, 126 # outline diamond rect fill 0/3/6/9 CW

# LINE 1-16
# 1,2 acolyte violet
# 3,4 ahsoka  purple
# 5,6 andor 71, 82
# 7 boba fett 2
# 8-14 mando
# 15,16 obiwan 70,80
set style line 1 lc rgb '#A71AFD' lt 1 lw 2 pt 9 dt '.' ps 1
set style line 2 lc rgb '#A71AFD' lt 1 lw 2 pt 9 ps 1

set style line 3 lc rgb '#FC12C9' lt 1 lw 2 pt 11 dt '.' ps 1
set style line 4 lc rgb '#FC12C9' lt 1 lw 2 pt 11 ps 1

set style line 5 lc rgb '#FECD0F' lt 1 lw 2 pt 7 dt '.' ps 1
set style line 6 lc rgb '#FECD0F' lt 1 lw 2 pt 7 ps 1

set style line 7 lc rgb '#E9700A' lt 1 lw 2 pt 3 ps 1

set style line 8 lc rgb '#10e1f8' lt 1 lw 2 pt 13 dt '.' ps 1
set style line 9 lc rgb '#10e1f8' lt 1 lw 2 pt 12 dt '-' ps 1
set style line 10 lc rgb '#10e1f8' lt 1 lw 2 pt 13 ps 1
set style line 11 lc rgb '#10B0FF' lt 1 lw 2 pt 13 dt '.' ps 1
set style line 12 lc rgb '#10B0FF' lt 1 lw 2 pt 13 ps 1
set style line 13 lc rgb '#3957FF' lt 1 lw 2 pt 13 dt '.' ps 1
set style line 14 lc rgb '#3957FF' lt 1 lw 2 pt 13 ps 1

set style line 15 lc rgb '#0AD811' lt 1 lw 2 pt 4 dt '.' ps 1
set style line 16 lc rgb '#0AD811' lt 1 lw 2 pt 5 ps 1


set style fill transparent solid 0.5 noborder

# LABELS, FORMATTING, MARGINS
set autoscale y
set ylabel "DOWNLOADS" font "Apercu,24" offset -1,0

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


set xtics 1 rotate by 90 right

set xlabel "WEEKS" font "Apercu,24" offset 0,-1
set output 'multi-week.svg'

#plot for [data in FILES] data u 1:2
#plot for [data in FILES] data u 1:2 w p pt 1 lt rgb 'black' notitle

#plot for [i=1:words(FILES)] word(FILES,i) u 1:2 w p pt 1 title word(TITLES,i)

# pointsize 0.5, 0.75, 1
plot for [i=1:words(FILES)] word(FILES,i) u 1:2 with linespoints ls i pointsize 0.75 title word(TITLES,i)

#plot for [i=1:words(FILES)] word(FILES,i) using 1:2 with linespoints ls 9 title word(TITLES,i)



#plot 'multi-weeks.csv' using 1:2 with linespoints ls 1
