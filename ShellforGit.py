# -*- coding: utf-8 -*-
"""
This program automatically extracts and analyses data from a database of AIDS Data.

Data is from:
US Department of Health and Human Services (US DHHS), Centers for Disease Control and Prevention (CDC), National Center for HIV, STD and TB Prevention (NCHSTP), AIDS Public Information Data Set (APIDS) US Surveillance Data for 1981-2002, CDC WONDER On-line Database, December 2005. Accessed at http://wonder.cdc.gov/aids-v2002.html on Mar 9, 2017 2:26:39 PM"

Program was written for analysis of the database and is provided as is.

"""
import pypyodbc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from AIDSAnalysisProcedures import CreateDataGrid, contourplotVitalAge,contourplotVital,contourplotHIVExpByAgeLogNorm,surface3dAIDSByAgeGroup,contourplotAIDSByAgeGroup,contourplotAIDSByAgeGroupLogNorm,contourplotHIVExpByYear,contourplotHIVExpByYearLogNorm,contourplotHIVExpByAge

plt.close()

#using pypyodbc

#Connect to database (enter your own driver and Database path) and generate cursor

conn_str = r'DRIVER={};DBQ=;'
cnxn = pypyodbc.connect(conn_str)
crsr = cnxn.cursor()

#Extract Table Names
Table_details = []
for row in crsr.columns():
    if 'MSys' not in row[2]:    #ignore access default databases/tables
        Table_details.append((row[2],row[3]))
np_tabledetails=np.array(Table_details)
Table_names = np.unique(np_tabledetails[:,0])


#This code currently assumes the first table in the database
TableChoice = Table_names[0]

#Extract all table column headings
Column_names = np_tabledetails[np_tabledetails[:,0]==TableChoice,1]

#Extract all the unique column entries and their frequency into a dataframe and save
df_BigCount=pd.DataFrame()
for name in Column_names[1:]:
    #find all the unique values in the column, including nulls
    sql = 'SELECT ' + str(name) + ', COUNT(*) FROM ' + str(TableChoice) + ' AS COUNT GROUP BY ' + str(name)
    BigCount = crsr.execute(sql).fetchall()
    df_interBigCount=pd.DataFrame(BigCount)
    df_interBigCount['Column']=str(name)
    df_BigCount=pd.concat([df_BigCount, df_interBigCount])
df_BigCount=df_BigCount[['Column',0,1]]

#DATA SETUP FOR ANALYSIS

#Set up a SQL string that extracts only complete data for analysis
sql = 'SELECT LOCATION, MONTH_DIAGNOSED_CODE, Age_at_Diagnosis_Code, HIV_Exposure_Category_Code, Vital_Status_Code, Cases FROM ' + str(TableChoice) + ' WHERE (LOCATION IS NOT NULL AND MONTH_DIAGNOSED_CODE IS NOT NULL AND Age_at_Diagnosis_Code IS NOT NULL AND HIV_Exposure_Category_Code IS NOT NULL AND Vital_Status_Code IS NOT NULL AND Cases IS NOT NULL)'
result = crsr.execute(sql).fetchall()

#Take the results and format them into a DataFrame with both string (location) and numeric (rest) data
df_result=pd.DataFrame(result)
#Replace hexadecimal age range code with numbers
df_result.iloc[:][2]=df_result.iloc[:][2].replace(['A','B','C'],['10','11','12'])
 #Convert Month code to decimal number: from YYYY/MM (1995/01/02/03=1995/Jan/Feb/Mar)) to YYYY.MM (1995/0.0/0.083/0.0167 (Jan/Feb/Mar)
df_result.iloc[:][1]=df_result.iloc[:][1].replace(['/All Months','/01','/02','/03','/04','/05','/06','/07','/08','/09','/10','/11','/12'],['.000','.000','.083','.167','.250','.333','.417','.500','.583','.667','.750','.833','.917'],regex=True)
#convert numeric columns saved as strings to numbers
df_result.iloc[:][1]=df_result.iloc[:][1].apply(pd.to_numeric)#Year of diagnosis
df_result.iloc[:][2]=df_result.iloc[:][2].apply(pd.to_numeric)#Age at diagnosis code
df_result.iloc[:][3]=df_result.iloc[:][3].apply(pd.to_numeric)#HIV Exposure Category code
df_result.iloc[:][4]=df_result.iloc[:][4].apply(pd.to_numeric)#Vital Status Code
df_result.iloc[:][5]=df_result.iloc[:][5].apply(pd.to_numeric)#Number of cases

