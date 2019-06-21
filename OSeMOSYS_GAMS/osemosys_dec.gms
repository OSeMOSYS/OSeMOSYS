* OSEMOSYS_DEC.GMS - declarations for sets, parameters, variables (but not equations)
*
* OSEMOSYS 2011.07.07 conversion to GAMS by Ken Noble, Noble-Soft Systems - August 2012
* OSEMOSYS 2017.11.08 update by Thorsten Burandt, Konstantin Löffler and Karlo Hainsch, TU Berlin (Workgroup for Infrastructure Policy) - October 2017
*
* OSEMOSYS 2017.11.08
* Open Source energy Modeling SYStem
*
* ============================================================================
*
* #########################################
* ######################## Model Definition #############
* #########################################
*
* ##############
* # Sets #
* ##############
*
set YEAR;
alias (y,yy,YEAR);
set TECHNOLOGY;
alias (t,TECHNOLOGY)
set TIMESLICE;
alias (l,TIMESLICE);
set FUEL;
alias (f,FUEL);
set EMISSION;
alias (e,EMISSION);
set MODE_OF_OPERATION;
alias (m,MODE_OF_OPERATION);
set REGION;
alias (r,REGION,rr);
set SEASON;
alias (ls,SEASON,lsls);
set DAYTYPE;
alias (ld,DAYTYPE,ldld);
set DAILYTIMEBRACKET;
alias (lh,DAILYTIMEBRACKET,lhlh);
set STORAGE;
alias (s,STORAGE);

*
* ####################
* # Parameters #
* ####################
*
* ####### Global #############
*
parameter YearSplit(TIMESLICE,YEAR);
parameter DiscountRate(REGION);
parameter DaySplit(YEAR,DAILYTIMEBRACKET);
parameter Conversionls(TIMESLICE,SEASON);
parameter Conversionld(TIMESLICE,DAYTYPE);
parameter Conversionlh(TIMESLICE,DAILYTIMEBRACKET);
parameter DaysInDayType(YEAR,SEASON,DAYTYPE);
parameter TradeRoute(REGION,rr,FUEL,YEAR);
parameter DepreciationMethod(REGION);
*
* ####### Demands #############
*
parameter SpecifiedAnnualDemand(REGION,FUEL,YEAR);
parameter SpecifiedDemandProfile(REGION,FUEL,TIMESLICE,YEAR);
parameter AccumulatedAnnualDemand(REGION,FUEL,YEAR);
*
* ######## Performance #############
*
parameter CapacityToActivityUnit(REGION,TECHNOLOGY);
parameter CapacityFactor(REGION,TECHNOLOGY,TIMESLICE,YEAR);
parameter AvailabilityFactor(REGION,TECHNOLOGY,YEAR);
parameter OperationalLife(REGION,TECHNOLOGY);
parameter ResidualCapacity(REGION,TECHNOLOGY,YEAR);
parameter InputActivityRatio(REGION,TECHNOLOGY,FUEL,MODE_OF_OPERATION,YEAR);
parameter OutputActivityRatio(REGION,TECHNOLOGY,FUEL,MODE_OF_OPERATION,YEAR);
*
* ######## Technology Costs #############
*
parameter CapitalCost(REGION,TECHNOLOGY,YEAR);
parameter VariableCost(REGION,TECHNOLOGY,MODE_OF_OPERATION,YEAR);
parameter FixedCost(REGION,TECHNOLOGY,YEAR);
*
* ######## Storage Parameters #############
*
parameter TechnologyToStorage(REGION,MODE_OF_OPERATION,TECHNOLOGY,STORAGE);
parameter TechnologyFromStorage(REGION,MODE_OF_OPERATION,TECHNOLOGY,STORAGE);
parameter StorageLevelStart(REGION,STORAGE);
parameter StorageMaxChargeRate(REGION,STORAGE);
parameter StorageMaxDischargeRate(REGION,STORAGE);
parameter MinStorageCharge(REGION,STORAGE,YEAR);
parameter OperationalLifeStorage(REGION,STORAGE);
parameter CapitalCostStorage(REGION,STORAGE,YEAR);
parameter ResidualStorageCapacity(REGION,STORAGE,YEAR);
*
* ######## Capacity Constraints #############
*
parameter CapacityOfOneTechnologyUnit(REGION,TECHNOLOGY,YEAR);
parameter TotalAnnualMaxCapacity(REGION,TECHNOLOGY,YEAR);
parameter TotalAnnualMinCapacity(REGION,TECHNOLOGY,YEAR);
*
* ######## Investment Constraints #############
*
parameter TotalAnnualMaxCapacityInvestment(REGION,TECHNOLOGY,YEAR);
parameter TotalAnnualMinCapacityInvestment(REGION,TECHNOLOGY,YEAR);
*
* ######## Activity Constraints #############
*
parameter TotalTechnologyAnnualActivityUpperLimit(REGION,TECHNOLOGY,YEAR);
parameter TotalTechnologyAnnualActivityLowerLimit(REGION,TECHNOLOGY,YEAR);
parameter TotalTechnologyModelPeriodActivityUpperLimit(REGION,TECHNOLOGY);
parameter TotalTechnologyModelPeriodActivityLowerLimit(REGION,TECHNOLOGY);
*
* ######## Reserve Margin ############
*
parameter ReserveMarginTagTechnology(REGION,TECHNOLOGY,YEAR);
parameter ReserveMarginTagFuel(REGION,FUEL,YEAR);
parameter ReserveMargin(REGION,YEAR);
*
* ######## RE Generation Target ############
*
parameter RETagTechnology(REGION,TECHNOLOGY,YEAR);
parameter RETagFuel(REGION,FUEL,YEAR);
parameter REMinProductionTarget(REGION,YEAR);
*
* ######### Emissions & Penalties #############
*
parameter EmissionActivityRatio(REGION,TECHNOLOGY,EMISSION,MODE_OF_OPERATION,YEAR);
parameter EmissionsPenalty(REGION,EMISSION,YEAR);
parameter AnnualExogenousEmission(REGION,EMISSION,YEAR);
parameter AnnualEmissionLimit(REGION,EMISSION,YEAR);
parameter ModelPeriodExogenousEmission(REGION,EMISSION);
parameter ModelPeriodEmissionLimit(REGION,EMISSION);

