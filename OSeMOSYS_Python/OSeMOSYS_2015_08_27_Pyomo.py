# OSeMOSYS_2015_08_27
# 
# Open Source energy MOdeling SYStem
#
# Main changes to previous version OSeMOSYS_2013_05_10
#		- Removed the parameter TechWithCapacityNeededToMeetPeakTS from constraint CAa4_Constraint_Capacity
#		- Fixed a bug related to using CapacityOfOneTechnologyUnit in constraint CAa5_TotalNewCapacity
#		- Fixed a bug in the storage equations which caused an error if more than one day type was used 
#		- DiscountRate is no longer technology-specific. Therefore, DiscountRateStorage is now replaced by DiscountRate.
#
# ============================================================================
#
#    Copyright [2010-2015] [OSeMOSYS Forum steering committee see: www.osemosys.org]
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
# ============================================================================
#
#  To run OSeMOSYS, enter the following line into your command prompt after replacing FILEPATH & YOURDATAFILE with your folder structure and data file name: 
#
#  C:\...FILEPATH...\glpsol -m C:\...FILEPATH...\OSeMOSYS_2015_08_27.txt -d C:\...FILEPATH...\YOURDATAFILE.txt -o C:\...FILEPATH...\Results.txt
#
#  Alternatively, install GUSEK (http://gusek.sourceforge.net/gusek.html) and run the model within this integrated development environment (IDE). 
#  To do so, open the .dat file and select "Use External .dat file" from the Options menu. Then change to the model file and select the "Go" icon or press F5.
#
#              			#########################################
######################			Model Definition				#############
#              			#########################################
#
#

from __future__ import division
from pyomo.environ import *
from pyomo.core import *
from pyomo.opt import SolverFactory
import os

model = AbstractModel()


###############
#    Sets     #
############### 

model.YEAR = Set()
model.TECHNOLOGY = Set()
model.TIMESLICE = Set()
model.FUEL = Set()
model.EMISSION = Set()
model.MODE_OF_OPERATION = Set()
model.REGION = Set()
model.SEASON = Set()
model.DAYTYPE = Set()
model.DAILYTIMEBRACKET = Set()
model.FLEXIBLEDEMANDTYPE = Set()
model.STORAGE = Set()

#####################
#    Parameters     #
#####################

########			Global 						#############

model.YearSplit = Param(model.TIMESLICE, model.YEAR)
model.DiscountRate = Param(model.REGION, default=0.05)
model.DaySplit = Param(model.DAILYTIMEBRACKET, model.YEAR, default=0.00137)
model.Conversionls = Param(model.TIMESLICE, model.SEASON, default=0)
model.Conversionld = Param(model.TIMESLICE, model.DAYTYPE, default=0)
model.Conversionlh = Param(model.TIMESLICE, model.DAILYTIMEBRACKET, default=0)
model.DaysInDayType = Param(model.SEASON, model.DAYTYPE, model.YEAR, default=7)
model.TradeRoute = Param(model.REGION, model.REGION, model.FUEL, model.YEAR, default=0)
model.DepreciationMethod = Param(model.REGION, default=1)

########			Demands 					#############

model.SpecifiedAnnualDemand = Param(model.REGION, model.FUEL, model.YEAR, default=0)
model.SpecifiedDemandProfile = Param(model.REGION, model.FUEL, model.TIMESLICE, model.YEAR, default=0)
model.AccumulatedAnnualDemand = Param(model.REGION, model.FUEL, model.YEAR, default=0)

#########			Performance					#############

model.CapacityToActivityUnit = Param(model.REGION, model.TECHNOLOGY, default=1)
model.CapacityFactor = Param(model.REGION, model.TECHNOLOGY, model.TIMESLICE, model.YEAR, default=1)
model.AvailabilityFactor = Param(model.REGION, model.TECHNOLOGY, model.YEAR, default=1)
model.OperationalLife = Param(model.REGION, model.TECHNOLOGY, default=1)
model.ResidualCapacity = Param(model.REGION, model.TECHNOLOGY, model.YEAR, default=0)
model.InputActivityRatio = Param(model.REGION, model.TECHNOLOGY, model.FUEL, model.MODE_OF_OPERATION, model.YEAR, default=0)
model.OutputActivityRatio = Param(model.REGION, model.TECHNOLOGY, model.FUEL, model.MODE_OF_OPERATION, model.YEAR, default=0)

#########			Technology Costs			#############

model.CapitalCost = Param(model.REGION, model.TECHNOLOGY, model.YEAR, default=0)
model.VariableCost = Param(model.REGION, model.TECHNOLOGY, model.MODE_OF_OPERATION, model.YEAR, default=0.00001)
model.FixedCost = Param(model.REGION, model.TECHNOLOGY, model.YEAR, default=0)

#########           		Storage                 		#############

model.TechnologyToStorage = Param(model.REGION, model.TECHNOLOGY, model.STORAGE, model.MODE_OF_OPERATION, default=0)
model.TechnologyFromStorage = Param(model.REGION, model.TECHNOLOGY, model.STORAGE, model.MODE_OF_OPERATION, default=0)
model.StorageLevelStart = Param(model.REGION, model.STORAGE, default=999)
model.StorageMaxChargeRate = Param(model.REGION, model.STORAGE, default=99)
model.StorageMaxDischargeRate = Param(model.REGION, model.STORAGE, default=99)
model.MinStorageCharge = Param(model.REGION, model.STORAGE, model.YEAR, default=0)
model.OperationalLifeStorage = Param(model.REGION, model.STORAGE, default=99)
model.CapitalCostStorage = Param(model.REGION, model.STORAGE, model.YEAR, default=0)
model.ResidualStorageCapacity = Param(model.REGION, model.STORAGE, model.YEAR, default=0)

#########			Capacity Constraints		#############

model.CapacityOfOneTechnologyUnit = Param(model.REGION, model.TECHNOLOGY, model.YEAR, default=0)
model.TotalAnnualMaxCapacity = Param(model.REGION, model.TECHNOLOGY, model.YEAR, default=99999)
model.TotalAnnualMinCapacity = Param(model.REGION, model.TECHNOLOGY, model.YEAR, default=0)

#########			Investment Constraints		#############

model.TotalAnnualMaxCapacityInvestment = Param(model.REGION, model.TECHNOLOGY, model.YEAR, default=99999)
model.TotalAnnualMinCapacityInvestment = Param(model.REGION, model.TECHNOLOGY, model.YEAR, default=0)

#########			Activity Constraints		#############

model.TotalTechnologyAnnualActivityUpperLimit = Param(model.REGION, model.TECHNOLOGY, model.YEAR, default=99999)
model.TotalTechnologyAnnualActivityLowerLimit = Param(model.REGION, model.TECHNOLOGY, model.YEAR, default=0)
model.TotalTechnologyModelPeriodActivityUpperLimit = Param(model.REGION, model.TECHNOLOGY, default=99999)
model.TotalTechnologyModelPeriodActivityLowerLimit = Param(model.REGION, model.TECHNOLOGY, default=0)

#########			Reserve Margin				############# 

model.ReserveMarginTagTechnology = Param(model.REGION, model.TECHNOLOGY, model.YEAR, default=0)
model.ReserveMarginTagFuel = Param(model.REGION, model.FUEL, model.YEAR, default=0)
model.ReserveMargin = Param(model.REGION, model.YEAR, default=1)

#########			RE Generation Target		############# 

