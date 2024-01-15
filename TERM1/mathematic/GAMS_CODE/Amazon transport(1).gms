$Ontext
How to best move a given mobile phone from Amazon distribution centres to demand zones
**Douglas Alem version**
$Offtext

Option optcr = 0.00;

*This command serves to include a list of options for the CPLEX optimisation package
File fcpx Cplex OPTION FILE /cplex.opt/;

Sets
i DCs          /Gourock,Bathgate,Dunfermline,Edinburgh,Portlethen/
j Demand zones /Perth,Dundee/
;

Parameter cap(i) weekly capacity of each DC (units)
/
Gourock     150
Bathgate    150
Dunfermline 100
Edinburgh   200
Portlethen  400
/
;

Parameter d(j) demand of units required
/
Perth  600
Dundee 600
/
;

Table distance(i,j) distance in miles 
             Perth    Dundee
Gourock      106      114
Bathgate      58       70
Dunfermline   28.2     41.5
Edinburgh     43.8     63
Portlethen    76.3     61
;

Scalar mile per mile shipping cost in pounds /3/;
Scalar penalty penalty for unmet demand per unit /500/;  

Parameter cost(i,j) shipping cost from i to j;
 cost(i,j) = distance(i,j)*mile;

Variables
z      total cost
x(i,j) quantity of mobile phones shipped from i to j
u(j)   unmet demand in each zone
Positive Variables x, u;

Equations
of       objective function 
constr1  capacity constraint
constr2  demand constraint
;

of..    z =e= sum((i,j), cost(i,j)*x(i,j)) + sum(j, penalty*u(j));
constr1(i)..  sum(j, x(i,j)) =l= cap(i);
constr2(j)..  sum(i, x(i,j)) + u(j) =e= d(j);

Model transport /of,constr1,constr2/;

**Solving the model :-) **

Solve transport using mip minimizing z;
Display x.l, x.m, u.l;




