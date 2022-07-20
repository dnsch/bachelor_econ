*------------------------------------------------------------------------------*
*   Stata Code for my Bachelor Thesis in Economics          
*   by
* 	Daniel Schäffer
*	2022        
*------------------------------------------------------------------------------*

clear all
set more off 

//change directory to yours!!
cd ""

import delimited growth_country_level_df.csv

encode country, gen(ncountry)

//Dust regression, commented out for better readibility
/*
*Predicted Dust:

*L0 dust_dry
eststo: reg dust_dry_t0 dust_pred_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 i.ncountry c.year i.ncountry#c.pow_year

estimates store model1


eststo: reg dust_dry_t0 dust_pred_wt_dry_t0 dust_pred_wt_dry_t1 prec_wt_dry_t0 prec_wt_dry_t1 temp_wt_dry_t0 temp_wt_dry_t1 i.ncountry c.year i.ncountry#c.pow_year

estimates store model2


eststo: reg dust_dry_t0 dust_pred_wt_dry_t0 dust_pred_wt_dry_t1 dust_pred_wt_dry_t2 prec_wt_dry_t0 prec_wt_dry_t1 prec_wt_dry_t2 temp_wt_dry_t0 temp_wt_dry_t1 temp_wt_dry_t2 i.ncountry c.year i.ncountry#c.pow_year

estimates store model3


eststo: reg dust_dry_t0 dust_pred_wt_dry_t0 dust_pred_wt_dry_t1 dust_pred_wt_dry_t2 dust_pred_wt_dry_t3 prec_wt_dry_t0 prec_wt_dry_t1 prec_wt_dry_t2 prec_wt_dry_t3 temp_wt_dry_t0 temp_wt_dry_t1 temp_wt_dry_t2 temp_wt_dry_t3 i.ncountry c.year i.ncountry#c.pow_year

estimates store model4


eststo: reg dust_dry_t0 dust_pred_wt_dry_t0 dust_pred_wt_dry_t1 dust_pred_wt_dry_t2 dust_pred_wt_dry_t3 dust_pred_wt_dry_t4 prec_wt_dry_t0 prec_wt_dry_t1 prec_wt_dry_t2 prec_wt_dry_t3 prec_wt_dry_t4 temp_wt_dry_t0 temp_wt_dry_t1 temp_wt_dry_t2 temp_wt_dry_t3 temp_wt_dry_t4 i.ncountry c.year i.ncountry#c.pow_year

estimates store model5

eststo: reg dust_dry_t0 dust_pred_wt_dry_t0 dust_pred_wt_dry_t1 dust_pred_wt_dry_t2 dust_pred_wt_dry_t3 dust_pred_wt_dry_t4 dust_pred_wt_dry_t5 prec_wt_dry_t0 prec_wt_dry_t1 prec_wt_dry_t2 prec_wt_dry_t3 prec_wt_dry_t4 prec_wt_dry_t5 temp_wt_dry_t0 temp_wt_dry_t1 temp_wt_dry_t2 temp_wt_dry_t3 temp_wt_dry_t4 temp_wt_dry_t5 i.ncountry c.year i.ncountry#c.pow_year

estimates store model6

esttab model1 model2 model3 model4 model5 model6 using l0_pred.csv, cells(b(star) se) stats(N r2_a, fmt(0 4)) keep(dust_pred_wt_dry_t0 dust_pred_wt_dry_t1 dust_pred_wt_dry_t2 dust_pred_wt_dry_t3 dust_pred_wt_dry_t4 dust_pred_wt_dry_t5 prec_wt_dry_t0 prec_wt_dry_t1 prec_wt_dry_t2 prec_wt_dry_t3 prec_wt_dry_t4 prec_wt_dry_t5 temp_wt_dry_t0 temp_wt_dry_t1 temp_wt_dry_t2 temp_wt_dry_t3 temp_wt_dry_t4 temp_wt_dry_t5 _cons) replace plain star(* 0.10 ** 0.05 *** 0.01) order(dust_pred_wt_dry_t0 dust_pred_wt_dry_t1 dust_pred_wt_dry_t2 dust_pred_wt_dry_t3 dust_pred_wt_dry_t4 dust_pred_wt_dry_t5 prec_wt_dry_t0 prec_wt_dry_t1 prec_wt_dry_t2 prec_wt_dry_t3 prec_wt_dry_t4 prec_wt_dry_t5 temp_wt_dry_t0 temp_wt_dry_t1 temp_wt_dry_t2 temp_wt_dry_t3 temp_wt_dry_t4 temp_wt_dry_t5 _cons)

***********************************

*L1 dust_dry

eststo: reg dust_dry_t1 dust_pred_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 i.ncountry c.year i.ncountry#c.pow_year

estimates store model1

eststo: reg dust_dry_t1 dust_pred_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_pred_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 i.ncountry c.year i.ncountry#c.pow_year 

estimates store model2

eststo: reg dust_dry_t1 dust_pred_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_pred_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 dust_pred_wt_dry_t2 prec_wt_dry_t2 temp_wt_dry_t2 i.ncountry c.year i.ncountry#c.pow_year

estimates store model3

eststo: reg dust_dry_t1 dust_pred_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_pred_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 dust_pred_wt_dry_t2 prec_wt_dry_t2 temp_wt_dry_t2 dust_pred_wt_dry_t3 prec_wt_dry_t3 temp_wt_dry_t3 i.ncountry c.year i.ncountry#c.pow_year

estimates store model4

eststo: reg dust_dry_t1 dust_pred_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_pred_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 dust_pred_wt_dry_t2 prec_wt_dry_t2 temp_wt_dry_t2 dust_pred_wt_dry_t3 prec_wt_dry_t3 temp_wt_dry_t3 dust_pred_wt_dry_t4 prec_wt_dry_t4 temp_wt_dry_t4 i.ncountry c.year i.ncountry#c.pow_year

estimates store model5

eststo: reg dust_dry_t1 dust_pred_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_pred_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 dust_pred_wt_dry_t2 prec_wt_dry_t2 temp_wt_dry_t2 dust_pred_wt_dry_t3 prec_wt_dry_t3 temp_wt_dry_t3 dust_pred_wt_dry_t4 prec_wt_dry_t4 temp_wt_dry_t4 dust_pred_wt_dry_t5 prec_wt_dry_t5 temp_wt_dry_t5 i.ncountry c.year i.ncountry#c.pow_year

estimates store model6

esttab model1 model2 model3 model4 model5 model6 using l1_pred.csv, cells(b(star) se) stats(N r2_a, fmt(0 4)) keep(dust_pred_wt_dry_t0 dust_pred_wt_dry_t1 dust_pred_wt_dry_t2 dust_pred_wt_dry_t3 dust_pred_wt_dry_t4 dust_pred_wt_dry_t5 prec_wt_dry_t0 prec_wt_dry_t1 prec_wt_dry_t2 prec_wt_dry_t3 prec_wt_dry_t4 prec_wt_dry_t5 temp_wt_dry_t0 temp_wt_dry_t1 temp_wt_dry_t2 temp_wt_dry_t3 temp_wt_dry_t4 temp_wt_dry_t5 _cons) replace plain star(* 0.10 ** 0.05 *** 0.01) order(dust_pred_wt_dry_t0 dust_pred_wt_dry_t1 dust_pred_wt_dry_t2 dust_pred_wt_dry_t3 dust_pred_wt_dry_t4 dust_pred_wt_dry_t5 prec_wt_dry_t0 prec_wt_dry_t1 prec_wt_dry_t2 prec_wt_dry_t3 prec_wt_dry_t4 prec_wt_dry_t5 temp_wt_dry_t0 temp_wt_dry_t1 temp_wt_dry_t2 temp_wt_dry_t3 temp_wt_dry_t4 temp_wt_dry_t5 _cons)


***********************************

*L2 dust_dry

eststo: reg dust_dry_t2 dust_pred_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 i.ncountry c.year i.ncountry#c.pow_year

estimates store model1

eststo: reg dust_dry_t2 dust_pred_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_pred_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 i.ncountry c.year i.ncountry#c.pow_year 

estimates store model2

eststo: reg dust_dry_t2 dust_pred_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_pred_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 dust_pred_wt_dry_t2 prec_wt_dry_t2 temp_wt_dry_t2 i.ncountry c.year i.ncountry#c.pow_year

estimates store model3

eststo: reg dust_dry_t2 dust_pred_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_pred_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 dust_pred_wt_dry_t2 prec_wt_dry_t2 temp_wt_dry_t2 dust_pred_wt_dry_t3 prec_wt_dry_t3 temp_wt_dry_t3 i.ncountry c.year i.ncountry#c.pow_year

estimates store model4

eststo: reg dust_dry_t2 dust_pred_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_pred_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 dust_pred_wt_dry_t2 prec_wt_dry_t2 temp_wt_dry_t2 dust_pred_wt_dry_t3 prec_wt_dry_t3 temp_wt_dry_t3 dust_pred_wt_dry_t4 prec_wt_dry_t4 temp_wt_dry_t4 i.ncountry c.year i.ncountry#c.pow_year

estimates store model5

eststo: reg dust_dry_t2 dust_pred_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_pred_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 dust_pred_wt_dry_t2 prec_wt_dry_t2 temp_wt_dry_t2 dust_pred_wt_dry_t3 prec_wt_dry_t3 temp_wt_dry_t3 dust_pred_wt_dry_t4 prec_wt_dry_t4 temp_wt_dry_t4 dust_pred_wt_dry_t5 prec_wt_dry_t5 temp_wt_dry_t5 i.ncountry c.year i.ncountry#c.pow_year

estimates store model6

esttab model1 model2 model3 model4 model5 model6 using l2_pred.csv, cells(b(star) se) stats(N r2_a, fmt(0 4)) keep(dust_pred_wt_dry_t0 dust_pred_wt_dry_t1 dust_pred_wt_dry_t2 dust_pred_wt_dry_t3 dust_pred_wt_dry_t4 dust_pred_wt_dry_t5 prec_wt_dry_t0 prec_wt_dry_t1 prec_wt_dry_t2 prec_wt_dry_t3 prec_wt_dry_t4 prec_wt_dry_t5 temp_wt_dry_t0 temp_wt_dry_t1 temp_wt_dry_t2 temp_wt_dry_t3 temp_wt_dry_t4 temp_wt_dry_t5 _cons) replace plain star(* 0.10 ** 0.05 *** 0.01) order(dust_pred_wt_dry_t0 dust_pred_wt_dry_t1 dust_pred_wt_dry_t2 dust_pred_wt_dry_t3 dust_pred_wt_dry_t4 dust_pred_wt_dry_t5 prec_wt_dry_t0 prec_wt_dry_t1 prec_wt_dry_t2 prec_wt_dry_t3 prec_wt_dry_t4 prec_wt_dry_t5 temp_wt_dry_t0 temp_wt_dry_t1 temp_wt_dry_t2 temp_wt_dry_t3 temp_wt_dry_t4 temp_wt_dry_t5 _cons)

***********************************

*L3 dust_dry

eststo: reg dust_dry_t3 dust_pred_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 i.ncountry c.year i.ncountry#c.pow_year

estimates store model1

eststo: reg dust_dry_t3 dust_pred_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_pred_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 i.ncountry c.year i.ncountry#c.pow_year 

estimates store model2

eststo: reg dust_dry_t3 dust_pred_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_pred_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 dust_pred_wt_dry_t2 prec_wt_dry_t2 temp_wt_dry_t2 i.ncountry c.year i.ncountry#c.pow_year

estimates store model3

eststo: reg dust_dry_t3 dust_pred_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_pred_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 dust_pred_wt_dry_t2 prec_wt_dry_t2 temp_wt_dry_t2 dust_pred_wt_dry_t3 prec_wt_dry_t3 temp_wt_dry_t3 i.ncountry c.year i.ncountry#c.pow_year

estimates store model4

eststo: reg dust_dry_t3 dust_pred_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_pred_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 dust_pred_wt_dry_t2 prec_wt_dry_t2 temp_wt_dry_t2 dust_pred_wt_dry_t3 prec_wt_dry_t3 temp_wt_dry_t3 dust_pred_wt_dry_t4 prec_wt_dry_t4 temp_wt_dry_t4 i.ncountry c.year i.ncountry#c.pow_year

estimates store model5

eststo: reg dust_dry_t3 dust_pred_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_pred_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 dust_pred_wt_dry_t2 prec_wt_dry_t2 temp_wt_dry_t2 dust_pred_wt_dry_t3 prec_wt_dry_t3 temp_wt_dry_t3 dust_pred_wt_dry_t4 prec_wt_dry_t4 temp_wt_dry_t4 dust_pred_wt_dry_t5 prec_wt_dry_t5 temp_wt_dry_t5 i.ncountry c.year i.ncountry#c.pow_year

estimates store model6

esttab model1 model2 model3 model4 model5 model6 using l3_pred.csv, cells(b(star) se) stats(N r2_a, fmt(0 4)) keep(dust_pred_wt_dry_t0 dust_pred_wt_dry_t1 dust_pred_wt_dry_t2 dust_pred_wt_dry_t3 dust_pred_wt_dry_t4 dust_pred_wt_dry_t5 prec_wt_dry_t0 prec_wt_dry_t1 prec_wt_dry_t2 prec_wt_dry_t3 prec_wt_dry_t4 prec_wt_dry_t5 temp_wt_dry_t0 temp_wt_dry_t1 temp_wt_dry_t2 temp_wt_dry_t3 temp_wt_dry_t4 temp_wt_dry_t5 _cons) replace plain star(* 0.10 ** 0.05 *** 0.01) order(dust_pred_wt_dry_t0 dust_pred_wt_dry_t1 dust_pred_wt_dry_t2 dust_pred_wt_dry_t3 dust_pred_wt_dry_t4 dust_pred_wt_dry_t5 prec_wt_dry_t0 prec_wt_dry_t1 prec_wt_dry_t2 prec_wt_dry_t3 prec_wt_dry_t4 prec_wt_dry_t5 temp_wt_dry_t0 temp_wt_dry_t1 temp_wt_dry_t2 temp_wt_dry_t3 temp_wt_dry_t4 temp_wt_dry_t5 _cons)

***********************************

*L4 dust_dry

eststo: reg dust_dry_t4 dust_pred_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 i.ncountry c.year i.ncountry#c.pow_year

estimates store model1

eststo: reg dust_dry_t4 dust_pred_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_pred_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 i.ncountry c.year i.ncountry#c.pow_year 

estimates store model2

eststo: reg dust_dry_t4 dust_pred_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_pred_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 dust_pred_wt_dry_t2 prec_wt_dry_t2 temp_wt_dry_t2 i.ncountry c.year i.ncountry#c.pow_year

estimates store model3

eststo: reg dust_dry_t4 dust_pred_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_pred_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 dust_pred_wt_dry_t2 prec_wt_dry_t2 temp_wt_dry_t2 dust_pred_wt_dry_t3 prec_wt_dry_t3 temp_wt_dry_t3 i.ncountry c.year i.ncountry#c.pow_year

estimates store model4

eststo: reg dust_dry_t4 dust_pred_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_pred_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 dust_pred_wt_dry_t2 prec_wt_dry_t2 temp_wt_dry_t2 dust_pred_wt_dry_t3 prec_wt_dry_t3 temp_wt_dry_t3 dust_pred_wt_dry_t4 prec_wt_dry_t4 temp_wt_dry_t4 i.ncountry c.year i.ncountry#c.pow_year

estimates store model5

eststo: reg dust_dry_t4 dust_pred_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_pred_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 dust_pred_wt_dry_t2 prec_wt_dry_t2 temp_wt_dry_t2 dust_pred_wt_dry_t3 prec_wt_dry_t3 temp_wt_dry_t3 dust_pred_wt_dry_t4 prec_wt_dry_t4 temp_wt_dry_t4 dust_pred_wt_dry_t5 prec_wt_dry_t5 temp_wt_dry_t5 i.ncountry c.year i.ncountry#c.pow_year

estimates store model6

esttab model1 model2 model3 model4 model5 model6 using l4_pred.csv, cells(b(star) se) stats(N r2_a, fmt(0 4)) keep(dust_pred_wt_dry_t0 dust_pred_wt_dry_t1 dust_pred_wt_dry_t2 dust_pred_wt_dry_t3 dust_pred_wt_dry_t4 dust_pred_wt_dry_t5 prec_wt_dry_t0 prec_wt_dry_t1 prec_wt_dry_t2 prec_wt_dry_t3 prec_wt_dry_t4 prec_wt_dry_t5 temp_wt_dry_t0 temp_wt_dry_t1 temp_wt_dry_t2 temp_wt_dry_t3 temp_wt_dry_t4 temp_wt_dry_t5 _cons) replace plain star(* 0.10 ** 0.05 *** 0.01) order(dust_pred_wt_dry_t0 dust_pred_wt_dry_t1 dust_pred_wt_dry_t2 dust_pred_wt_dry_t3 dust_pred_wt_dry_t4 dust_pred_wt_dry_t5 prec_wt_dry_t0 prec_wt_dry_t1 prec_wt_dry_t2 prec_wt_dry_t3 prec_wt_dry_t4 prec_wt_dry_t5 temp_wt_dry_t0 temp_wt_dry_t1 temp_wt_dry_t2 temp_wt_dry_t3 temp_wt_dry_t4 temp_wt_dry_t5 _cons)

***********************************

*L5 dust_dry

eststo: reg dust_dry_t5 dust_pred_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 i.ncountry c.year i.ncountry#c.pow_year

estimates store model1

eststo: reg dust_dry_t5 dust_pred_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_pred_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 i.ncountry c.year i.ncountry#c.pow_year 

estimates store model2

eststo: reg dust_dry_t5 dust_pred_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_pred_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 dust_pred_wt_dry_t2 prec_wt_dry_t2 temp_wt_dry_t2 i.ncountry c.year i.ncountry#c.pow_year

estimates store model3

eststo: reg dust_dry_t5 dust_pred_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_pred_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 dust_pred_wt_dry_t2 prec_wt_dry_t2 temp_wt_dry_t2 dust_pred_wt_dry_t3 prec_wt_dry_t3 temp_wt_dry_t3 i.ncountry c.year i.ncountry#c.pow_year

estimates store model4

eststo: reg dust_dry_t5 dust_pred_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_pred_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 dust_pred_wt_dry_t2 prec_wt_dry_t2 temp_wt_dry_t2 dust_pred_wt_dry_t3 prec_wt_dry_t3 temp_wt_dry_t3 dust_pred_wt_dry_t4 prec_wt_dry_t4 temp_wt_dry_t4 i.ncountry c.year i.ncountry#c.pow_year

estimates store model5

eststo: reg dust_dry_t5 dust_pred_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_pred_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 dust_pred_wt_dry_t2 prec_wt_dry_t2 temp_wt_dry_t2 dust_pred_wt_dry_t3 prec_wt_dry_t3 temp_wt_dry_t3 dust_pred_wt_dry_t4 prec_wt_dry_t4 temp_wt_dry_t4 dust_pred_wt_dry_t5 prec_wt_dry_t5 temp_wt_dry_t5 i.ncountry c.year i.ncountry#c.pow_year

estimates store model6

esttab model1 model2 model3 model4 model5 model6 using l5_pred.csv, cells(b(star) se) stats(N r2_a, fmt(0 4)) keep(dust_pred_wt_dry_t0 dust_pred_wt_dry_t1 dust_pred_wt_dry_t2 dust_pred_wt_dry_t3 dust_pred_wt_dry_t4 dust_pred_wt_dry_t5 prec_wt_dry_t0 prec_wt_dry_t1 prec_wt_dry_t2 prec_wt_dry_t3 prec_wt_dry_t4 prec_wt_dry_t5 temp_wt_dry_t0 temp_wt_dry_t1 temp_wt_dry_t2 temp_wt_dry_t3 temp_wt_dry_t4 temp_wt_dry_t5 _cons) replace plain star(* 0.10 ** 0.05 *** 0.01) order(dust_pred_wt_dry_t0 dust_pred_wt_dry_t1 dust_pred_wt_dry_t2 dust_pred_wt_dry_t3 dust_pred_wt_dry_t4 dust_pred_wt_dry_t5 prec_wt_dry_t0 prec_wt_dry_t1 prec_wt_dry_t2 prec_wt_dry_t3 prec_wt_dry_t4 prec_wt_dry_t5 temp_wt_dry_t0 temp_wt_dry_t1 temp_wt_dry_t2 temp_wt_dry_t3 temp_wt_dry_t4 temp_wt_dry_t5 _cons)
**********************************************************************

*Simulated Dust:

*L0 dust_dry

eststo: reg dust_dry_t0 dust_sim_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 i.ncountry c.year i.ncountry#c.pow_year

estimates store model1

eststo: reg dust_dry_t0 dust_sim_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_sim_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 i.ncountry c.year i.ncountry#c.pow_year 

estimates store model2

eststo: reg dust_dry_t0 dust_sim_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_sim_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 dust_sim_wt_dry_t2 prec_wt_dry_t2 temp_wt_dry_t2 i.ncountry c.year i.ncountry#c.pow_year

estimates store model3

eststo: reg dust_dry_t0 dust_sim_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_sim_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 dust_sim_wt_dry_t2 prec_wt_dry_t2 temp_wt_dry_t2 dust_sim_wt_dry_t3 prec_wt_dry_t3 temp_wt_dry_t3 i.ncountry c.year i.ncountry#c.pow_year

estimates store model4

eststo: reg dust_dry_t0 dust_sim_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_sim_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 dust_sim_wt_dry_t2 prec_wt_dry_t2 temp_wt_dry_t2 dust_sim_wt_dry_t3 prec_wt_dry_t3 temp_wt_dry_t3 dust_sim_wt_dry_t4 prec_wt_dry_t4 temp_wt_dry_t4 i.ncountry c.year i.ncountry#c.pow_year

estimates store model5

eststo: reg dust_dry_t0 dust_sim_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_sim_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 dust_sim_wt_dry_t2 prec_wt_dry_t2 temp_wt_dry_t2 dust_sim_wt_dry_t3 prec_wt_dry_t3 temp_wt_dry_t3 dust_sim_wt_dry_t4 prec_wt_dry_t4 temp_wt_dry_t4 dust_sim_wt_dry_t5 prec_wt_dry_t5 temp_wt_dry_t5 i.ncountry c.year i.ncountry#c.pow_year 

estimates store model6

esttab model1 model2 model3 model4 model5 model6 using l0_sim.csv, cells(b(star) se) stats(N r2_a, fmt(0 4)) keep(dust_sim_wt_dry_t0 dust_sim_wt_dry_t1 dust_sim_wt_dry_t2 dust_sim_wt_dry_t3 dust_sim_wt_dry_t4 dust_sim_wt_dry_t5 prec_wt_dry_t0 prec_wt_dry_t1 prec_wt_dry_t2 prec_wt_dry_t3 prec_wt_dry_t4 prec_wt_dry_t5 temp_wt_dry_t0 temp_wt_dry_t1 temp_wt_dry_t2 temp_wt_dry_t3 temp_wt_dry_t4 temp_wt_dry_t5 _cons) replace plain star(* 0.10 ** 0.05 *** 0.01) order(dust_sim_wt_dry_t0 dust_sim_wt_dry_t1 dust_sim_wt_dry_t2 dust_sim_wt_dry_t3 dust_sim_wt_dry_t4 dust_sim_wt_dry_t5 prec_wt_dry_t0 prec_wt_dry_t1 prec_wt_dry_t2 prec_wt_dry_t3 prec_wt_dry_t4 prec_wt_dry_t5 temp_wt_dry_t0 temp_wt_dry_t1 temp_wt_dry_t2 temp_wt_dry_t3 temp_wt_dry_t4 temp_wt_dry_t5 _cons)

***********************************

*L1 dust_dry

eststo: reg dust_dry_t1 dust_sim_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 i.ncountry c.year i.ncountry#c.pow_year

estimates store model1

eststo: reg dust_dry_t1 dust_sim_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_sim_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 i.ncountry c.year i.ncountry#c.pow_year 

estimates store model2

eststo: reg dust_dry_t1 dust_sim_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_sim_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 dust_sim_wt_dry_t2 prec_wt_dry_t2 temp_wt_dry_t2 i.ncountry c.year i.ncountry#c.pow_year

estimates store model3

eststo: reg dust_dry_t1 dust_sim_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_sim_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 dust_sim_wt_dry_t2 prec_wt_dry_t2 temp_wt_dry_t2 dust_sim_wt_dry_t3 prec_wt_dry_t3 temp_wt_dry_t3 i.ncountry c.year i.ncountry#c.pow_year

estimates store model4

eststo: reg dust_dry_t1 dust_sim_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_sim_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 dust_sim_wt_dry_t2 prec_wt_dry_t2 temp_wt_dry_t2 dust_sim_wt_dry_t3 prec_wt_dry_t3 temp_wt_dry_t3 dust_sim_wt_dry_t4 prec_wt_dry_t4 temp_wt_dry_t4 i.ncountry c.year i.ncountry#c.pow_year

estimates store model5

eststo: reg dust_dry_t1 dust_sim_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_sim_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 dust_sim_wt_dry_t2 prec_wt_dry_t2 temp_wt_dry_t2 dust_sim_wt_dry_t3 prec_wt_dry_t3 temp_wt_dry_t3 dust_sim_wt_dry_t4 prec_wt_dry_t4 temp_wt_dry_t4 dust_sim_wt_dry_t5 prec_wt_dry_t5 temp_wt_dry_t5 i.ncountry c.year i.ncountry#c.pow_year 

estimates store model6

esttab model1 model2 model3 model4 model5 model6 using l1_sim.csv, cells(b(star) se) stats(N r2_a, fmt(0 4)) keep(dust_sim_wt_dry_t0 dust_sim_wt_dry_t1 dust_sim_wt_dry_t2 dust_sim_wt_dry_t3 dust_sim_wt_dry_t4 dust_sim_wt_dry_t5 prec_wt_dry_t0 prec_wt_dry_t1 prec_wt_dry_t2 prec_wt_dry_t3 prec_wt_dry_t4 prec_wt_dry_t5 temp_wt_dry_t0 temp_wt_dry_t1 temp_wt_dry_t2 temp_wt_dry_t3 temp_wt_dry_t4 temp_wt_dry_t5 _cons) replace plain star(* 0.10 ** 0.05 *** 0.01) order(dust_sim_wt_dry_t0 dust_sim_wt_dry_t1 dust_sim_wt_dry_t2 dust_sim_wt_dry_t3 dust_sim_wt_dry_t4 dust_sim_wt_dry_t5 prec_wt_dry_t0 prec_wt_dry_t1 prec_wt_dry_t2 prec_wt_dry_t3 prec_wt_dry_t4 prec_wt_dry_t5 temp_wt_dry_t0 temp_wt_dry_t1 temp_wt_dry_t2 temp_wt_dry_t3 temp_wt_dry_t4 temp_wt_dry_t5 _cons)
***********************************

*L2 dust_dry

eststo: reg dust_dry_t2 dust_sim_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 i.ncountry c.year i.ncountry#c.pow_year

estimates store model1

eststo: reg dust_dry_t2 dust_sim_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_sim_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 i.ncountry c.year i.ncountry#c.pow_year 

estimates store model2

eststo: reg dust_dry_t2 dust_sim_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_sim_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 dust_sim_wt_dry_t2 prec_wt_dry_t2 temp_wt_dry_t2 i.ncountry c.year i.ncountry#c.pow_year

estimates store model3

eststo: reg dust_dry_t2 dust_sim_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_sim_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 dust_sim_wt_dry_t2 prec_wt_dry_t2 temp_wt_dry_t2 dust_sim_wt_dry_t3 prec_wt_dry_t3 temp_wt_dry_t3 i.ncountry c.year i.ncountry#c.pow_year

estimates store model4

eststo: reg dust_dry_t2 dust_sim_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_sim_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 dust_sim_wt_dry_t2 prec_wt_dry_t2 temp_wt_dry_t2 dust_sim_wt_dry_t3 prec_wt_dry_t3 temp_wt_dry_t3 dust_sim_wt_dry_t4 prec_wt_dry_t4 temp_wt_dry_t4 i.ncountry c.year i.ncountry#c.pow_year

estimates store model5

eststo: reg dust_dry_t2 dust_sim_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_sim_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 dust_sim_wt_dry_t2 prec_wt_dry_t2 temp_wt_dry_t2 dust_sim_wt_dry_t3 prec_wt_dry_t3 temp_wt_dry_t3 dust_sim_wt_dry_t4 prec_wt_dry_t4 temp_wt_dry_t4 dust_sim_wt_dry_t5 prec_wt_dry_t5 temp_wt_dry_t5 i.ncountry c.year i.ncountry#c.pow_year 

estimates store model6

esttab model1 model2 model3 model4 model5 model6 using l2_sim.csv, cells(b(star) se) stats(N r2_a, fmt(0 4)) keep(dust_sim_wt_dry_t0 dust_sim_wt_dry_t1 dust_sim_wt_dry_t2 dust_sim_wt_dry_t3 dust_sim_wt_dry_t4 dust_sim_wt_dry_t5 prec_wt_dry_t0 prec_wt_dry_t1 prec_wt_dry_t2 prec_wt_dry_t3 prec_wt_dry_t4 prec_wt_dry_t5 temp_wt_dry_t0 temp_wt_dry_t1 temp_wt_dry_t2 temp_wt_dry_t3 temp_wt_dry_t4 temp_wt_dry_t5 _cons) replace plain star(* 0.10 ** 0.05 *** 0.01) order(dust_sim_wt_dry_t0 dust_sim_wt_dry_t1 dust_sim_wt_dry_t2 dust_sim_wt_dry_t3 dust_sim_wt_dry_t4 dust_sim_wt_dry_t5 prec_wt_dry_t0 prec_wt_dry_t1 prec_wt_dry_t2 prec_wt_dry_t3 prec_wt_dry_t4 prec_wt_dry_t5 temp_wt_dry_t0 temp_wt_dry_t1 temp_wt_dry_t2 temp_wt_dry_t3 temp_wt_dry_t4 temp_wt_dry_t5 _cons)

***********************************

*L3 dust_dry

eststo: reg dust_dry_t3 dust_sim_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 i.ncountry c.year i.ncountry#c.pow_year

estimates store model1

eststo: reg dust_dry_t3 dust_sim_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_sim_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 i.ncountry c.year i.ncountry#c.pow_year 

estimates store model2

eststo: reg dust_dry_t3 dust_sim_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_sim_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 dust_sim_wt_dry_t2 prec_wt_dry_t2 temp_wt_dry_t2 i.ncountry c.year i.ncountry#c.pow_year

estimates store model3

eststo: reg dust_dry_t3 dust_sim_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_sim_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 dust_sim_wt_dry_t2 prec_wt_dry_t2 temp_wt_dry_t2 dust_sim_wt_dry_t3 prec_wt_dry_t3 temp_wt_dry_t3 i.ncountry c.year i.ncountry#c.pow_year

estimates store model4

eststo: reg dust_dry_t3 dust_sim_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_sim_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 dust_sim_wt_dry_t2 prec_wt_dry_t2 temp_wt_dry_t2 dust_sim_wt_dry_t3 prec_wt_dry_t3 temp_wt_dry_t3 dust_sim_wt_dry_t4 prec_wt_dry_t4 temp_wt_dry_t4 i.ncountry c.year i.ncountry#c.pow_year

estimates store model5

eststo: reg dust_dry_t3 dust_sim_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_sim_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 dust_sim_wt_dry_t2 prec_wt_dry_t2 temp_wt_dry_t2 dust_sim_wt_dry_t3 prec_wt_dry_t3 temp_wt_dry_t3 dust_sim_wt_dry_t4 prec_wt_dry_t4 temp_wt_dry_t4 dust_sim_wt_dry_t5 prec_wt_dry_t5 temp_wt_dry_t5 i.ncountry c.year i.ncountry#c.pow_year 

estimates store model6

esttab model1 model2 model3 model4 model5 model6 using l3_sim.csv, cells(b(star) se) stats(N r2_a, fmt(0 4)) keep(dust_sim_wt_dry_t0 dust_sim_wt_dry_t1 dust_sim_wt_dry_t2 dust_sim_wt_dry_t3 dust_sim_wt_dry_t4 dust_sim_wt_dry_t5 prec_wt_dry_t0 prec_wt_dry_t1 prec_wt_dry_t2 prec_wt_dry_t3 prec_wt_dry_t4 prec_wt_dry_t5 temp_wt_dry_t0 temp_wt_dry_t1 temp_wt_dry_t2 temp_wt_dry_t3 temp_wt_dry_t4 temp_wt_dry_t5 _cons) replace plain star(* 0.10 ** 0.05 *** 0.01) order(dust_sim_wt_dry_t0 dust_sim_wt_dry_t1 dust_sim_wt_dry_t2 dust_sim_wt_dry_t3 dust_sim_wt_dry_t4 dust_sim_wt_dry_t5 prec_wt_dry_t0 prec_wt_dry_t1 prec_wt_dry_t2 prec_wt_dry_t3 prec_wt_dry_t4 prec_wt_dry_t5 temp_wt_dry_t0 temp_wt_dry_t1 temp_wt_dry_t2 temp_wt_dry_t3 temp_wt_dry_t4 temp_wt_dry_t5 _cons)

***********************************

*L4 dust_dry

eststo: reg dust_dry_t4 dust_sim_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 i.ncountry c.year i.ncountry#c.pow_year

estimates store model1

eststo: reg dust_dry_t4 dust_sim_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_sim_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 i.ncountry c.year i.ncountry#c.pow_year 

estimates store model2

eststo: reg dust_dry_t4 dust_sim_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_sim_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 dust_sim_wt_dry_t2 prec_wt_dry_t2 temp_wt_dry_t2 i.ncountry c.year i.ncountry#c.pow_year

estimates store model3

eststo: reg dust_dry_t4 dust_sim_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_sim_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 dust_sim_wt_dry_t2 prec_wt_dry_t2 temp_wt_dry_t2 dust_sim_wt_dry_t3 prec_wt_dry_t3 temp_wt_dry_t3 i.ncountry c.year i.ncountry#c.pow_year

estimates store model4

eststo: reg dust_dry_t4 dust_sim_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_sim_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 dust_sim_wt_dry_t2 prec_wt_dry_t2 temp_wt_dry_t2 dust_sim_wt_dry_t3 prec_wt_dry_t3 temp_wt_dry_t3 dust_sim_wt_dry_t4 prec_wt_dry_t4 temp_wt_dry_t4 i.ncountry c.year i.ncountry#c.pow_year

estimates store model5

eststo: reg dust_dry_t4 dust_sim_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_sim_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 dust_sim_wt_dry_t2 prec_wt_dry_t2 temp_wt_dry_t2 dust_sim_wt_dry_t3 prec_wt_dry_t3 temp_wt_dry_t3 dust_sim_wt_dry_t4 prec_wt_dry_t4 temp_wt_dry_t4 dust_sim_wt_dry_t5 prec_wt_dry_t5 temp_wt_dry_t5 i.ncountry c.year i.ncountry#c.pow_year 

estimates store model6

esttab model1 model2 model3 model4 model5 model6 using l4_sim.csv, cells(b(star) se) stats(N r2_a, fmt(0 4)) keep(dust_sim_wt_dry_t0 dust_sim_wt_dry_t1 dust_sim_wt_dry_t2 dust_sim_wt_dry_t3 dust_sim_wt_dry_t4 dust_sim_wt_dry_t5 prec_wt_dry_t0 prec_wt_dry_t1 prec_wt_dry_t2 prec_wt_dry_t3 prec_wt_dry_t4 prec_wt_dry_t5 temp_wt_dry_t0 temp_wt_dry_t1 temp_wt_dry_t2 temp_wt_dry_t3 temp_wt_dry_t4 temp_wt_dry_t5 _cons) replace plain star(* 0.10 ** 0.05 *** 0.01) order(dust_sim_wt_dry_t0 dust_sim_wt_dry_t1 dust_sim_wt_dry_t2 dust_sim_wt_dry_t3 dust_sim_wt_dry_t4 dust_sim_wt_dry_t5 prec_wt_dry_t0 prec_wt_dry_t1 prec_wt_dry_t2 prec_wt_dry_t3 prec_wt_dry_t4 prec_wt_dry_t5 temp_wt_dry_t0 temp_wt_dry_t1 temp_wt_dry_t2 temp_wt_dry_t3 temp_wt_dry_t4 temp_wt_dry_t5 _cons)

***********************************

*L5 dust_dry

eststo: reg dust_dry_t5 dust_sim_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 i.ncountry c.year i.ncountry#c.pow_year

estimates store model1

eststo: reg dust_dry_t5 dust_sim_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_sim_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 i.ncountry c.year i.ncountry#c.pow_year 

estimates store model2

eststo: reg dust_dry_t5 dust_sim_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_sim_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 dust_sim_wt_dry_t2 prec_wt_dry_t2 temp_wt_dry_t2 i.ncountry c.year i.ncountry#c.pow_year

estimates store model3

eststo: reg dust_dry_t5 dust_sim_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_sim_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 dust_sim_wt_dry_t2 prec_wt_dry_t2 temp_wt_dry_t2 dust_sim_wt_dry_t3 prec_wt_dry_t3 temp_wt_dry_t3 i.ncountry c.year i.ncountry#c.pow_year

estimates store model4

eststo: reg dust_dry_t5 dust_sim_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_sim_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 dust_sim_wt_dry_t2 prec_wt_dry_t2 temp_wt_dry_t2 dust_sim_wt_dry_t3 prec_wt_dry_t3 temp_wt_dry_t3 dust_sim_wt_dry_t4 prec_wt_dry_t4 temp_wt_dry_t4 i.ncountry c.year i.ncountry#c.pow_year

estimates store model5

eststo: reg dust_dry_t5 dust_sim_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 dust_sim_wt_dry_t1 prec_wt_dry_t1 temp_wt_dry_t1 dust_sim_wt_dry_t2 prec_wt_dry_t2 temp_wt_dry_t2 dust_sim_wt_dry_t3 prec_wt_dry_t3 temp_wt_dry_t3 dust_sim_wt_dry_t4 prec_wt_dry_t4 temp_wt_dry_t4 dust_sim_wt_dry_t5 prec_wt_dry_t5 temp_wt_dry_t5 i.ncountry c.year i.ncountry#c.pow_year  

estimates store model6

esttab model1 model2 model3 model4 model5 model6 using l5_sim.csv, cells(b(star) se) stats(N r2_a, fmt(0 4)) keep(dust_sim_wt_dry_t0 dust_sim_wt_dry_t1 dust_sim_wt_dry_t2 dust_sim_wt_dry_t3 dust_sim_wt_dry_t4 dust_sim_wt_dry_t5 prec_wt_dry_t0 prec_wt_dry_t1 prec_wt_dry_t2 prec_wt_dry_t3 prec_wt_dry_t4 prec_wt_dry_t5 temp_wt_dry_t0 temp_wt_dry_t1 temp_wt_dry_t2 temp_wt_dry_t3 temp_wt_dry_t4 temp_wt_dry_t5 _cons) replace plain star(* 0.10 ** 0.05 *** 0.01) order(dust_sim_wt_dry_t0 dust_sim_wt_dry_t1 dust_sim_wt_dry_t2 dust_sim_wt_dry_t3 dust_sim_wt_dry_t4 dust_sim_wt_dry_t5 prec_wt_dry_t0 prec_wt_dry_t1 prec_wt_dry_t2 prec_wt_dry_t3 prec_wt_dry_t4 prec_wt_dry_t5 temp_wt_dry_t0 temp_wt_dry_t1 temp_wt_dry_t2 temp_wt_dry_t3 temp_wt_dry_t4 temp_wt_dry_t5 _cons)

*/



