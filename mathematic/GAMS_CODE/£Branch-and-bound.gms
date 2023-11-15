Option optcr=0.00;

$ontext

This code solves the B&B example of the slides

$offtext

*This command serves to include a list of options for the CPLEX optimisation package
File fcpx Cplex Option File/cplex.opt/;

Positive variables x1,x2;
Free variable z;

* Let's solve the initial node - the LP relaxation!
equations of,eq1,eq2;

of..            z =e= 3*x1 + 4*x2;
eq1.. 2*x1 +   x2 =l= 6;
eq2.. 2*x1 + 3*x2 =l= 9;

Model node0 /of,eq1,eq2/;
Solve node0 using lp maximizing z;
* The solution is x1 = 2.25 and x2 = 1.5 with z(0) = 12.75
* Notice that x2 is farther from an integral value
* We know that, in any integer programming solution, x2 must be
* either an integer <=1 or an integer >= 2. Thus, let us include
* constraints to limit its fractional value:

* Iteration 1
equations eq3, eq4;

eq3.. x2 =l= 1;
eq4.. x2 =g= 2;

Model node1 /of,eq1,eq2,eq3/;
Model node2 /of,eq1,eq2,eq4/;

Solve node1 using lp maximizing z;
* Solution x1 = 2.5 and x2 = 1 with z(1) = 11.5

Solve node2 using lp maximizing z;
* Solution x1 = 1.5 and x2 = 2 with z(2) = 12.5

$ontext

* Notice that node2 has a larger objective function value (more nearly optimal)
* Indeed, 12.5 > 11.5
* Thus, let's us branch from node2
* We know that, in any integer programming solution, x1 must be
* either an integer <= 1 or an integer >= 2. Thus, let us include
* constraints to limit its fractional value:

equations eq5, eq6;

eq5.. x1 =l= 1;
eq6.. x1 =g= 2;

Model node3 /of,eq1,eq2,eq4,eq5/;
Model node4 /of,eq1,eq2,eq4,eq6/;

Solve node3 using lp maximizing z;
* Solution x1 = 1 and x2 = 2.33 with z(3) = 12.33

Solve node4 using lp maximizing z;
* INFEASIBLE Solution!

* Notice that node4 results in an infeasible solution
* Thus, we can bound this node!
* We know that, in any integer programming solution, x2 must be
* either an integer <= 2 or an integer >= 3. Thus, let us include
* constraints to limit its fractional value:

equations eq7, eq8;

eq7.. x2 =l= 2;
eq8.. x2 =g= 3;

Model node5 /of,eq1,eq2,eq4,eq5,eq7/;
Model node6 /of,eq1,eq2,eq4,eq5,eq8/;

Solve node5 using lp maximizing z;
* Solution x1 = 1 and x2 = 2 with z(5) = 11

Solve node6 using lp maximizing z;
* Solution x1 = 0 and x2 = 3 with z(6) = 12

************ using the B&B method directly *************************************
Integer variables x1i,x2i;
equations ofi,eq1i,eq2i;

ofi..            z =e= 3*x1i + 4*x2i;
eq1i.. 2*x1i +   x2i =l= 6;
eq2i.. 2*x1i + 3*x2i =l= 9;

Model mip1 /ofi,eq1i,eq2i/;

Solve mip1 using MIP maximizing z;
$offtext