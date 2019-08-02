# -*- coding: utf-8 -*-
"""
Created on Fri Aug 02 10:31:06 2019

@author: TinaB
"""


## Script to calculate NOF / NPS bands for HCL
###########################################################
import pandas as pd
import matplotlib.pyplot as plt
import numpy
from hilltoppy.web_service import measurement_list, measurement_list_all, site_list, get_data, wq_sample_parameter_list
from datetime import datetime
import seaborn as sns
##############################################
## define path where graphs are saved
#datapath_out = 'C:\\data\\TLI\\SQ\\HTnew\\limits\\2019\\'
datapath_out = 'C:\\data\\TT\\2019\\'

base_url = 'http://wateruse.ecan.govt.nz'
hts = 'WQAll.hts'

site = 'SQ30147'
sitename = 'Katrine'
sitename1= 'Loch Katrine'

#site = 'SQ34907'
#sitename1 = 'Lake Benmore, Haldon Arm'
#sitename = 'Benmore_Haldon'

startdate = '2006-01-12'
enddate = '2019-05-01'

def calcTLI(x):
    print sitename
    
#    ## TP #####
    measurement = 'Total Phosphorus'
    wq1 = get_data(base_url, hts, site, measurement, from_date=startdate, to_date=enddate,dtl_method='half').reset_index()    #, dtl_method='half')
    dates_TP = wq1['DateTime']

############# remove this when data base fixed
    TP1 = wq1['Value']
    TP_1 = pd.to_numeric(TP1, errors='coerce')
    TP_values = TP_1.astype(float).fillna(0.002).values
    TP = numpy.zeros(len(TP_values))
###### remove this when database fixed
    for i in range (0,len(TP_values)):
        if ((sitename == 'Sumner') or (sitename == 'Coleridge')) and (TP_values[i] > 0.055): 
            TP[i] = 2.0    
        elif ((sitename == 'Benmore_Haldon')) and (TP_values[i] > 0.055): 
            TP[i] = 4.0 
        elif ((sitename == 'Marion') and (TP_values[i] > 0.3)):
            TP[i] = 13.0
        # For Lake Benmore non-detects are treated as dl, not half dl
        elif (((sitename == 'Benmore_Dam') or (sitename == 'Benmore_Ahuriri') or (sitename == 'Benmore_Haldon')) and (TP_values[i] == 0.002)):
            TP[i] = 4.0   
        else:
            TP[i] = 1000.0*TP_values[i]   
  
    raw_data = {'DateTP': dates_TP,'TP': TP}
################ remove to here   
### put back in: 
#    TP_1 = 1000.0*pd.to_numeric(TP1, errors='coerce')
####   make new dataframe
#    raw_data = {'Date': dates_TP,'TP': TP_values}
    df = pd.DataFrame(raw_data, columns = ['DateTP', 'TP'])
    
    ##### drop Benmore Boat data
    if (sitename == 'Benmore_Haldon'):
#        df['Date']= pd.to_datetime(df['Date'])
#        df['Date'] = df['Date'].apply(lambda x: x.date())
#        print df.DateTP
##        date_list = ('2018-10-26')
#        date_list = pd.to_datetime('2018-10-26').date()
##        df.drop(pd.to_datetime('2018-10-26'))
##        date_list = [datetime(2018, 10, 26),
##                 datetime(2018, 11, 20),
##                 datetime(2018, 12, 19),
##                 datetime(2019, 1, 21),
##                 datetime(2019, 2, 12),
##                 datetime(2019, 3, 18),
##                 datetime(2019, 4, 12)]
#        print date_list
##        df = df.drop(df.Date[date_list])
        df = df.drop([df.index[60],df.index[61],df.index[62],df.index[65],df.index[67]])## 21-1-19 and 12-4-19 not pushed through yet
        print df
        #https://stackoverflow.com/questions/35372499/how-can-i-delete-rows-for-a-particular-date-in-a-pandas-dataframe
        #https://thispointer.com/python-pandas-how-to-drop-rows-in-dataframe-by-index-labels/
