# -*- coding: utf-8 -*-
"""
This program is a partner program to ShellforGit.py, which automatically extracts and analyses data from a database of AIDS Data.

Data is from:
US Department of Health and Human Services (US DHHS), Centers for Disease Control and Prevention (CDC), National Center for HIV, STD and TB Prevention (NCHSTP), AIDS Public Information Data Set (APIDS) US Surveillance Data for 1981-2002, CDC WONDER On-line Database, December 2005. Accessed at http://wonder.cdc.gov/aids-v2002.html on Mar 9, 2017 2:26:39 PM"

Program was written for analysis of the database and is provided as is.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib import cm


def CreateDataGrid(np_columnorganized):
     
    datagrid=np.zeros((np.unique(np_columnorganized[0,:]).shape[0],np.unique(np_columnorganized[1,:]).shape[0]))
    
    datagridindexYear=0
    for DiagYear in np.unique(np_columnorganized[0,:]):  #years
        datagridindexAge=0
        for AgeCode in np.unique(np_columnorganized[1,:]):  #Age Code
            Intermediate = np_columnorganized[:,np_columnorganized[0,:]==DiagYear]
            Final = Intermediate[:,Intermediate[1,:]==AgeCode]
            datagrid[datagridindexYear,datagridindexAge]=np.sum(Final,axis=1)[2]
            datagridindexAge=datagridindexAge + 1
        datagridindexYear = datagridindexYear + 1
    
    return datagrid

def surface3dAIDSByAgeGroup(x,y,z,labels):
    plt.close()
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    Q,R=np.meshgrid(x,y)
    ax.plot_surface(Q,R,z.T,cmap=cm.coolwarm,linewidth=0, antialiased=False)
    plt.xlim(1980,2005)
    plt.xlabel('Year of Diagnosis')
    plt.ylim(0,12)
    ax.set_yticklabels([labels[0],labels[2],labels[4],labels[6],labels[8],labels[10],labels[12]],rotation=-15,verticalalignment='baseline',horizontalalignment='left', fontsize=6)
    plt.title('AIDS Diagnoses By Age Group: All Years')
    ax.set_zlabel('Cases Diagnosed')
    plt.tight_layout()
    plt.show()
    

def contourplotAIDSByAgeGroup(x,y,z, labels,location):
    plt.close()
    fig = plt.figure()
    # contour the gridded data, plotting dots at the randomly spaced data points.
    #CS = plt.contour(x,y,z.T,15,linewidths=0.5,colors='k')
    CS = plt.contourf(x,y,z.T,15,cmap=plt.cm.jet)
    cbar = plt.colorbar() # draw colorbar
    plt.xlim(1981,2003)
    plt.xticks([1981,1985,1990,1995,2000, 2003],['1981','1985','1990','1995','2000','2003'])
    plt.xlabel('Year of Diagnosis')
    plt.ylim(0,12)
    plt.yticks(location,labels, rotation='horizontal')
    plt.title('AIDS Diagnoses By Age Group: All Years')
    cbar.set_label('Cases Diagnosed')
    plt.tight_layout()
    plt.show()
    
def contourplotAIDSByAgeGroupLogNorm(x,y,z,labels,location):
    plt.close()
    fig = plt.figure()
    # contour the gridded data, plotting dots at the randomly spaced data points.
    #CS = plt.contour(x,y,z.T,15,linewidths=0.5,colors='k')
    CS = plt.contourf(x,y,z.T,15,cmap=plt.cm.jet, norm=LogNorm())
    cbar = plt.colorbar() # draw colorbar
    plt.xlim(1981,2003)
    plt.xticks([1981,1985,1990,1995,2000, 2003],['1981','1985','1990','1995','2000','2003'])
    plt.xlabel('Year of Diagnosis')
    plt.ylim(0,12)
    plt.yticks(location,labels, rotation='horizontal')
    plt.title('AIDS Diagnoses By Age Group: All Years')
    cbar.set_label('Cases Diagnosed')
    plt.tight_layout()
    plt.show()

def contourplotHIVExpByYear(x,y,z, labels,location):
    plt.close()
    fig = plt.figure()
    # contour the gridded data, plotting dots at the randomly spaced data points.
    #CS = plt.contour(x,y,z.T,15,linewidths=0.5,colors='k')
    CS = plt.contourf(x,y,z.T,15,cmap=plt.cm.jet)
    cbar = plt.colorbar() # draw colorbar
    plt.xlim(1981,2003)
    plt.xticks([1981,1985,1990,1995,2000, 2003],['1981','1985','1990','1995','2000','2003'])
    plt.xlabel('Year of Diagnosis')
    plt.yticks(location,labels, rotation='horizontal',fontsize=8)
    plt.title('AIDS Diagnoses By HIV Exposure: All Years')
    cbar.set_label('Cases Diagnosed')
    plt.tight_layout()
    plt.show()
    
def contourplotHIVExpByYearLogNorm(x,y,z,labels,location):
    plt.close()
    fig = plt.figure()
    # contour the gridded data, plotting dots at the randomly spaced data points.
    #CS = plt.contour(x,y,z.T,15,linewidths=0.5,colors='k')
    CS = plt.contourf(x,y,z.T,15,cmap=plt.cm.jet, norm=LogNorm())
    cbar = plt.colorbar() # draw colorbar
    plt.xlim(1981,2003)
    plt.xticks([1981,1985,1990,1995,2000, 2003],['1981','1985','1990','1995','2000','2003'])
    plt.xlabel('Year of Diagnosis')
    plt.yticks(location,labels, rotation='horizontal', fontsize=8)
    plt.title('AIDS Diagnoses By HIV Exposure: All Years')
    cbar.set_label('Cases Diagnosed')
    plt.tight_layout()
    plt.show()
    

def contourplotHIVExpByAge(x,y,z, labels,location,labelsy,location2):
    plt.close()
    fig = plt.figure()
    # contour the gridded data, plotting dots at the randomly spaced data points.
   # CS = plt.contour(x,y,z.T,15,linewidths=0.5,colors='k')
    CS = plt.contourf(x,y,z.T,15,cmap=plt.cm.jet)
    cbar = plt.colorbar() # draw colorbar
    plt.xlabel('Age At Diagnosis')
    plt.xticks(location2,labelsy, rotation='vertical', fontsize=6)
    plt.yticks(location,labels, rotation='horizontal',fontsize=6)
    plt.title('AIDS Diagnoses By HIV Exposure Type and Age at Diagnosis')
    cbar.set_label('Cases Diagnosed')
    plt.tight_layout()
    plt.show()
    
def contourplotHIVExpByAgeLogNorm(x,y,z,labels,location,labelsy,location2):
    plt.close()
    fig = plt.figure()
    # contour the gridded data, plotting dots at the randomly spaced data points.
    #CS = plt.contour(x,y,z.T,15,linewidths=0.5,colors='k')
    CS = plt.contourf(x,y,z.T,15,cmap=plt.cm.jet, norm=LogNorm())
    cbar = plt.colorbar() # draw colorbar
    plt.xlabel('Age At Diagnosis')
    plt.xticks(location2,labelsy, rotation='vertical', fontsize=6)
    plt.yticks(location,labels, rotation='horizontal', fontsize=6)
    plt.title('AIDS Diagnoses By HIV Exposure Type and Age at Diagnosis')
    cbar.set_label('Cases Diagnosed')
    plt.tight_layout()
    plt.show()
    
def contourplotVital(x,y,z, labels,location):
    plt.close()
    fig = plt.figure()
    # contour the gridded data, plotting dots at the randomly spaced data points.
    #CS = plt.contour(x,y,z.T,15,linewidths=0.5,colors='k')
    CS = plt.contourf(x,y,z.T,15,cmap=plt.cm.jet)
    cbar = plt.colorbar() # draw colorbar
    plt.xlim(1982,2000)
    plt.xlabel('Year of Diagnosis')
    plt.xticks([1982,1985,1990,1995,2000],['1982','1985','1990','1995','2000'])
    plt.yticks(location,labels, rotation='horizontal',fontsize=8)
    plt.title('Case Mortality Percentage By Exposure and Year')
    cbar.set_label('Percent Mortality by 2001, All Causes')
    plt.tight_layout()
    plt.show()
    
def contourplotVitalAge(x,y,z, labels,location):
    plt.close()
    fig = plt.figure()
    # contour the gridded data, plotting dots at the randomly spaced data points.
    #CS = plt.contour(x,y,z.T,15,linewidths=0.5,colors='k')
    CS = plt.contourf(x,y,z.T,15,cmap=plt.cm.jet)
    cbar = plt.colorbar() # draw colorbar
    plt.xlim(1982,2000)
    plt.xlabel('Year of Diagnosis')
    plt.xticks([1982,1985,1990,1995,2000],['1982','1985','1990','1995','2000'])
    plt.yticks(location,labels, rotation='horizontal',fontsize=8)
    plt.title('Case Mortality Percentage By Age at Diagnosis and Year')
    cbar.set_label('Percent Mortality by 2001, All Causes')
    plt.tight_layout()
    plt.show()
