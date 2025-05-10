set terminal postscript eps enhanced color font 'Helvetica,14'
set output 'output_data/r431.hi_barolocentered/0/r431_rc_inc_pa.eps'
unset key
set size 0.60, 1
set style line 1 lc rgb '#A9A9A9' lt 4 pt 7 lw 1
set style line 2 lc rgb '#B22222' lt 9 pt 9 lw 1
set macros
XTICS   = 'set xtics 33.170216; set mxtics 2; set format x "%g" '
NOXTICS = 'unset xlabel; set xtics  33.170216; set mxtics 2; set format x '' '
LABELF  = 'set xlabel font "Helvetica,13"; set ylabel font "Helvetica,13" '
TICSF   = 'set xtics font "Helvetica,12"; set ytics font "Helvetica,12" '
TMARGIN = 'set tmargin at screen 0.95; set bmargin at screen 0.47; set lmargin at screen 0.10; set rmargin at screen 0.50'
MMARGIN = 'set tmargin at screen 0.47; set bmargin at screen 0.27; set lmargin at screen 0.10; set rmargin at screen 0.50'
BMARGIN = 'set tmargin at screen 0.27; set bmargin at screen 0.10; set lmargin at screen 0.10; set rmargin at screen 0.50'
set multiplot layout 3,1 rowsfirst
@LABELF
@TICSF
@TMARGIN
@NOXTICS
set yrange [-5:124.421]
set ylabel 'V_c  [km/s]'
set ytics 50
set mytics 5
plot 'output_data/r431.hi_barolocentered/0/rings_final1.txt' u 2:3:($3+$13):($3+$14) w errorbars ls 1, 'output_data/r431.hi_barolocentered/0/rings_final1.txt' u 2:3 w lp ls 1, 'output_data/r431.hi_barolocentered/0/rings_final2.txt' u 2:3:($3+$13):($3+$14) w errorbars ls 2, 'output_data/r431.hi_barolocentered/0/rings_final2.txt' u 2:3 w lp ls 2
set title ''
@MMARGIN
@NOXTICS
set yrange [79.4339:97.0858]
set ylabel 'i [deg]'
set ytics 5
set mytics 5
plot 'output_data/r431.hi_barolocentered/0/rings_final1.txt' u 2:5:($5+$17):($5+$18) w errorbars ls 1, 'output_data/r431.hi_barolocentered/0/rings_final1.txt' u 2:5 w lp ls 1, 'output_data/r431.hi_barolocentered/0/rings_final2.txt' u 2:5 w lp ls 2
@BMARGIN
@XTICS
set xlabel 'Radius [arcsec]'
set yrange [83.2706:119.281]
set ylabel 'P.A. [deg]'
set ytics 5
set mytics 5
plot 'output_data/r431.hi_barolocentered/0/rings_final1.txt' u 2:6:($6+$19):($6+$20) w errorbars ls 1, 'output_data/r431.hi_barolocentered/0/rings_final1.txt' u 2:6 w lp ls 1, 'output_data/r431.hi_barolocentered/0/rings_final2.txt' u 2:6 w lp ls 2
unset multiplot
set output 'output_data/r431.hi_barolocentered/0/r431_disp_vsys_z0.eps'
unset key
set xlabel 'Radius [arcsec]'
set xtics 200
set mxtics 2
set macros
TMARGIN = 'set tmargin at screen 0.94; set bmargin at screen 0.66; set lmargin at screen 0.10; set rmargin at screen 0.50'
MMARGIN = 'set tmargin at screen 0.66; set bmargin at screen 0.38; set lmargin at screen 0.10; set rmargin at screen 0.50'
BMARGIN = 'set tmargin at screen 0.38; set bmargin at screen 0.10; set lmargin at screen 0.10; set rmargin at screen 0.50'
set multiplot layout 3,1 rowsfirst
@LABELF
@TICSF
@TMARGIN
@NOXTICS
set yrange [0:5.00488]
set ylabel '{/Symbol s} [km/s]'
set ytics 5
set mytics 5
plot 'output_data/r431.hi_barolocentered/0/rings_final1.txt' u 2:4:($4+$15):($4+$16) w errorbars ls 1, 'output_data/r431.hi_barolocentered/0/rings_final1.txt' u 2:4 w lp ls 1, 'output_data/r431.hi_barolocentered/0/rings_final2.txt' u 2:4:($3+$15):($3+$16) w errorbars ls 2, 'output_data/r431.hi_barolocentered/0/rings_final2.txt' u 2:4 w lp ls 2
@MMARGIN
@NOXTICS
set yrange [-23.3698:-6.34082]
set ylabel 'V_{sys} [km/s]'
plot 'output_data/r431.hi_barolocentered/0/rings_final1.txt' u 2:12:($12+$21):($12+$22) w errorbars ls 1, 'output_data/r431.hi_barolocentered/0/rings_final1.txt' u 2:12 w lp ls 1, 'output_data/r431.hi_barolocentered/0/rings_final2.txt' u 2:12 w lp ls 2
@BMARGIN
@XTICS
set xlabel 'Radius [arcsec]'
set yrange [0:0]
set ylabel 'Scale height [arcsec]'
plot 'output_data/r431.hi_barolocentered/0/rings_final1.txt'u 2:8 w lp ls 1, 'output_data/r431.hi_barolocentered/0/rings_final2.txt' u 2:8 w lp ls 2
unset multiplot
set output 'output_data/r431.hi_barolocentered/0/r431_xc_yc_cd.eps'
set multiplot layout 3,1 rowsfirst
@LABELF
@TICSF
@TMARGIN
@NOXTICS
set yrange [84.726:103.554]
set ylabel 'X_c [pix]'
plot 'output_data/r431.hi_barolocentered/0/rings_final1.txt' u 2:10 w lp ls 1, 'output_data/r431.hi_barolocentered/0/rings_final2.txt' u 2:10 w lp ls 2
@MMARGIN
@NOXTICS
set yrange [86.6928:105.958]
set ylabel 'Y_c [pix]'
plot 'output_data/r431.hi_barolocentered/0/rings_final1.txt' u 2:11 w lp ls 1, 'output_data/r431.hi_barolocentered/0/rings_final2.txt' u 2:11 w lp ls 2
unset multiplot; reset