#Create the labels for any sort of plot, etc.  The code number in the database acts as the index of the list, which is why "None" was added to the HIV Exposure category.  There is no category 6, as well.
Vital_Code_Label = ['Alive Before 2001', 'Dead Before 2001']
Age_At_Diagnosis_Label = [	'< 1 Year Old',
							'1-12 Years Old',
							'13-19 Years Old',
							'20-24 Years Old',
							'25-29 Years Old',
							'30-34 Years Old',
							'35-39 Years Old \n or Age is Missing',
							'40-44 Years Old',
							'45-49 Years Old',
							'50-54 Years Old',
							'55-59 Years Old',
							'60-64 Years Old',
							'65+ Years Old']
HIV_Exposure_Category_Label = [
								'Male homosexual/\nbisexual contact',
								'IV drug use\n(female and hetero male)',
								'Male homo/bisexual\nand IV drug use',
								'Hemophilia/coagulation\ndisorder',
								'Heterosexual contact\n with HIV',
								'Receipt of blood, blood \ncomponents or tissue',
								'Risk not reported\n or identified',
								'Pediatric hemophilia',
								'Mother with HIV\n or HIV risk',
								'Pediatric receipt\n of blood',
								'Pediatric risk not\n reported or identified']

#Data analysis and plots

#Bar plot of age at diagnosis for all years
np_AgeAtDiag=np.array([df_result.iloc[:][2], df_result.iloc[:][5]])
AgeResult=np.zeros((13,2))
for index in range(0,13):
    AgeResult[index,0]=index
    AgeResult[index,1]=sum(np_AgeAtDiag[1,np_AgeAtDiag[0,:]==index])
plt.close()
fig = plt.figure()
plt.bar(AgeResult[:,0],AgeResult[:,1])
plt.xticks(AgeResult[:,0],Age_At_Diagnosis_Label, rotation='vertical')
plt.ylabel('Number of Diagnoses')
plt.title('AIDS Diagnoses By Age Group: All Years')
plt.tight_layout()
plt.show()
Age_At_Diagnosis_Code=AgeResult[:,0]

#Surface and contour plot of age at diagnosis for per reporting year
#Separate the diagnoses into bins based on year and age bracket.
#Create the grid for plotting

#Take columns 1,2,5: Year of Diagnosis, Age at Diagnosis, and Cases
np_AgeAtDiagByYear=np.array([df_result.iloc[:][1], df_result.iloc[:][2], df_result.iloc[:][5]])
#create Datagrid
datagridAgeAtDiag=CreateDataGrid(np_AgeAtDiagByYear)

#plot results
x = np.unique(np_AgeAtDiagByYear[0,:])
y = np.unique(np_AgeAtDiagByYear[1,:])
z = datagridAgeAtDiag

surface3dAIDSByAgeGroup(x,y,z,Age_At_Diagnosis_Label)
contourplotAIDSByAgeGroup(x,y,z,Age_At_Diagnosis_Label,AgeResult[:,0])
contourplotAIDSByAgeGroupLogNorm(x,y,z,Age_At_Diagnosis_Label,AgeResult[:,0])

#Bar plot of all diagnoses by year
plt.close()
fig = plt.figure()
plt.bar(x,datagridAgeAtDiag.sum(axis=1),width=0.1)
plt.xlabel('Year')
plt.ylabel('Number of Diagnoses')
plt.title('AIDS Diagnoses By Year')
plt.tight_layout()
plt.xlim([1980,2005])
plt.show()

#Bar plot of cumulative diagnoses by year
plt.close()
fig = plt.figure()
plt.bar(x,np.cumsum(datagridAgeAtDiag.sum(axis=1)),width=0.1)
plt.xlabel('Year')
plt.ylabel('Cumulative Diagnoses')
plt.title('Cumulative AIDS Diagnoses By Year')
plt.tight_layout()
plt.xlim([1980,2005])
plt.show()



