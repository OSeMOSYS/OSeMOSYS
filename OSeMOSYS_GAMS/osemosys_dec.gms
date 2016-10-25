* OSEMOSYS_DEC.GMS - declarations for sets, parameters, variables (but not equations)
*
* OSEMOSYS 2011.07.07 conversion to GAMS by Ken Noble, Noble-Soft Systems - August 2012
*
* OSEMOSYS 2011.07.07
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
alias (r,REGION);
set BOUNDARY_INSTANCES;
alias (b,BOUNDARY_INSTANCES);
set STORAGE;
alias (s,STORAGE);
*
* ####################
* # Parameters #
* ####################
*
* ####### Global #############
*
parameter StartYear;
parameter YearSplit(TIMESLICE,YEAR);
parameter DiscountRate(REGION,TECHNOLOGY);
*
* ####### Demands #############
*
parameter SpecifiedAnnualDemand(REGION,FUEL,YEAR);
parameter SpecifiedDemandProfile(REGION,FUEL,TIMESLICE,YEAR);
positive variable RateOfDemand(YEAR,TIMESLICE,FUEL,REGION);
positive variable Demand(YEAR,TIMESLICE,FUEL,REGION);
parameter AccumulatedAnnualDemand(REGION,FUEL,YEAR);
*
* ######## Technology #############
*
* ######## Performance #############
*
parameter CapacityToActivityUnit(REGION,TECHNOLOGY);
parameter TechWithCapacityNeededToMeetPeakTS(REGION,TECHNOLOGY);
parameter CapacityFactor(REGION,TECHNOLOGY,YEAR);
parameter AvailabilityFactor(REGION,TECHNOLOGY,YEAR);
parameter OperationalLife(REGION,TECHNOLOGY);
parameter ResidualCapacity(REGION,TECHNOLOGY,YEAR);
parameter SalvageFactor(REGION,TECHNOLOGY,YEAR);
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
parameter StorageInflectionTimes(YEAR,TIMESLICE,BOUNDARY_INSTANCES);
parameter TechnologyToStorage(REGION,TECHNOLOGY,STORAGE,MODE_OF_OPERATION);
parameter TechnologyFromStorage(REGION,TECHNOLOGY,STORAGE,MODE_OF_OPERATION);
parameter StorageUpperLimit(REGION,STORAGE);
parameter StorageLowerLimit(REGION,STORAGE);
*
* ######## Capacity Constraints #############
*
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
parameter YearVal(YEAR);
*
* #####################
* # Model Variables #
* #####################
*
* ############### Capacity Variables ############*
*
positive variable NewCapacity(YEAR,TECHNOLOGY,REGION);
positive variable AccumulatedNewCapacity(YEAR,TECHNOLOGY,REGION);
positive variable TotalCapacityAnnual(YEAR,TECHNOLOGY,REGION);
*
*############### Activity Variables #############
*
positive variable RateOfActivity(YEAR,TIMESLICE,TECHNOLOGY,MODE_OF_OPERATION,REGION);
positive variable RateOfTotalActivity(YEAR,TIMESLICE,TECHNOLOGY,REGION);
positive variable TotalTechnologyAnnualActivity(YEAR,TECHNOLOGY,REGION);
positive variable TotalAnnualTechnologyActivityByMode(YEAR,TECHNOLOGY,MODE_OF_OPERATION,REGION);
positive variable RateOfProductionByTechnologyByMode(YEAR,TIMESLICE,TECHNOLOGY,MODE_OF_OPERATION,FUEL,REGION);
positive variable RateOfProductionByTechnology(YEAR,TIMESLICE,TECHNOLOGY,FUEL,REGION);
positive variable ProductionByTechnology(YEAR,TIMESLICE,TECHNOLOGY,FUEL,REGION);
positive variable ProductionByTechnologyAnnual(YEAR,TECHNOLOGY,FUEL,REGION);
positive variable RateOfProduction(YEAR,TIMESLICE,FUEL,REGION);
positive variable Production(YEAR,TIMESLICE,FUEL,REGION);
positive variable RateOfUseByTechnologyByMode(YEAR,TIMESLICE,TECHNOLOGY,MODE_OF_OPERATION,FUEL,REGION);
positive variable RateOfUseByTechnology(YEAR,TIMESLICE,TECHNOLOGY,FUEL,REGION);
positive variable UseByTechnologyAnnual(YEAR,TECHNOLOGY,FUEL,REGION);
positive variable RateOfUse(YEAR,TIMESLICE,FUEL,REGION);
positive variable UseByTechnology(YEAR,TIMESLICE,TECHNOLOGY,FUEL,REGION);
positive variable Use(YEAR,TIMESLICE,FUEL,REGION);
*
positive variable ProductionAnnual(YEAR,FUEL,REGION);
positive variable UseAnnual(YEAR,FUEL,REGION);
*
* ############### Costing Variables #############
*
positive variable CapitalInvestment(YEAR,TECHNOLOGY,REGION);
positive variable DiscountedCapitalInvestment(YEAR,TECHNOLOGY,REGION);
*
positive variable SalvageValue(YEAR,TECHNOLOGY,REGION);
positive variable DiscountedSalvageValue(YEAR,TECHNOLOGY,REGION);
positive variable OperatingCost(YEAR,TECHNOLOGY,REGION);
positive variable DiscountedOperatingCost(YEAR,TECHNOLOGY,REGION);
*
positive variable AnnualVariableOperatingCost(YEAR,TECHNOLOGY,REGION);
positive variable AnnualFixedOperatingCost(YEAR,TECHNOLOGY,REGION);
positive variable VariableOperatingCost(YEAR,TIMESLICE,TECHNOLOGY,REGION);
*
positive variable TotalDiscountedCost(YEAR,TECHNOLOGY,REGION);
*
positive variable ModelPeriodCostByRegion (REGION);
*
* ############### Storage Variables #############
*
free variable NetStorageCharge(STORAGE,YEAR,TIMESLICE,REGION);
free variable StorageLevel(STORAGE,BOUNDARY_INSTANCES,REGION);
free variable StorageCharge(STORAGE,YEAR,TIMESLICE,REGION);
free variable StorageDischarge(STORAGE,YEAR,TIMESLICE,REGION);
*
* ######## Reserve Margin #############
*
positive variable TotalCapacityInReserveMargin(REGION,YEAR);
positive variable DemandNeedingReserveMargin(YEAR,TIMESLICE,REGION);
*
* ######## RE Gen Target #############
*
free variable TotalGenerationByRETechnologies(YEAR,REGION);
free variable TotalREProductionAnnual(YEAR,REGION);
free variable RETotalDemandOfTargetFuelAnnual(YEAR,REGION);
*
free variable TotalTechnologyModelPeriodActivity(TECHNOLOGY,REGION);
*
* ######## Emissions #############
*
positive variable AnnualTechnologyEmissionByMode(YEAR,TECHNOLOGY,EMISSION,MODE_OF_OPERATION,REGION);
positive variable AnnualTechnologyEmission(YEAR,TECHNOLOGY,EMISSION,REGION);
positive variable AnnualTechnologyEmissionPenaltyByEmission(YEAR,TECHNOLOGY,EMISSION,REGION);
positive variable AnnualTechnologyEmissionsPenalty(YEAR,TECHNOLOGY,REGION);
positive variable DiscountedTechnologyEmissionsPenalty(YEAR,TECHNOLOGY,REGION);
positive variable AnnualEmissions(YEAR,EMISSION,REGION);
free variable EmissionsProduction(YEAR,TECHNOLOGY,EMISSION,MODE_OF_OPERATION,REGION);
positive variable ModelPeriodEmissions(EMISSION,REGION);
