* OSEMOSYS_RES.GMS - create results in file SelResults.CSV
*
* OSEMOSYS 2011.07.07 conversion to GAMS by Ken Noble, Noble-Soft Systems - August 2012
* OSEMOSYS 2016.08.01 update by Thorsten Burandt, Konstantin Löffler and Karlo Hainsch, TU Berlin (Workgroup for Infrastructure Policy) - October 2017
*
FILE ANT /SelResults.CSV/;
PUT ANT; ANT.ND=6; ANT.PW=400; ANT.PC=5;
* Total emissions (by region, emission)
loop((r,e),
put / "ModelPeriodEmissions",r.TL,e.TL,ModelPeriodEmissions.L(e,r);
);
put /;
* Total cost (by region)
loop(r,
put / "ModelPeriodCostByRegion",r.TL,ModelPeriodCostByRegion.L(r);
);
put /;
* Accumulated Annual Demand (by region, fuel, timeslice, year)
loop((r,f)$(sum(y, AccumulatedAnnualDemand(r,f,y)) > 0),
put / "AccumulatedAnnualDemand",r.TL,f.TL;
loop(y, put AccumulatedAnnualDemand(r,f,y));
);
put /;
* Demand by TimeSlice (by region, fuel, timeslice, year)
loop((r,f)$(sum(y, SpecifiedAnnualDemand(r,f,y)) > 0),
loop(l,
put / "DemandByTimeSlice",r.TL,f.TL,l.TL;
loop(y, put Demand.L(r,l,f,y));
);
);
put /;
* Fuel Production by TimeSlice (by region, fuel, timeslice, year)
loop((r,f,l),
put / "FuelProductionByTimeSlice",r.TL,f.TL,l.TL;
loop(y, put Production.L(r,l,f,y));
);
put /;
* Total Annual Capacity (by region, technology, year)
loop((r,t),
put / "TotalAnnualCapacity",r.TL,t.TL;
loop(y, put TotalCapacityAnnual.L(r,t,y));
);
put /;
* New Annual Capacity (by region, technology, year)
loop((r,t),
put / "NewAnnualCapacity",r.TL,t.TL;
loop(y, put NewCapacity.L(r,t,y));
);
put /;
* Annual Technology Production (by region, technology, fuel, year)
loop((r,t,f)$(sum((y,m), OutputActivityRatio(r,t,f,m,y)) > 0),
put / "AnnualProductionByTechnology",r.TL,t.TL,f.TL;
loop(y, put ProductionByTechnologyAnnual.L(r,t,f,y));
);
put /;
* Annual Technology Use (by region, technology, fuel, year)
loop((r,t,f)$(sum((y,m), InputActivityRatio(r,t,f,m,y)) > 0),
put / "AnnualUseByTechnology",r.TL,t.TL,f.TL;
loop(y, put UseByTechnologyAnnual.L(r,t,f,y));
);
put /;
* Technology Production in each TimeSlice (by region, technology, fuel, timeslice, year)
loop((r,t,f)$(sum((y,m), OutputActivityRatio(r,t,f,m,y)) > 0),
loop(l,
put / "ProductionByTechnologyByTimeSlice",r.TL,t.TL,f.TL,l.TL;
loop(y, put ProductionByTechnology.L(r,l,t,f,y));
);
);
put /;
* Technology Use in each TimeSlice (by region, technology, fuel, timeslice, year)
loop((r,t,f)$(sum((y,m), InputActivityRatio(r,t,f,m,y)) > 0),
loop(l,
put / "UseByTechnologyByTimeSlice",r.TL,t.TL,f.TL,l.TL;
loop(y, put UseByTechnology.L(r,l,t,f,y));
);
);
put /;
* Total Annual Emissions (by region, emission, year)
loop((r,e),
put / "AnnualEmissions",r.TL,e.TL;
loop(y, put AnnualEmissions.L(r,e,y));
);
put /;
* Annual Emissions (by region, technology, emission, year)
loop((r,t,e)$(sum((y,m), EmissionActivityRatio(r,t,e,m,y)) > 0),
put / "AnnualEmissionsByTechnology",r.TL,t.TL,e.TL;
loop(y, put AnnualTechnologyEmission.L(r,t,e,y));
);
put /;
PUTCLOSE ANT;