model.RETagTechnology = Param(model.REGION, model.TECHNOLOGY, model.YEAR, default=0)
model.RETagFuel = Param(model.REGION, model.FUEL, model.YEAR, default=0)
model.REMinProductionTarget = Param(model.REGION, model.YEAR, default=0)

#########			Emissions & Penalties		#############

model.EmissionActivityRatio = Param(model.REGION, model.TECHNOLOGY, model.EMISSION, model.MODE_OF_OPERATION, model.YEAR, default=0)
model.EmissionsPenalty = Param(model.REGION, model.EMISSION, model.YEAR, default=0)
model.AnnualExogenousEmission = Param(model.REGION, model.EMISSION, model.YEAR, default=0)
model.AnnualEmissionLimit = Param(model.REGION, model.EMISSION, model.YEAR, default=99999)
model.ModelPeriodExogenousEmission = Param(model.REGION, model.EMISSION, default=0)
model.ModelPeriodEmissionLimit = Param(model.REGION, model.EMISSION, default=99999)

######################
#   Model Variables  #
######################

########			Demands 					#############

model.RateOfDemand = Var(model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.Demand = Var(model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, domain=NonNegativeReals, initialize=0.0)

########     		Storage                 		#############

model.RateOfStorageCharge = Var(model.REGION, model.STORAGE, model.SEASON, model.DAYTYPE, model.DAILYTIMEBRACKET, model.YEAR, initialize=0.0)
model.RateOfStorageDischarge = Var(model.REGION, model.STORAGE, model.SEASON, model.DAYTYPE, model.DAILYTIMEBRACKET, model.YEAR, initialize=0.0)
model.NetChargeWithinYear = Var(model.REGION, model.STORAGE, model.SEASON, model.DAYTYPE, model.DAILYTIMEBRACKET, model.YEAR, initialize=0.0)
model.NetChargeWithinDay = Var(model.REGION, model.STORAGE, model.SEASON, model.DAYTYPE, model.DAILYTIMEBRACKET, model.YEAR, initialize=0.0)
model.StorageLevelYearStart = Var(model.REGION, model.STORAGE, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.StorageLevelYearFinish = Var(model.REGION, model.STORAGE, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.StorageLevelSeasonStart = Var(model.REGION, model.STORAGE, model.SEASON, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.StorageLevelDayTypeStart = Var(model.REGION, model.STORAGE, model.SEASON, model.DAYTYPE, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.StorageLevelDayTypeFinish = Var(model.REGION, model.STORAGE, model.SEASON, model.DAYTYPE, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.StorageLowerLimit = Var(model.REGION, model.STORAGE, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.StorageUpperLimit = Var(model.REGION, model.STORAGE, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.AccumulatedNewStorageCapacity = Var(model.REGION, model.STORAGE, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.NewStorageCapacity = Var(model.REGION, model.STORAGE, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.CapitalInvestmentStorage = Var(model.REGION, model.STORAGE, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.DiscountedCapitalInvestmentStorage = Var(model.REGION, model.STORAGE, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.SalvageValueStorage = Var(model.REGION, model.STORAGE, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.DiscountedSalvageValueStorage = Var(model.REGION, model.STORAGE, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.TotalDiscountedStorageCost = Var(model.REGION, model.STORAGE, model.YEAR, domain=NonNegativeReals, initialize=0.0)

#########		    Capacity Variables 			############# 

model.NumberOfNewTechnologyUnits = Var(model.REGION, model.TECHNOLOGY, model.YEAR, domain=NonNegativeIntegers, initialize=0)
model.NewCapacity = Var(model.REGION, model.TECHNOLOGY, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.AccumulatedNewCapacity = Var(model.REGION, model.TECHNOLOGY, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.TotalCapacityAnnual = Var(model.REGION, model.TECHNOLOGY, model.YEAR, domain=NonNegativeReals, initialize=0.0)

#########		    Activity Variables 			#############

model.RateOfActivity = Var(model.REGION, model.TIMESLICE, model.TECHNOLOGY, model.MODE_OF_OPERATION, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.RateOfTotalActivity = Var(model.REGION, model.TECHNOLOGY, model.TIMESLICE, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.TotalTechnologyAnnualActivity = Var(model.REGION, model.TECHNOLOGY, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.TotalAnnualTechnologyActivityByMode = Var(model.REGION, model.TECHNOLOGY, model.MODE_OF_OPERATION, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.RateOfProductionByTechnologyByMode = Var(model.REGION, model.TIMESLICE, model.TECHNOLOGY, model.MODE_OF_OPERATION, model.FUEL, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.RateOfProductionByTechnology = Var(model.REGION, model.TIMESLICE, model.TECHNOLOGY, model.FUEL, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.ProductionByTechnology = Var(model.REGION, model.TIMESLICE, model.TECHNOLOGY, model.FUEL, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.ProductionByTechnologyAnnual = Var(model.REGION, model.TECHNOLOGY, model.FUEL, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.RateOfProduction = Var(model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.Production = Var(model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.RateOfUseByTechnologyByMode = Var(model.REGION, model.TIMESLICE, model.TECHNOLOGY, model.MODE_OF_OPERATION, model.FUEL, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.RateOfUseByTechnology = Var(model.REGION, model.TIMESLICE, model.TECHNOLOGY, model.FUEL, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.UseByTechnologyAnnual = Var(model.REGION, model.TECHNOLOGY, model.FUEL, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.RateOfUse = Var(model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.UseByTechnology = Var(model.REGION, model.TIMESLICE, model.TECHNOLOGY, model.FUEL, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.Use = Var(model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.Trade = Var(model.REGION, model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, initialize=0.0)
model.TradeAnnual = Var(model.REGION, model.REGION, model.FUEL, model.YEAR, initialize=0.0)

model.ProductionAnnual = Var(model.REGION, model.FUEL, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.UseAnnual = Var(model.REGION, model.FUEL, model.YEAR, domain=NonNegativeReals, initialize=0.0)


#########		    Costing Variables 			#############

model.CapitalInvestment = Var(model.REGION, model.TECHNOLOGY, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.DiscountedCapitalInvestment = Var(model.REGION, model.TECHNOLOGY, model.YEAR, domain=NonNegativeReals, initialize=0.0)

model.SalvageValue = Var(model.REGION, model.TECHNOLOGY, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.DiscountedSalvageValue = Var(model.REGION, model.TECHNOLOGY, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.OperatingCost = Var(model.REGION, model.TECHNOLOGY, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.DiscountedOperatingCost = Var(model.REGION, model.TECHNOLOGY, model.YEAR, domain=NonNegativeReals, initialize=0.0)

model.AnnualVariableOperatingCost = Var(model.REGION, model.TECHNOLOGY, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.AnnualFixedOperatingCost = Var(model.REGION, model.TECHNOLOGY, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.VariableOperatingCost = Var(model.REGION, model.TECHNOLOGY, model.TIMESLICE, model.YEAR, domain=NonNegativeReals, initialize=0.0)

model.TotalDiscountedCostByTechnology = Var(model.REGION, model.TECHNOLOGY, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.TotalDiscountedCost = Var(model.REGION, model.YEAR, domain=NonNegativeReals, initialize=0.0)

model.ModelPeriodCostByRegion = Var(model.REGION, domain=NonNegativeReals, initialize=0.0)

#########			Reserve Margin				#############

model.TotalCapacityInReserveMargin = Var(model.REGION, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.DemandNeedingReserveMargin = Var(model.REGION,model.TIMESLICE, model.YEAR, domain=NonNegativeReals, initialize=0.0)

#########			RE Gen Target				#############

model.TotalREProductionAnnual = Var(model.REGION, model.YEAR, initialize=0.0)
model.RETotalDemandOfTargetFuelAnnual = Var(model.REGION, model.YEAR, initialize=0.0)

model.TotalTechnologyModelPeriodActivity = Var(model.REGION, model.TECHNOLOGY, initialize=0.0)

#########			Emissions					#############

model.AnnualTechnologyEmissionByMode = Var(model.REGION, model.TECHNOLOGY, model.EMISSION, model.MODE_OF_OPERATION, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.AnnualTechnologyEmission = Var(model.REGION, model.TECHNOLOGY, model.EMISSION, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.AnnualTechnologyEmissionPenaltyByEmission = Var(model.REGION, model.TECHNOLOGY, model.EMISSION, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.AnnualTechnologyEmissionsPenalty = Var(model.REGION, model.TECHNOLOGY, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.DiscountedTechnologyEmissionsPenalty = Var(model.REGION, model.TECHNOLOGY, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.AnnualEmissions = Var(model.REGION, model.EMISSION, model.YEAR, domain=NonNegativeReals, initialize=0.0)
model.ModelPeriodEmissions = Var(model.REGION, model.EMISSION, domain=NonNegativeReals, initialize=0.0)


######################
# Objective Function #
######################


def ObjectiveFunction_rule(model):
	return sum(model.ModelPeriodCostByRegion[r] for r in model.REGION)
model.OBJ = Objective(rule=ObjectiveFunction_rule, sense=minimize)


#####################
# Constraints       #
#####################


def SpecifiedDemand_rule(model,r,f,l,y):
	return model.SpecifiedAnnualDemand[r,f,y]*model.SpecifiedDemandProfile[r,f,l,y]/model.YearSplit[l,y] == model.RateOfDemand[r,l,f,y]
model.SpecifiedDemand = Constraint(model.REGION, model.FUEL, model.TIMESLICE, model.YEAR, rule=SpecifiedDemand_rule)


#########       	Capacity Adequacy A	     	#############

	
def TotalNewCapacity_1_rule(model,r,t,y):
	return model.AccumulatedNewCapacity[r,t,y] == sum(model.NewCapacity[r,t,yy] for yy in model.YEAR if ((y-yy < model.OperationalLife[r,t]) and (y-yy >= 0)))
model.TotalNewCapacity_1 = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=TotalNewCapacity_1_rule)
	
def TotalAnnualCapacity_rule(model,r,t,y):
	return model.AccumulatedNewCapacity[r,t,y] + model.ResidualCapacity[r,t,y] == model.TotalCapacityAnnual[r,t,y]
model.TotalAnnualCapacity_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=TotalAnnualCapacity_rule)

def TotalActivityOfEachTechnology_rule(model,r,t,l,y):
	return sum(model.RateOfActivity[r,l,t,m,y] for m in model.MODE_OF_OPERATION) == model.RateOfTotalActivity[r,t,l,y]
model.TotalActivityOfEachTechnology = Constraint(model.REGION, model.TECHNOLOGY, model.TIMESLICE, model.YEAR, rule=TotalActivityOfEachTechnology_rule)

def ConstraintCapacity_rule(model,r,l,t,y):
	return model.RateOfTotalActivity[r,t,l,y] <= model.TotalCapacityAnnual[r,t,y]*model.CapacityFactor[r,t,l,y]*model.CapacityToActivityUnit[r,t]
model.ConstraintCapacity = Constraint(model.REGION, model.TIMESLICE, model.TECHNOLOGY, model.YEAR, rule=ConstraintCapacity_rule)

# def TotalNewCapacity_2_rule(model,r,t,y):
	# if model.CapacityOfOneTechnologyUnit != 0:
		# return model.CapacityOfOneTechnologyUnit[r,t,y]*model.NumberOfNewTechnologyUnits[r,t,y] == model.NewCapacity[r,t,y]
	# else: 
		# Constraint.Skip
# model.TotalNewCapacity_2 = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=TotalNewCapacity_2_rule)


#########       	Capacity Adequacy B		 	#############


def PlannedMaintenance_rule(model,r,t,y):
	return sum(model.RateOfTotalActivity[r,t,l,y]*model.YearSplit[l,y] for l in model.TIMESLICE) <= sum(model.TotalCapacityAnnual[r,t,y]*model.CapacityFactor[r,t,l,y]*model.YearSplit[l,y] for l in model.TIMESLICE)*model.AvailabilityFactor[r,t,y]*model.CapacityToActivityUnit[r,t]
model.PlannedMaintenance = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=PlannedMaintenance_rule)


#########	        Energy Balance A    	 	#############


def RateOfFuelProduction1_rule(model,r,l,f,t,m,y):
	if model.OutputActivityRatio[r,t,f,m,y] != 0:
		return model.RateOfProductionByTechnologyByMode[r,l,t,m,f,y] == model.RateOfActivity[r,l,t,m,y]*model.OutputActivityRatio[r,t,f,m,y]
	else:
		return model.RateOfProductionByTechnologyByMode[r,l,t,m,f,y] == 0
model.RateOfFuelProduction1 = Constraint(model.REGION, model.TIMESLICE, model.FUEL, model.TECHNOLOGY, model.MODE_OF_OPERATION, model.YEAR, rule=RateOfFuelProduction1_rule)

# def RateOfFuelProduction1_rule(model,r,l,f,t,m,y):
	# return model.RateOfProductionByTechnologyByMode[r,l,t,m,f,y] == model.RateOfActivity[r,l,t,m,y]*model.OutputActivityRatio[r,t,f,m,y]
# model.RateOfFuelProduction1 = Constraint(model.REGION, model.TIMESLICE, model.FUEL, model.TECHNOLOGY, model.MODE_OF_OPERATION, model.YEAR, rule=RateOfFuelProduction1_rule)

# def RateOfFuelProduction2_rule(model,r,l,f,t,y):
	# return  model.RateOfProductionByTechnology[r,l,t,f,y] == sum(model.RateOfProductionByTechnologyByMode[r,l,t,m,f,y] for m in model.MODE_OF_OPERATION if model.OutputActivityRatio[r,t,f,m,y] != 0)
# model.RateOfFuelProduction2 = Constraint(model.REGION, model.TIMESLICE, model.FUEL, model.TECHNOLOGY, model.YEAR, rule=RateOfFuelProduction2_rule)

def RateOfFuelProduction2_rule(model,r,l,f,t,y):
	return  model.RateOfProductionByTechnology[r,l,t,f,y] == sum(model.RateOfProductionByTechnologyByMode[r,l,t,m,f,y] for m in model.MODE_OF_OPERATION)
model.RateOfFuelProduction2 = Constraint(model.REGION, model.TIMESLICE, model.FUEL, model.TECHNOLOGY, model.YEAR, rule=RateOfFuelProduction2_rule)

def RateOfFuelProduction3_rule(model,r,l,f,y):
	return model.RateOfProduction[r,l,f,y] == sum(model.RateOfProductionByTechnology[r,l,t,f,y] for t in model.TECHNOLOGY)
model.RateOfFuelProduction3 = Constraint(model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, rule=RateOfFuelProduction3_rule)

# def RateOfFuelUse1_rule(model,r,l,f,t,m,y):
	# if model.InputActivityRatio[r,t,f,m,y] != 0:
		# return model.RateOfActivity[r,l,t,m,y]*model.InputActivityRatio[r,t,f,m,y] == model.RateOfUseByTechnologyByMode[r,l,t,m,f,y]
	# else:
		# return model.RateOfUseByTechnologyByMode[r,l,t,m,f,y] == 0
# model.RateOfFuelUse1 = Constraint(model.REGION, model.TIMESLICE, model.FUEL, model.TECHNOLOGY, model.MODE_OF_OPERATION, model.YEAR, rule=RateOfFuelUse1_rule)

def RateOfFuelUse1_rule(model,r,l,f,t,m,y):
	return model.RateOfActivity[r,l,t,m,y]*model.InputActivityRatio[r,t,f,m,y] == model.RateOfUseByTechnologyByMode[r,l,t,m,f,y]
model.RateOfFuelUse1 = Constraint(model.REGION, model.TIMESLICE, model.FUEL, model.TECHNOLOGY, model.MODE_OF_OPERATION, model.YEAR, rule=RateOfFuelUse1_rule)

# def RateOfFuelUse2_rule(model,r,l,f,t,y):
	# return model.RateOfUseByTechnology[r,l,t,f,y] == sum(model.RateOfUseByTechnologyByMode[r,l,t,m,f,y] for m in model.MODE_OF_OPERATION if model.InputActivityRatio[r,t,f,m,y] != 0)
# model.RateOfFuelUse2 = Constraint(model.REGION, model.TIMESLICE, model.FUEL, model.TECHNOLOGY, model.YEAR, rule=RateOfFuelUse2_rule)

def RateOfFuelUse2_rule(model,r,l,f,t,y):
	return model.RateOfUseByTechnology[r,l,t,f,y] == sum(model.RateOfUseByTechnologyByMode[r,l,t,m,f,y] for m in model.MODE_OF_OPERATION)
model.RateOfFuelUse2 = Constraint(model.REGION, model.TIMESLICE, model.FUEL, model.TECHNOLOGY, model.YEAR, rule=RateOfFuelUse2_rule)

def RateOfFuelUse3_rule(model,r,l,f,y):
	return sum(model.RateOfUseByTechnology[r,l,t,f,y] for t in model.TECHNOLOGY) == model.RateOfUse[r,l,f,y]
model.RateOfFuelUse3 = Constraint(model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, rule=RateOfFuelUse3_rule)

def EnergyBalanceEachTS1_rule(model,r,l,f,y):
	return model.RateOfProduction[r,l,f,y]*model.YearSplit[l,y] == model.Production[r,l,f,y]
model.EnergyBalanceEachTS1 = Constraint(model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, rule=EnergyBalanceEachTS1_rule)

def EnergyBalanceEachTS2_rule(model,r,l,f,y):
	return model.RateOfUse[r,l,f,y]*model.YearSplit[l,y] == model.Use[r,l,f,y]
model.EnergyBalanceEachTS2 = Constraint(model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, rule=EnergyBalanceEachTS2_rule)

def EnergyBalanceEachTS3_rule(model,r,l,f,y):
	return model.RateOfDemand[r,l,f,y]*model.YearSplit[l,y] == model.Demand[r,l,f,y]
model.EnergyBalanceEachTS3 = Constraint(model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, rule=EnergyBalanceEachTS3_rule)

def EnergyBalanceEachTS4_rule(model,r,rr,l,f,y):
	return model.Trade[r,rr,l,f,y] + model.Trade[rr,r,l,f,y] == 0
model.EnergyBalanceEachTS4 = Constraint(model.REGION, model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, rule= EnergyBalanceEachTS4_rule)

def EnergyBalanceEachTS5_rule(model,r,l,f,y):
	return model.Production[r,l,f,y] >= model.Demand[r,l,f,y] + model.Use[r,l,f,y] + sum(model.Trade[r,rr,l,f,y]*model.TradeRoute[r,rr,f,y] for rr in model.REGION)
model.EnergyBalanceEachTS5 = Constraint(model.REGION, model.TIMESLICE, model.FUEL, model.YEAR, rule=EnergyBalanceEachTS5_rule)


#########        	Energy Balance B		 	#############


def EnergyBalanceEachYear1_rule(model,r,f,y):
	return sum(model.Production[r,l,f,y] for l in model.TIMESLICE) == model.ProductionAnnual[r,f,y]
model.EnergyBalanceEachYear1 = Constraint(model.REGION, model.FUEL, model.YEAR, rule=EnergyBalanceEachYear1_rule)

def EnergyBalanceEachYear2_rule(model,r,f,y):
	return sum(model.Use[r,l,f,y] for l in model.TIMESLICE) == model.UseAnnual[r,f,y]
model.EnergyBalanceEachYear2 = Constraint(model.REGION, model.FUEL, model.YEAR, rule=EnergyBalanceEachYear2_rule)

def EnergyBalanceEachYear3_rule(model,r,rr,f,y):
	return sum(model.Trade[r,rr,l,f,y] for l in model.TIMESLICE) == model.TradeAnnual[r,rr,f,y]
model.EnergyBalanceEachYear3 = Constraint(model.REGION, model.REGION, model.FUEL, model.YEAR, rule=EnergyBalanceEachYear3_rule)
	
def EnergyBalanceEachYear4_rule(model,r,f,y):
	return model.ProductionAnnual[r,f,y] >= model.UseAnnual[r,f,y] + sum(model.TradeAnnual[r,rr,f,y]*model.TradeRoute[r,rr,f,y] for rr in model.REGION) + model.AccumulatedAnnualDemand[r,f,y]
model.EnergyBalanceEachYear4 = Constraint(model.REGION, model.FUEL, model.YEAR, rule=EnergyBalanceEachYear4_rule)


#########        	Accounting Technology Production/Use	#############

	
def FuelProductionByTechnology_rule(model,r,l,t,f,y):
	return model.RateOfProductionByTechnology[r,l,t,f,y]*model.YearSplit[l,y] == model.ProductionByTechnology[r,l,t,f,y]
model.FuelProductionByTechnology = Constraint(model.REGION, model.TIMESLICE, model.TECHNOLOGY, model.FUEL, model.YEAR, rule=FuelProductionByTechnology_rule)

def FuelUseByTechnology_rule(model,r,l,t,f,y):
	return model.RateOfUseByTechnology[r,l,t,f,y]*model.YearSplit[l,y] == model.UseByTechnology[r,l,t,f,y]
model.FuelUseByTechnology = Constraint(model.REGION, model.TIMESLICE, model.TECHNOLOGY, model.FUEL, model.YEAR, rule=FuelUseByTechnology_rule)

def AverageAnnualRateOfActivity_rule(model,r,t,m,y):
	return sum(model.RateOfActivity[r,l,t,m,y]*model.YearSplit[l,y] for l in model.TIMESLICE) == model.TotalAnnualTechnologyActivityByMode[r,t,m,y]
model.AverageAnnualRateOfActivity = Constraint(model.REGION, model.TECHNOLOGY, model.MODE_OF_OPERATION, model.YEAR, rule=AverageAnnualRateOfActivity_rule)

def ModelPeriodCostByRegion_rule(model,r):
	return model.ModelPeriodCostByRegion[r] == sum(model.TotalDiscountedCost[r,y] for y in model.YEAR)
model.ModelPeriodCostByRegion_constraint = Constraint(model.REGION, rule=ModelPeriodCostByRegion_rule)

# def ModelPeriodCost_rule(model):
	# return model.ModelPeriodCost == sum(model.ModelPeriodCostByRegion[r] for r in model.REGION)
# model.ModelPeriodCost_Constraint = Constraint(rule=ModelPeriodCost_rule)


#########       	Capital Costs 		     	#############


def UndiscountedCapitalInvestment_rule(model,r,t,y):
	return model.CapitalCost[r,t,y]*model.NewCapacity[r,t,y] == model.CapitalInvestment[r,t,y]
model.UndiscountedCapitalInvestment = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=UndiscountedCapitalInvestment_rule)

def DiscountedCapitalInvestment_rule(model,r,t,y):
	return model.CapitalInvestment[r,t,y]/((1+model.DiscountRate[r])**(y-min(model.YEAR))) == model.DiscountedCapitalInvestment[r,t,y]
model.DiscountedCapitalInvestment_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=DiscountedCapitalInvestment_rule)


#########        	Operating Costs 		 	#############


def OperatingCostsVariable_rule(model,r,t,l,y):
	return sum(model.TotalAnnualTechnologyActivityByMode[r,t,m,y]*model.VariableCost[r,t,m,y] for m in model.MODE_OF_OPERATION) == model.AnnualVariableOperatingCost[r,t,y]
model.OperatingCostsVariable = Constraint(model.REGION, model.TECHNOLOGY, model.TIMESLICE, model.YEAR, rule=OperatingCostsVariable_rule)

def OperatingCostsFixedAnnual_rule(model,r,t,y):
	return model.TotalCapacityAnnual[r,t,y]*model.FixedCost[r,t,y] == model.AnnualFixedOperatingCost[r,t,y]
model.OperatingCostsFixedAnnual = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=OperatingCostsFixedAnnual_rule)

def OperatingCostsTotalAnnual_rule(model,r,t,y):
	return model.AnnualFixedOperatingCost[r,t,y] + model.AnnualVariableOperatingCost[r,t,y] == model.OperatingCost[r,t,y]
model.OperatingCostsTotalAnnual = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=OperatingCostsTotalAnnual_rule)

def DiscountedOperatingCostsTotalAnnual_rule(model,r,t,y):
	return model.OperatingCost[r,t,y]/((1+model.DiscountRate[r])**(y-min(model.YEAR) + 0.5)) == model.DiscountedOperatingCost[r,t,y]
model.DiscountedOperatingCostsTotalAnnual = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=DiscountedOperatingCostsTotalAnnual_rule)


#########       	Total Discounted Costs	 	#############


def TotalDiscountedCostByTechnology_rule(model,r,t,y):
	return model.DiscountedOperatingCost[r,t,y] + model.DiscountedCapitalInvestment[r,t,y] + model.DiscountedTechnologyEmissionsPenalty[r,t,y] - model.DiscountedSalvageValue[r,t,y] == model.TotalDiscountedCostByTechnology[r,t,y]
model.TotalDiscountedCostByTechnology_constraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=TotalDiscountedCostByTechnology_rule)

# def TotalDiscountedCost_rule(model,r,y):
	# return sum(model.TotalDiscountedCostByTechnology[r,t,y] for t in model.TECHNOLOGY) + sum(model.TotalDiscountedStorageCost[r,s,y] for s in model.STORAGE) == model.TotalDiscountedCost[r,y]
# model.TotalDiscountedCost_constraint = Constraint(model.REGION, model.YEAR, rule=TotalDiscountedCost_rule)

def TotalDiscountedCost_rule(model,r,y):
	return sum(model.TotalDiscountedCostByTechnology[r,t,y] for t in model.TECHNOLOGY) == model.TotalDiscountedCost[r,y]
model.TotalDiscountedCost_constraint = Constraint(model.REGION, model.YEAR, rule=TotalDiscountedCost_rule)


#########      		Total Capacity Constraints 	##############

def TotalAnnualMaxCapacityConstraint_rule(model,r,t,y): 
	return model.TotalCapacityAnnual[r,t,y] <= model.TotalAnnualMaxCapacity[r,t,y]
model.TotalAnnualMaxCapacityConstraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=TotalAnnualMaxCapacityConstraint_rule)

def TotalAnnualMinCapacityConstraint_rule(model,r,t,y): 
	return model.TotalCapacityAnnual[r,t,y] >= model.TotalAnnualMinCapacity[r,t,y]
model.TotalAnnualMinCapacityConstraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=TotalAnnualMinCapacityConstraint_rule)           
										 

#########           Salvage Value            	#############

def SalvageValueAtEndOfPeriod1_rule(model,r,t,y): 
	if model.DepreciationMethod[r] == 1 and ((y + model.OperationalLife[r,t]-1) > max(model.YEAR)) and model.DiscountRate[r]>0: 
		return model.SalvageValue[r,t,y] == model.CapitalCost[r,t,y]*model.NewCapacity[r,t,y]*(1-(((1+model.DiscountRate[r])**(max(model.YEAR)- y+1)-1)/((1+model.DiscountRate[r])**model.OperationalLife[r,t]-1)))
	elif (model.DepreciationMethod[r] == 1 and ((y + model.OperationalLife[r,t]-1) > max(model.YEAR)) and model.DiscountRate[r] == 0) or (model.DepreciationMethod[r] == 2 and (y + model.OperationalLife[r,t]-1) > (max(model.YEAR))):
		return model.SalvageValue[r,t,y] == model.CapitalCost[r,t,y]*model.NewCapacity[r,t,y]*(1-(max(model.YEAR)- y+1)/model.OperationalLife[r,t])
	else:
		return model.SalvageValue[r,t,y] == 0
model.SalvageValueAtEndOfPeriod1 = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=SalvageValueAtEndOfPeriod1_rule)

def SalvageValueDiscountedToStartYear_rule(model,r,t,y):
	return model.DiscountedSalvageValue[r,t,y] == model.SalvageValue[r,t,y]/((1+model.DiscountRate[r])**(1+max(model.YEAR)-min(model.YEAR)))
model.SalvageValueDiscountedToStartYear = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=SalvageValueDiscountedToStartYear_rule)


#########    		New Capacity Constraints  	##############

def TotalAnnualMaxNewCapacityConstraint_rule(model,r,t,y): 
	return model.NewCapacity[r,t,y] <= model.TotalAnnualMaxCapacityInvestment[r,t,y]
model.TotalAnnualMaxNewCapacityConstraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=TotalAnnualMaxNewCapacityConstraint_rule)

def TotalAnnualMinNewCapacityConstraint_rule(model,r,t,y): 
	return model.NewCapacity[r,t,y] >= model.TotalAnnualMinCapacityInvestment[r,t,y]
model.TotalAnnualMinNewCapacityConstraint = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=TotalAnnualMinNewCapacityConstraint_rule)       


#########   		Annual Activity Constraints	##############

def TotalAnnualTechnologyActivity_rule(model,r,t,y):
	return sum(model.RateOfTotalActivity[r,t,l,y]*model.YearSplit[l,y] for l in model.TIMESLICE) == model.TotalTechnologyAnnualActivity[r,t,y]
model.TotalAnnualTechnologyActivity = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=TotalAnnualTechnologyActivity_rule)

def TotalAnnualTechnologyActivityUpperLimit_rule(model,r,t,y):
	return model.TotalTechnologyAnnualActivity[r,t,y] <= model.TotalTechnologyAnnualActivityUpperLimit[r,t,y]
model.TotalAnnualTechnologyActivityUpperlimit = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=TotalAnnualTechnologyActivityUpperLimit_rule)

def TotalAnnualTechnologyActivityLowerLimit_rule(model,r,t,y):
	return model.TotalTechnologyAnnualActivity[r,t,y] >= model.TotalTechnologyAnnualActivityLowerLimit[r,t,y]
model.TotalAnnualTechnologyActivityLowerlimit = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=TotalAnnualTechnologyActivityLowerLimit_rule)


#########    		Total Activity Constraints 	##############

def TotalModelHorizonTechnologyActivity_rule(model,r,t):
	return sum(model.TotalTechnologyAnnualActivity[r,t,y] for y in model.YEAR) == model.TotalTechnologyModelPeriodActivity[r,t]
model.TotalModelHorizonTechnologyActivity = Constraint(model.REGION, model.TECHNOLOGY, rule=TotalModelHorizonTechnologyActivity_rule)

def TotalModelHorizonTechnologyActivityUpperLimit_rule(model,r,t):
	return model.TotalTechnologyModelPeriodActivity[r,t] <= model.TotalTechnologyModelPeriodActivityUpperLimit[r,t]
model.TotalModelHorizonTechnologyActivityUpperLimit = Constraint(model.REGION, model.TECHNOLOGY, rule=TotalModelHorizonTechnologyActivityUpperLimit_rule)

def TotalModelHorizonTechnologyActivityLowerLimit_rule(model,r,t):
	return model.TotalTechnologyModelPeriodActivity[r,t] >= model.TotalTechnologyModelPeriodActivityLowerLimit[r,t]
model.TotalModelHorizonTechnologyActivityLowerLimit = Constraint(model.REGION, model.TECHNOLOGY, rule=TotalModelHorizonTechnologyActivityLowerLimit_rule)


#########   		Emissions Accounting		##############


def AnnualEmissionProductionByMode_rule(model,r,t,e,m,y):
	if model.EmissionActivityRatio[r,t,e,m,y] != 0:
		return model.EmissionActivityRatio[r,t,e,m,y]*model.TotalAnnualTechnologyActivityByMode[r,t,m,y] == model.AnnualTechnologyEmissionByMode[r,t,e,m,y]
	else:
		return model.AnnualTechnologyEmissionByMode[r,t,e,m,y] == 0
model.AnnualEmissionProductionByMode = Constraint(model.REGION, model.TECHNOLOGY, model.EMISSION, model.MODE_OF_OPERATION, model.YEAR, rule=AnnualEmissionProductionByMode_rule)

def AnnualEmissionProduction_rule(model,r,t,e,y):
	return sum(model.AnnualTechnologyEmissionByMode[r,t,e,m,y] for m in model.MODE_OF_OPERATION) == model.AnnualTechnologyEmission[r,t,e,y]
model.AnnualEmissionProduction = Constraint(model.REGION, model.TECHNOLOGY, model.EMISSION, model.YEAR, rule=AnnualEmissionProduction_rule)

def EmissionPenaltyByTechAndEmission_rule(model,r,t,e,y):
	return model.AnnualTechnologyEmission[r,t,e,y]*model.EmissionsPenalty[r,e,y] == model.AnnualTechnologyEmissionPenaltyByEmission[r,t,e,y]
model.EmissionPenaltyByTechAndEmission = Constraint(model.REGION, model.TECHNOLOGY, model.EMISSION, model.YEAR, rule=EmissionPenaltyByTechAndEmission_rule)

def EmissionsPenaltyByTechnology_rule(model,r,t,y):
	return sum(model.AnnualTechnologyEmissionPenaltyByEmission[r,t,e,y] for e in model.EMISSION) == model.AnnualTechnologyEmissionsPenalty[r,t,y]
model.EmissionsPenaltyByTechnology = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=EmissionsPenaltyByTechnology_rule)

def DiscountedEmissionsPenaltyByTechnology_rule(model,r,t,y):
	return model.AnnualTechnologyEmissionsPenalty[r,t,y]/((1+model.DiscountRate[r])**(y-min(model.YEAR)+0.5)) == model.DiscountedTechnologyEmissionsPenalty[r,t,y]
model.DiscountedEmissionsPenaltyByTechnology = Constraint(model.REGION, model.TECHNOLOGY, model.YEAR, rule=DiscountedEmissionsPenaltyByTechnology_rule)

def EmissionsAccounting1_rule(model,r,e,y):
	return sum(model.AnnualTechnologyEmission[r,t,e,y] for t in model.TECHNOLOGY) == model.AnnualEmissions[r,e,y]
model.EmissionsAccounting1 = Constraint(model.REGION, model.EMISSION, model.YEAR, rule=EmissionsAccounting1_rule)

def EmissionsAccounting2_rule(model,r,e):
	return sum(model.AnnualEmissions[r,e,y] for y in model.YEAR) == model.ModelPeriodEmissions[r,e] - model.ModelPeriodExogenousEmission[r,e]
model.EmissionsAccounting2 = Constraint(model.REGION, model.EMISSION, rule=EmissionsAccounting2_rule)

def AnnualEmissionsLimit_rule(model,r,e,y):
	return model.AnnualEmissions[r,e,y] + model.AnnualExogenousEmission[r,e,y] <= model.AnnualEmissionLimit[r,e,y]
model.AnnualEmissionsLimit = Constraint(model.REGION, model.EMISSION, model.YEAR, rule=AnnualEmissionsLimit_rule)

def ModelPeriodEmissionsLimit_rule(model,r,e):
	return model.ModelPeriodEmissions[r,e] <= model.ModelPeriodEmissionLimit[r,e]
model.ModelPeriodEmissionsLimit = Constraint(model.REGION, model.EMISSION, rule=ModelPeriodEmissionsLimit_rule)


#########   		Reserve Margin Constraint	############## NTS: Should change demand for production

def ReserveMargin_TechnologiesIncluded_rule(model,r,l,y):
	return (sum((model.TotalAnnualCapacity[r,t,y]*model.ReserveMarginTagTechnology[r,t,y]*model.CapacityToActivityUnit[r,t]) for t in model.TECHNOLOGY) == model.TotalCapacityInReserveMargin[r,y])
ReserveMargin_TechnologiesIncluded = Constraint(model.REGION, model.TIMESLICE, model.YEAR, rule=ReserveMargin_TechnologiesIncluded_rule)

def ReserveMargin_FuelsIncluded_rule(model,r,l,y):
	return sum((model.RateOfProduction[r,l,f,y]*model.ReserveMarginTagFuel) for f in model.FUEL) == model.DemandNeedingReserveMargin[r,l,y]
ReserveMargin_FuelsIncluded = Constraint(model.REGION, model.TIMESLICE, model.YEAR, rule=ReserveMargin_FuelsIncluded_rule)

def ReserveMarginConstraint_rule(model,r,l,y):
	return model.DemandNeedingReserveMargin[r,l,y]*model.ReserveMargin[r,y] <= model.TotalCapacityInReserveMargin[r,y]
ReserveMarginConstraint = Constraint(model.REGION, model.TIMESLICE, model.YEAR, rule=ReserveMarginConstraint_rule)


# modeldata = ModelData()
# modeldata.add = ('OSeMOSYS_2015_08_27_Pyomo.dat')
# modeldata.read(model)

opt = SolverFactory('cplex')

instance = model.create_instance(os.getcwd() + '\UTOPIA_2015_08_27.dat')
results = opt.solve(instance)
# results.write()
#model.solutions.load_from(results)
instance.write('problem.lp', io_options={'symbolic_solver_labels':True})

# def pyomo_postprocess(options=None,instance=None,results=None):
	# instance.solutions.load_from(results)
	# with open('C:\OSeMOSYS_Pyomo\pyomo_test_2015-08-27.txt', 'w') as f:
		# f.write ('{} {} {}\n'.format("objective ", value(instance.OBJ)))
		# for v in instance.component_objects(Var, active=True):
			# varobject = getattr(instance, str(v))
			# for index in varobject:
				# f.write ('{} {}\n'.format(v, varobject[index].value))
	# close()

		
# instance = model.create_instance()
#instance.display()

#############################################################

#########   		RE Production Target		############## NTS: Should change demand for production
#
# s.t. RE1_FuelProductionByTechnologyAnnual{model.REGION, model.TECHNOLOGY, model.FUEL, model.YEAR}: sum{model.TIMESLICE} ProductionByTechnology[r,l,t,f,y] = ProductionByTechnologyAnnual[r,t,f,y];
# s.t. RE2_TechIncluded{model.REGION, model.YEAR}: sum{model.TECHNOLOGY, model.FUEL} ProductionByTechnologyAnnual[r,t,f,y]*RETagTechnology[r,t,y] = TotalREProductionAnnual[r,y];
# s.t. RE3_FuelIncluded{model.REGION, model.YEAR}: sum{model.TIMESLICE, model.FUEL} RateOfDemand[r,l,f,y]*YearSplit[l,y]*RETagFuel[r,f,y] = RETotalDemandOfTargetFuelAnnual[r,y]; 
# s.t. RE4_EnergyConstraint{model.REGION, model.YEAR}:REMinProductionTarget[r,y]*RETotalDemandOfTargetFuelAnnual[r,y] <= TotalREProductionAnnual[r,y];
# s.t. RE5_FuelUseByTechnologyAnnual{model.REGION, model.TECHNOLOGY, model.FUEL, model.YEAR}: sum{model.TIMESLICE} RateOfUseByTechnology[r,l,t,f,y]*YearSplit[l,y] = UseByTechnologyAnnual[r,t,f,y];
#
###########################################################################################
#
#solve;
#
#########################################################################################################
#																										#
# 	Summary results tables below are printed to a comma-separated file called "SelectedResults.csv"		#
#	For a full set of results please see "Results.txt"													#
#	If you don't want these printed, please comment-out or delete them.									#
#																										#
#########################################################################################################
#
#	table result{(f,t) in s} OUT "...": f~FROM, t~TO, x[f,t]~FLOW;
#	table result{model.YEAR, model.REGION} OUT "CSV" "Output.csv": y~YEARS, r~REGION, TotalDiscountedCost[y,r];
#
####	Summary results 	###
#
###		Total costs and emissions by region	###
#
# printf "\n" > "SelectedResults.csv";
# printf "Summary" >> "SelectedResults.csv";
# for {model.REGION} 	{printf ",%s", r >> "SelectedResults.csv";
					# }
# printf "\n" >> "SelectedResults.csv";
# printf "Emissions" >> "SelectedResults.csv";
# printf "\n" >> "SelectedResults.csv";
# for {model.REGION} 	{
					# for {model.EMISSION} 	{
											# printf ",%s", e >> "SelectedResults.csv";
											# printf ",%g", ModelPeriodEmissions[r,e] >> "SelectedResults.csv";
											# printf "\n" >> "SelectedResults.csv";
											# }
					# }
# printf "\n" >> "SelectedResults.csv";
# printf "Cost" >> "SelectedResults.csv";
# for {model.REGION} {printf ",%g", ModelPeriodCostByRegion[r] >> "SelectedResults.csv";
# }
# printf "\n" >> "SelectedResults.csv";
# #
# ### 	Time Independent demand	###
# #
# printf "\n" >> "SelectedResults.csv";
# printf "TID Demand" >> "SelectedResults.csv";
# printf "\n" >> "SelectedResults.csv";
# printf "\n" >> "SelectedResults.csv";
	# for {model.REGION} 	{printf ",%s", r >> "SelectedResults.csv";
						# printf "\n" >> "SelectedResults.csv";
						# for {model.FUEL} {printf "\n" >> "SelectedResults.csv";
										# printf ",%s", f >> "SelectedResults.csv";
										# printf "\n" >> "SelectedResults.csv";
										# for {model.YEAR } 	{
															# printf "%g", y >> "SelectedResults.csv";
															# printf ",%g", AccumulatedAnnualDemand[r,f,y] >> "SelectedResults.csv";
															# printf "\n" >> "SelectedResults.csv";
															# }
											# }
						# }
# #
# ### 	Time Dependent demand	###
# #
# printf "\n" >> "SelectedResults.csv";
# printf "Time Dependent Demand (Energy Units)" >> "SelectedResults.csv";
# printf "\n" >> "SelectedResults.csv";
# printf "\n" >> "SelectedResults.csv";
	# for {model.REGION} {printf ",%s", r >> "SelectedResults.csv";
						# printf "\n" >> "SelectedResults.csv";
						# for {model.FUEL} {printf ",%s", f >> "SelectedResults.csv";
										# printf "\n" >> "SelectedResults.csv";
										# for {model.TIMESLICE}	{
																# printf ",%s", l >> "SelectedResults.csv";
																# }
										# printf "\n" >> "SelectedResults.csv";
										# for {model.YEAR } 	{
															# printf "%g", y >> "SelectedResults.csv";
															# for { model.TIMESLICE} 	{
																					# printf ",%g", RateOfDemand[r,l,f,y]*YearSplit[l,y] >> "SelectedResults.csv";
																					# }
															# printf "\n" >> "SelectedResults.csv";
															# }
										# }
						# }
# #
# ### 	Time Dependent production ###
# #
# printf "\n" >> "SelectedResults.csv";
# printf "Time Dependent Production (Energy Units) Test" >> "SelectedResults.csv";
# printf "\n" >> "SelectedResults.csv";
# printf "\n" >> "SelectedResults.csv";
	# for {model.REGION} {printf ",%s", r >> "SelectedResults.csv";
						# printf "\n" >> "SelectedResults.csv";
						# for {model.FUEL} {printf ",%s", f >> "SelectedResults.csv";
										# printf "\n" >> "SelectedResults.csv";
										# for {model.TIMESLICE}	{
																# printf ",%s", l >> "SelectedResults.csv";
																# }
										# printf "\n" >> "SelectedResults.csv";
										# for {model.YEAR } 	{
															# printf "%g", y >> "SelectedResults.csv";
															# for { model.TIMESLICE} 	{
																					# printf ",%g", Production[r,l,f,y] >> "SelectedResults.csv";
																					# }
															# printf "\n" >> "SelectedResults.csv";
															# }
										# }
						# }
# #
# ####	Total Annual Capacity	###
# #
# printf "\n" >> "SelectedResults.csv";
# printf "TotalAnnualCapacity (Capacity Units)" >> "SelectedResults.csv";
# printf "\n" >> "SelectedResults.csv";
# for {model.TECHNOLOGY} {printf ",%s", t >> "SelectedResults.csv";}
# printf "\n" >> "SelectedResults.csv";
# for {model.REGION}	{
		# for { model.YEAR } {
							# printf "%g", y >> "SelectedResults.csv";
							# for { model.TECHNOLOGY } {
													# printf ",%g", TotalCapacityAnnual[r,t,y] >> "SelectedResults.csv";
													# }
							# printf "\n" >> "SelectedResults.csv";
							# }
					# }
# #
# ####	New Annual Capacity	###
# #
# printf "\n" >> "SelectedResults.csv";
# printf "NewCapacity (Capacity Units )" >> "SelectedResults.csv";
# printf "\n" >> "SelectedResults.csv";
# printf "\n" >> "SelectedResults.csv";
# for {model.TECHNOLOGY} 	{printf ",%s", t >> "SelectedResults.csv";}
# printf "\n" >> "SelectedResults.csv";
# for {model.REGION}	{
					# for { model.YEAR } 	{
										# printf "%g", y >> "SelectedResults.csv";
										# for { model.TECHNOLOGY } 	{
																	# printf ",%g", NewCapacity[r,t,y] >> "SelectedResults.csv";
																	# }
										# printf "\n" >> "SelectedResults.csv";
										# }
					# }
# #
# ### Annual Production ###
# #
# printf "\n" >> "SelectedResults.csv";
# printf "\n" >> "SelectedResults.csv";
# printf "Annual Production (Energy Units)" >> "SelectedResults.csv";
# printf "\n" >> "SelectedResults.csv";
# for {model.REGION} 	{printf ",%s", r >> "SelectedResults.csv";
					# printf "\n" >> "SelectedResults.csv";
					# for {model.TECHNOLOGY} 	{printf "%s", t >> "SelectedResults.csv";
											# for {model.FUEL}{printf",%s",f >> "SelectedResults.csv";
															# }
											# printf "\n" >> "SelectedResults.csv";
											# for {model.YEAR } 	{
																# printf "%g", y >> "SelectedResults.csv";
																# for {model.FUEL}{
																				# printf ",%g", ProductionByTechnologyAnnual[r,t,f,y] >> "SelectedResults.csv";
																				# }
																# printf "\n" >> "SelectedResults.csv";
																# }
						# printf "\n" >> "SelectedResults.csv";
											# }
					# }
# #
# ### Annual Use ###
# #
# printf "Annual Use (Energy Units)" >> "SelectedResults.csv";
# printf "\n" >> "SelectedResults.csv";
# for {model.REGION} {printf ",%s", r >> "SelectedResults.csv";
					# printf "\n" >> "SelectedResults.csv";
					# for {model.TECHNOLOGY} 	{printf "%s", t >> "SelectedResults.csv";
											# for {model.FUEL}{printf",%s",f >> "SelectedResults.csv";
															# }
											# printf "\n" >> "SelectedResults.csv";
											# for {model.YEAR } 	{
																# printf "%g", y >> "SelectedResults.csv";
																# for {model.FUEL}{
																				# printf ",%g", UseByTechnologyAnnual[r,t,f,y] >> "SelectedResults.csv";
																				# }
																# printf "\n" >> "SelectedResults.csv";
																# }
						# printf "\n" >> "SelectedResults.csv";
											# }
					# }
# #
# ###		Technology Production in each TS ###
# #
# printf "\n" >> "SelectedResults.csv";
# printf "ProductionByTechnology (Energy Units)" >> "SelectedResults.csv";
# printf "\n" >> "SelectedResults.csv";
# printf "\n" >> "SelectedResults.csv";
# for {model.REGION} {printf ",%s", r >> "SelectedResults.csv";
	# printf "\n" >> "SelectedResults.csv";
	# for {model.TECHNOLOGY} {printf "%s", t >> "SelectedResults.csv";
					# for {model.FUEL}{printf",%s",f >> "SelectedResults.csv";
						# for {model.TIMESLICE}{
							# printf ",%s", l >> "SelectedResults.csv";
						# }
					# }
					# printf "\n" >> "SelectedResults.csv";
					# for {model.YEAR } {
						# printf "%g", y >> "SelectedResults.csv";
						# for {model.FUEL}{printf "," >> "SelectedResults.csv";
							# for { model.TIMESLICE} {
										# printf ",%g", ProductionByTechnology[r,l,t,f,y] >> "SelectedResults.csv";
								# }
						# }
						# printf "\n" >> "SelectedResults.csv";
					# }
	# }
# }
# #
# ###		Technology Use in each TS	###
# #
# printf "\n" >> "SelectedResults.csv";
# printf "Use By Technology (Energy Units)" >> "SelectedResults.csv";
# printf "\n" >> "SelectedResults.csv";
# printf "\n" >> "SelectedResults.csv";
# for {model.REGION} {printf ",%s", r >> "SelectedResults.csv";
	# printf "\n" >> "SelectedResults.csv";
	# for {model.TECHNOLOGY} {printf "%s", t >> "SelectedResults.csv";
					# for {model.FUEL}{printf",%s",f >> "SelectedResults.csv";
						# for {model.TIMESLICE}{
							# printf ",%s", l >> "SelectedResults.csv";
						# }
					# }
					# printf "\n" >> "SelectedResults.csv";
					# for {model.YEAR } {
						# printf "%g", y >> "SelectedResults.csv";
						# for {model.FUEL}{printf "," >> "SelectedResults.csv";
							# for { model.TIMESLICE} {
										# printf ",%g", UseByTechnology[r,l,t,f,y] >> "SelectedResults.csv";
								# }
						# }
						# printf "\n" >> "SelectedResults.csv";
					# }
	# }
# }
# #
# ###		Total Annual Emissions	###
# #
# printf "\n" >> "SelectedResults.csv";
# printf "Annual Emissions (Emissions Units)" >> "SelectedResults.csv";
# printf "\n" >> "SelectedResults.csv";
	# for {model.REGION} 	{printf ",%s", r >> "SelectedResults.csv";
						# printf "\n" >> "SelectedResults.csv";
						# for {model.EMISSION} 	{printf ",%s", e >> "SelectedResults.csv";
												# printf "\n" >> "SelectedResults.csv";
												# printf "\n" >> "SelectedResults.csv";
												# for {model.YEAR } 	{
																	# printf "%g", y >> "SelectedResults.csv";
																	# printf ",%g", AnnualEmissions[r,e,y]>> "SelectedResults.csv";
																	# printf "\n" >> "SelectedResults.csv";
																	# }
												# }
						# }
# #
# ### Annual Emissions by Technology ###
# #
# printf "\n" >> "SelectedResults.csv";
# printf "Annual Emissions by Technology (Emissions Units)" >> "SelectedResults.csv";
# printf "\n" >> "SelectedResults.csv";
# for {model.REGION} {printf ",%s", r >> "SelectedResults.csv";
					# printf "\n" >> "SelectedResults.csv";
					# for {model.TECHNOLOGY} 	{printf "%s", t >> "SelectedResults.csv";
											# for {model.EMISSION}{printf",%s",e >> "SelectedResults.csv";
															# }
											# printf "\n" >> "SelectedResults.csv";
											# for {model.YEAR } 	{
																# printf "%g", y >> "SelectedResults.csv";
																# for {model.EMISSION}{
																				# printf ",%g", AnnualTechnologyEmission[r,t,e,y] >> "SelectedResults.csv";
																				# }
																# printf "\n" >> "SelectedResults.csv";
																# }
						# printf "\n" >> "SelectedResults.csv";
											# }
					# }						
# end;