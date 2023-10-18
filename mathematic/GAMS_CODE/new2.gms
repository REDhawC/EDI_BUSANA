$Ontext
This code refers to the production planning problem Computer lab 13/10/2023
$Offtext


Set t weeks /week1*week4/;

Parameter c(t) production cost
/
week1 79
week2 80
week3 81
week4 82
/;

Parameter h(t) holding cost;
h(t) = 0.01 * c(t);

Parameter d(t) demand
/
week1 2500
week2 2500
week3 2500
week4 2500
/;

Parameter cap(t) capacity
/
week1 3000
week2 3000
week3 3000
week4 1500
/;


Variables
x(t) produciton level,
inv(t) inventory level,
z objective value
;

*Postive -> non-Negative Variable
Positive variables  x,inv;
Free variable z;

Equations
ObjFunction       objective function 
demand(t)  capacity constraint
capacity(t)  demand constraint
inventory_limit(t) inventory constraint
;

ObjFunction.. z =e= sum(t,c(t)*x(t) + h(t)*inv(t));
demand(t)..x(t) + inv(t-1) =e= d(t) + inv(t);
capacity(t)..x(t) =l= cap(t);
inventory_limit(t).. inv(t) =l= 1000;
* =l= -> 'larger' than or equal to

Model mobile /all/;
* Model mobile /ObjFunction，demand,capacity/;
Solve mobile using LP minimizing z;
Display x.l, x.m,inv.l,inv.m;
*x.l -> primal ; x.m -> marginal cost