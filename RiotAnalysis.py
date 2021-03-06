# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 19:12:51 2016

@author: Annie Tran
"""

import pandas as pd
import numpy as np
import os

os.chdir('/Users/isarasuntichotinun/Desktop/ANNIE/CSC 591/riot_predictor/')
LAriots = pd.read_csv('SCAD_LA_32.csv')
#LAriots = pd.read_csv('SCAD_Africa_32.csv')

#https://www.numbeo.com/crime/rankings_by_country.jsp crime statistics
#drop the riots with pro-governent as issue
LAriots=LAriots[LAriots['issue1']!=11]

#Only riots after 2006
#LAriots=LAriots[LAriots['eyr']>=2006]

#dropping some columns
LAriots = LAriots.drop(LAriots.columns[[6, 7, 8, 9,10,11]], axis=1)
LAriots = LAriots.drop(LAriots.columns[[0,1]], axis=1)
LAriots = LAriots.drop('acd_quest',1)
LAriots = LAriots.drop('actor1',1)
LAriots = LAriots.drop('actor2',1)
LAriots = LAriots.drop('actor3',1)
LAriots = LAriots.drop('target2',1)
LAriots = LAriots.drop('cgovtarget',1)
LAriots = LAriots.drop('rgovtarget',1)
LAriots = LAriots.drop('repress',1)
LAriots = LAriots.drop('elocal',1)
LAriots = LAriots.drop('ilocal',1)
LAriots = LAriots.drop('sublocal',1)
LAriots = LAriots.drop('gislocnum',1)
LAriots = LAriots.drop('issue2',1)
LAriots = LAriots.drop('issue3',1)
LAriots = LAriots.drop('nsource',1)
LAriots = LAriots.drop('issuenote',1)
LAriots = LAriots.drop('acd_questionable',1)
LAriots = LAriots.drop('latitude',1)
LAriots = LAriots.drop('longitude',1)
LAriots = LAriots.drop('notes',1)
LAriots = LAriots.drop('coder',1)
LAriots = LAriots.drop('geo_comments',1)
LAriots = LAriots.drop('location_precision',1)
LAriots = LAriots.drop('id',1)
LAriots = LAriots.drop('eventid',1)
LAriots = LAriots.drop('eyr',1)
LAriots = LAriots.drop('ccode',1)
LAriots=LAriots[LAriots['etype']!=7] #get rid of pro-government violence
LAriots=LAriots[LAriots['etype']!=10] #get rid of intra-government violence
#LAriots=LAriots[LAriots['etype']!=8] #get rid of anti-government violence
#LAriots=LAriots[LAriots['etype']!=9] #get rid of extra-government violence
LAriots=LAriots[LAriots['issue1']!=13] #drop 'other' issue
LAriots=LAriots[LAriots['issue1']!=14] #drop 'unknown' issue

LAriots = LAriots.reset_index(drop=True)

#If it starts out as a riot, mark it as a riot:
LAriots['riot']=LAriots['etype'].map(lambda x: 0 if int(x) in {1, 2, 5, 6} else 1)

#if it escalates to a riot, mark it as a riot:
for i in range(len(LAriots['riot'])):
    if int(LAriots['escalation'].iloc[i]) in {3,4,8,9}:
        LAriots.set_value(i,'riot',1)

LAriots.to_csv('cleanedLA.csv', sep=',', index_col = False)
#LAriots.to_csv('cleanedAfrica.csv', sep=',')


#rename columns
LAriots.rename(columns={'countryname': 'country', 'target1': 'target','issue1':'issue'}, inplace=True)

#convert categorical to numbers:
#issue: 
    #1: Election
    #2: Economy, Jobs
    #3: Food, Water
    #4: Environment Degradation
    #5: Ethnic Discrimination
    #6: Religion
    #7: Education
    #8: Foreign Affairs
    #9: Domestic War, Violence
    #10: Human Rights
    #11: Sport
    
    
 #target
    #1: Opposition supporters
    #2: Government
    #3: Police
    #4: Corporations/Companies
    #5: Religious Group
    #6: Fans
    #7: Military
    #8: Tourist
 
LAriots['target cat']=np.nan

#government
for i in range(len(LAriots)):
    if 'Government' in LAriots['target'][i]:
        LAriots['target cat'][i]=2
    
for i in range(len(LAriots)):
    if pd.isnull(LAriots['target cat'][i]):
        if 'Candidate' in LAriots['target'][i]:
            LAriots['target cat'][i]=2

for i in range(len(LAriots)):
    if pd.isnull(LAriots['target cat'][i]):
        if 'Constitution' in LAriots['target'][i]:
            LAriots['target cat'][i]=2
    

#Military
for i in range(len(LAriots)):
    if 'Military' in LAriots['target'][i] or 'military' in LAriots['target'][i] or 'Army' in LAriots['target'][i]:
        LAriots['target cat'][i]=7

#Opposition 
for i in range(len(LAriots)):
    if 'Citizens' in LAriots['target'][i] or 'citizens' in LAriots['target'][i]:
        LAriots['target cat'][i]=1

for i in range(len(LAriots)):
    if pd.isnull(LAriots['target cat'][i]):
        if 'activists' in LAriots['target'][i] or 'supporters' in LAriots['target'][i] or \
            'supporter' in LAriots['target'][i] or 'activist' in LAriots['target'][i]:
            LAriots['target cat'][i]=1
for i in range(len(LAriots)):
    if 'Civilians' in LAriots['target'][i] or 'Citizen' in LAriots['target'][i]:
        LAriots['target cat'][i]=1
    
for i in range(len(LAriots)):
    if pd.isnull(LAriots['target cat'][i]):
        if 'Election' in LAriots['target'][i]:
            LAriots['target cat'][i]=1
    
#company
 for i in range(len(LAriots)):
    if pd.isnull(LAriots['target cat'][i]):
        if 'company' in LAriots['issuenote'][i] or 'companies' in LAriots['issuenote'][i] or \
            "company's" in LAriots['issuenote'][i]:
            LAriots['target cat'][i]=4
    
    
#religous 
for i in range(len(LAriots)):
    if pd.isnull(LAriots['target cat'][i]):
        if 'church' in LAriots['target'][i] or 'nuns' in LAriots['target'][i]:
            LAriots['target cat'][i]=5
    

#police
for i in range(len(LAriots)):
    if pd.isnull(LAriots['target cat'][i]):
        if 'police' in LAriots['target'][i] or 'Police' in LAriots['target'][i]:
            LAriots['target cat'][i]=3
        


sum(pd.isnull(LAriots['target cat']))
 
 
wikilist=open('/Users/isarasuntichotinun/Desktop/ANNIE/CSC 591/Data/WikiList.txt')
wikilist=wikilist.readlines()
 
 