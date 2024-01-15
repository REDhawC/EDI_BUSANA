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
week1 2000  # updated capacity for week 1
week2 3000
week3 3000
week4 1000
/;

Parameter max_inventory / 1000 /;  # max inventory limit

Variables
x(t) production level,
inv(t) inventory level,
z objective value
;

Positive variables x, inv;  # changed from 'Postive' to 'Positive'
Free variable z;

Equations
ObjFunction objective function 
demand(t) demand constraint  # swapped labels for clarity
capacity(t) capacity constraint  # swapped labels for clarity
inventory_limit(t) inventory constraint
;

ObjFunction.. z =e= sum(t, c(t)*x(t) + h(t)*inv(t));
demand(t).. x(t) + inv(t-1) =e= d(t) + inv(t);
capacity(t).. x(t) =l= cap(t);
inventory_limit(t).. inv(t) =l= max_inventory;  # added inventory limit constraint

Model mobile /all/;
Solve mobile using LP minimizing z;
Display x.l, inv.l;  # removed x.m and inv.m as they're not necessary for displaying results