*
* #####################
* # Model Variables #
* #####################
*
* ############### Demands ############
*
positive variable RateOfDemand(REGION,TIMESLICE,FUEL,YEAR);
positive variable Demand(REGION,TIMESLICE,FUEL,YEAR);
*
* ############### Storage ###########
*
free variable  RateOfStorageCharge(REGION,STORAGE,SEASON,DAYTYPE,DAILYTIMEBRACKET,YEAR);
free variable  RateOfStorageDischarge(REGION,STORAGE,SEASON,DAYTYPE,DAILYTIMEBRACKET,YEAR);
free variable  NetChargeWithinYear(REGION,STORAGE,SEASON,DAYTYPE,DAILYTIMEBRACKET,YEAR);
free variable  NetChargeWithinDay(REGION,STORAGE,SEASON,DAYTYPE,DAILYTIMEBRACKET,YEAR);
positive variable StorageLevelYearStart(REGION,STORAGE,YEAR);
positive variable StorageLevelYearFinish(REGION,STORAGE,YEAR);
positive variable StorageLevelSeasonStart(REGION,STORAGE,SEASON,YEAR);
positive variable StorageLevelDayTypeStart(REGION,STORAGE,SEASON,DAYTYPE,YEAR);
positive variable StorageLevelDayTypeFinish(REGION,STORAGE,SEASON,DAYTYPE,YEAR);
positive variable StorageLowerLimit(REGION,STORAGE,YEAR);
positive variable StorageUpperLimit(REGION,STORAGE,YEAR);
positive variable AccumulatedNewStorageCapacity(REGION,STORAGE,YEAR);
positive variable NewStorageCapacity(REGION,STORAGE,YEAR);
positive variable CapitalInvestmentStorage(REGION,STORAGE,YEAR);
positive variable DiscountedCapitalInvestmentStorage(REGION,STORAGE,YEAR);
positive variable SalvageValueStorage(REGION,STORAGE,YEAR);
positive variable DiscountedSalvageValueStorage(REGION,STORAGE,YEAR);
positive variable TotalDiscountedStorageCost(REGION,STORAGE,YEAR);
*
* ############### Capacity Variables ############
*
integer variable NumberOfNewTechnologyUnits(REGION,TECHNOLOGY,YEAR);
positive variable NewCapacity(REGION,TECHNOLOGY,YEAR);
positive variable AccumulatedNewCapacity(REGION,TECHNOLOGY,YEAR);
positive variable TotalCapacityAnnual(REGION,TECHNOLOGY,YEAR);
*
* ############### Activity Variables #############
*
positive variable RateOfActivity(REGION,TIMESLICE,TECHNOLOGY,MODE_OF_OPERATION,YEAR);
positive variable RateOfTotalActivity(REGION,TIMESLICE,TECHNOLOGY,YEAR);
positive variable TotalTechnologyAnnualActivity(REGION,TECHNOLOGY,YEAR);
positive variable TotalAnnualTechnologyActivityByMode(REGION,TECHNOLOGY,MODE_OF_OPERATION,YEAR);
positive variable RateOfProductionByTechnologyByMode(REGION,TIMESLICE,TECHNOLOGY,MODE_OF_OPERATION,FUEL,YEAR);
positive variable RateOfProductionByTechnology(REGION,TIMESLICE,TECHNOLOGY,FUEL,YEAR);
positive variable ProductionByTechnology(REGION,TIMESLICE,TECHNOLOGY,FUEL,YEAR);
positive variable ProductionByTechnologyAnnual(REGION,TECHNOLOGY,FUEL,YEAR);
positive variable RateOfProduction(REGION,TIMESLICE,FUEL,YEAR);
positive variable Production(REGION,TIMESLICE,FUEL,YEAR);
positive variable RateOfUseByTechnologyByMode(REGION,TIMESLICE,TECHNOLOGY,MODE_OF_OPERATION,FUEL,YEAR);
positive variable RateOfUseByTechnology(REGION,TIMESLICE,TECHNOLOGY,FUEL,YEAR);
positive variable UseByTechnologyAnnual(REGION,TECHNOLOGY,FUEL,YEAR);
positive variable RateOfUse(REGION,TIMESLICE,FUEL,YEAR);
positive variable UseByTechnology(REGION,TIMESLICE,TECHNOLOGY,FUEL,YEAR);
positive variable Use(REGION,TIMESLICE,FUEL,YEAR);
positive variable Trade(REGION,rr,TIMESLICE,FUEL,YEAR);
positive variable TradeAnnual(REGION,rr,FUEL,YEAR);
*
positive variable ProductionAnnual(REGION,FUEL,YEAR);
positive variable UseAnnual(REGION,FUEL,YEAR);
*
* ############### Costing Variables #############
*
positive variable CapitalInvestment(REGION,TECHNOLOGY,YEAR);
positive variable DiscountedCapitalInvestment(REGION,TECHNOLOGY,YEAR);
*
positive variable SalvageValue(REGION,TECHNOLOGY,YEAR);
positive variable DiscountedSalvageValue(REGION,TECHNOLOGY,YEAR);
positive variable OperatingCost(REGION,TECHNOLOGY,YEAR);
positive variable DiscountedOperatingCost(REGION,TECHNOLOGY,YEAR);
*
positive variable AnnualVariableOperatingCost(REGION,TECHNOLOGY,YEAR);
positive variable AnnualFixedOperatingCost(REGION,TECHNOLOGY,YEAR);
positive variable VariableOperatingCost(REGION,TIMESLICE,TECHNOLOGY,YEAR);
*
positive variable TotalDiscountedCostByTechnology(REGION,TECHNOLOGY,YEAR);
positive variable TotalDiscountedCost(REGION,YEAR);
*
positive variable ModelPeriodCostByRegion(REGION);
*
* ######## Reserve Margin #############
*
positive variable TotalCapacityInReserveMargin(REGION,YEAR);
positive variable DemandNeedingReserveMargin(REGION,TIMESLICE,YEAR);
*
* ######## RE Gen Target #############
*
free variable TotalREProductionAnnual(REGION,YEAR);
free variable RETotalProductionOfTargetFuelAnnual(REGION,YEAR);
*
free variable TotalTechnologyModelPeriodActivity(REGION,TECHNOLOGY);
*
* ######## Emissions #############
*
positive variable AnnualTechnologyEmissionByMode(REGION,TECHNOLOGY,EMISSION,MODE_OF_OPERATION,YEAR);
positive variable AnnualTechnologyEmission(REGION,TECHNOLOGY,EMISSION,YEAR);
positive variable AnnualTechnologyEmissionPenaltyByEmission(REGION,TECHNOLOGY,EMISSION,YEAR);
positive variable AnnualTechnologyEmissionsPenalty(REGION,TECHNOLOGY,YEAR);
positive variable DiscountedTechnologyEmissionsPenalty(REGION,TECHNOLOGY,YEAR);
positive variable AnnualEmissions(REGION,EMISSION,YEAR);
positive variable ModelPeriodEmissions(EMISSION,REGION);