#       
    ### TN ###
    measurement = 'Total Nitrogen'
    wq1 = get_data(base_url, hts, site, measurement, from_date=startdate, to_date=enddate, dtl_method='half').reset_index()
    dates_TN = wq1['DateTime']
    TN1 = wq1['Value']   
    TN_1 = pd.to_numeric(TN1, errors='coerce')
    TN_values = TN_1.astype(float).fillna(0.005).values

############# remove this when data base fixed
    TN = numpy.zeros(len(TN_values))

    for i in range (0,len(TN_values)):
        if ((sitename == 'Marion') and (TN_values[i] > 1.3)):
            TN[i] = 350.0
        else:
            TN[i] = 1000.0*TN_values[i]

    raw_data2 = {'DateTN': dates_TN,'TN': TN}
############### remove to here 
  
############# put this back in
#    TN_values = 1000.0*pd.to_numeric(TN1, errors='coerce')
#    ## make data frame with Date,TN
#    raw_data2 = {'Date': dates_TN,'TN': TN_values}
    df2 = pd.DataFrame(raw_data2, columns = ['DateTN', 'TN'])
    
        ##### drop Benmore Boat data
    if (sitename == 'Benmore_Haldon'):
#        print df2.DateTN
        df2 = df2.drop([df2.index[60],df2.index[61],df2.index[62],df2.index[65],df2.index[67]])## 21-1-19 and 12-4-19 not pushed through yet
        print df2

############## chla ###                     
    measurement = 'Chlorophyll a (planktonic)'
    wq1 = get_data(base_url, hts, site, measurement, from_date=startdate, to_date=enddate, dtl_method='half').reset_index()
    dates_chla = wq1['DateTime']  
    chla1 = wq1['Value']    
    chla_1 = pd.to_numeric(chla1, errors='coerce')
    chla_values2 = chla_1.astype(float).fillna(0.1).values                    

    chla = numpy.zeros(len(chla_values2))
    for i in range (0,len(chla_values2)):
############# remove this when data base fixed
        if ((sitename == 'Marion') and (chla_values2[i] > 50.0)):
            chla[i] = 2.7
############### remove to her and change elif to if
#        elif (chla_values2[i] < 0.19):
#            chla[i] = 1000.0*chla_values2[i]
#            #remove next two lines when 2011 marhc april fixed
        elif (chla_values2[i] > 150):
            chla[i] = chla_values2[i]/1000.0
        else:
            chla[i] = chla_values2[i]
    
    raw_data3 = {'DateChla': dates_chla,'chla': chla}
    df3 = pd.DataFrame(raw_data3, columns = ['DateChla', 'chla'])
    
    ##### drop Benmore Boat data
    if (sitename == 'Benmore_Haldon'):
#        print df3.DateChla
        df3 = df3.drop([df3.index[62],df3.index[63],df3.index[64],df3.index[67],df3.index[69]])## 21-1-19 and 12-4-19 not pushed through yet
        print df3

    df.set_index(['DateTP'])
    df2.set_index(['DateTN'])
    df3.set_index(['DateChla'])   
    
   
    sq = site
    print sq 
    
### for Lake  For Lake Benmore non-detects are treated as dl, not half dl
    if ((sitename == 'Benmore_Dam') or (sitename == 'Benmore_Ahuriri') or (sitename == 'Benmore_Haldon')): 
        measurement = 'Total Phosphorus'
        wq1 = get_data(base_url, hts, site, measurement, from_date=startdate, to_date=enddate).reset_index()
        dates_TP = wq1['DateTime']

        TP1 = wq1['Value']
        TP_1 = pd.to_numeric(TP1, errors='coerce')
        TP_values = TP_1.astype(float).fillna(0.004).values
        TP = numpy.zeros(len(TP_values))
        for i in range (0,len(TP_values)):
            if ((sitename == 'Benmore_Haldon')) and (TP_values[i] > 0.055): 
                TP[i] = 4.0 
            elif (TP_values[i] == 0.002):
                TP[i] = 4.0   
            else:
                TP[i] = 1000.0*TP_values[i]         
        raw_data = {'DateTP': dates_TP,'TP': TP}
        df = pd.DataFrame(raw_data, columns = ['DateTP', 'TP'])   
        df.set_index(['DateTP'])
        
        
