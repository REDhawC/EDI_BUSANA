$title Production Planning Problem (lot-sizing problem)
* Douglas Alem version *
$ontext
This code refers to a numerical example of the Production Planning Problem proposed in slide 24 of lecture 4
$offtext

$eolcom //

// Basic options - the most important is the relative optimality gap (for MIP problems only!)
 Options reslim = 60, iterlim = 1e7, limrow = 1000, limcol = 1000, optcr = 0.00;

 Sets
 i         products                        /prod1*prod5/
 t         periods                         /time1*time4/
 ;
 Alias(t,tt); // Alias will make a copy of your set t

 Table c(i,t) unit cost per product i in period t ($)
          time1          time2       time3       time4
  prod1   298.00         299.00      308.00      318.00
  prod2   370.00         375.00      376.00      379.00
  prod3   441.00         443.00      447.00      449.00
  prod4   130.00         131.00      134.00      141.00
  prod5    63.00          67.00       73.00       77.00
  ;
 // Assumption: inventory costs are 0.1% of the corresponding production costs
 Parameter h(i,t) unit inventory cost per product i in period t ($);
           h(i,t) = 0.001*c(i,t);
 // Assumption: inventory costs are 100 times the corresponding production costs
 Parameter f(i,t) setup cost per product i in period t ($);
           f(i,t) = 100*c(i,t);
 // There is a fine of 1,000 per unit of backlog
 Parameter h_(i) unit backlogging cost per product i;
           h_(i)=10000;

 Table d(i,t) demand for item i in period t ($)
             time1      time2       time3       time4
  prod1      75.000     177.000     133.000      95.000
  prod2      94.000      83.000     102.000     179.000
  prod3      60.000     125.000     200.000     137.000
  prod4     199.000     165.000      69.000     146.000
  prod5      74.000      87.000     151.000     115.000
  ;

 Parameter p(i) processing time of item i (minutes)
 /prod1 28
  prod2 30
  prod3 47
  prod4 19
  prod5 13
 /;

 Table s(i,t) setup time of item i in period t (minutes)
            time1      time2      time3        time4
  Prod1      50.000     50.000     50.000       50.000
  Prod2      90.000     90.000     90.000       90.000
  Prod3     100.000    100.000    100.000      100.000
  Prod4      30.000     30.000     30.000       30.000
  Prod5      20.000     20.000     20.000       20.000;

 Parameter cap(t) production capacity of period t (minutes);
           cap('time1') = 17000;
           cap('time2') = 17000;
           cap('time3') = 17000;
           cap('time4') = 18000;

 Parameter bigM(i) big number;
  bigM(i) = sum(t,d(i,t));

 Variables
  x(i,t)         Quantity of item type i produced in period t
  In(i,t)        Inventory of item type i in period t
  I_(i,t)        Backlogging of item type i in period t
  y(i,t)         Set-up variable
  of             Objective function value

 Binary variables   y;
 Positive variables x, In, I_;
 I_.up(i,'time4')=0; // The backlog in the last time period must be zero!

 Equations
  obj_func,
  inv_balance,
  regular_cap,
  setup
  ;

  obj_func..         OF =E= sum((i,t),c(i,t)*X(i,t)) + sum((i,t),f(i,t)*y(i,t)) + sum((i,t),h(i,t)*In(i,t)+h_(i)*I_(i,t));
  inv_balance(i,t)..            x(i,t) + In(i,t-1) + I_(i,t) =e= d(i,t) + In(i,t) +I_(i,t-1);
  regular_cap(t)..        sum(i,p(i)*x(i,t) + s(i,t)*y(i,t)) =l= cap(t);
  setup(i,t)..                                        x(i,t) =l= bigM(i)*y(i,t);

 Model Lotsizing
  /
  obj_func,
  inv_balance,
  regular_cap,
  setup,
  /;

 // Here, we use MIP (Mixed-Integer Programming) because we have to solve an optimisation model that contains a binary decision variable (y_{it})
 // The algorithm that solves an MIP is quite different from the one that solves an LP
 Solve Lotsizing using MIP minimizing of;
 Scalar z_mip; z_mip=OF.l; // This is the optimal value!

 // RMIP (Relaxed MIP) solves the relaxation of any integer problem (minimization problem: lower bound);
 Solve Lotsizing using RMIP minimizing of;
 Scalar z_lp; z_lp=OF.l;// This is the linear programming relaxation value!

 // Heuristic procedure for the lot-sizing problem (minimization problem: upper bound)
 Scalar count /1/;
 For(count=1 to card(t) by 1,
  Loop(t,
       y.prior(i,t)$(ord(t)=count)=0;
       y.prior(i,t)$(ord(t)>count)=+inf;
       );
  Solve Lotsizing using MIP minimizing of;
   Loop(t,y.fx(i,t)$(ord(t)=count)=y.l(i,t);
     );
    );
 Scalar z_h; z_h=OF.L; // This is the heuristic solution

 Scalar gap_integral; gap_integral = (z_mip-z_lp)*100/z_mip;
 Scalar gap_primal;   gap_primal   = (z_h-z_mip)*100/z_mip;
 Scalar gap_duality;  gap_duality  = (z_h-z_lp)*100/z_h;

 Display z_mip, z_lp, z_h, gap_integral, gap_primal, gap_duality;

$onText
The results show that the Linear Programming relaxation is poor and the heuristic
solution has an even worse performance in terms of gaps!
$offtext


