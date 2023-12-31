$ontext
A Location-Allocation Problem for Disaster Preparedness in Brazil
$offtext
$eolcom //
 Option optcr = 0.00;

 Set i  warehouses  /AC,AL,AP,AM,BA,CE,ES,GO,MA,MT,MS,MG,PA,PB,PR,PE,PI,RJ,RN,RS,RO,RR,SC,SP,SE,TO/;
 Set j  demand zoes /AC,AL,AP,AM,BA,CE,ES,GO,MA,MT,MS,MG,PA,PB,PR,PE,PI,RJ,RN,RS,RO,RR,SC,SP,SE,TO/;
 Alias(j,jj); // This creates an identical copy of set j

 Parameter d(j) estimated number of victims' needs per year (in units of relief aid items)
 /AC  21050.000,    AL  23339.000,    AP   1186.000,    AM 169946.000
  BA  64799.000,    CE  85137.000,    ES  63471.000,    GO   2546.000
  MA 236059.000,    MT   5741.000,    MS   8808.000,    MG  85236.000
  PA  52595.000,    PB  39015.000,    PR  56465.000,    PE 122130.000
  PI  76199.000,    RJ  97111.000,    RN  33141.000,    RS 154597.000
  RO  20001.000,    RR    456.000,    SC 189100.000,    SP  51271.000
  SE   5204.000,    TO    820.000
 /;

 Parameter cap(i) yearly capacity of each warehouse located at i (units of relief aid items);
  cap(i) = 250000;

 Parameter fixed_cost(i) fixed cost for establishing & operating a warehouse at location i (US$ dollars);
  fixed_cost(i) = 40000;

 Table distance(i,j) road distances between warehouse & demand zones
               AC          AL          AP          AM          BA          CE          ES          GO          MA          MT          MS          MG          PA          PB          PR          PE          PI          RJ          RN          RS           RO
         AC                4989.770    4473.070    1401.560    4540.370    5212.750    4063.920    2896.520    4238.210    1966.300    2668.300    3553.810    3990.120    5347.330    3665.110    5231.760    4148.440    3890.150    5516.090    4404.200     514.470
         AL    4992.700                2844.120    5366.280     580.310     945.760    1617.580    2093.380    1568.110    3023.530    2821.940    1802.250    2043.470     375.760    2785.680     260.180    1137.950    2078.110     544.520    3514.790    4479.180
         AP    4476.350    2843.780                3072.590    2930.000    2098.920    3528.000    2318.530    1138.920    2341.230    3045.360    3016.210     525.720    2848.510    3636.020    2831.770    1471.810    3442.620    2605.500    4365.140    3959.270
         AM    1405.910    5370.740    3072.210                4921.330    5593.710    4444.880    3277.490    4619.170    2347.260    3049.260    3934.780    4371.080    5728.290    4046.080    5612.720    4529.400    4271.110    5897.060    4785.160     888.840
         BA    4544.220     599.680    2930.180    4917.800                1205.350    1169.390    1644.900    1654.170    2575.050    2373.460    1353.770    2129.530     957.240    2337.200     841.660    1224.010    1629.630    1126.000    3066.310    4030.700
         CE    5213.530    1030.320    2101.080    5587.110    1205.460                2175.020    2314.210     897.560    3244.360    3152.790    2327.800    1537.850     668.740    3311.230     772.880     592.070    2603.660     516.240    4040.340    4700.010
         ES    4071.030    1617.420    3530.080    4444.610    1168.410    2172.230                1389.800    2621.050    2101.860    1944.350     517.390    3096.420    1974.980    1348.280    1859.400    2190.900     517.060    2143.740    2077.390    3557.510
         GO    2900.150    2093.990    2319.470    3273.720    1644.590    2316.970    1388.750                2017.420     930.980     839.410     876.960    1963.280    2451.550    1320.220    2335.970    1881.230    1338.280    2620.310    2049.330    2386.620
         MA    4246.420    1569.930    1139.750    4620.000    1656.150     896.520    2625.720    2018.080                2695.310    2852.840    2778.500     576.530    1555.600    3335.570    1659.730     434.570    3054.350    1403.090    4064.680    3732.900
         MT    1971.330    3026.770    2341.480    2344.910    2577.370    3249.750    2100.910     933.520    2696.340                 705.290    1590.810    2499.270    3384.330    1702.110    3268.750    2546.240    1927.150    3553.090    2441.200    1457.810
         MS    2671.740    3370.150    3042.070    3045.310    2920.750    3155.080    1951.410     838.850    2851.630     702.570                1573.930    2797.500    3727.710    1000.200    3612.130    2719.340    1441.250    3896.470    1739.290    2158.220
         MG    3558.000    1803.110    3017.490    3931.570    1353.710    2329.630     517.000     877.210    2778.450    1588.830    1573.480                2661.300    2160.670     987.780    2045.100    2348.290     438.750    2329.430    1716.900    3044.480
         PA    3995.210    2044.320     526.340    4368.790    2130.540    1536.080    3100.110    1961.580     576.080    2495.300    2796.350    2659.260                2049.050    3279.080    2032.310     908.970    3085.680    2042.660    4008.190    3481.690
         PB    5337.300     374.220    2851.270    5710.880     924.910     668.730    1962.180    2437.980    1575.610    3368.130    3166.540    2146.850    2050.620                3130.280     116.770    1145.100    2422.710     180.120    3859.390    4823.780
         PR    3668.040    2793.630    3639.690    4041.620    2344.230    3320.150    1354.490    1323.150    3337.640    1698.870    1000.450     997.410    3283.500    3151.190                3035.610    3031.850     844.330    3319.950     742.570    3154.520
         PE    5221.110     258.030    2832.850    5594.690     808.720     773.290    1845.990    2321.790    1680.170    3251.940    3050.340    2030.660    2032.200     115.920    3014.090                1126.680    2306.520     284.680    3743.200    4707.590
         PI    4154.390    1138.200    1470.870    4527.960    1224.420     592.220    2193.990    1880.980     432.280    2544.090    2719.560    2346.770     907.640    1142.930    3033.900    1126.180                2622.620    1099.110    3763.010    3640.870
         RJ    3891.930    2077.150    3445.560    4265.510    1627.750    2603.660     556.490    1340.090    3052.480    1922.760    1434.580     439.510    3089.370    2434.710     838.500    2319.130    2622.330                2603.470    1567.610    3378.410
         RN    5504.980     541.900    2625.800    5878.560    1092.590     515.410    2129.860    2605.660    1422.290    3535.810    3334.220    2314.530    2062.570     180.310    3297.960     284.450    1115.930    2590.390                4027.070    4991.460
         RS    4091.820    3521.050    4367.100    4465.400    3071.640    4047.560    2081.900    2050.560    4065.050    2122.650    1424.230    1724.820    4010.910    3878.600     741.290    3763.030    3759.260    1571.740    4047.370                3578.300
         RO     517.300    4482.070    3959.300     887.790    4032.670    4705.040    3556.210    2388.820    3730.500    1458.590    2160.590    3046.110    3482.410    4839.630    3157.410    4724.050    3640.730    3382.450    5008.390    3896.490
         RR    2185.960    6150.780    2295.620     782.200    5701.380    6373.760    5224.920    4057.530    5399.210    3127.310    3829.300    4714.820    2806.590    6508.340    4826.120    6392.760    5309.440    5051.160    6677.100    5565.200    1668.880
         SC    3968.250    3081.870    3927.930    4341.820    2632.470    3608.380    1642.720    1611.380    3625.870    1999.080    1300.660    1285.650    3571.730    3439.430     302.120    3323.850    3320.080    1132.560    3608.190     456.720    3454.730
         SP    3503.390    2385.420    3256.410    3876.960    1936.010    2911.930     946.270     939.860    2954.350    1534.220    1009.310     589.190    2900.220    2742.970     404.440    2627.400    2648.570     436.110    2911.740    1133.550    2989.860
         SE    4737.270     268.980    2836.910    5110.850     324.880    1112.080    1362.150    1837.950    1560.900    2768.100    2566.510    1546.820    2036.260     626.530    2530.250     510.960    1130.750    1822.680     795.300    3259.360    4223.750
         TO    3474.320    1892.100    1562.860    3847.900    1442.700    1699.650    2037.400     827.920    1260.810    1505.150    1662.690    1525.600    1206.670    2249.660    2145.420    2134.080    1110.710    1952.010    2057.900    2874.530    2960.800

 +                   RR          SC          SP          SE          TO

         AC    2183.020    3964.370    3499.560    4733.880    3469.970
         AL    6147.740    3074.970    2386.860     270.600    1890.610
         AP    2295.510    3925.310    3252.230    2837.340    1561.090
         AM     782.160    4345.340    3880.520    5114.850    3850.930
         BA    5699.260    2626.490    1938.380     343.790    1442.130
         CE    6368.570    3600.520    2912.410    1112.790    1698.690
         ES    5226.070    1637.560     940.100    1361.530    2038.650
         GO    4055.180    1609.510     936.430    1838.100     828.040
         MA    5401.460    3624.860    2951.780    1563.490    1260.640
         MT    3126.370    2001.370    1536.550    2770.880    1506.960
         MS    3826.770    1299.460    1009.110    3114.260    1662.250
         MG    4713.030    1277.070     588.960    1547.220    1526.060
         PA    2807.200    3568.370    2895.290    2037.880    1204.150
         PB    6492.330    3419.570    2731.460     615.190    2235.210
         PR    4823.070     302.740     401.540    2537.740    2148.260
         PE    6376.140    3303.370    2615.270     499.000    2119.020
         PI    5309.420    3323.190    2650.110    1131.760    1109.420
         RJ    5046.960    1127.790     430.330    1821.260    1954.130
         RN    6660.020    3587.250    2899.140     782.880    2402.890
         RS    5246.850     456.970    1128.950    3265.160    2875.670
         RO    1669.250    3456.670    2991.850    4226.180    2962.260
         RR                5125.380    4660.560    5894.890    4630.970
         SC    5123.280                 689.780    2825.980    2436.490
         SP    4658.420     693.730                2129.530    1764.980
         SE    5892.310    2819.540    2131.430                1635.180
         TO    4629.360    2434.700    1761.630    1636.210
         ;

 Scalar fuel diesel cost (US$) /1/;
 Scalar efficiency efficiency (km per litre) /5/;
 Parameter c(i,j) shipping cost from i to j;
  c(i,j) = (fuel/efficiency)*distance(i,j);