#Take columns 1,3,5: Year of Diagnosis, HIV Exposure Category, and Cases
#Bar plot of HIV Exposure code for all years
np_HIVExposeCat=np.array([df_result.iloc[:][3], df_result.iloc[:][5]])
HIVArray=np.zeros((13,2))
for index in range(0,13):
    HIVArray[index,0]=index
    HIVArray[index,1]=sum(np_HIVExposeCat[1,np_HIVExposeCat[0,:]==index])
#There are two categories labels that are created but unused: 0 and 6.  Renive and refactor
HIVArray = np.delete(HIVArray,6,axis=0)
HIVArray = np.delete(HIVArray,0,axis=0)
for index in range(len(HIVArray)):
    HIVArray[index,0]=index

#Bar Plot
plt.close()
fig = plt.figure()
plt.bar(HIVArray[:,0],HIVArray[:,1])
plt.xticks(HIVArray[:,0],HIV_Exposure_Category_Label, rotation='vertical')
plt.ylabel('Number of Diagnoses')
plt.title('AIDS Diagnoses By HIV Exposure Category: All Years')
plt.tight_layout()
plt.show()

#Bar Plot log scale
plt.close()
fig = plt.figure()
plt.bar(HIVArray[:,0],HIVArray[:,1],log=True)
plt.xticks(HIVArray[:,0],HIV_Exposure_Category_Label, rotation='vertical')
plt.ylabel('Number of Diagnoses')
plt.title('AIDS Diagnoses By HIV Exposure Category: All Years')
plt.tight_layout()
plt.show()

np_HIVExposeCatByYear=np.array([df_result.iloc[:][1], df_result.iloc[:][3], df_result.iloc[:][5]])
#create Datagrid
datagridHIVExpByYear=CreateDataGrid(np_HIVExposeCatByYear)

#plot results
x = np.unique(np_HIVExposeCatByYear[0,:])
y = [0,1,2,3,4,5,6,7,8,9,10]
z = datagridHIVExpByYear

contourplotHIVExpByYear(x,y,z,HIV_Exposure_Category_Label,y)
z[z==0]=0.1 #replace all zeros with 0.1 in order to produce a prettier contour graph
contourplotHIVExpByYearLogNorm(x,y,z,HIV_Exposure_Category_Label,y)


#Take columns 2,3,5: Age at Diagnosis, HIV Exposure Category, and Cases
np_HIVExposeCatByAge=np.array([df_result.iloc[:][2], df_result.iloc[:][3], df_result.iloc[:][5]])
#create Datagrid
datagridHIVExpByAge=CreateDataGrid(np_HIVExposeCatByAge)

#plot results
x = np.unique(np_HIVExposeCatByAge[0,:])
y = [0,1,2,3,4,5,6,7,8,9,10]
z = datagridHIVExpByAge

contourplotHIVExpByAge(x,y,z,HIV_Exposure_Category_Label,y,Age_At_Diagnosis_Label,Age_At_Diagnosis_Code)
z[z==0]=0.1
contourplotHIVExpByAgeLogNorm(x,y,z,HIV_Exposure_Category_Label,y,Age_At_Diagnosis_Label,Age_At_Diagnosis_Code)


#Take columns 1,3,4,5: Year of Diagnosis, HIV Exposure, Vital Stats, and Cases
np_VitalYear=np.array([df_result.iloc[:][1], df_result.iloc[:][3], df_result.iloc[:][4], df_result.iloc[:][5]])

#Separate data based upon vital stats.  Set cases to zero so all dates can be represented in subsequent analysis
np_VitalYearZero=np_VitalYear
np_VitalYearZero[3,np_VitalYear[2,:]==1]=0
np_VitalYearZero=np.delete(np_VitalYearZero,2,axis=0)
datagridVitalYearZero=CreateDataGrid(np_VitalYearZero)

#Have to repeat due to a subtle bug in which both vital years were affected by the zeroing command
np_VitalYear=np.array([df_result.iloc[:][1], df_result.iloc[:][3], df_result.iloc[:][4], df_result.iloc[:][5]])
np_VitalYearOne=np_VitalYear
np_VitalYearOne[3,np_VitalYear[2,:]==0]=0
np_VitalYearOne=np.delete(np_VitalYearOne,2,axis=0)
datagridVitalYearOne=CreateDataGrid(np_VitalYearOne)