###################################################################
##output csv withdate, chla, Tn, TP, Turbidity for timetrends
##https://pypi.org/project/pymannkendall/
#    
#    ### Turbidity ### 
#
#    measurement = 'Turbidity'
#    wq1 = get_data(base_url, hts, site, measurement, from_date=startdate, to_date=enddate).reset_index()
#    dates_Turbidity = wq1['DateTime']
#    Turbidity_values1 = wq1['Value']
#    
#    Turb_1 = pd.to_numeric(Turbidity_values1, errors='coerce')
#    Turbidity_values = Turb_1.astype(float).fillna(0.1).values   
#    
#    raw_data4 = {'DateT': dates_Turbidity,'Turbidity': Turbidity_values}
#    df4 = pd.DataFrame(raw_data4, columns = ['DateT', 'Turbidity'])
#    
#        ##### drop Benmore Boat data
#    if (sitename == 'Benmore_Haldon'):
#        print df4.DateT
#        df4 = df4.drop([df4.index[59],df4.index[60],df4.index[61],df4.index[64],df4.index[66]])## 21-1-19 and 12-4-19 not pushed through yet
#        print df4
#
#    df4.set_index(['DateT'])
#
###Output
##### build dataframe with all
#    dfcombined= pd.concat([df, df2, df3, df4], axis=1, join_axes=[df.index])
#    # Output to csv
#    dfcombined.to_csv(str(datapath_out)+'TT_'+sitename+'.csv')
#    
    
###############################

# Medians and NPS bands
#TN
    new_df = df2.set_index('DateTN').copy()
    new_df.index = pd.to_datetime(new_df.index)

    ## annual medians
    TN_mean1 = new_df.resample('A-JUN').median() # annual meadian for hydro year 
    TN_mean = TN_mean1.TN 
    Years_TN = pd.DatetimeIndex(TN_mean.index).year
                               
    ######### Polymictic lakes
    if ((sitename == 'Emma') or (sitename == 'Emily') or (sitename == 'Georgina') or (sitename == 'MaoriFront') or (sitename == 'MaoriBack') or (sitename == 'Denny') or (sitename == 'McGregor') or (sitename == 'Middleton')or (sitename == 'Kellands_shore') or (sitename == 'Kellands_mid')):
        
        TN_bands = numpy.zeros(len(TN_mean))
        for i in range(0,len(TN_mean)):
            if (TN_mean[i] <= 300.0):
                TN_bands[i] = 1.0
            elif (300.0 <TN_mean[i] <= 500.0):
                 TN_bands[i] = 2.0
            elif (500.0 <TN_mean[i] <= 800.0):
                 TN_bands[i] = 3.0
            elif (TN_mean[i] > 800.0):
                 TN_bands[i] = 4.0
            else:
                TN_bands[i] = 100.0    
#        print TN_bands        
    else:
        TN_bands = numpy.zeros(len(TN_mean))
        for i in range(0,len(TN_mean)):
            if (TN_mean[i] <= 160.0):
                TN_bands[i] = 1.0
            elif (160.0 <TN_mean[i] <= 350.0):
                 TN_bands[i] = 2.0
            elif (350.0 <TN_mean[i] <= 750.0):
                 TN_bands[i] = 3.0
            elif (TN_mean[i] > 750.0):
                 TN_bands[i] = 4.0
            else:
                TN_bands[i] = 100.0    
#        print TN_bands
    