***********************************

//generate dust instruments
//generate predicted dust instrument
reg dust_dry_t0 dust_pred_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 i.ncountry c.year i.ncountry#c.pow_year

predict dust_dry_stat_predict_lag0 if e(sample)
predict dust_dry_stat_predict_res if e(sample), res

//generate simulated dust instrument
reg dust_dry_t0 dust_sim_wt_dry_t0 prec_wt_dry_t0 temp_wt_dry_t0 i.ncountry c.year i.ncountry#c.pow_year

predict dust_dry_sim_predict_lag0 if e(sample)
predict dust_dry_sim_predict_res if e(sample), res

//generate lead statistical model input regression prediction variables
gen dust_dry_stat_predict_lead1 = dust_dry_stat_predict_lag0[_n+1]
gen dust_dry_stat_predict_lead2 = dust_dry_stat_predict_lag0[_n+2]
gen dust_dry_stat_predict_lead3 = dust_dry_stat_predict_lag0[_n+3]
gen dust_dry_stat_predict_lead4 = dust_dry_stat_predict_lag0[_n+4]
gen dust_dry_stat_predict_lead5 = dust_dry_stat_predict_lag0[_n+5]

//generate lagged physical model input regression prediction variables
gen dust_dry_stat_predict_lag1 = dust_dry_stat_predict_lag0[_n-1]
gen dust_dry_stat_predict_lag2 = dust_dry_stat_predict_lag0[_n-2]
gen dust_dry_stat_predict_lag3 = dust_dry_stat_predict_lag0[_n-3]
gen dust_dry_stat_predict_lag4 = dust_dry_stat_predict_lag0[_n-4]
gen dust_dry_stat_predict_lag5 = dust_dry_stat_predict_lag0[_n-5]