totalVitalDataGrid=datagridVitalYearZero+datagridVitalYearOne

#Calculate percentage of diagnoses dead at 2001
PercentVitalYearOne = np.round(np.divide(datagridVitalYearOne,totalVitalDataGrid,out=np.zeros_like(datagridVitalYearOne), where=totalVitalDataGrid!=0),2)

#plot results
x = np.unique(np_VitalYear[0,:])
y = [0,1,2,3,4,5,6,7,8,9,10]
z = PercentVitalYearOne

contourplotVital(x,y,z,HIV_Exposure_Category_Label,y)




#Take columns 1,2,4,5: Year of Diagnosis, Age At Exposure, Vital Stats, and Cases
np_VitalAgeYear=np.array([df_result.iloc[:][1], df_result.iloc[:][2], df_result.iloc[:][4], df_result.iloc[:][5]])

#Separate data based upon vital stats.  Set cases to zero so all dates can be represented in subsequent analysis
np_VitalAgeYearZero=np_VitalAgeYear
np_VitalAgeYearZero[3,np_VitalAgeYear[2,:]==1]=0
np_VitalAgeYearZero=np.delete(np_VitalAgeYearZero,2,axis=0)
datagridVitalAgeYearZero=CreateDataGrid(np_VitalAgeYearZero)

#Have to repeat due to a subtle bug in which both vital years were affected by the zeroing command
np_VitalAgeYear=np.array([df_result.iloc[:][1], df_result.iloc[:][2], df_result.iloc[:][4], df_result.iloc[:][5]])
np_VitalAgeYearOne=np_VitalAgeYear
np_VitalAgeYearOne[3,np_VitalAgeYear[2,:]==0]=0
np_VitalAgeYearOne=np.delete(np_VitalAgeYearOne,2,axis=0)
datagridVitalAgeYearOne=CreateDataGrid(np_VitalAgeYearOne)

totalVitalAgeDataGrid=datagridVitalAgeYearZero+datagridVitalAgeYearOne

#Calculate percentage of diagnoses dead at 2001
PercentVitalAgeYearOne = np.round(np.divide(datagridVitalAgeYearOne,totalVitalAgeDataGrid,out=np.zeros_like(datagridVitalAgeYearOne), where=totalVitalAgeDataGrid!=0),2)

#plot results
x = np.unique(np_VitalAgeYear[0,:])
y = np.unique(np_VitalAgeYear[1,:])
z = PercentVitalAgeYearOne

contourplotVitalAge(x,y,z,Age_At_Diagnosis_Label,AgeResult[:,0])

#Bar chart showing total diagnoses and deaths by 2000
totalOne=datagridVitalAgeYearOne.sum(axis=1)
totalYear=totalVitalAgeDataGrid.sum(axis=1)

plt.close()
fig = plt.figure()
p1 = plt.bar(x,totalYear, width=0.1)
p2 = plt.bar(x,totalOne,width=0.1,color='#d62728')
plt.ylabel('Number of Diagnoses')
plt.xlabel('Year')
plt.title('AIDS Diagnoses By Year and Mortality by 2000')
plt.legend((p1[0],p2[0]),('Total Diagnoses','Dead by 2000'))
plt.xlim([1980,2005])

#Bar chart showing total cases and deaths by 2000
totalOne=datagridVitalAgeYearOne.sum(axis=1)
totalYear=totalVitalAgeDataGrid.sum(axis=1)

#create a fake data set to put on top of deaths from 2000 on becaus otherwise it fills to 2003 with a flat line.
yq=np.array(x)
yq[yq>2000]=600000
yq[yq<2000]=0

plt.close()
fig = plt.figure()
p1 = plt.bar(x,np.cumsum(totalYear), width=0.1,color='b')
p2 = plt.bar(x,np.cumsum(totalOne),width=0.1,color='#d62728')
p3 = plt.bar(x,yq,width=0.1,color='b')
plt.ylabel('Total Diagnoses')
plt.xlabel('Year')
plt.title('Cumulative AIDS Diagnoses By Year and Mortality by 2000')
plt.legend((p1[0],p2[0]),('Total Diagnoses','Dead by 2000'))
plt.xlim([1980,2005])

cnxn.close()