#    TN_bands = []
#    for i in range(0,len(TN_mean)):
#        if (TN_mean[i] < 160.1):
#            TN_bands[i] = 'A'
#        elif (160.1 <TN_mean[i] < 350.1):
#             TN_bands[i] = 'B'
#        elif (350.1 <TN_mean[i] < 750.1):
#             TN_bands[i] = 'C'
#        elif (TN_mean[i] > 750.1):
#             TN_bands[i] = 'D'
#        else:
#            TN_bands[i] = 'NA'
#    print TN_bands
                               
#    raw_data5 = {'Year': Years_TN,'TNmean': TN_mean, 'TNBand': TN_bands}
#    df_Mean_TN= pd.DataFrame(raw_data5, columns = ['Year', 'TNmean','TNBand'])
##    print df_Mean_TN
    
    # TP    
    new_df = df.set_index('DateTP').copy()
    new_df.index = pd.to_datetime(new_df.index)
    ## annual means
    TP_mean1 = new_df.resample('A-JUN').median() 
    TP_mean = TP_mean1.TP 
    Years_TP = pd.DatetimeIndex(TP_mean.index).year
                               
    TP_bands = numpy.zeros(len(TP_mean))
    for i in range(0,len(TP_mean)):
        if (TP_mean[i] <= 10.0):
            TP_bands[i] = 1.0
        elif (10.0 <TP_mean[i] <= 20.0):
             TP_bands[i] = 2.0
        elif (20.0 <TP_mean[i] <= 50.0):
             TP_bands[i] = 3.0
        elif (TP_mean[i] > 50.0):
             TP_bands[i] = 4.0
        else:
            TP_bands[i] = 100.0    
#    print TP_bands
                               
#    raw_data6 = {'Year': Years_TP,'TPmean': TP_mean}
#    df_Mean_TP= pd.DataFrame(raw_data6, columns = ['Year', 'TPmean'])
    
    #Chla
    new_df = df3.set_index('DateChla').copy()
    new_df.index = pd.to_datetime(new_df.index)

    ## annual means    
    chla_mean1 = new_df.resample('A-JUN').median()
    chla_mean = chla_mean1.chla 
    Years_chla = pd.DatetimeIndex(chla_mean.index).year
                                 
    chla_bands = numpy.zeros(len(chla_mean))
    for i in range(0,len(chla_mean)):
        if (chla_mean[i] <= 2.0):
            chla_bands[i] = 1.0
        elif (2.0 <chla_mean[i] <= 5.0):
             chla_bands[i] = 2.0
        elif (5.0 <chla_mean[i] <= 12.0):
             chla_bands[i] = 3.0
        elif (chla_mean[i] > 12.0):
             chla_bands[i] = 4.0
        else:
            chla_bands[i] = 100.0    
#    print chla_bands
    
    ## annual max  
    chla_max1 = new_df.resample('A-JUN').max()
    chla_max = chla_max1.chla 
                                 
    chla_max_bands = numpy.zeros(len(chla_max))
    for i in range(0,len(chla_max)):
        if (chla_max[i] <= 10.0):
            chla_max_bands[i] = 1.0
        elif (10.0 <chla_max[i] <= 25.0):
             chla_max_bands[i] = 2.0
        elif (25.0 <chla_max[i] <= 60.0):
             chla_max_bands[i] = 3.0
        elif (chla_max[i] > 60.0):
             chla_max_bands[i] = 4.0
        else:
            chla_max_bands[i] = 100.0    
#    print chla_max_bands
                      
                                 
#    raw_data7 = {'Year': Years_chla,'chla_mean': chla_mean}
#    df_Mean_chla= pd.DataFrame(raw_data7, columns = ['Year', 'chla_mean'])
    
    raw_data8 = {'Year': Years_TN,'TNmean': TN_mean, 'TNBand': TN_bands,'TPmean': TP_mean, 'TPBand': TP_bands,'chlamean': chla_mean, 'chlaBand': chla_bands,'chlamax': chla_max, 'chlaMaxBand': chla_max_bands}
    
    df_NPS= pd.DataFrame(raw_data8, columns = ['Year','TNmean','TNBand','TPmean','TPBand','chlamean','chlaBand','chlamax','chlaMaxBand'])
    print df_NPS
    
    ##Output
