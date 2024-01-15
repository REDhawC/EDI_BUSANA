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
Gourock     1500
Bathgate    1500
Dunfermline  900
Edinburgh   2100
Portlethen  7000
/
;

Parameter d(j) demand of units required
/
Perth  4000
Dundee 6000
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

Parameter cost(i,j) shipping cost from i to j;
 cost(i,j) = distance(i,j)*mile;

Variables
z      total cost
x(i,j) quantity of mobile phones shipped from i to j
Positive variables x;

Equations
of       objective function 
constr1  capacity constraint
constr2  demand constraint
;

of..                       z =e= sum((i,j), cost(i,j)*X(i,j));
constr1(i)..  sum(j, x(i,j)) =l= cap(i);
constr2(j)..  sum(i, x(i,j)) =g= d(j);

Model transport /of,constr1,constr2/;

**Solving the model :-) **

Solve transport using mip minimizing z;
Display x.l, x.m;