//generate lead physical model input regression prediction variables
gen dust_dry_sim_predict_lead1 = dust_dry_sim_predict_lag0[_n+1]
gen dust_dry_sim_predict_lead2 = dust_dry_sim_predict_lag0[_n+2]
gen dust_dry_sim_predict_lead3 = dust_dry_sim_predict_lag0[_n+3]
gen dust_dry_sim_predict_lead4 = dust_dry_sim_predict_lag0[_n+4]
gen dust_dry_sim_predict_lead5 = dust_dry_sim_predict_lag0[_n+5]

//generate lagged physical model input regression prediction variables
gen dust_dry_sim_predict_lag1 = dust_dry_sim_predict_lag0[_n-1]
gen dust_dry_sim_predict_lag2 = dust_dry_sim_predict_lag0[_n-2]
gen dust_dry_sim_predict_lag3 = dust_dry_sim_predict_lag0[_n-3]
gen dust_dry_sim_predict_lag4 = dust_dry_sim_predict_lag0[_n-4]
gen dust_dry_sim_predict_lag5 = dust_dry_sim_predict_lag0[_n-5]

//generate lead aod_values
gen aod_yr_lead1 = aod_yr_t0[_n+1]
gen aod_yr_lead2 = aod_yr_t0[_n+2]
gen aod_yr_lead3 = aod_yr_t0[_n+3]
gen aod_yr_lead4 = aod_yr_t0[_n+4]
gen aod_yr_lead5 = aod_yr_t0[_n+5]

//generate lagged aod_values
gen aod_yr_lag1 = aod_yr_t0[_n-1]
gen aod_yr_lag2 = aod_yr_t0[_n-2]
gen aod_yr_lag3 = aod_yr_t0[_n-3]
gen aod_yr_lag4 = aod_yr_t0[_n-4]
gen aod_yr_lag5 = aod_yr_t0[_n-5]

//generate lead pm25_values
gen pm25_yr_lead1 = pm25_yr_t0[_n+1]
gen pm25_yr_lead2 = pm25_yr_t0[_n+2]
gen pm25_yr_lead3 = pm25_yr_t0[_n+3]
gen pm25_yr_lead4 = pm25_yr_t0[_n+4]
gen pm25_yr_lead5 = pm25_yr_t0[_n+5]

//generate lagged pm25_values
gen pm25_yr_lag1 = pm25_yr_t0[_n-1]
gen pm25_yr_lag2 = pm25_yr_t0[_n-2]
gen pm25_yr_lag3 = pm25_yr_t0[_n-3]
gen pm25_yr_lag4 = pm25_yr_t0[_n-4]
gen pm25_yr_lag5 = pm25_yr_t0[_n-5]

//generate lead prec
gen prec_yr_lead1 = prec_yr_t0[_n+1]
gen prec_yr_lead2 = prec_yr_t0[_n+2]
gen prec_yr_lead3 = prec_yr_t0[_n+3]
gen prec_yr_lead4 = prec_yr_t0[_n+4]
gen prec_yr_lead5 = prec_yr_t0[_n+5]

//generate lead temp
gen temp_yr_lead1 = temp_yr_t0[_n+1]
gen temp_yr_lead2 = temp_yr_t0[_n+2]
gen temp_yr_lead3 = temp_yr_t0[_n+3]
gen temp_yr_lead4 = temp_yr_t0[_n+4]
gen temp_yr_lead5 = temp_yr_t0[_n+5]

//todo: add pm2.5 values

gen bodele_aod_dry_lag1 = bodele_aod_dry[_n-1]
gen bodele_aod_wet_lag1 = bodele_x[_n-1]

gen bodele_pm25_dry_lag1 = bodele_pm25_dry[_n-1]
gen bodele_pm25_wet_lag1 = v140[_n-1]