#        ### build dataframe with all
#    dfcombined= pd.concat([df_TLI, df_chla, df_TP, df_TN], axis=1, join_axes=[df_TLI.index])
    # Output to csv
    df_NPS.to_csv(str(datapath_out)+'NPS_'+sitename+'.csv')
    
                
#    ########### Write all data to csv
#    df['SiteName'] = 'Lake'+sitename
#    df['SQ'] = site  
#    df['Parameter'] = 'TP' 
#     
#    df.to_csv(str(datapath_out)+'TP_all_lakes.csv', mode='a', encoding='utf-8', header=False)#, header= ['Date','TP','Sitename','SQ','Parameter'])
#    print 'written csv'
#    
#    df2['SiteName'] = 'Lake'+sitename
#    df2['SQ'] = site  
#    df2['Parameter'] = 'TP'     
#    df2.to_csv(str(datapath_out)+'TN_all_lakes.csv', mode='a', encoding='utf-8', header=False)#, header= ['Date','TP','Sitename','SQ','Parameter'])
#    print 'written csv'
#    
#    df3['SiteName'] = 'Lake'+sitename
#    df3['SQ'] = site  
#    df3['Parameter'] = 'chla'    
##    print df3
#    df3.to_csv(str(datapath_out)+'chla_all_lakes.csv', mode='a', encoding='utf-8', header=False)#, header= ['Date','TP','Sitename','SQ','Parameter'])
#    print 'written csv'    
    
#    ### write means    
#    df_Mean_chla['SiteName'] = 'Lake'+sitename
#    df_Mean_chla['SQ'] = site  
#    df_Mean_chla['Parameter'] = 'chla_mean'     
#    df_Mean_chla.to_csv(str(datapath_out)+'ChlaMeans_all_lakes.csv', mode='a', encoding='utf-8', header=False)
#    print 'written csv'
#    
#    df_Mean_TN['SiteName'] = 'Lake'+sitename
#    df_Mean_TN['SQ'] = site  
#    df_Mean_TN['Parameter'] = 'TN_mean'     
#    df_Mean_TN.to_csv(str(datapath_out)+'TNMeans_all_lakes.csv', mode='a', encoding='utf-8', header=False)
#    print 'written csv'
#    
#    df_Mean_TP['SiteName'] = 'Lake'+sitename
#    df_Mean_TP['SQ'] = site  
#    df_Mean_TP['Parameter'] = 'chla_max'     
#    df_Mean_TP.to_csv(str(datapath_out)+'TPMeans_all_lakes.csv', mode='a', encoding='utf-8', header=False)
#    print 'written csv'    
#    

    
calcTLI(site)


site = 'SQ30079'
sitename = 'Sumner'
sitename1 = 'Lake Sumner'
calcTLI(site)

site = 'SQ30141'
sitename = 'Taylor'
sitename1 = 'Lake Taylor'
calcTLI(site)

site = 'SQ30140'
sitename = 'Sheppard'
sitename1 = 'Lake Sheppard'
calcTLI(site)

site = 'SQ30144'
sitename = 'Marion'
sitename1 = 'Lake Marion'
calcTLI(site)

site = 'SQ35642'
sitename = 'Mason'
sitename1 = 'Lake Mason'
calcTLI(site)

site = 'SQ30521'
sitename = 'Sarah'
sitename1 = 'Lake Sarah'
calcTLI(site)


site = 'SQ30525'
sitename = 'Grasmere'
sitename1 = 'Lake Grasmere'
calcTLI(site)

site = 'SQ30497'
sitename = 'Pearson'
sitename1 = 'Lake Pearson'
calcTLI(site)