Scalar investment investment level /1000000/; // Plan A
* Scalar investment investment level /500000/; // Plan B
Scalar max_number_depots maximum number of depots to set-up /20/; // Plan A
* Scalar max_number_depots maximum number of depots to set-up /15/; // Plan B

 Variables
  Z      Optimal value
  Y(i)   Binary variable to indicate whether warehouse is set-up at location i
  X(i,j) quantity of relief aid items shipped from i to j
 Positive variables X;
 Binary variable Y;
 Equations
  of       objective function
  constr1  capacity constraint & logical constraint
  constr2  victims' needs constraint
  constr3  investment level
  constr4  maximum number of warehouses to set-up
  constr5 fairness
;

  of..  z =e= sum((i,j),x(i,j));
  constr1(i)..  sum(j, X(i,j)) =l= cap(i)*Y(i);
  constr2(j)..  sum(i,X(i,j)) =l= d(j);
  constr3..  sum(i,fixed_cost(i)*Y(i)) + sum((i, j),c(i,j)*X(i,j))  =l= investment;
  constr4..  sum(i,Y(i)) =l= max_number_depots;
  constr5(j)..  sum(i,X(i,j)) =g= 0.6*d(j);

 Model LocationAllocation /of,constr1,constr2,constr3,constr4/;
 Parameter service_rate(j); Scalar global; // Based on the output
 Solve LocationAllocation using MIP  maximizing z;
  service_rate(j)$(d(j)<>0) = (sum(i,X.l(i,j))/d(j))*100;
  service_rate(j)$(d(j)<>0 and (sum(i,X.l(i,j))=0)) = eps;
  service_rate(j)$(d(j)=0) = 1;
  global = (1/card(j))*sum(j,service_rate(j));
  Display Y.l, X.l, Z.l,service_rate, global;