//Need to drop missing variables since spatial_hac_iv cannot handle them
foreach v of var * { 
	drop if missing(`v') 
}



//perform IV regression with AOD

//Statistical model regression:


//Penn World Tables
eststo: spatial_hac_iv pwt_growth prec_yr_t0 temp_yr_t0 i.ncountry c.year i.ncountry#c.pow_year (aod_yr_t0 = dust_dry_stat_predict_lag0), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar

estimates store model1

eststo: spatial_hac_iv pwt_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 i.ncountry c.year i.ncountry#c.pow_year (aod_yr_t0 aod_yr_lag1 = dust_dry_stat_predict_lag0 dust_dry_stat_predict_lag1), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar

estimates store model2

eststo: spatial_hac_iv pwt_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 i.ncountry c.year i.ncountry#c.pow_year (aod_yr_t0 aod_yr_lag1 aod_yr_lag2 = dust_dry_stat_predict_lag0 dust_dry_stat_predict_lag1 dust_dry_stat_predict_lag2 ), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar

estimates store model3

eststo: spatial_hac_iv pwt_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 i.ncountry c.year i.ncountry#c.pow_year (aod_yr_t0 aod_yr_lag1 aod_yr_lag2 aod_yr_lag3 = dust_dry_stat_predict_lag0 dust_dry_stat_predict_lag1 dust_dry_stat_predict_lag2 dust_dry_stat_predict_lag3), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar

estimates store model4

eststo:spatial_hac_iv pwt_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 prec_yr_t4 temp_yr_t4 i.ncountry c.year i.ncountry#c.pow_year (aod_yr_t0 aod_yr_lag1 aod_yr_lag2 aod_yr_lag3 aod_yr_lag4 = dust_dry_stat_predict_lag0 dust_dry_stat_predict_lag1 dust_dry_stat_predict_lag2 dust_dry_stat_predict_lag3 dust_dry_stat_predict_lag4), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar 

estimates store model5

eststo: spatial_hac_iv pwt_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 prec_yr_t4 temp_yr_t4 prec_yr_t5 temp_yr_t5 i.ncountry c.year i.ncountry#c.pow_year (aod_yr_t0 aod_yr_lag1 aod_yr_lag2 aod_yr_lag3 aod_yr_lag4 aod_yr_lag5 = dust_dry_stat_predict_lag0 dust_dry_stat_predict_lag1 dust_dry_stat_predict_lag2 dust_dry_stat_predict_lag3 dust_dry_stat_predict_lag4 dust_dry_stat_predict_lag5), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar 

estimates store model6

esttab model1 model2 model3 model4 model5 model6 using aod_pwt.csv , cells(b(star fmt(7)) se) stats(N r2, fmt(0 4)) keep(aod_yr_t0 aod_yr_lag1 aod_yr_lag2 aod_yr_lag3 aod_yr_lag4 aod_yr_lag5 prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 prec_yr_t4 temp_yr_t4 prec_yr_t5 temp_yr_t5) replace plain star(* 0.10 ** 0.05 *** 0.01)

bysort country: egen aod_yr_t0_sd=sd(aod_yr_t0)
mean(aod_yr_t0_sd)
//.0497168

esttab model6 using aod_pwt_aod_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(aod_yr_t0 aod_yr_lag1 aod_yr_lag2 aod_yr_lag3 aod_yr_lag4 aod_yr_lag5) transform(aod_yr_t0 .0497168*@ .0497168 aod_yr_lag1 .0497168*@ .0497168 aod_yr_lag2 .0497168*@ .0497168 aod_yr_lag3 .0497168*@ .0497168 aod_yr_lag4 .0497168*@ .0497168 aod_yr_lag5 .0497168*@ .0497168) replace plain

esttab model1 using aod_pwt_aodl0_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(aod_yr_t0) transform(aod_yr_t0 .0497168*@ .0497168) replace plain

//precipitation:
bysort country: egen prec_yr_t0_sd=sd(prec_yr_t0)
mean(prec_yr_t0_sd)
//7.83e-06

esttab model6 using aod_pwt_prec_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(prec_yr_t0 prec_yr_t1 prec_yr_t2 prec_yr_t3 prec_yr_t4 prec_yr_t5) transform(prec_yr_t0 7.83e-06*@ 7.83e-06 prec_yr_t1 7.83e-06*@ 7.83e-06 prec_yr_t2 7.83e-06*@ 7.83e-06 prec_yr_t3 7.83e-06*@ 7.83e-06 prec_yr_t4 7.83e-06*@ 7.83e-06 prec_yr_t5 7.83e-06*@ 7.83e-06) replace plain

//temperature:
bysort country: egen temp_yr_t0_sd=sd(temp_yr_t0)
mean(temp_yr_t0_sd)
//.4324855

esttab model6 using aod_pwt_temp_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(temp_yr_t0 temp_yr_t1 temp_yr_t2 temp_yr_t3 temp_yr_t4 temp_yr_t5) transform(temp_yr_t0 .4324855*@ .4324855 temp_yr_t1 .4324855*@ .4324855 temp_yr_t2 .4324855*@ .4324855 temp_yr_t3 .4324855*@ .4324855 temp_yr_t4 .4324855*@ .4324855 temp_yr_t5 .4324855*@ .4324855) replace plain



//Maddison Project:
eststo:spatial_hac_iv mpd_growth prec_yr_t0 temp_yr_t0 i.ncountry c.year i.ncountry#c.pow_year (aod_yr_t0 = dust_dry_stat_predict_lag0), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar

estimates store model1

eststo:spatial_hac_iv mpd_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 i.ncountry c.year i.ncountry#c.pow_year (aod_yr_t0 aod_yr_lag1 = dust_dry_stat_predict_lag0 dust_dry_stat_predict_lag1), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar

estimates store model2

eststo:spatial_hac_iv mpd_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 i.ncountry c.year i.ncountry#c.pow_year (aod_yr_t0 aod_yr_lag1 aod_yr_lag2 = dust_dry_stat_predict_lag0 dust_dry_stat_predict_lag1 dust_dry_stat_predict_lag2 ), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar 

estimates store model3

eststo:spatial_hac_iv mpd_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 i.ncountry c.year i.ncountry#c.pow_year (aod_yr_t0 aod_yr_lag1 aod_yr_lag2 aod_yr_lag3 = dust_dry_stat_predict_lag0 dust_dry_stat_predict_lag1 dust_dry_stat_predict_lag2 dust_dry_stat_predict_lag3), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar

estimates store model4

eststo:spatial_hac_iv mpd_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 prec_yr_t4 temp_yr_t4 i.ncountry c.year i.ncountry#c.pow_year (aod_yr_t0 aod_yr_lag1 aod_yr_lag2 aod_yr_lag3 aod_yr_lag4 = dust_dry_stat_predict_lag0 dust_dry_stat_predict_lag1 dust_dry_stat_predict_lag2 dust_dry_stat_predict_lag3 dust_dry_stat_predict_lag4), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar 

estimates store model5

eststo:spatial_hac_iv mpd_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 prec_yr_t4 temp_yr_t4 prec_yr_t5 temp_yr_t5 i.ncountry c.year i.ncountry#c.pow_year (aod_yr_t0 aod_yr_lag1 aod_yr_lag2 aod_yr_lag3 aod_yr_lag4 aod_yr_lag5 = dust_dry_stat_predict_lag0 dust_dry_stat_predict_lag1 dust_dry_stat_predict_lag2 dust_dry_stat_predict_lag3 dust_dry_stat_predict_lag4 dust_dry_stat_predict_lag5), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar  

estimates store model6

esttab model1 model2 model3 model4 model5 model6 using aod_mpd.csv , cells(b(star fmt(7)) se) stats(N r2, fmt(0 4)) keep(aod_yr_t0 aod_yr_lag1 aod_yr_lag2 aod_yr_lag3 aod_yr_lag4 aod_yr_lag5 prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 prec_yr_t4 temp_yr_t4 prec_yr_t5 temp_yr_t5) replace plain star(* 0.10 ** 0.05 *** 0.01)

//aod:
esttab model6 using aod_mpd_aod_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(aod_yr_t0 aod_yr_lag1 aod_yr_lag2 aod_yr_lag3 aod_yr_lag4 aod_yr_lag5) transform(aod_yr_t0 .0497168*@ .0497168 aod_yr_lag1 .0497168*@ .0497168 aod_yr_lag2 .0497168*@ .0497168 aod_yr_lag3 .0497168*@ .0497168 aod_yr_lag4 .0497168*@ .0497168 aod_yr_lag5 .0497168*@ .0497168) replace plain

esttab model1 using aod_mpd_aodl0_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(aod_yr_t0) transform(aod_yr_t0 .0497168*@ .0497168) replace plain

//precipitation:
esttab model6 using aod_mpd_prec_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(prec_yr_t0 prec_yr_t1 prec_yr_t2 prec_yr_t3 prec_yr_t4 prec_yr_t5) transform(prec_yr_t0 7.83e-06*@ 7.83e-06 prec_yr_t1 7.83e-06*@ 7.83e-06 prec_yr_t2 7.83e-06*@ 7.83e-06 prec_yr_t3 7.83e-06*@ 7.83e-06 prec_yr_t4 7.83e-06*@ 7.83e-06 prec_yr_t5 7.83e-06*@ 7.83e-06) replace plain

//temperature
esttab model6 using aod_mpd_temp_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(temp_yr_t0 temp_yr_t1 temp_yr_t2 temp_yr_t3 temp_yr_t4 temp_yr_t5) transform(temp_yr_t0 .4324855*@ .4324855 temp_yr_t1 .4324855*@ .4324855 temp_yr_t2 .4324855*@ .4324855 temp_yr_t3 .4324855*@ .4324855 temp_yr_t4 .4324855*@ .4324855 temp_yr_t5 .4324855*@ .4324855) replace plain

//World Development Indicators:
eststo:spatial_hac_iv wbdi_growth prec_yr_t0 temp_yr_t0 i.ncountry c.year i.ncountry#c.pow_year (aod_yr_t0 = dust_dry_stat_predict_lag0), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar

estimates store model1

eststo:spatial_hac_iv wbdi_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 i.ncountry c.year i.ncountry#c.pow_year (aod_yr_t0 aod_yr_lag1 = dust_dry_stat_predict_lag0 dust_dry_stat_predict_lag1), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar

estimates store model2

eststo:spatial_hac_iv wbdi_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 i.ncountry c.year i.ncountry#c.pow_year (aod_yr_t0 aod_yr_lag1 aod_yr_lag2 = dust_dry_stat_predict_lag0 dust_dry_stat_predict_lag1 dust_dry_stat_predict_lag2 ), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar

estimates store model3 

eststo:spatial_hac_iv wbdi_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 i.ncountry c.year i.ncountry#c.pow_year (aod_yr_t0 aod_yr_lag1 aod_yr_lag2 aod_yr_lag3 = dust_dry_stat_predict_lag0 dust_dry_stat_predict_lag1 dust_dry_stat_predict_lag2 dust_dry_stat_predict_lag3), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar

estimates store model4

eststo:spatial_hac_iv wbdi_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 prec_yr_t4 temp_yr_t4 i.ncountry c.year i.ncountry#c.pow_year (aod_yr_t0 aod_yr_lag1 aod_yr_lag2 aod_yr_lag3 aod_yr_lag4 = dust_dry_stat_predict_lag0 dust_dry_stat_predict_lag1 dust_dry_stat_predict_lag2 dust_dry_stat_predict_lag3 dust_dry_stat_predict_lag4), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar 

estimates store model5

eststo:spatial_hac_iv wbdi_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 prec_yr_t4 temp_yr_t4 prec_yr_t5 temp_yr_t5 i.ncountry c.year i.ncountry#c.pow_year (aod_yr_t0 aod_yr_lag1 aod_yr_lag2 aod_yr_lag3 aod_yr_lag4 aod_yr_lag5 = dust_dry_stat_predict_lag0 dust_dry_stat_predict_lag1 dust_dry_stat_predict_lag2 dust_dry_stat_predict_lag3 dust_dry_stat_predict_lag4 dust_dry_stat_predict_lag5), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar  

estimates store model6

esttab model1 model2 model3 model4 model5 model6 using aod_wbdi.csv , cells(b(star fmt(7)) se) stats(N r2, fmt(0 4)) keep(aod_yr_t0 aod_yr_lag1 aod_yr_lag2 aod_yr_lag3 aod_yr_lag4 aod_yr_lag5 prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 prec_yr_t4 temp_yr_t4 prec_yr_t5 temp_yr_t5) replace plain star(* 0.10 ** 0.05 *** 0.01)

//aod:
esttab model6 using aod_wbdi_aod_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(aod_yr_t0 aod_yr_lag1 aod_yr_lag2 aod_yr_lag3 aod_yr_lag4 aod_yr_lag5) transform(aod_yr_t0 .0497168*@ .0497168 aod_yr_lag1 .0497168*@ .0497168 aod_yr_lag2 .0497168*@ .0497168 aod_yr_lag3 .0497168*@ .0497168 aod_yr_lag4 .0497168*@ .0497168 aod_yr_lag5 .0497168*@ .0497168) replace plain

esttab model1 using aod_wbdi_aodl0_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(aod_yr_t0) transform(aod_yr_t0 .0497168*@ .0497168) replace plain

//precipitation:
esttab model6 using aod_wbdi_prec_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(prec_yr_t0 prec_yr_t1 prec_yr_t2 prec_yr_t3 prec_yr_t4 prec_yr_t5) transform(prec_yr_t0 7.83e-06*@ 7.83e-06 prec_yr_t1 7.83e-06*@ 7.83e-06 prec_yr_t2 7.83e-06*@ 7.83e-06 prec_yr_t3 7.83e-06*@ 7.83e-06 prec_yr_t4 7.83e-06*@ 7.83e-06 prec_yr_t5 7.83e-06*@ 7.83e-06) replace plain

//temperature
esttab model6 using aod_wbdi_temp_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(temp_yr_t0 temp_yr_t1 temp_yr_t2 temp_yr_t3 temp_yr_t4 temp_yr_t5) transform(temp_yr_t0 .4324855*@ .4324855 temp_yr_t1 .4324855*@ .4324855 temp_yr_t2 .4324855*@ .4324855 temp_yr_t3 .4324855*@ .4324855 temp_yr_t4 .4324855*@ .4324855 temp_yr_t5 .4324855*@ .4324855) replace plain

//--------------------------------------------------------------------------------

//Physical model regression:


//Penn World Tables
eststo:spatial_hac_iv pwt_growth prec_yr_t0 temp_yr_t0 i.ncountry c.year i.ncountry#c.pow_year (aod_yr_t0 = dust_dry_sim_predict_lag0), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar

estimates store model1

eststo:spatial_hac_iv pwt_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 i.ncountry c.year i.ncountry#c.pow_year (aod_yr_t0 aod_yr_lag1 = dust_dry_sim_predict_lag0 dust_dry_sim_predict_lag1), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar

estimates store model2

eststo:spatial_hac_iv pwt_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 i.ncountry c.year i.ncountry#c.pow_year (aod_yr_t0 aod_yr_lag1 aod_yr_lag2 = dust_dry_sim_predict_lag0 dust_dry_sim_predict_lag1 dust_dry_sim_predict_lag2 ), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar 

estimates store model3

eststo:spatial_hac_iv pwt_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 i.ncountry c.year i.ncountry#c.pow_year (aod_yr_t0 aod_yr_lag1 aod_yr_lag2 aod_yr_lag3 = dust_dry_sim_predict_lag0 dust_dry_sim_predict_lag1 dust_dry_sim_predict_lag2 dust_dry_sim_predict_lag3), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar

estimates store model4

eststo:spatial_hac_iv pwt_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 prec_yr_t4 temp_yr_t4 i.ncountry c.year i.ncountry#c.pow_year (aod_yr_t0 aod_yr_lag1 aod_yr_lag2 aod_yr_lag3 aod_yr_lag4 = dust_dry_sim_predict_lag0 dust_dry_sim_predict_lag1 dust_dry_sim_predict_lag2 dust_dry_sim_predict_lag3 dust_dry_sim_predict_lag4), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar 

estimates store model5

eststo:spatial_hac_iv pwt_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 prec_yr_t4 temp_yr_t4 prec_yr_t5 temp_yr_t5 i.ncountry c.year i.ncountry#c.pow_year (aod_yr_t0 aod_yr_lag1 aod_yr_lag2 aod_yr_lag3 aod_yr_lag4 aod_yr_lag5 = dust_dry_sim_predict_lag0 dust_dry_sim_predict_lag1 dust_dry_sim_predict_lag2 dust_dry_sim_predict_lag3 dust_dry_sim_predict_lag4 dust_dry_sim_predict_lag5), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar  

estimates store model6

esttab model1 model2 model3 model4 model5 model6 using aod_pwt_sim.csv , cells(b(star fmt(7)) se) stats(N r2, fmt(0 4)) keep(aod_yr_t0 aod_yr_lag1 aod_yr_lag2 aod_yr_lag3 aod_yr_lag4 aod_yr_lag5 prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 prec_yr_t4 temp_yr_t4 prec_yr_t5 temp_yr_t5) replace plain star(* 0.10 ** 0.05 *** 0.01)

//aod:
esttab model6 using aod_pwt_sim_aod_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(aod_yr_t0 aod_yr_lag1 aod_yr_lag2 aod_yr_lag3 aod_yr_lag4 aod_yr_lag5) transform(aod_yr_t0 .0497168*@ .0497168 aod_yr_lag1 .0497168*@ .0497168 aod_yr_lag2 .0497168*@ .0497168 aod_yr_lag3 .0497168*@ .0497168 aod_yr_lag4 .0497168*@ .0497168 aod_yr_lag5 .0497168*@ .0497168) replace plain

esttab model1 using aod_pwt_sim_aodl0_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(aod_yr_t0) transform(aod_yr_t0 .0497168*@ .0497168) replace plain

//precipitation:
esttab model6 using aod_pwt_sim_prec_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(prec_yr_t0 prec_yr_t1 prec_yr_t2 prec_yr_t3 prec_yr_t4 prec_yr_t5) transform(prec_yr_t0 7.83e-06*@ 7.83e-06 prec_yr_t1 7.83e-06*@ 7.83e-06 prec_yr_t2 7.83e-06*@ 7.83e-06 prec_yr_t3 7.83e-06*@ 7.83e-06 prec_yr_t4 7.83e-06*@ 7.83e-06 prec_yr_t5 7.83e-06*@ 7.83e-06) replace plain

//temperature
esttab model6 using aod_pwt_sim_temp_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(temp_yr_t0 temp_yr_t1 temp_yr_t2 temp_yr_t3 temp_yr_t4 temp_yr_t5) transform(temp_yr_t0 .4324855*@ .4324855 temp_yr_t1 .4324855*@ .4324855 temp_yr_t2 .4324855*@ .4324855 temp_yr_t3 .4324855*@ .4324855 temp_yr_t4 .4324855*@ .4324855 temp_yr_t5 .4324855*@ .4324855) replace plain


//Maddison Project:
eststo:spatial_hac_iv mpd_growth prec_yr_t0 temp_yr_t0 i.ncountry c.year i.ncountry#c.pow_year (aod_yr_t0 = dust_dry_sim_predict_lag0), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar

estimates store model1

eststo:spatial_hac_iv mpd_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 i.ncountry c.year i.ncountry#c.pow_year (aod_yr_t0 aod_yr_lag1 = dust_dry_sim_predict_lag0 dust_dry_sim_predict_lag1), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar

estimates store model2

eststo:spatial_hac_iv mpd_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 i.ncountry c.year i.ncountry#c.pow_year (aod_yr_t0 aod_yr_lag1 aod_yr_lag2 = dust_dry_sim_predict_lag0 dust_dry_sim_predict_lag1 dust_dry_sim_predict_lag2 ), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar 

estimates store model3

eststo:spatial_hac_iv mpd_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 i.ncountry c.year i.ncountry#c.pow_year (aod_yr_t0 aod_yr_lag1 aod_yr_lag2 aod_yr_lag3 = dust_dry_sim_predict_lag0 dust_dry_sim_predict_lag1 dust_dry_sim_predict_lag2 dust_dry_sim_predict_lag3), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar

estimates store model4

eststo:spatial_hac_iv mpd_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 prec_yr_t4 temp_yr_t4 i.ncountry c.year i.ncountry#c.pow_year (aod_yr_t0 aod_yr_lag1 aod_yr_lag2 aod_yr_lag3 aod_yr_lag4 = dust_dry_sim_predict_lag0 dust_dry_sim_predict_lag1 dust_dry_sim_predict_lag2 dust_dry_sim_predict_lag3 dust_dry_sim_predict_lag4), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar 

estimates store model5

eststo:spatial_hac_iv mpd_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 prec_yr_t4 temp_yr_t4 prec_yr_t5 temp_yr_t5 i.ncountry c.year i.ncountry#c.pow_year (aod_yr_t0 aod_yr_lag1 aod_yr_lag2 aod_yr_lag3 aod_yr_lag4 aod_yr_lag5 = dust_dry_sim_predict_lag0 dust_dry_sim_predict_lag1 dust_dry_sim_predict_lag2 dust_dry_sim_predict_lag3 dust_dry_sim_predict_lag4 dust_dry_sim_predict_lag5), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar  

estimates store model6

esttab model1 model2 model3 model4 model5 model6 using aod_mpd_sim.csv , cells(b(star fmt(7)) se) stats(N r2, fmt(0 4)) keep(aod_yr_t0 aod_yr_lag1 aod_yr_lag2 aod_yr_lag3 aod_yr_lag4 aod_yr_lag5 prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 prec_yr_t4 temp_yr_t4 prec_yr_t5 temp_yr_t5) replace plain star(* 0.10 ** 0.05 *** 0.01)

//aod:
esttab model6 using aod_mpd_sim_aod_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(aod_yr_t0 aod_yr_lag1 aod_yr_lag2 aod_yr_lag3 aod_yr_lag4 aod_yr_lag5) transform(aod_yr_t0 .0497168*@ .0497168 aod_yr_lag1 .0497168*@ .0497168 aod_yr_lag2 .0497168*@ .0497168 aod_yr_lag3 .0497168*@ .0497168 aod_yr_lag4 .0497168*@ .0497168 aod_yr_lag5 .0497168*@ .0497168) replace plain

esttab model1 using aod_mpd_sim_aodl0_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(aod_yr_t0) transform(aod_yr_t0 .0497168*@ .0497168) replace plain

//precipitation:
esttab model6 using aod_mpd_sim_prec_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(prec_yr_t0 prec_yr_t1 prec_yr_t2 prec_yr_t3 prec_yr_t4 prec_yr_t5) transform(prec_yr_t0 7.83e-06*@ 7.83e-06 prec_yr_t1 7.83e-06*@ 7.83e-06 prec_yr_t2 7.83e-06*@ 7.83e-06 prec_yr_t3 7.83e-06*@ 7.83e-06 prec_yr_t4 7.83e-06*@ 7.83e-06 prec_yr_t5 7.83e-06*@ 7.83e-06) replace plain

//temperature
esttab model6 using aod_mpd_sim_temp_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(temp_yr_t0 temp_yr_t1 temp_yr_t2 temp_yr_t3 temp_yr_t4 temp_yr_t5) transform(temp_yr_t0 .4324855*@ .4324855 temp_yr_t1 .4324855*@ .4324855 temp_yr_t2 .4324855*@ .4324855 temp_yr_t3 .4324855*@ .4324855 temp_yr_t4 .4324855*@ .4324855 temp_yr_t5 .4324855*@ .4324855) replace plain

//World Development Indicators:
eststo:spatial_hac_iv wbdi_growth prec_yr_t0 temp_yr_t0 i.ncountry c.year i.ncountry#c.pow_year (aod_yr_t0 = dust_dry_sim_predict_lag0), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar

estimates store model1

eststo:spatial_hac_iv wbdi_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 i.ncountry c.year i.ncountry#c.pow_year (aod_yr_t0 aod_yr_lag1 = dust_dry_sim_predict_lag0 dust_dry_sim_predict_lag1), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar

estimates store model2

eststo:spatial_hac_iv wbdi_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 i.ncountry c.year i.ncountry#c.pow_year (aod_yr_t0 aod_yr_lag1 aod_yr_lag2 = dust_dry_sim_predict_lag0 dust_dry_sim_predict_lag1 dust_dry_sim_predict_lag2 ), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar 

estimates store model3

eststo:spatial_hac_iv wbdi_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 i.ncountry c.year i.ncountry#c.pow_year (aod_yr_t0 aod_yr_lag1 aod_yr_lag2 aod_yr_lag3 = dust_dry_sim_predict_lag0 dust_dry_sim_predict_lag1 dust_dry_sim_predict_lag2 dust_dry_sim_predict_lag3), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar

estimates store model4

eststo:spatial_hac_iv wbdi_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 prec_yr_t4 temp_yr_t4 i.ncountry c.year i.ncountry#c.pow_year (aod_yr_t0 aod_yr_lag1 aod_yr_lag2 aod_yr_lag3 aod_yr_lag4 = dust_dry_sim_predict_lag0 dust_dry_sim_predict_lag1 dust_dry_sim_predict_lag2 dust_dry_sim_predict_lag3 dust_dry_sim_predict_lag4), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar 

estimates store model5

eststo:spatial_hac_iv wbdi_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 prec_yr_t4 temp_yr_t4 prec_yr_t5 temp_yr_t5 i.ncountry c.year i.ncountry#c.pow_year (aod_yr_t0 aod_yr_lag1 aod_yr_lag2 aod_yr_lag3 aod_yr_lag4 aod_yr_lag5 = dust_dry_sim_predict_lag0 dust_dry_sim_predict_lag1 dust_dry_sim_predict_lag2 dust_dry_sim_predict_lag3 dust_dry_sim_predict_lag4 dust_dry_sim_predict_lag5), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar  

estimates store model6

esttab model1 model2 model3 model4 model5 model6 using aod_wbdi_sim.csv , cells(b(star fmt(7)) se) stats(N r2, fmt(0 4)) keep(aod_yr_t0 aod_yr_lag1 aod_yr_lag2 aod_yr_lag3 aod_yr_lag4 aod_yr_lag5 prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 prec_yr_t4 temp_yr_t4 prec_yr_t5 temp_yr_t5) replace plain star(* 0.10 ** 0.05 *** 0.01)

//aod:
esttab model6 using aod_wbdi_sim_aod_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(aod_yr_t0 aod_yr_lag1 aod_yr_lag2 aod_yr_lag3 aod_yr_lag4 aod_yr_lag5) transform(aod_yr_t0 .0497168*@ .0497168 aod_yr_lag1 .0497168*@ .0497168 aod_yr_lag2 .0497168*@ .0497168 aod_yr_lag3 .0497168*@ .0497168 aod_yr_lag4 .0497168*@ .0497168 aod_yr_lag5 .0497168*@ .0497168) replace plain

esttab model1 using aod_wbdi_sim_aodl0_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(aod_yr_t0) transform(aod_yr_t0 .0497168*@ .0497168) replace plain

//precipitation:
esttab model6 using aod_wbdi_sim_prec_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(prec_yr_t0 prec_yr_t1 prec_yr_t2 prec_yr_t3 prec_yr_t4 prec_yr_t5) transform(prec_yr_t0 7.83e-06*@ 7.83e-06 prec_yr_t1 7.83e-06*@ 7.83e-06 prec_yr_t2 7.83e-06*@ 7.83e-06 prec_yr_t3 7.83e-06*@ 7.83e-06 prec_yr_t4 7.83e-06*@ 7.83e-06 prec_yr_t5 7.83e-06*@ 7.83e-06) replace plain

//temperature
esttab model6 using aod_wbdi_sim_temp_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(temp_yr_t0 temp_yr_t1 temp_yr_t2 temp_yr_t3 temp_yr_t4 temp_yr_t5) transform(temp_yr_t0 .4324855*@ .4324855 temp_yr_t1 .4324855*@ .4324855 temp_yr_t2 .4324855*@ .4324855 temp_yr_t3 .4324855*@ .4324855 temp_yr_t4 .4324855*@ .4324855 temp_yr_t5 .4324855*@ .4324855) replace plain

//*************************************************************************************
//*************************************************************************************


//perform IV regression with PM25

//Statistical model regression:

//Penn World Tables
eststo: spatial_hac_iv pwt_growth prec_yr_t0 temp_yr_t0 i.ncountry c.year i.ncountry#c.pow_year (pm25_yr_t0 = dust_dry_stat_predict_lag0), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar

estimates store model1

eststo: spatial_hac_iv pwt_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 i.ncountry c.year i.ncountry#c.pow_year (pm25_yr_t0 pm25_yr_lag1 = dust_dry_stat_predict_lag0 dust_dry_stat_predict_lag1), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar

estimates store model2

eststo: spatial_hac_iv pwt_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 i.ncountry c.year i.ncountry#c.pow_year (pm25_yr_t0 pm25_yr_lag1 pm25_yr_lag2 = dust_dry_stat_predict_lag0 dust_dry_stat_predict_lag1 dust_dry_stat_predict_lag2 ), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar

estimates store model3

eststo: spatial_hac_iv pwt_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 i.ncountry c.year i.ncountry#c.pow_year (pm25_yr_t0 pm25_yr_lag1 pm25_yr_lag2 pm25_yr_lag3 = dust_dry_stat_predict_lag0 dust_dry_stat_predict_lag1 dust_dry_stat_predict_lag2 dust_dry_stat_predict_lag3), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar

estimates store model4

eststo:spatial_hac_iv pwt_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 prec_yr_t4 temp_yr_t4 i.ncountry c.year i.ncountry#c.pow_year (pm25_yr_t0 pm25_yr_lag1 pm25_yr_lag2 pm25_yr_lag3 pm25_yr_lag4 = dust_dry_stat_predict_lag0 dust_dry_stat_predict_lag1 dust_dry_stat_predict_lag2 dust_dry_stat_predict_lag3 dust_dry_stat_predict_lag4), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar 

estimates store model5


eststo: spatial_hac_iv pwt_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 prec_yr_t4 temp_yr_t4 prec_yr_t5 temp_yr_t5 i.ncountry c.year i.ncountry#c.pow_year (pm25_yr_t0 pm25_yr_lag1 pm25_yr_lag2 pm25_yr_lag3 pm25_yr_lag4 pm25_yr_lag5 = dust_dry_stat_predict_lag0 dust_dry_stat_predict_lag1 dust_dry_stat_predict_lag2 dust_dry_stat_predict_lag3 dust_dry_stat_predict_lag4 dust_dry_stat_predict_lag5), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar  

estimates store model6

esttab model1 model2 model3 model4 model5 model6 using pm25_pwt.csv, cells(b(star fmt(7)) se) stats(N r2, fmt(0 4)) keep(pm25_yr_t0 pm25_yr_lag1 pm25_yr_lag2 pm25_yr_lag3 pm25_yr_lag4 pm25_yr_lag5 prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 prec_yr_t4 temp_yr_t4 prec_yr_t5 temp_yr_t5) replace plain star(* 0.10 ** 0.05 *** 0.01) transform(pm25_yr_t0 10^-9*@ 10^-9 pm25_yr_lag1 10^-9*@ 10^-9 pm25_yr_lag2 10^-9*@ 10^-9 pm25_yr_lag3 10^-9*@ 10^-9 pm25_yr_lag4 10^-9*@ 10^-9 pm25_yr_lag5 10^-9*@ 10^-9)

bysort country: egen pm25_yr_t0_sd=sd(pm25_yr_t0)
mean(pm25_yr_t0_sd)
//5.87e-09

//pm25:
esttab model6 using pm25_pwt_pm25_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(pm25_yr_t0 pm25_yr_lag1 pm25_yr_lag2 pm25_yr_lag3 pm25_yr_lag4 pm25_yr_lag5) transform(pm25_yr_t0 5.87e-09*@ 5.87e-09 pm25_yr_lag1 5.87e-09*@ 5.87e-09 pm25_yr_lag2 5.87e-09*@ 5.87e-09 pm25_yr_lag3 5.87e-09*@ 5.87e-09 pm25_yr_lag4 5.87e-09*@ 5.87e-09 pm25_yr_lag5 5.87e-09*@ 5.87e-09) replace plain

esttab model1 using pm25_pwt_pm25l0_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(pm25_yr_t0) transform(pm25_yr_t0 5.87e-09*@ 5.87e-09) replace plain

//precipitation:
esttab model6 using pm25_pwt_prec_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(prec_yr_t0 prec_yr_t1 prec_yr_t2 prec_yr_t3 prec_yr_t4 prec_yr_t5) transform(prec_yr_t0 7.83e-06*@ 7.83e-06 prec_yr_t1 7.83e-06*@ 7.83e-06 prec_yr_t2 7.83e-06*@ 7.83e-06 prec_yr_t3 7.83e-06*@ 7.83e-06 prec_yr_t4 7.83e-06*@ 7.83e-06 prec_yr_t5 7.83e-06*@ 7.83e-06) replace plain

//temperature
esttab model6 using pm25_pwt_temp_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(temp_yr_t0 temp_yr_t1 temp_yr_t2 temp_yr_t3 temp_yr_t4 temp_yr_t5) transform(temp_yr_t0 .4324855*@ .4324855 temp_yr_t1 .4324855*@ .4324855 temp_yr_t2 .4324855*@ .4324855 temp_yr_t3 .4324855*@ .4324855 temp_yr_t4 .4324855*@ .4324855 temp_yr_t5 .4324855*@ .4324855) replace plain


//Maddison Project:
eststo:spatial_hac_iv mpd_growth prec_yr_t0 temp_yr_t0 i.ncountry c.year i.ncountry#c.pow_year (pm25_yr_t0 = dust_dry_stat_predict_lag0), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar

estimates store model1

eststo:spatial_hac_iv mpd_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 i.ncountry c.year i.ncountry#c.pow_year (pm25_yr_t0 pm25_yr_lag1 = dust_dry_stat_predict_lag0 dust_dry_stat_predict_lag1), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar

estimates store model2

eststo:spatial_hac_iv mpd_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 i.ncountry c.year i.ncountry#c.pow_year (pm25_yr_t0 pm25_yr_lag1 pm25_yr_lag2 = dust_dry_stat_predict_lag0 dust_dry_stat_predict_lag1 dust_dry_stat_predict_lag2 ), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar 

estimates store model3

eststo:spatial_hac_iv mpd_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 i.ncountry c.year i.ncountry#c.pow_year (pm25_yr_t0 pm25_yr_lag1 pm25_yr_lag2 pm25_yr_lag3 = dust_dry_stat_predict_lag0 dust_dry_stat_predict_lag1 dust_dry_stat_predict_lag2 dust_dry_stat_predict_lag3), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar

estimates store model4

eststo:spatial_hac_iv mpd_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 prec_yr_t4 temp_yr_t4 i.ncountry c.year i.ncountry#c.pow_year (pm25_yr_t0 pm25_yr_lag1 pm25_yr_lag2 pm25_yr_lag3 pm25_yr_lag4 = dust_dry_stat_predict_lag0 dust_dry_stat_predict_lag1 dust_dry_stat_predict_lag2 dust_dry_stat_predict_lag3 dust_dry_stat_predict_lag4), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar 

estimates store model5

eststo:spatial_hac_iv mpd_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 prec_yr_t4 temp_yr_t4 prec_yr_t5 temp_yr_t5 i.ncountry c.year i.ncountry#c.pow_year (pm25_yr_t0 pm25_yr_lag1 pm25_yr_lag2 pm25_yr_lag3 pm25_yr_lag4 pm25_yr_lag5 = dust_dry_stat_predict_lag0 dust_dry_stat_predict_lag1 dust_dry_stat_predict_lag2 dust_dry_stat_predict_lag3 dust_dry_stat_predict_lag4 dust_dry_stat_predict_lag5), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar  

estimates store model6

esttab model1 model2 model3 model4 model5 model6 using pm25_mpd.csv , cells(b(star fmt(7)) se) stats(N r2, fmt(0 4)) keep(pm25_yr_t0 pm25_yr_lag1 pm25_yr_lag2 pm25_yr_lag3 pm25_yr_lag4 pm25_yr_lag5 prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 prec_yr_t4 temp_yr_t4 prec_yr_t5 temp_yr_t5) replace plain star(* 0.10 ** 0.05 *** 0.01) transform(pm25_yr_t0 10^-9*@ 10^-9 pm25_yr_lag1 10^-9*@ 10^-9 pm25_yr_lag2 10^-9*@ 10^-9 pm25_yr_lag3 10^-9*@ 10^-9 pm25_yr_lag4 10^-9*@ 10^-9 pm25_yr_lag5 10^-9*@ 10^-9)

//pm25:
esttab model6 using pm25_mpd_pm25_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(pm25_yr_t0 pm25_yr_lag1 pm25_yr_lag2 pm25_yr_lag3 pm25_yr_lag4 pm25_yr_lag5) transform(pm25_yr_t0 5.87e-09*@ 5.87e-09 pm25_yr_lag1 5.87e-09*@ 5.87e-09 pm25_yr_lag2 5.87e-09*@ 5.87e-09 pm25_yr_lag3 5.87e-09*@ 5.87e-09 pm25_yr_lag4 5.87e-09*@ 5.87e-09 pm25_yr_lag5 5.87e-09*@ 5.87e-09) replace plain

esttab model1 using pm25_mpd_pm25l0_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(pm25_yr_t0) transform(pm25_yr_t0 5.87e-09*@ 5.87e-09) replace plain

//precipitation:
esttab model6 using pm25_mpd_prec_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(prec_yr_t0 prec_yr_t1 prec_yr_t2 prec_yr_t3 prec_yr_t4 prec_yr_t5) transform(prec_yr_t0 7.83e-06*@ 7.83e-06 prec_yr_t1 7.83e-06*@ 7.83e-06 prec_yr_t2 7.83e-06*@ 7.83e-06 prec_yr_t3 7.83e-06*@ 7.83e-06 prec_yr_t4 7.83e-06*@ 7.83e-06 prec_yr_t5 7.83e-06*@ 7.83e-06) replace plain

//temperature:
esttab model6 using pm25_mpd_temp_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(temp_yr_t0 temp_yr_t1 temp_yr_t2 temp_yr_t3 temp_yr_t4 temp_yr_t5) transform(temp_yr_t0 .4324855*@ .4324855 temp_yr_t1 .4324855*@ .4324855 temp_yr_t2 .4324855*@ .4324855 temp_yr_t3 .4324855*@ .4324855 temp_yr_t4 .4324855*@ .4324855 temp_yr_t5 .4324855*@ .4324855) replace plain

//World Development Indicators:
eststo:spatial_hac_iv wbdi_growth prec_yr_t0 temp_yr_t0 i.ncountry c.year i.ncountry#c.pow_year (pm25_yr_t0 = dust_dry_stat_predict_lag0), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar

estimates store model1

eststo:spatial_hac_iv wbdi_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 i.ncountry c.year i.ncountry#c.pow_year (pm25_yr_t0 pm25_yr_lag1 = dust_dry_stat_predict_lag0 dust_dry_stat_predict_lag1), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar

estimates store model2

eststo:spatial_hac_iv wbdi_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 i.ncountry c.year i.ncountry#c.pow_year (pm25_yr_t0 pm25_yr_lag1 pm25_yr_lag2 = dust_dry_stat_predict_lag0 dust_dry_stat_predict_lag1 dust_dry_stat_predict_lag2 ), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar

estimates store model3 

eststo:spatial_hac_iv wbdi_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 i.ncountry c.year i.ncountry#c.pow_year (pm25_yr_t0 pm25_yr_lag1 pm25_yr_lag2 pm25_yr_lag3 = dust_dry_stat_predict_lag0 dust_dry_stat_predict_lag1 dust_dry_stat_predict_lag2 dust_dry_stat_predict_lag3), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar

estimates store model4

eststo:spatial_hac_iv wbdi_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 prec_yr_t4 temp_yr_t4 i.ncountry c.year i.ncountry#c.pow_year (pm25_yr_t0 pm25_yr_lag1 pm25_yr_lag2 pm25_yr_lag3 pm25_yr_lag4 = dust_dry_stat_predict_lag0 dust_dry_stat_predict_lag1 dust_dry_stat_predict_lag2 dust_dry_stat_predict_lag3 dust_dry_stat_predict_lag4), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar 

estimates store model5

eststo:spatial_hac_iv wbdi_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 prec_yr_t4 temp_yr_t4 prec_yr_t5 temp_yr_t5 i.ncountry c.year i.ncountry#c.pow_year (pm25_yr_t0 pm25_yr_lag1 pm25_yr_lag2 pm25_yr_lag3 pm25_yr_lag4 pm25_yr_lag5 = dust_dry_stat_predict_lag0 dust_dry_stat_predict_lag1 dust_dry_stat_predict_lag2 dust_dry_stat_predict_lag3 dust_dry_stat_predict_lag4 dust_dry_stat_predict_lag5), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar  

estimates store model6

esttab model1 model2 model3 model4 model5 model6 using pm25_wbdi.csv , cells(b(star fmt(7)) se) stats(N r2, fmt(0 4)) keep(pm25_yr_t0 pm25_yr_lag1 pm25_yr_lag2 pm25_yr_lag3 pm25_yr_lag4 pm25_yr_lag5 prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 prec_yr_t4 temp_yr_t4 prec_yr_t5 temp_yr_t5) replace plain star(* 0.10 ** 0.05 *** 0.01) transform(pm25_yr_t0 10^-9*@ 10^-9 pm25_yr_lag1 10^-9*@ 10^-9 pm25_yr_lag2 10^-9*@ 10^-9 pm25_yr_lag3 10^-9*@ 10^-9 pm25_yr_lag4 10^-9*@ 10^-9 pm25_yr_lag5 10^-9*@ 10^-9)

//pm25:
esttab model6 using pm25_wbdi_pm25_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(pm25_yr_t0 pm25_yr_lag1 pm25_yr_lag2 pm25_yr_lag3 pm25_yr_lag4 pm25_yr_lag5) transform(pm25_yr_t0 5.87e-09*@ 5.87e-09 pm25_yr_lag1 5.87e-09*@ 5.87e-09 pm25_yr_lag2 5.87e-09*@ 5.87e-09 pm25_yr_lag3 5.87e-09*@ 5.87e-09 pm25_yr_lag4 5.87e-09*@ 5.87e-09 pm25_yr_lag5 5.87e-09*@ 5.87e-09) replace plain

esttab model1 using pm25_wbdi_pm25l0_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(pm25_yr_t0) transform(pm25_yr_t0 5.87e-09*@ 5.87e-09) replace plain

//precipitation:
esttab model6 using pm25_wbdi_prec_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(prec_yr_t0 prec_yr_t1 prec_yr_t2 prec_yr_t3 prec_yr_t4 prec_yr_t5) transform(prec_yr_t0 7.83e-06*@ 7.83e-06 prec_yr_t1 7.83e-06*@ 7.83e-06 prec_yr_t2 7.83e-06*@ 7.83e-06 prec_yr_t3 7.83e-06*@ 7.83e-06 prec_yr_t4 7.83e-06*@ 7.83e-06 prec_yr_t5 7.83e-06*@ 7.83e-06) replace plain

//temperature:
esttab model6 using pm25_wbdi_temp_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(temp_yr_t0 temp_yr_t1 temp_yr_t2 temp_yr_t3 temp_yr_t4 temp_yr_t5) transform(temp_yr_t0 .4324855*@ .4324855 temp_yr_t1 .4324855*@ .4324855 temp_yr_t2 .4324855*@ .4324855 temp_yr_t3 .4324855*@ .4324855 temp_yr_t4 .4324855*@ .4324855 temp_yr_t5 .4324855*@ .4324855) replace plain

//--------------------------------------------------------------------------------



//Physical model regression:

//Penn World Tables
eststo:spatial_hac_iv pwt_growth prec_yr_t0 temp_yr_t0 i.ncountry c.year i.ncountry#c.pow_year (pm25_yr_t0 = dust_dry_sim_predict_lag0), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar

estimates store model1

eststo:spatial_hac_iv pwt_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 i.ncountry c.year i.ncountry#c.pow_year (pm25_yr_t0 pm25_yr_lag1 = dust_dry_sim_predict_lag0 dust_dry_sim_predict_lag1), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar

estimates store model2

eststo:spatial_hac_iv pwt_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 i.ncountry c.year i.ncountry#c.pow_year (pm25_yr_t0 pm25_yr_lag1 pm25_yr_lag2 = dust_dry_sim_predict_lag0 dust_dry_sim_predict_lag1 dust_dry_sim_predict_lag2 ), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar 

estimates store model3

eststo:spatial_hac_iv pwt_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 i.ncountry c.year i.ncountry#c.pow_year (pm25_yr_t0 pm25_yr_lag1 pm25_yr_lag2 pm25_yr_lag3 = dust_dry_sim_predict_lag0 dust_dry_sim_predict_lag1 dust_dry_sim_predict_lag2 dust_dry_sim_predict_lag3), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar

estimates store model4

eststo:spatial_hac_iv pwt_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 prec_yr_t4 temp_yr_t4 i.ncountry c.year i.ncountry#c.pow_year (pm25_yr_t0 pm25_yr_lag1 pm25_yr_lag2 pm25_yr_lag3 pm25_yr_lag4 = dust_dry_sim_predict_lag0 dust_dry_sim_predict_lag1 dust_dry_sim_predict_lag2 dust_dry_sim_predict_lag3 dust_dry_sim_predict_lag4), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar 

estimates store model5

eststo:spatial_hac_iv pwt_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 prec_yr_t4 temp_yr_t4 prec_yr_t5 temp_yr_t5 i.ncountry c.year i.ncountry#c.pow_year (pm25_yr_t0 pm25_yr_lag1 pm25_yr_lag2 pm25_yr_lag3 pm25_yr_lag4 pm25_yr_lag5 = dust_dry_sim_predict_lag0 dust_dry_sim_predict_lag1 dust_dry_sim_predict_lag2 dust_dry_sim_predict_lag3 dust_dry_sim_predict_lag4 dust_dry_sim_predict_lag5), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar  

estimates store model6

esttab model1 model2 model3 model4 model5 model6 using pm25_pwt_sim.csv , cells(b(star fmt(7)) se) stats(N r2, fmt(0 4)) keep(pm25_yr_t0 pm25_yr_lag1 pm25_yr_lag2 pm25_yr_lag3 pm25_yr_lag4 pm25_yr_lag5 prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 prec_yr_t4 temp_yr_t4 prec_yr_t5 temp_yr_t5) replace plain star(* 0.10 ** 0.05 *** 0.01) transform(pm25_yr_t0 10^-9*@ 10^-9 pm25_yr_lag1 10^-9*@ 10^-9 pm25_yr_lag2 10^-9*@ 10^-9 pm25_yr_lag3 10^-9*@ 10^-9 pm25_yr_lag4 10^-9*@ 10^-9 pm25_yr_lag5 10^-9*@ 10^-9)

//pm25:
esttab model6 using pm25_pwt_sim_pm25_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(pm25_yr_t0 pm25_yr_lag1 pm25_yr_lag2 pm25_yr_lag3 pm25_yr_lag4 pm25_yr_lag5) transform(pm25_yr_t0 5.87e-09*@ 5.87e-09 pm25_yr_lag1 5.87e-09*@ 5.87e-09 pm25_yr_lag2 5.87e-09*@ 5.87e-09 pm25_yr_lag3 5.87e-09*@ 5.87e-09 pm25_yr_lag4 5.87e-09*@ 5.87e-09 pm25_yr_lag5 5.87e-09*@ 5.87e-09) replace plain

esttab model1 using pm25_pwt_sim_pm25l0_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(pm25_yr_t0) transform(pm25_yr_t0 5.87e-09*@ 5.87e-09) replace plain

//precipitation:
esttab model6 using pm25_pwt_sim_prec_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(prec_yr_t0 prec_yr_t1 prec_yr_t2 prec_yr_t3 prec_yr_t4 prec_yr_t5) transform(prec_yr_t0 7.83e-06*@ 7.83e-06 prec_yr_t1 7.83e-06*@ 7.83e-06 prec_yr_t2 7.83e-06*@ 7.83e-06 prec_yr_t3 7.83e-06*@ 7.83e-06 prec_yr_t4 7.83e-06*@ 7.83e-06 prec_yr_t5 7.83e-06*@ 7.83e-06) replace plain

//temperature:
esttab model6 using pm25_pwt_sim_temp_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(temp_yr_t0 temp_yr_t1 temp_yr_t2 temp_yr_t3 temp_yr_t4 temp_yr_t5) transform(temp_yr_t0 .4324855*@ .4324855 temp_yr_t1 .4324855*@ .4324855 temp_yr_t2 .4324855*@ .4324855 temp_yr_t3 .4324855*@ .4324855 temp_yr_t4 .4324855*@ .4324855 temp_yr_t5 .4324855*@ .4324855) replace plain


//Maddison Project:
eststo:spatial_hac_iv mpd_growth prec_yr_t0 temp_yr_t0 i.ncountry c.year i.ncountry#c.pow_year (pm25_yr_t0 = dust_dry_sim_predict_lag0), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar

estimates store model1

eststo:spatial_hac_iv mpd_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 i.ncountry c.year i.ncountry#c.pow_year (pm25_yr_t0 pm25_yr_lag1 = dust_dry_sim_predict_lag0 dust_dry_sim_predict_lag1), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar

estimates store model2

eststo:spatial_hac_iv mpd_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 i.ncountry c.year i.ncountry#c.pow_year (pm25_yr_t0 pm25_yr_lag1 pm25_yr_lag2 = dust_dry_sim_predict_lag0 dust_dry_sim_predict_lag1 dust_dry_sim_predict_lag2 ), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar 

estimates store model3

eststo:spatial_hac_iv mpd_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 i.ncountry c.year i.ncountry#c.pow_year (pm25_yr_t0 pm25_yr_lag1 pm25_yr_lag2 pm25_yr_lag3 = dust_dry_sim_predict_lag0 dust_dry_sim_predict_lag1 dust_dry_sim_predict_lag2 dust_dry_sim_predict_lag3), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar

estimates store model4

eststo:spatial_hac_iv mpd_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 prec_yr_t4 temp_yr_t4 i.ncountry c.year i.ncountry#c.pow_year (pm25_yr_t0 pm25_yr_lag1 pm25_yr_lag2 pm25_yr_lag3 pm25_yr_lag4 = dust_dry_sim_predict_lag0 dust_dry_sim_predict_lag1 dust_dry_sim_predict_lag2 dust_dry_sim_predict_lag3 dust_dry_sim_predict_lag4), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar 

estimates store model5

eststo:spatial_hac_iv mpd_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 prec_yr_t4 temp_yr_t4 prec_yr_t5 temp_yr_t5 i.ncountry c.year i.ncountry#c.pow_year (pm25_yr_t0 pm25_yr_lag1 pm25_yr_lag2 pm25_yr_lag3 pm25_yr_lag4 pm25_yr_lag5 = dust_dry_sim_predict_lag0 dust_dry_sim_predict_lag1 dust_dry_sim_predict_lag2 dust_dry_sim_predict_lag3 dust_dry_sim_predict_lag4 dust_dry_sim_predict_lag5), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar  

estimates store model6

esttab model1 model2 model3 model4 model5 model6 using pm25_mpd_sim.csv , cells(b(star fmt(7)) se) stats(N r2, fmt(0 4)) keep(pm25_yr_t0 pm25_yr_lag1 pm25_yr_lag2 pm25_yr_lag3 pm25_yr_lag4 pm25_yr_lag5 prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 prec_yr_t4 temp_yr_t4 prec_yr_t5 temp_yr_t5) replace plain star(* 0.10 ** 0.05 *** 0.01) transform(pm25_yr_t0 10^-9*@ 10^-9 pm25_yr_lag1 10^-9*@ 10^-9 pm25_yr_lag2 10^-9*@ 10^-9 pm25_yr_lag3 10^-9*@ 10^-9 pm25_yr_lag4 10^-9*@ 10^-9 pm25_yr_lag5 10^-9*@ 10^-9)

//pm25:
esttab model6 using pm25_mpd_sim_pm25_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(pm25_yr_t0 pm25_yr_lag1 pm25_yr_lag2 pm25_yr_lag3 pm25_yr_lag4 pm25_yr_lag5) transform(pm25_yr_t0 5.87e-09*@ 5.87e-09 pm25_yr_lag1 5.87e-09*@ 5.87e-09 pm25_yr_lag2 5.87e-09*@ 5.87e-09 pm25_yr_lag3 5.87e-09*@ 5.87e-09 pm25_yr_lag4 5.87e-09*@ 5.87e-09 pm25_yr_lag5 5.87e-09*@ 5.87e-09) replace plain

esttab model1 using pm25_mpd_sim_pm25l0_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(pm25_yr_t0) transform(pm25_yr_t0 5.87e-09*@ 5.87e-09) replace plain

//precipitation:
esttab model6 using pm25_mpd_sim_prec_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(prec_yr_t0 prec_yr_t1 prec_yr_t2 prec_yr_t3 prec_yr_t4 prec_yr_t5) transform(prec_yr_t0 7.83e-06*@ 7.83e-06 prec_yr_t1 7.83e-06*@ 7.83e-06 prec_yr_t2 7.83e-06*@ 7.83e-06 prec_yr_t3 7.83e-06*@ 7.83e-06 prec_yr_t4 7.83e-06*@ 7.83e-06 prec_yr_t5 7.83e-06*@ 7.83e-06) replace plain

//temperature:
esttab model6 using pm25_mpd_sim_temp_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(temp_yr_t0 temp_yr_t1 temp_yr_t2 temp_yr_t3 temp_yr_t4 temp_yr_t5) transform(temp_yr_t0 .4324855*@ .4324855 temp_yr_t1 .4324855*@ .4324855 temp_yr_t2 .4324855*@ .4324855 temp_yr_t3 .4324855*@ .4324855 temp_yr_t4 .4324855*@ .4324855 temp_yr_t5 .4324855*@ .4324855) replace plain


//World Development Indicators:
eststo:spatial_hac_iv wbdi_growth prec_yr_t0 temp_yr_t0 i.ncountry c.year i.ncountry#c.pow_year (pm25_yr_t0 = dust_dry_sim_predict_lag0), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar

estimates store model1

eststo:spatial_hac_iv wbdi_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 i.ncountry c.year i.ncountry#c.pow_year (pm25_yr_t0 pm25_yr_lag1 = dust_dry_sim_predict_lag0 dust_dry_sim_predict_lag1), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar

estimates store model2

eststo:spatial_hac_iv wbdi_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 i.ncountry c.year i.ncountry#c.pow_year (pm25_yr_t0 pm25_yr_lag1 pm25_yr_lag2 = dust_dry_sim_predict_lag0 dust_dry_sim_predict_lag1 dust_dry_sim_predict_lag2 ), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar 

estimates store model3

eststo:spatial_hac_iv wbdi_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 i.ncountry c.year i.ncountry#c.pow_year (pm25_yr_t0 pm25_yr_lag1 pm25_yr_lag2 pm25_yr_lag3 = dust_dry_sim_predict_lag0 dust_dry_sim_predict_lag1 dust_dry_sim_predict_lag2 dust_dry_sim_predict_lag3), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar

estimates store model4

eststo:spatial_hac_iv wbdi_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 prec_yr_t4 temp_yr_t4 i.ncountry c.year i.ncountry#c.pow_year (pm25_yr_t0 pm25_yr_lag1 pm25_yr_lag2 pm25_yr_lag3 pm25_yr_lag4 = dust_dry_sim_predict_lag0 dust_dry_sim_predict_lag1 dust_dry_sim_predict_lag2 dust_dry_sim_predict_lag3 dust_dry_sim_predict_lag4), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar 

estimates store model5

eststo:spatial_hac_iv wbdi_growth prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 prec_yr_t4 temp_yr_t4 prec_yr_t5 temp_yr_t5 i.ncountry c.year i.ncountry#c.pow_year (pm25_yr_t0 pm25_yr_lag1 pm25_yr_lag2 pm25_yr_lag3 pm25_yr_lag4 pm25_yr_lag5 = dust_dry_sim_predict_lag0 dust_dry_sim_predict_lag1 dust_dry_sim_predict_lag2 dust_dry_sim_predict_lag3 dust_dry_sim_predict_lag4 dust_dry_sim_predict_lag5), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar  

estimates store model6

esttab model1 model2 model3 model4 model5 model6 using pm25_wbdi_sim.csv , cells(b(star fmt(7)) se) stats(N r2, fmt(0 4)) keep(pm25_yr_t0 pm25_yr_lag1 pm25_yr_lag2 pm25_yr_lag3 pm25_yr_lag4 pm25_yr_lag5 prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 prec_yr_t2 temp_yr_t2 prec_yr_t3 temp_yr_t3 prec_yr_t4 temp_yr_t4 prec_yr_t5 temp_yr_t5) replace plain star(* 0.10 ** 0.05 *** 0.01) transform(pm25_yr_t0 10^-9*@ 10^-9 pm25_yr_lag1 10^-9*@ 10^-9 pm25_yr_lag2 10^-9*@ 10^-9 pm25_yr_lag3 10^-9*@ 10^-9 pm25_yr_lag4 10^-9*@ 10^-9 pm25_yr_lag5 10^-9*@ 10^-9)

//pm25:
esttab model6 using pm25_wbdi_sim_pm25_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(pm25_yr_t0 pm25_yr_lag1 pm25_yr_lag2 pm25_yr_lag3 pm25_yr_lag4 pm25_yr_lag5) transform(pm25_yr_t0 5.87e-09*@ 5.87e-09 pm25_yr_lag1 5.87e-09*@ 5.87e-09 pm25_yr_lag2 5.87e-09*@ 5.87e-09 pm25_yr_lag3 5.87e-09*@ 5.87e-09 pm25_yr_lag4 5.87e-09*@ 5.87e-09 pm25_yr_lag5 5.87e-09*@ 5.87e-09) replace plain

esttab model1 using pm25_wbdi_sim_pm25l0_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(pm25_yr_t0) transform(pm25_yr_t0 5.87e-09*@ 5.87e-09) replace plain

//precipitation:
esttab model6 using pm25_wbdi_sim_prec_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(prec_yr_t0 prec_yr_t1 prec_yr_t2 prec_yr_t3 prec_yr_t4 prec_yr_t5) transform(prec_yr_t0 7.83e-06*@ 7.83e-06 prec_yr_t1 7.83e-06*@ 7.83e-06 prec_yr_t2 7.83e-06*@ 7.83e-06 prec_yr_t3 7.83e-06*@ 7.83e-06 prec_yr_t4 7.83e-06*@ 7.83e-06 prec_yr_t5 7.83e-06*@ 7.83e-06) replace plain

//temperature:
esttab model6 using pm25_wbdi_sim_temp_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(temp_yr_t0 temp_yr_t1 temp_yr_t2 temp_yr_t3 temp_yr_t4 temp_yr_t5) transform(temp_yr_t0 .4324855*@ .4324855 temp_yr_t1 .4324855*@ .4324855 temp_yr_t2 .4324855*@ .4324855 temp_yr_t3 .4324855*@ .4324855 temp_yr_t4 .4324855*@ .4324855 temp_yr_t5 .4324855*@ .4324855) replace plain


//*************************************************************************************
//*************************************************************************************


//AOD
//perform reduced form regression
//bodele aod dry and wet robustness
eststo:reg pwt_growth bodele_aod_dry bodele_aod_dry_lag1 prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 i.ncountry c.year i.ncountry#c.pow_year

estimates store model1

eststo:reg mpd_growth bodele_aod_dry bodele_aod_dry_lag1 prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 i.ncountry c.year i.ncountry#c.pow_year

estimates store model2

eststo:reg wbdi_growth bodele_aod_dry bodele_aod_dry_lag1 prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 i.ncountry c.year i.ncountry#c.pow_year

estimates store model3

esttab model1 model2 model3 using aod_bodele_dry.csv , cells(b(star fmt(7)) se) stats(N r2_a, fmt(0 4)) keep(bodele_aod_dry bodele_aod_dry_lag1 prec_yr_t0 prec_yr_t1 temp_yr_t0 temp_yr_t1 _cons) replace plain star(* 0.10 ** 0.05 *** 0.01) order(bodele_aod_dry bodele_aod_dry_lag1 prec_yr_t0 prec_yr_t1 temp_yr_t0 temp_yr_t1 _cons)


bysort country: egen bodele_aod_yr_sd=sd(bodele_y)
//.0501506

esttab model1 model2 model3 using aod_bodele_dryl0l1_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(bodele_aod_dry bodele_aod_dry_lag1) transform(bodele_aod_dry .0501506*@ .0501506 bodele_aod_dry_lag1 .0501506*@ .0501506) replace plain



eststo:reg pwt_growth bodele_x bodele_aod_wet_lag1 prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 i.ncountry c.year i.ncountry#c.pow_year

estimates store model1

eststo:reg mpd_growth bodele_x bodele_aod_wet_lag1 prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 i.ncountry c.year i.ncountry#c.pow_year

estimates store model2

eststo:reg wbdi_growth bodele_x bodele_aod_wet_lag1 prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 i.ncountry c.year i.ncountry#c.pow_year

estimates store model3

esttab model1 model2 model3 using aod_bodele_wet.csv , cells(b(star fmt(7)) se) stats(N r2_a, fmt(0 4)) keep(bodele_x bodele_aod_wet_lag1 prec_yr_t0 prec_yr_t1 temp_yr_t0 temp_yr_t1 _cons) replace plain star(* 0.10 ** 0.05 *** 0.01) order(bodele_x bodele_aod_wet_lag1 prec_yr_t0 prec_yr_t1 temp_yr_t0 temp_yr_t1 _cons)

esttab model1 model2 model3 using aod_bodele_wetl0l1_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(bodele_x bodele_aod_wet_lag1) transform(bodele_x .0501506*@ .0501506 bodele_aod_wet_lag1 .0501506*@ .0501506) replace plain


//perform lead regression:
//pred values
//pwt
eststo: spatial_hac_iv pwt_growth prec_yr_t0 temp_yr_t0 prec_yr_lead1 temp_yr_lead1 prec_yr_lead2 temp_yr_lead2 prec_yr_lead3 temp_yr_lead3 prec_yr_lead4 temp_yr_lead4 prec_yr_lead5 temp_yr_lead5 i.ncountry c.year i.ncountry#c.pow_year (aod_yr_t0 aod_yr_lead1 aod_yr_lead2 aod_yr_lead3 aod_yr_lead4 aod_yr_lead5 = dust_dry_stat_predict_lag0 dust_dry_stat_predict_lead1 dust_dry_stat_predict_lead2 dust_dry_stat_predict_lead3 dust_dry_stat_predict_lead4 dust_dry_stat_predict_lead5), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar 

estimates store model6

esttab model6 model6 model6 model6 model6 model6 using aod_pwt_lead.csv , cells(b(star fmt(7)) se) stats(N r2, fmt(0 4)) keep(aod_yr_t0 aod_yr_lead1 aod_yr_lead2 aod_yr_lead3 aod_yr_lead4 aod_yr_lead5 prec_yr_t0 temp_yr_t0 prec_yr_lead1 temp_yr_lead1 prec_yr_lead2 temp_yr_lead2 prec_yr_lead3 temp_yr_lead3 prec_yr_lead4 temp_yr_lead4 prec_yr_lead5 temp_yr_lead5) replace plain star(* 0.10 ** 0.05 *** 0.01)

esttab model6 using aod_pwt_backward_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(aod_yr_t0 aod_yr_lead1 aod_yr_lead2 aod_yr_lead3 aod_yr_lead4 aod_yr_lead5) transform(aod_yr_t0 .0497168*@ .0497168 aod_yr_lead1 .0497168*@ .0497168 aod_yr_lead2 .0497168*@ .0497168 aod_yr_lead3 .0497168*@ .0497168 aod_yr_lead4 .0497168*@ .0497168 aod_yr_lead5 .0497168*@ .0497168) replace plain

//mpd

eststo: spatial_hac_iv mpd_growth prec_yr_t0 temp_yr_t0 prec_yr_lead1 temp_yr_lead1 prec_yr_lead2 temp_yr_lead2 prec_yr_lead3 temp_yr_lead3 prec_yr_lead4 temp_yr_lead4 prec_yr_lead5 temp_yr_lead5 i.ncountry c.year i.ncountry#c.pow_year (aod_yr_t0 aod_yr_lead1 aod_yr_lead2 aod_yr_lead3 aod_yr_lead4 aod_yr_lead5 = dust_dry_stat_predict_lag0 dust_dry_stat_predict_lead1 dust_dry_stat_predict_lead2 dust_dry_stat_predict_lead3 dust_dry_stat_predict_lead4 dust_dry_stat_predict_lead5), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar 

estimates store model6

esttab model6 model6 model6 model6 model6 model6 using aod_mpd_lead.csv , cells(b(star fmt(7)) se) stats(N r2, fmt(0 4)) keep(aod_yr_t0 aod_yr_lead1 aod_yr_lead2 aod_yr_lead3 aod_yr_lead4 aod_yr_lead5 prec_yr_t0 temp_yr_t0 prec_yr_lead1 temp_yr_lead1 prec_yr_lead2 temp_yr_lead2 prec_yr_lead3 temp_yr_lead3 prec_yr_lead4 temp_yr_lead4 prec_yr_lead5 temp_yr_lead5) replace plain star(* 0.10 ** 0.05 *** 0.01)

esttab model6 using aod_mpd_backward_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(aod_yr_t0 aod_yr_lead1 aod_yr_lead2 aod_yr_lead3 aod_yr_lead4 aod_yr_lead5) transform(aod_yr_t0 .0497168*@ .0497168 aod_yr_lead1 .0497168*@ .0497168 aod_yr_lead2 .0497168*@ .0497168 aod_yr_lead3 .0497168*@ .0497168 aod_yr_lead4 .0497168*@ .0497168 aod_yr_lead5 .0497168*@ .0497168) replace plain

//wbdi

eststo: spatial_hac_iv wbdi_growth prec_yr_t0 temp_yr_t0 prec_yr_lead1 temp_yr_lead1 prec_yr_lead2 temp_yr_lead2 prec_yr_lead3 temp_yr_lead3 prec_yr_lead4 temp_yr_lead4 prec_yr_lead5 temp_yr_lead5 i.ncountry c.year i.ncountry#c.pow_year (aod_yr_t0 aod_yr_lead1 aod_yr_lead2 aod_yr_lead3 aod_yr_lead4 aod_yr_lead5 = dust_dry_stat_predict_lag0 dust_dry_stat_predict_lead1 dust_dry_stat_predict_lead2 dust_dry_stat_predict_lead3 dust_dry_stat_predict_lead4 dust_dry_stat_predict_lead5), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar 

estimates store model6

esttab model6 model6 model6 model6 model6 model6 using aod_wbdi_lead.csv , cells(b(star fmt(7)) se) stats(N r2, fmt(0 4)) keep(aod_yr_t0 aod_yr_lead1 aod_yr_lead2 aod_yr_lead3 aod_yr_lead4 aod_yr_lead5 prec_yr_t0 temp_yr_t0 prec_yr_lead1 temp_yr_lead1 prec_yr_lead2 temp_yr_lead2 prec_yr_lead3 temp_yr_lead3 prec_yr_lead4 temp_yr_lead4 prec_yr_lead5 temp_yr_lead5) replace plain star(* 0.10 ** 0.05 *** 0.01)


esttab model6 using aod_wbdi_backward_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(aod_yr_t0 aod_yr_lead1 aod_yr_lead2 aod_yr_lead3 aod_yr_lead4 aod_yr_lead5) transform(aod_yr_t0 .0497168*@ .0497168 aod_yr_lead1 .0497168*@ .0497168 aod_yr_lead2 .0497168*@ .0497168 aod_yr_lead3 .0497168*@ .0497168 aod_yr_lead4 .0497168*@ .0497168 aod_yr_lead5 .0497168*@ .0497168) replace plain


//sim values

//pwt
eststo: spatial_hac_iv pwt_growth prec_yr_t0 temp_yr_t0 prec_yr_lead1 temp_yr_lead1 prec_yr_lead2 temp_yr_lead2 prec_yr_lead3 temp_yr_lead3 prec_yr_lead4 temp_yr_lead4 prec_yr_lead5 temp_yr_lead5 i.ncountry c.year i.ncountry#c.pow_year (aod_yr_t0 aod_yr_lead1 aod_yr_lead2 aod_yr_lead3 aod_yr_lead4 aod_yr_lead5 = dust_dry_stat_predict_lag0 dust_dry_sim_predict_lead1 dust_dry_sim_predict_lead2 dust_dry_sim_predict_lead3 dust_dry_sim_predict_lead4 dust_dry_sim_predict_lead5), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar 

estimates store model6

esttab model6 model6 model6 model6 model6 model6 using aod_pwt_sim_lead.csv , cells(b(star fmt(7)) se) stats(N r2, fmt(0 4)) keep(aod_yr_t0 aod_yr_lead1 aod_yr_lead2 aod_yr_lead3 aod_yr_lead4 aod_yr_lead5 prec_yr_t0 temp_yr_t0 prec_yr_lead1 temp_yr_lead1 prec_yr_lead2 temp_yr_lead2 prec_yr_lead3 temp_yr_lead3 prec_yr_lead4 temp_yr_lead4 prec_yr_lead5 temp_yr_lead5) replace plain star(* 0.10 ** 0.05 *** 0.01)

esttab model6 using aod_pwt_backward_response_sim.csv, cells(b(fmt(7)) ci(fmt(7))) keep(aod_yr_t0 aod_yr_lead1 aod_yr_lead2 aod_yr_lead3 aod_yr_lead4 aod_yr_lead5) transform(aod_yr_t0 .0497168*@ .0497168 aod_yr_lead1 .0497168*@ .0497168 aod_yr_lead2 .0497168*@ .0497168 aod_yr_lead3 .0497168*@ .0497168 aod_yr_lead4 .0497168*@ .0497168 aod_yr_lead5 .0497168*@ .0497168) replace plain

//mpd

eststo: spatial_hac_iv mpd_growth prec_yr_t0 temp_yr_t0 prec_yr_lead1 temp_yr_lead1 prec_yr_lead2 temp_yr_lead2 prec_yr_lead3 temp_yr_lead3 prec_yr_lead4 temp_yr_lead4 prec_yr_lead5 temp_yr_lead5 i.ncountry c.year i.ncountry#c.pow_year (aod_yr_t0 aod_yr_lead1 aod_yr_lead2 aod_yr_lead3 aod_yr_lead4 aod_yr_lead5 = dust_dry_stat_predict_lag0 dust_dry_sim_predict_lead1 dust_dry_sim_predict_lead2 dust_dry_sim_predict_lead3 dust_dry_sim_predict_lead4 dust_dry_sim_predict_lead5), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar 

estimates store model6

esttab model6 model6 model6 model6 model6 model6 using aod_mpd_sim_lead.csv , cells(b(star fmt(7)) se) stats(N r2, fmt(0 4)) keep(aod_yr_t0 aod_yr_lead1 aod_yr_lead2 aod_yr_lead3 aod_yr_lead4 aod_yr_lead5 prec_yr_t0 temp_yr_t0 prec_yr_lead1 temp_yr_lead1 prec_yr_lead2 temp_yr_lead2 prec_yr_lead3 temp_yr_lead3 prec_yr_lead4 temp_yr_lead4 prec_yr_lead5 temp_yr_lead5) replace plain star(* 0.10 ** 0.05 *** 0.01)

esttab model6 using aod_mpd_backward_response_sim.csv, cells(b(fmt(7)) ci(fmt(7))) keep(aod_yr_t0 aod_yr_lead1 aod_yr_lead2 aod_yr_lead3 aod_yr_lead4 aod_yr_lead5) transform(aod_yr_t0 .0497168*@ .0497168 aod_yr_lead1 .0497168*@ .0497168 aod_yr_lead2 .0497168*@ .0497168 aod_yr_lead3 .0497168*@ .0497168 aod_yr_lead4 .0497168*@ .0497168 aod_yr_lead5 .0497168*@ .0497168) replace plain

//wbdi

eststo: spatial_hac_iv wbdi_growth prec_yr_t0 temp_yr_t0 prec_yr_lead1 temp_yr_lead1 prec_yr_lead2 temp_yr_lead2 prec_yr_lead3 temp_yr_lead3 prec_yr_lead4 temp_yr_lead4 prec_yr_lead5 temp_yr_lead5 i.ncountry c.year i.ncountry#c.pow_year (aod_yr_t0 aod_yr_lead1 aod_yr_lead2 aod_yr_lead3 aod_yr_lead4 aod_yr_lead5 = dust_dry_stat_predict_lag0 dust_dry_sim_predict_lead1 dust_dry_sim_predict_lead2 dust_dry_sim_predict_lead3 dust_dry_sim_predict_lead4 dust_dry_sim_predict_lead5), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar 

estimates store model6

esttab model6 model6 model6 model6 model6 model6 using aod_wbdi_sim_lead.csv , cells(b(star fmt(7)) se) stats(N r2, fmt(0 4)) keep(aod_yr_t0 aod_yr_lead1 aod_yr_lead2 aod_yr_lead3 aod_yr_lead4 aod_yr_lead5 prec_yr_t0 temp_yr_t0 prec_yr_lead1 temp_yr_lead1 prec_yr_lead2 temp_yr_lead2 prec_yr_lead3 temp_yr_lead3 prec_yr_lead4 temp_yr_lead4 prec_yr_lead5 temp_yr_lead5) replace plain star(* 0.10 ** 0.05 *** 0.01)

esttab model6 using aod_wbdi_backward_response_sim.csv, cells(b(fmt(7)) ci(fmt(7))) keep(aod_yr_t0 aod_yr_lead1 aod_yr_lead2 aod_yr_lead3 aod_yr_lead4 aod_yr_lead5) transform(aod_yr_t0 .0497168*@ .0497168 aod_yr_lead1 .0497168*@ .0497168 aod_yr_lead2 .0497168*@ .0497168 aod_yr_lead3 .0497168*@ .0497168 aod_yr_lead4 .0497168*@ .0497168 aod_yr_lead5 .0497168*@ .0497168) replace plain

//*************************************************************************************
//*************************************************************************************

//PM25
//perform reduced form regression
//bodele pm25 dry and wet robustness

eststo:reg pwt_growth bodele_pm25_dry bodele_pm25_dry_lag1 prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 i.ncountry c.year i.ncountry#c.pow_year

estimates store model1

eststo:reg mpd_growth bodele_pm25_dry bodele_pm25_dry_lag1 prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 i.ncountry c.year i.ncountry#c.pow_year

estimates store model2

eststo:reg wbdi_growth bodele_pm25_dry bodele_pm25_dry_lag1 prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 i.ncountry c.year i.ncountry#c.pow_year

estimates store model3

esttab model1 model2 model3 using pm25_bodele_dryl0l1_response.csv , cells(b(star fmt(7)) se) stats(N r2, fmt(0 4)) keep(bodele_pm25_dry bodele_pm25_dry_lag1 prec_yr_t0 prec_yr_t1 temp_yr_t0 temp_yr_t1 _cons) replace plain star(* 0.10 ** 0.05 *** 0.01) transform(bodele_pm25_dry 10^-9*@ 10^-9 bodele_pm25_dry_lag1 10^-9*@ 10^-9) order(bodele_pm25_dry bodele_pm25_dry_lag1 prec_yr_t0 prec_yr_t1 temp_yr_t0 temp_yr_t1 _cons) 

bysort country: egen bodele_pm25_yr_sd=sd(v141)
//8.56e-09

esttab model1 model2 model3 using pm25_bodele_dryl0l1_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(bodele_pm25_dry bodele_pm25_dry_lag1) transform(bodele_pm25_dry 8.56e-09*@ 8.56e-09 bodele_pm25_dry_lag1 8.56e-09*@ 8.56e-09) replace plain






eststo:reg pwt_growth v140 bodele_pm25_wet_lag1 prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 i.ncountry c.year i.ncountry#c.pow_year

estimates store model1

eststo:reg mpd_growth v140 bodele_pm25_wet_lag1 prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 i.ncountry c.year i.ncountry#c.pow_year

estimates store model2

eststo:reg wbdi_growth v140 bodele_pm25_wet_lag1 prec_yr_t0 temp_yr_t0 prec_yr_t1 temp_yr_t1 i.ncountry c.year i.ncountry#c.pow_year

estimates store model3

esttab model1 model2 model3 using pm25_bodele_wet.csv , cells(b(star fmt(7)) se) stats(N r2, fmt(0 4)) keep(v140 bodele_pm25_wet_lag1 prec_yr_t0 prec_yr_t1 temp_yr_t0 temp_yr_t1 _cons) replace plain star(* 0.10 ** 0.05 *** 0.01) transform(v140 10^-9*@ 10^-9 bodele_pm25_wet_lag1 10^-9*@ 10^-9) order(v140 bodele_pm25_wet_lag1 prec_yr_t0 prec_yr_t1 temp_yr_t0 temp_yr_t1 _cons)

bysort country: egen bodele_pm25_wet_sd=sd(bodele_pm25_wet)
//8.81e-09

esttab model1 model2 model3 using pm25_bodele_wetl0l1_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(v140 bodele_pm25_wet_lag1) transform(v140 8.56e-09*@ 8.56e-09 bodele_pm25_wet_lag1 8.56e-09*@ 8.56e-09) replace plain

//perform lead regression:
//pred values
//pwt
eststo: spatial_hac_iv pwt_growth prec_yr_t0 temp_yr_t0 prec_yr_lead1 temp_yr_lead1 prec_yr_lead2 temp_yr_lead2 prec_yr_lead3 temp_yr_lead3 prec_yr_lead4 temp_yr_lead4 prec_yr_lead5 temp_yr_lead5 i.ncountry c.year i.ncountry#c.pow_year (pm25_yr_t0 pm25_yr_lead1 pm25_yr_lead2 pm25_yr_lead3 pm25_yr_lead4 pm25_yr_lead5 = dust_dry_stat_predict_lag0 dust_dry_stat_predict_lead1 dust_dry_stat_predict_lead2 dust_dry_stat_predict_lead3 dust_dry_stat_predict_lead4 dust_dry_stat_predict_lead5), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar 

estimates store model6

esttab model6 model6 model6 model6 model6 model6 using pm25_pwt_lead.csv , cells(b(star fmt(7)) se) stats(N r2, fmt(0 4)) keep(pm25_yr_t0 pm25_yr_lead1 pm25_yr_lead2 pm25_yr_lead3 pm25_yr_lead4 pm25_yr_lead5 prec_yr_t0 temp_yr_t0 prec_yr_lead1 temp_yr_lead1 prec_yr_lead2 temp_yr_lead2 prec_yr_lead3 temp_yr_lead3 prec_yr_lead4 temp_yr_lead4 prec_yr_lead5 temp_yr_lead5) replace plain star(* 0.10 ** 0.05 *** 0.01) transform(pm25_yr_t0 10^-9*@ 10^-9 pm25_yr_lead1 10^-9*@ 10^-9 pm25_yr_lead2 10^-9*@ 10^-9 pm25_yr_lead3 10^-9*@ 10^-9 pm25_yr_lead4 10^-9*@ 10^-9 pm25_yr_lead5 10^-9*@ 10^-9)

esttab model6 using pm25_pwt_backward_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(pm25_yr_t0 pm25_yr_lead1 pm25_yr_lead2 pm25_yr_lead3 pm25_yr_lead4 pm25_yr_lead5) transform(pm25_yr_t0 5.87e-09*@ 5.87e-09 pm25_yr_lead1 5.87e-09*@ 5.87e-09 pm25_yr_lead2 5.87e-09*@ 5.87e-09 pm25_yr_lead3 5.87e-09*@ 5.87e-09 pm25_yr_lead4 5.87e-09*@ 5.87e-09 pm25_yr_lead5 5.87e-09*@ 5.87e-09) replace plain

//mpd

eststo: spatial_hac_iv mpd_growth prec_yr_t0 temp_yr_t0 prec_yr_lead1 temp_yr_lead1 prec_yr_lead2 temp_yr_lead2 prec_yr_lead3 temp_yr_lead3 prec_yr_lead4 temp_yr_lead4 prec_yr_lead5 temp_yr_lead5 i.ncountry c.year i.ncountry#c.pow_year (pm25_yr_t0 pm25_yr_lead1 pm25_yr_lead2 pm25_yr_lead3 pm25_yr_lead4 pm25_yr_lead5 = dust_dry_stat_predict_lag0 dust_dry_stat_predict_lead1 dust_dry_stat_predict_lead2 dust_dry_stat_predict_lead3 dust_dry_stat_predict_lead4 dust_dry_stat_predict_lead5), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar 

estimates store model6

esttab model6 model6 model6 model6 model6 model6 using pm25_mpd_lead.csv , cells(b(star fmt(7)) se) stats(N r2, fmt(0 4)) keep(pm25_yr_t0 pm25_yr_lead1 pm25_yr_lead2 pm25_yr_lead3 pm25_yr_lead4 pm25_yr_lead5 prec_yr_t0 temp_yr_t0 prec_yr_lead1 temp_yr_lead1 prec_yr_lead2 temp_yr_lead2 prec_yr_lead3 temp_yr_lead3 prec_yr_lead4 temp_yr_lead4 prec_yr_lead5 temp_yr_lead5) replace plain star(* 0.10 ** 0.05 *** 0.01) transform(pm25_yr_t0 10^-9*@ 10^-9 pm25_yr_lead1 10^-9*@ 10^-9 pm25_yr_lead2 10^-9*@ 10^-9 pm25_yr_lead3 10^-9*@ 10^-9 pm25_yr_lead4 10^-9*@ 10^-9 pm25_yr_lead5 10^-9*@ 10^-9)

esttab model6 using pm25_mpd_backward_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(pm25_yr_t0 pm25_yr_lead1 pm25_yr_lead2 pm25_yr_lead3 pm25_yr_lead4 pm25_yr_lead5) transform(pm25_yr_t0 5.87e-09*@ 5.87e-09 pm25_yr_lead1 5.87e-09*@ 5.87e-09 pm25_yr_lead2 5.87e-09*@ 5.87e-09 pm25_yr_lead3 5.87e-09*@ 5.87e-09 pm25_yr_lead4 5.87e-09*@ 5.87e-09 pm25_yr_lead5 5.87e-09*@ 5.87e-09) replace plain

//wbdi

eststo: spatial_hac_iv wbdi_growth prec_yr_t0 temp_yr_t0 prec_yr_lead1 temp_yr_lead1 prec_yr_lead2 temp_yr_lead2 prec_yr_lead3 temp_yr_lead3 prec_yr_lead4 temp_yr_lead4 prec_yr_lead5 temp_yr_lead5 i.ncountry c.year i.ncountry#c.pow_year (pm25_yr_t0 pm25_yr_lead1 pm25_yr_lead2 pm25_yr_lead3 pm25_yr_lead4 pm25_yr_lead5 = dust_dry_stat_predict_lag0 dust_dry_stat_predict_lead1 dust_dry_stat_predict_lead2 dust_dry_stat_predict_lead3 dust_dry_stat_predict_lead4 dust_dry_stat_predict_lead5), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar 

estimates store model6

esttab model6 model6 model6 model6 model6 model6 using pm25_wbdi_lead.csv , cells(b(star fmt(7)) se) stats(N r2, fmt(0 4)) keep(pm25_yr_t0 pm25_yr_lead1 pm25_yr_lead2 pm25_yr_lead3 pm25_yr_lead4 pm25_yr_lead5 prec_yr_t0 temp_yr_t0 prec_yr_lead1 temp_yr_lead1 prec_yr_lead2 temp_yr_lead2 prec_yr_lead3 temp_yr_lead3 prec_yr_lead4 temp_yr_lead4 prec_yr_lead5 temp_yr_lead5) replace plain star(* 0.10 ** 0.05 *** 0.01) transform(pm25_yr_t0 10^-9*@ 10^-9 pm25_yr_lead1 10^-9*@ 10^-9 pm25_yr_lead2 10^-9*@ 10^-9 pm25_yr_lead3 10^-9*@ 10^-9 pm25_yr_lead4 10^-9*@ 10^-9 pm25_yr_lead5 10^-9*@ 10^-9)

esttab model6 using pm25_wbdi_backward_response.csv, cells(b(fmt(7)) ci(fmt(7))) keep(pm25_yr_t0 pm25_yr_lead1 pm25_yr_lead2 pm25_yr_lead3 pm25_yr_lead4 pm25_yr_lead5) transform(pm25_yr_t0 5.87e-09*@ 5.87e-09 pm25_yr_lead1 5.87e-09*@ 5.87e-09 pm25_yr_lead2 5.87e-09*@ 5.87e-09 pm25_yr_lead3 5.87e-09*@ 5.87e-09 pm25_yr_lead4 5.87e-09*@ 5.87e-09 pm25_yr_lead5 5.87e-09*@ 5.87e-09) replace plain

//sim values

//pwt
eststo: spatial_hac_iv pwt_growth prec_yr_t0 temp_yr_t0 prec_yr_lead1 temp_yr_lead1 prec_yr_lead2 temp_yr_lead2 prec_yr_lead3 temp_yr_lead3 prec_yr_lead4 temp_yr_lead4 prec_yr_lead5 temp_yr_lead5 i.ncountry c.year i.ncountry#c.pow_year (pm25_yr_t0 pm25_yr_lead1 pm25_yr_lead2 pm25_yr_lead3 pm25_yr_lead4 pm25_yr_lead5 = dust_dry_stat_predict_lag0 dust_dry_sim_predict_lead1 dust_dry_sim_predict_lead2 dust_dry_sim_predict_lead3 dust_dry_sim_predict_lead4 dust_dry_sim_predict_lead5), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar 

estimates store model6

esttab model6 model6 model6 model6 model6 model6 using pm25_pwt_sim_lead.csv , cells(b(star fmt(7)) se) stats(N r2, fmt(0 4)) keep(pm25_yr_t0 pm25_yr_lead1 pm25_yr_lead2 pm25_yr_lead3 pm25_yr_lead4 pm25_yr_lead5 prec_yr_t0 temp_yr_t0 prec_yr_lead1 temp_yr_lead1 prec_yr_lead2 temp_yr_lead2 prec_yr_lead3 temp_yr_lead3 prec_yr_lead4 temp_yr_lead4 prec_yr_lead5 temp_yr_lead5) replace plain star(* 0.10 ** 0.05 *** 0.01) transform(pm25_yr_t0 10^-9*@ 10^-9 pm25_yr_lead1 10^-9*@ 10^-9 pm25_yr_lead2 10^-9*@ 10^-9 pm25_yr_lead3 10^-9*@ 10^-9 pm25_yr_lead4 10^-9*@ 10^-9 pm25_yr_lead5 10^-9*@ 10^-9)

esttab model6 using pm25_pwt_backward_response_sim.csv, cells(b(fmt(7)) ci(fmt(7))) keep(pm25_yr_t0 pm25_yr_lead1 pm25_yr_lead2 pm25_yr_lead3 pm25_yr_lead4 pm25_yr_lead5) transform(pm25_yr_t0 5.87e-09*@ 5.87e-09 pm25_yr_lead1 5.87e-09*@ 5.87e-09 pm25_yr_lead2 5.87e-09*@ 5.87e-09 pm25_yr_lead3 5.87e-09*@ 5.87e-09 pm25_yr_lead4 5.87e-09*@ 5.87e-09 pm25_yr_lead5 5.87e-09*@ 5.87e-09) replace plain

//mpd

eststo: spatial_hac_iv mpd_growth prec_yr_t0 temp_yr_t0 prec_yr_lead1 temp_yr_lead1 prec_yr_lead2 temp_yr_lead2 prec_yr_lead3 temp_yr_lead3 prec_yr_lead4 temp_yr_lead4 prec_yr_lead5 temp_yr_lead5 i.ncountry c.year i.ncountry#c.pow_year (pm25_yr_t0 pm25_yr_lead1 pm25_yr_lead2 pm25_yr_lead3 pm25_yr_lead4 pm25_yr_lead5 = dust_dry_stat_predict_lag0 dust_dry_sim_predict_lead1 dust_dry_sim_predict_lead2 dust_dry_sim_predict_lead3 dust_dry_sim_predict_lead4 dust_dry_sim_predict_lead5), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar 

estimates store model6

esttab model6 model6 model6 model6 model6 model6 using pm25_mpd_sim_lead.csv , cells(b(star fmt(7)) se) stats(N r2, fmt(0 4)) keep(pm25_yr_t0 pm25_yr_lead1 pm25_yr_lead2 pm25_yr_lead3 pm25_yr_lead4 pm25_yr_lead5 prec_yr_t0 temp_yr_t0 prec_yr_lead1 temp_yr_lead1 prec_yr_lead2 temp_yr_lead2 prec_yr_lead3 temp_yr_lead3 prec_yr_lead4 temp_yr_lead4 prec_yr_lead5 temp_yr_lead5) replace plain star(* 0.10 ** 0.05 *** 0.01) transform(pm25_yr_t0 10^-9*@ 10^-9 pm25_yr_lead1 10^-9*@ 10^-9 pm25_yr_lead2 10^-9*@ 10^-9 pm25_yr_lead3 10^-9*@ 10^-9 pm25_yr_lead4 10^-9*@ 10^-9 pm25_yr_lead5 10^-9*@ 10^-9)

esttab model6 using pm25_mpd_backward_response_sim.csv, cells(b(fmt(7)) ci(fmt(7))) keep(pm25_yr_t0 pm25_yr_lead1 pm25_yr_lead2 pm25_yr_lead3 pm25_yr_lead4 pm25_yr_lead5) transform(pm25_yr_t0 5.87e-09*@ 5.87e-09 pm25_yr_lead1 5.87e-09*@ 5.87e-09 pm25_yr_lead2 5.87e-09*@ 5.87e-09 pm25_yr_lead3 5.87e-09*@ 5.87e-09 pm25_yr_lead4 5.87e-09*@ 5.87e-09 pm25_yr_lead5 5.87e-09*@ 5.87e-09) replace plain


//wbdi

eststo: spatial_hac_iv wbdi_growth prec_yr_t0 temp_yr_t0 prec_yr_lead1 temp_yr_lead1 prec_yr_lead2 temp_yr_lead2 prec_yr_lead3 temp_yr_lead3 prec_yr_lead4 temp_yr_lead4 prec_yr_lead5 temp_yr_lead5 i.ncountry c.year i.ncountry#c.pow_year (pm25_yr_t0 pm25_yr_lead1 pm25_yr_lead2 pm25_yr_lead3 pm25_yr_lead4 pm25_yr_lead5 = dust_dry_stat_predict_lag0 dust_dry_sim_predict_lead1 dust_dry_sim_predict_lead2 dust_dry_sim_predict_lead3 dust_dry_sim_predict_lead4 dust_dry_sim_predict_lead5), lat(centroid_lat) lon(centroid_lon) timevar(year) panelvar(ncountry) distcutoff(1000) lagcutoff(5) bartlett disp star dropvar 

estimates store model6

esttab model6 model6 model6 model6 model6 model6 using pm25_wbdi_sim_lead.csv , cells(b(star fmt(7)) se) stats(N r2, fmt(0 4)) keep(pm25_yr_t0 pm25_yr_lead1 pm25_yr_lead2 pm25_yr_lead3 pm25_yr_lead4 pm25_yr_lead5 prec_yr_t0 temp_yr_t0 prec_yr_lead1 temp_yr_lead1 prec_yr_lead2 temp_yr_lead2 prec_yr_lead3 temp_yr_lead3 prec_yr_lead4 temp_yr_lead4 prec_yr_lead5 temp_yr_lead5) replace plain star(* 0.10 ** 0.05 *** 0.01) transform(pm25_yr_t0 10^-9*@ 10^-9 pm25_yr_lead1 10^-9*@ 10^-9 pm25_yr_lead2 10^-9*@ 10^-9 pm25_yr_lead3 10^-9*@ 10^-9 pm25_yr_lead4 10^-9*@ 10^-9 pm25_yr_lead5 10^-9*@ 10^-9)

esttab model6 using pm25_wbdi_backward_response_sim.csv, cells(b(fmt(7)) ci(fmt(7))) keep(pm25_yr_t0 pm25_yr_lead1 pm25_yr_lead2 pm25_yr_lead3 pm25_yr_lead4 pm25_yr_lead5) transform(pm25_yr_t0 5.87e-09*@ 5.87e-09 pm25_yr_lead1 5.87e-09*@ 5.87e-09 pm25_yr_lead2 5.87e-09*@ 5.87e-09 pm25_yr_lead3 5.87e-09*@ 5.87e-09 pm25_yr_lead4 5.87e-09*@ 5.87e-09 pm25_yr_lead5 5.87e-09*@ 5.87e-09) replace plain

clear all
exit