site = 'SQ30486'
sitename = 'Hawdon'
sitename1 = 'Lake Hawdon'
calcTLI(site)

site = 'SQ31043'
sitename = 'Lyndon'
sitename1 = 'Lake Lyndon'
calcTLI(site)

site = 'SQ31047'
sitename = 'Georgina'
sitename1 = 'Lake Georgina'
calcTLI(site)

site = 'SQ31051'
sitename = 'Ida'
sitename1 = 'Lake Ida'
calcTLI(site)

site = 'SQ31065'
sitename = 'Selfe'
sitename1 = 'Lake Selfe'
calcTLI(site)

site = 'SQ31045'
sitename = 'Coleridge'
sitename1 = 'Lake Coleridge'
calcTLI(site)

site = 'SQ31050'
sitename = 'Evelyn'
sitename1 = 'Lake Evelyn'
calcTLI(site)

site = 'SQ31052'
sitename = 'Catherine'
sitename1 = 'Lake Catherine'
calcTLI(site)

site = 'SQ31064'
sitename = 'Henrietta'
sitename1 = 'Lake Henrietta'
calcTLI(site)

site = 'SQ35362'
sitename ='Emily'
sitename1 ='Lake Emily'
calcTLI(site)

site = 'SQ35363'
sitename = 'MaoriFront'
sitename1 = 'Maori Lake (Front)'
calcTLI(site)

site = 'SQ35364'
sitename = 'MaoriBack'
sitename1 = 'Maori Lake (Back)'
calcTLI(site)

site = 'SQ35888'
sitename = 'Denny'
sitename1 = 'Lake Denny'
calcTLI(site)

site = 'SQ31093'
sitename = 'Heron'
sitename1 = 'Lake Heron'
calcTLI(site)

site = 'SQ32801'
sitename = 'Emma'
sitename1 = 'Lake Emma'
calcTLI(site)

site = 'SQ32802'
sitename = 'Camp'
sitename1 = 'Lake Camp'
calcTLI(site)

site = 'SQ32804'
sitename = 'Clearwater'
sitename1 = 'Lake Clearwater'
calcTLI(site)

site = 'SQ35823'
sitename = 'McGregor'
sitename1 = 'Lake McGregor'
calcTLI(site)
 
site = 'SQ20927'
sitename = 'Middleton'
sitename1 = 'Lake Middleton'
calcTLI(site)

site = 'SQ31096'
sitename = 'Alexandrina'
sitename1 = 'Lake Alexandrina'
calcTLI(site)

site = 'SQ32908'
sitename = 'Tekapo'
sitename1 = 'Lake Tekapo'
calcTLI(site)

site = 'SQ34908'
sitename = 'Pukaki'
sitename1 = 'Lake Pukaki'
calcTLI(site)

site = 'SQ32909'
sitename = 'Ohau'
sitename1 = 'Lake Ohau'
calcTLI(site)

site = 'SQ34907'
sitename1 = 'Lake Benmore, Haldon Arm'
sitename = 'Benmore_Haldon'
calcTLI(site)

site = 'SQ35639'
sitename1 = 'Lake Benmore, Ahuriri Arm'
sitename = 'Benmore_Ahuriri'
calcTLI(site)

site = 'SQ35640'
sitename1 = 'Lake Benmore, near dam'
sitename = 'Benmore_Dam'
calcTLI(site)

site = 'SQ35641'
sitename = 'Aviemore'
sitename1 = 'Lake Aviemore'
calcTLI(site)

site = 'SQ35833'
sitename1 = 'Kelland Pond, mid-lake'
sitename = 'Kellands_mid'

calcTLI(site)

site = 'SQ10805'
sitename1 = 'Kellands Pond, shore'
sitename = 'Kellands_shore'
calcTLI(site)

site = 'SQ36148'
sitename1 = 'Lake Opuha'
sitename = 'Opuha'
calcTLI(site)





