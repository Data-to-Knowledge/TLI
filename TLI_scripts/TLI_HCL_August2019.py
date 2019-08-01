# -*- coding: utf-8 -*-
"""
Created on Thu Jun 07 14:09:18 2018

@author: TinaB
"""
## Script to calculate TLIs, plot TLI, plot scatterplots of TN, TP, turbisity, chla
## Also outputs TN, TP, CHla means and raw data as csvs
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
datapath_out = 'C:\\data\\TLI\\SQ\\HTnew\\2019b\\'

base_url = 'http://wateruse.ecan.govt.nz'
hts = 'WQAll.hts'

site = 'SQ30147'
sitename = 'Katrine'
sitename1= 'Loch Katrine'

#site = 'SQ34907'
#sitename1 = 'Lake Benmore, Haldon Arm'
#sitename = 'Benmore_Haldon'

startdate = '2004-01-12'
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
  
    raw_data = {'Date': dates_TP,'TP': TP}
################ remove to here   
### put back in: 
#    TP_1 = 1000.0*pd.to_numeric(TP1, errors='coerce')
####   make new dataframe
#    raw_data = {'Date': dates_TP,'TP': TP_values}
    df = pd.DataFrame(raw_data, columns = ['Date', 'TP'])
    
    ##### drop Benmore Boat data
    if (sitename == 'Benmore_Haldon'):
#        df['Date']= pd.to_datetime(df['Date'])
#        df['Date'] = df['Date'].apply(lambda x: x.date())
        print df.Date
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

    raw_data2 = {'Date': dates_TN,'TN': TN}
############### remove to here 
  
############# put this back in
#    TN_values = 1000.0*pd.to_numeric(TN1, errors='coerce')
#    ## make data frame with Date,TN
#    raw_data2 = {'Date': dates_TN,'TN': TN_values}
    df2 = pd.DataFrame(raw_data2, columns = ['Date', 'TN'])
    
        ##### drop Benmore Boat data
    if (sitename == 'Benmore_Haldon'):
        print df2.Date
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
    
    raw_data3 = {'Date': dates_chla,'chla': chla}
    df3 = pd.DataFrame(raw_data3, columns = ['Date', 'chla'])
    
    ##### drop Benmore Boat data
    if (sitename == 'Benmore_Haldon'):
        print df3.Date
        df3 = df3.drop([df3.index[62],df3.index[63],df3.index[64],df3.index[67],df3.index[69]])## 21-1-19 and 12-4-19 not pushed through yet
        print df3

    ### Turbidity ### 

    measurement = 'Turbidity'
    wq1 = get_data(base_url, hts, site, measurement, from_date=startdate, to_date=enddate).reset_index()
    dates_Turbidity = wq1['DateTime']
    Turbidity_values1 = wq1['Value']
    
    Turb_1 = pd.to_numeric(Turbidity_values1, errors='coerce')
    Turbidity_values = Turb_1.astype(float).fillna(0.1).values   
    
    raw_data4 = {'Date': dates_Turbidity,'Turbidity': Turbidity_values}
    df4 = pd.DataFrame(raw_data4, columns = ['Date', 'Turbidity'])
    
        ##### drop Benmore Boat data
    if (sitename == 'Benmore_Haldon'):
        print df4.Date
        df4 = df4.drop([df4.index[59],df4.index[60],df4.index[61],df4.index[64],df4.index[66]])## 21-1-19 and 12-4-19 not pushed through yet
        print df4

    df.set_index(['Date'])
    df2.set_index(['Date'])
    df3.set_index(['Date'])
    df4.set_index(['Date'])
    
    
    #########Limits
    if ((sitename == 'Sumner') or (sitename == 'Coleridge')):
        TLI_limit = 2.0
        y_lim = 3.5
        TP_limit = 4.0
        TN_limit = 73.0
        chla_limit = 0.82
    elif ((sitename == 'Emma') or (sitename == 'Emily') or (sitename == 'Georgina')
    or (sitename == 'MaoriFront') or (sitename == 'MaoriBack')):
        TLI_limit = 4.0
        y_lim = 6.0
        TP_limit = 20.0
        TN_limit = 340.0
        chla_limit = 5.0       
    elif (sitename == 'Denny'):
        TLI_limit = 3.0
        y_lim = 7.0
        TP_limit = 9.0
        TN_limit = 160.0
        chla_limit = 2.0  
# PC5
    elif ((sitename == 'Ohau') or (sitename == 'Pukaki') or (sitename == 'Tekapo')):
        TLI_limit = 1.7
        y_lim = 3.5
        TP_limit = 10.0
        TN_limit = 160.0
        chla_limit = 2.0  
    elif (sitename == 'Benmore_Haldon'):
        TLI_limit = 2.7
        y_lim = 5.0
        TP_limit = 10.0
        TN_limit = 160.0
        chla_limit = 2.0  
    elif (sitename == 'Benmore_Dam'):
        TLI_limit = 2.7
        y_lim = 5.0
        TP_limit = 10.0
        TN_limit = 160.0
        chla_limit = 2.0  
    elif (sitename == 'Benmore_Ahuriri'):
        TLI_limit = 2.9
        y_lim = 5.0
        TP_limit = 10.0
        TN_limit = 160.0
        chla_limit = 5.0  
    elif (sitename == 'Aviemore'):
        TLI_limit = 2.0
        y_lim = 5.0
        TP_limit = 10.0
        TN_limit = 160.0
        chla_limit = 2.0  
    elif (sitename == 'McGregor'):        
        TLI_limit = 3.2
        y_lim = 5.0
        TP_limit = 20.0
        TN_limit = 350.0
        chla_limit = 2.0  
    elif (sitename == 'Middleton'):        
        TLI_limit = 3.6
        y_lim = 5.0
        TP_limit = 10.0
        TN_limit = 160.0
        chla_limit = 2.0  
    elif (sitename == 'Alexandrina'):        
        TLI_limit = 3.1
        y_lim = 5.0
        TP_limit = 10.0
        TN_limit = 350.0
        chla_limit = 2.0  
    elif ((sitename == 'Kellands_shore') or (sitename == 'Kellands_mid')):        
        TLI_limit = 3.2
        y_lim = 6.0
        TP_limit = 10.0
        TN_limit = 500.0
        chla_limit = 2.0  
    else:
        TLI_limit = 3.0
        y_lim = 5.0
        TP_limit = 9.0
        TN_limit = 160.0
        chla_limit = 2.0 
    
    sq = site
    print sq
    filename = sq+'_scatterplot'
    fig, ax = plt.subplots(2,2, figsize=(8.5, 5))
    ax[0,0].plot(df.Date,df.TP, marker = '.', linestyle = 'None')
    ax[0,0].legend(frameon=True, facecolor = 'white', framealpha = 1.0)
    ax[0,0].set_ylabel('Total Phosphorus in microg/L')
#    ax[0,0].axhline(y = TP_limit, linewidth=2, color='#d62728', label = 'CLWRP limit')
    ax[0,0].set_title(sitename1)
    ax[0,1].plot(df2.Date,df2.TN, marker = '.', linestyle = 'None')
    ax[0,1].legend(frameon=True, facecolor = 'white', framealpha = 1.0)
    ax[0,1].set_ylabel('Total Nitrogen in microg/L')
#    ax[0,1].axhline(y = TN_limit, linewidth=2, color='#d62728', label = 'CLWRP limit')
    ax[1,0].plot(df3.Date,df3.chla, marker = '.', linestyle = 'None')
    ax[1,0].legend(frameon=True, facecolor = 'white', framealpha = 1.0)
    ax[1,0].set_ylabel('Chlorophyll a in microg/L')
#    ax[1,0].axhline(y = chla_limit, linewidth=2, color='#d62728', label = 'CLWRP limit')
    ax[1,1].plot(df4.Date,df4.Turbidity, marker = '.', linestyle = 'None')
    ax[1,1].legend(frameon=True, facecolor = 'white', framealpha = 1.0)
    ax[1,1].set_ylabel('Turbidity in NTU')
    plt.tight_layout()
    plt.show()
    plt.savefig(str(datapath_out)+filename+'.png')
    plt.close()   
    

# TLI caluclations (HCL)
### for Lake  For Lake Benmore non-detects are treated as dl, not half dl
    if ((sitename == 'Benmore_Dam') or (sitename == 'Benmore_Ahuriri') or (sitename == 'Benmore_Haldon')): 
        measurement = 'Total Phosphorus'
        wq1 = get_data(base_url, hts, site, measurement, from_date='2004-01-12', to_date=enddate).reset_index()
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
        raw_data = {'Date': dates_TP,'TP': TP}
        df = pd.DataFrame(raw_data, columns = ['Date', 'TP'])   
        df.set_index(['Date'])

# TLI caluclations (HCL)
    new_df = df2.set_index('Date').copy()
    new_df.index = pd.to_datetime(new_df.index)
    TLN_data = new_df.resample('A-JUN').mean() # annual mean for hydro year
    TLN2 = TLN_data.resample('A-JUN').apply(lambda x: -3.61 + 3.01*numpy.log10(x))
    ## annual means
    TN_mean1 = new_df.resample('A-JUN').mean() # annual mean for hydro year 
    TN_mean = TN_mean1.TN 
    Years_TN = pd.DatetimeIndex(TN_mean.index).year
                               
    raw_data5 = {'Year': Years_TN,'TNmean': TN_mean}
    df_Mean_TN= pd.DataFrame(raw_data5, columns = ['Year', 'TNmean'])
        
    new_df = df.set_index('Date').copy()
    new_df.index = pd.to_datetime(new_df.index)
    TLP_data = new_df.resample('A-JUN').mean()
    TLP2 = TLP_data.resample('A-JUN').apply(lambda x: 0.218 + 2.92*numpy.log10(x))
    ## annual means
    TP_mean1 = new_df.resample('A-JUN').mean() 
    TP_mean = TP_mean1.TP 
    Years_TP = pd.DatetimeIndex(TP_mean.index).year
                               
    raw_data6 = {'Year': Years_TP,'TPmean': TP_mean}
    df_Mean_TP= pd.DataFrame(raw_data6, columns = ['Year', 'TPmean'])
    
    new_df = df3.set_index('Date').copy()
    new_df.index = pd.to_datetime(new_df.index)
    TLC_data = new_df.resample('A-JUN').mean()
    TLC2 = TLC_data.resample('A-JUN').apply(lambda x: 2.22 + 2.54*numpy.log10(x))
    ## annual means    
    chla_mean1 = new_df.resample('A-JUN').mean()
    chla_mean = chla_mean1.chla 
    Years_chla = pd.DatetimeIndex(chla_mean.index).year
                                 
    raw_data7 = {'Year': Years_chla,'chla_mean': chla_mean}
    df_Mean_chla= pd.DataFrame(raw_data7, columns = ['Year', 'chla_mean'])
    
# Calculate TLI and make array with years    
    TLI_data = (TLN2.TN + TLP2.TP + TLC2.chla)/3.0   
    Years = pd.DatetimeIndex(TLI_data.index).year
                            
# Output to csv
    TLI_data.to_csv(str(datapath_out)+'TLI'+sitename+'.csv')
#                    , header= ['Year', 'TLI_score'])
    
    # Plot TLI barchart with "limit' line
    n_groups = len (TLI_data)
    fig, ax = plt.subplots()    
    index = numpy.arange(n_groups)
    bar_width = 0.35   
        
       
    # Graph    
    filename = sq+'_TLI'
    rects1 = ax.bar(index, TLI_data, bar_width, color='b',
#                    yerr=std_men, error_kw=error_config,
                    label='TLI') 
    ax.set_ylim(0,y_lim)
    ax.set_xlabel('Year', fontsize=14)
    ax.set_ylabel('TLI Score', fontsize=14)
    ax.set_title(sitename1, fontsize=16)
    ax.set_xticks(index) # + bar_width/2)
    ax.set_xticklabels((Years))
    plt.axhline(y = TLI_limit, linewidth=4, color='#d62728', label = 'CLWRP limit')
    ax.legend()
    fig.tight_layout()
    plt.show()    
    plt.savefig(str(datapath_out)+filename+'.png')   
    
    ### means, plan compliance                               
#    print TN_mean
#    print TP_mean
#    print chla_mean
    Years_ab = Years
#    Years_ab=["%02d" % b for b in range(Years_abr)]
#    Years_ab = str(Years_abr).zfill(2) 
    print Years_ab
    if (sitename != 'Kellands_shore'):                    
          
        filename = sq+'_scatterplot_means'
        fig, ax = plt.subplots(2,2, figsize=(8.5, 5))
        
        ax[0,0].bar(index, TLI_data, bar_width, color='b',label = 'TLI')
        ax[0,0].axhline(y = TLI_limit, linewidth=2, color='#d62728', label = 'CLWRP limit')
#        ax[0,0].legend(frameon=True, facecolor = 'white', framealpha = 1.0)
        ax[0,0].set_ylabel('TLI Score')
        ax[0,0].set_xticks(index) # + bar_width/2)
        ax[0,0].set_xticklabels((Years_ab), rotation='vertical')
        ax[0,0].set_title(sitename1)
    
        ax[0,1].bar(index, TN_mean, bar_width, color='b', label='TN annual mean') 
        ax[0,1].axhline(y = TN_limit, linewidth=2, color='#d62728')#, label = 'CLWRP limit')
        ax[0,1].legend(frameon=True, facecolor = 'white', framealpha = 1.0)
        ax[0,1].set_ylabel('Total Nitrogen in microg/L')
        ax[0,1].set_xticks(index) # + bar_width/2)
        ax[0,1].set_xticklabels((Years_ab), rotation='vertical')
        
        ax[1,0].bar(index, chla_mean, bar_width, color='b', label='Chla annual mean') 
        ax[1,0].axhline(y = chla_limit, linewidth=2, color='#d62728')#, label = 'CLWRP limit')
        ax[1,0].legend(frameon=True, facecolor = 'white', framealpha = 1.0)
        ax[1,0].set_ylabel('Chlorophyll a in microg/L')
        ax[1,0].set_xlabel('Year')
        ax[1,0].set_xticks(index) # + bar_width/2)
        ax[1,0].set_xticklabels((Years_ab), rotation='vertical')
        
        ax[1,1].bar(index, TP_mean, bar_width, color='b', label='TP annual mean') 
        ax[1,1].axhline(y = TP_limit, linewidth=2, color='#d62728')#, label = 'CLWRP limit')
        ax[1,1].legend(frameon=True, facecolor = 'white', framealpha = 1.0)
        ax[1,1].set_ylabel('Total Phosphorus in microg/L')
        ax[1,1].set_xlabel('Year')
        ax[1,1].set_xticks(index) # + bar_width/2)
        ax[1,1].set_xticklabels((Years_ab), rotation='vertical')
    
        plt.tight_layout()
        plt.show()
        plt.savefig(str(datapath_out)+filename+'.png')
        plt.close()  
        
        
   
 #######       
    # redo scatterplots for lakes with little data
    if ((sitename == 'Catherine') or (sitename == 'Denny') or (sitename == 'Evelyn')
    or (sitename == 'Henrietta') or (sitename == 'McGregor') or (sitename == 'Kellands_mid')
    or (sitename == 'Opuha') or (sitename == 'Emily') or (sitename == 'MaoriBack') or
    (sitename == 'MaoriFront')):
        filename = sq+'_scatterplot'
        fig, ax = plt.subplots(2,2, figsize=(8.5, 5))
        ax[0,0].plot(df.Date,df.TP, marker = '.', linestyle = 'None')
#        ax[0,0].axhline(y = TP_limit, linewidth=4, color='#d62728', label = 'CLWRP limit')
        ax[0,0].legend(frameon=True, facecolor = 'white', framealpha = 1.0)
        ax[0,0].set_ylabel('Total Phosphorus in microg/L')
        ax[0,0].set_title(sitename1)
        ax[0,1].plot(df2.Date,df2.TN, marker = '.', linestyle = 'None')
#        ax[0,1].axhline(y = TN_limit, linewidth=2, color='#d62728', label = 'CLWRP limit')
        ax[0,1].legend(frameon=True, facecolor = 'white', framealpha = 1.0)
        ax[0,1].set_ylabel('Total Nitrogen in microg/L')
        ax[1,0].plot(df3.Date,df3.chla, marker = '.', linestyle = 'None')
#        ax[1,0].axhline(y = chla_limit, linewidth=2, color='#d62728', label = 'CLWRP limit')
        ax[1,0].legend(frameon=True, facecolor = 'white', framealpha = 1.0)
        ax[1,0].set_ylabel('Chlorophyll a in microg/L')
        ax[1,1].plot(df4.Date,df4.Turbidity, marker = '.', linestyle = 'None')
        ax[1,1].legend(frameon=True, facecolor = 'white', framealpha = 1.0)
        ax[1,1].set_ylabel('Turbidity in NTU')
        plt.tight_layout()
#        fig.autofmt_xdate()
        fig.autofmt_xdate(bottom=0.2, rotation=45, ha='right')
        plt.show()
        plt.savefig(str(datapath_out)+filename+'.png')
        plt.close()
        
    # force chla on same date scale as other parameters    
    if (sitename == 'Kellands_shore'):
        filename = sq+'_scatterplot'
        fig, ax = plt.subplots(2,2, figsize=(8.5, 5))
        ax[0,0].plot(df.Date,df.TP, marker = '.', linestyle = 'None')
        ax[0,0].legend(frameon=True, facecolor = 'white', framealpha = 1.0)
        ax[0,0].set_ylabel('Total Phosphorus in microg/L')
#        ax[0,0].axhline(y = TP_limit, linewidth=4, color='#d62728', label = 'CLWRP limit')
        ax[0,0].set_title(sitename1)
        ax[0,1].plot(df2.Date,df2.TN, marker = '.', linestyle = 'None')
        ax[0,1].legend(frameon=True, facecolor = 'white', framealpha = 1.0)
        ax[0,1].set_ylabel('Total Nitrogen in microg/L')
        ax[1,0].plot(df3.Date,df3.chla, marker = '.', linestyle = 'None')
        ax[1,0].set_xlim('2004-01-12', '2017-07-01')
        ax[1,0].legend(frameon=True, facecolor = 'white', framealpha = 1.0)
        ax[1,0].set_ylabel('Chlorophyll a in microg/L')
        ax[1,1].plot(df4.Date,df4.Turbidity, marker = '.', linestyle = 'None')
        ax[1,1].legend(frameon=True, facecolor = 'white', framealpha = 1.0)
        ax[1,1].set_ylabel('Turbidity in NTU')
        plt.tight_layout()
        fig.autofmt_xdate()
        plt.show()
        plt.savefig(str(datapath_out)+filename+'.png')
        plt.close()     
                
    ########### Write all data to csv
    df['SiteName'] = 'Lake'+sitename
    df['SQ'] = site  
    df['Parameter'] = 'TP' 
     
    df.to_csv(str(datapath_out)+'TP_all_lakes.csv', mode='a', encoding='utf-8', header=False)#, header= ['Date','TP','Sitename','SQ','Parameter'])
    print 'written csv'
    
    df2['SiteName'] = 'Lake'+sitename
    df2['SQ'] = site  
    df2['Parameter'] = 'TN'     
    df2.to_csv(str(datapath_out)+'TN_all_lakes.csv', mode='a', encoding='utf-8', header=False)#, header= ['Date','TP','Sitename','SQ','Parameter'])
    print 'written csv'
    
    df3['SiteName'] = 'Lake'+sitename
    df3['SQ'] = site  
    df3['Parameter'] = 'chla'    
#    print df3
    df3.to_csv(str(datapath_out)+'chla_all_lakes.csv', mode='a', encoding='utf-8', header=False)#, header= ['Date','TP','Sitename','SQ','Parameter'])
    print 'written csv'    
    
    ### write means    
    df_Mean_chla['SiteName'] = 'Lake'+sitename
    df_Mean_chla['SQ'] = site  
    df_Mean_chla['Parameter'] = 'chla_mean'     
    df_Mean_chla.to_csv(str(datapath_out)+'ChlaMeans_all_lakes.csv', mode='a', encoding='utf-8', header=False)
    print 'written csv'
    
    df_Mean_TN['SiteName'] = 'Lake'+sitename
    df_Mean_TN['SQ'] = site  
    df_Mean_TN['Parameter'] = 'TN_mean'     
    df_Mean_TN.to_csv(str(datapath_out)+'TNMeans_all_lakes.csv', mode='a', encoding='utf-8', header=False)
    print 'written csv'
    
    df_Mean_TP['SiteName'] = 'Lake'+sitename
    df_Mean_TP['SQ'] = site  
    df_Mean_TP['Parameter'] = 'TP_mean'     
    df_Mean_TP.to_csv(str(datapath_out)+'TPMeans_all_lakes.csv', mode='a', encoding='utf-8', header=False)
    print 'written csv'    
    
    a = TLI_data
    return a
    
a = calcTLI(site)
TLI_frame = a

site = 'SQ30079'
sitename = 'Sumner'
sitename1 = 'Lake Sumner'
a = calcTLI(site)
# Make a TLI summary table for all lakes
result = pd.concat([TLI_frame, a], axis=1, join_axes=[TLI_frame.index])

site = 'SQ30141'
sitename = 'Taylor'
sitename1 = 'Lake Taylor'
a = calcTLI(site)
result = pd.concat([result, a], axis=1, join_axes=[TLI_frame.index])

site = 'SQ30140'
sitename = 'Sheppard'
sitename1 = 'Lake Sheppard'
a = calcTLI(site)
result = pd.concat([result, a], axis=1, join_axes=[TLI_frame.index])

site = 'SQ30144'
sitename = 'Marion'
sitename1 = 'Lake Marion'
a = calcTLI(site)
result = pd.concat([result, a], axis=1, join_axes=[TLI_frame.index])

site = 'SQ35642'
sitename = 'Mason'
sitename1 = 'Lake Mason'
a = calcTLI(site)
result = pd.concat([result, a], axis=1, join_axes=[TLI_frame.index])

site = 'SQ30521'
sitename = 'Sarah'
sitename1 = 'Lake Sarah'
a = calcTLI(site)
result = pd.concat([result, a], axis=1, join_axes=[TLI_frame.index])

site = 'SQ30525'
sitename = 'Grasmere'
sitename1 = 'Lake Grasmere'
a = calcTLI(site)
result = pd.concat([result, a], axis=1, join_axes=[TLI_frame.index])

site = 'SQ30497'
sitename = 'Pearson'
sitename1 = 'Lake Pearson'
a = calcTLI(site)
result = pd.concat([result, a], axis=1, join_axes=[TLI_frame.index])

site = 'SQ30486'
sitename = 'Hawdon'
sitename1 = 'Lake Hawdon'
a = calcTLI(site)
result = pd.concat([result, a], axis=1, join_axes=[TLI_frame.index])

site = 'SQ31043'
sitename = 'Lyndon'
sitename1 = 'Lake Lyndon'
a = calcTLI(site)
result = pd.concat([result, a], axis=1, join_axes=[TLI_frame.index])

site = 'SQ31047'
sitename = 'Georgina'
sitename1 = 'Lake Georgina'
a = calcTLI(site)
result = pd.concat([result, a], axis=1, join_axes=[TLI_frame.index])

site = 'SQ31051'
sitename = 'Ida'
sitename1 = 'Lake Ida'
a = calcTLI(site)
result = pd.concat([result, a], axis=1, join_axes=[TLI_frame.index])

site = 'SQ31065'
sitename = 'Selfe'
sitename1 = 'Lake Selfe'
a = calcTLI(site)
result = pd.concat([result, a], axis=1, join_axes=[TLI_frame.index])

site = 'SQ31045'
sitename = 'Coleridge'
sitename1 = 'Lake Coleridge'
a = calcTLI(site)
result = pd.concat([result, a], axis=1, join_axes=[TLI_frame.index])

site = 'SQ31050'
sitename = 'Evelyn'
sitename1 = 'Lake Evelyn'
a = calcTLI(site)
result = pd.concat([result, a], axis=1, join_axes=[TLI_frame.index])

site = 'SQ31052'
sitename = 'Catherine'
sitename1 = 'Lake Catherine'
a = calcTLI(site)
result = pd.concat([result, a], axis=1, join_axes=[TLI_frame.index])

site = 'SQ31064'
sitename = 'Henrietta'
sitename1 = 'Lake Henrietta'
a = calcTLI(site)
result = pd.concat([result, a], axis=1, join_axes=[TLI_frame.index])

site = 'SQ35362'
sitename ='Emily'
sitename1 ='Lake Emily'
a = calcTLI(site)
result = pd.concat([result, a], axis=1, join_axes=[TLI_frame.index])

site = 'SQ35363'
sitename = 'MaoriFront'
sitename1 = 'Maori Lake (Front)'
a = calcTLI(site)
result = pd.concat([result, a], axis=1, join_axes=[TLI_frame.index])

site = 'SQ35364'
sitename = 'MaoriBack'
sitename1 = 'Maori Lake (Back)'
a = calcTLI(site)
result = pd.concat([result, a], axis=1, join_axes=[TLI_frame.index])

site = 'SQ35888'
sitename = 'Denny'
sitename1 = 'Lake Denny'
a = calcTLI(site)
result = pd.concat([result, a], axis=1, join_axes=[TLI_frame.index])

site = 'SQ31093'
sitename = 'Heron'
sitename1 = 'Lake Heron'
a = calcTLI(site)
result = pd.concat([result, a], axis=1, join_axes=[TLI_frame.index])

site = 'SQ32801'
sitename = 'Emma'
sitename1 = 'Lake Emma'
a = calcTLI(site)
result = pd.concat([result, a], axis=1, join_axes=[TLI_frame.index])

site = 'SQ32802'
sitename = 'Camp'
sitename1 = 'Lake Camp'
a = calcTLI(site)
result = pd.concat([result, a], axis=1, join_axes=[TLI_frame.index])

site = 'SQ32804'
sitename = 'Clearwater'
sitename1 = 'Lake Clearwater'
a = calcTLI(site)
result = pd.concat([result, a], axis=1, join_axes=[TLI_frame.index])

site = 'SQ35823'
sitename = 'McGregor'
sitename1 = 'Lake McGregor'
a = calcTLI(site)
result = pd.concat([result, a], axis=1, join_axes=[TLI_frame.index])
 
site = 'SQ20927'
sitename = 'Middleton'
sitename1 = 'Lake Middleton'
a = calcTLI(site)
result = pd.concat([result, a], axis=1, join_axes=[TLI_frame.index])

site = 'SQ31096'
sitename = 'Alexandrina'
sitename1 = 'Lake Alexandrina'
a = calcTLI(site)
result = pd.concat([result, a], axis=1, join_axes=[TLI_frame.index])

site = 'SQ32908'
sitename = 'Tekapo'
sitename1 = 'Lake Tekapo'
a = calcTLI(site)
result = pd.concat([result, a], axis=1, join_axes=[TLI_frame.index])

site = 'SQ34908'
sitename = 'Pukaki'
sitename1 = 'Lake Pukaki'
a = calcTLI(site)
result = pd.concat([result, a], axis=1, join_axes=[TLI_frame.index])

site = 'SQ32909'
sitename = 'Ohau'
sitename1 = 'Lake Ohau'
a = calcTLI(site)
result = pd.concat([result, a], axis=1, join_axes=[TLI_frame.index])

site = 'SQ34907'
sitename1 = 'Lake Benmore, Haldon Arm'
sitename = 'Benmore_Haldon'
a = calcTLI(site)
result = pd.concat([result, a], axis=1, join_axes=[TLI_frame.index])

site = 'SQ35639'
sitename1 = 'Lake Benmore, Ahuriri Arm'
sitename = 'Benmore_Ahuriri'
a = calcTLI(site)
result = pd.concat([result, a], axis=1, join_axes=[TLI_frame.index])

site = 'SQ35640'
sitename1 = 'Lake Benmore, near dam'
sitename = 'Benmore_Dam'
a = calcTLI(site)
result = pd.concat([result, a], axis=1, join_axes=[TLI_frame.index])

site = 'SQ35641'
sitename = 'Aviemore'
sitename1 = 'Lake Aviemore'
a = calcTLI(site)
result = pd.concat([result, a], axis=1, join_axes=[TLI_frame.index])

site = 'SQ35833'
sitename1 = 'Kelland Pond, mid-lake'
sitename = 'Kellands_mid'

a = calcTLI(site)
result = pd.concat([result, a], axis=1, join_axes=[TLI_frame.index])

site = 'SQ10805'
sitename1 = 'Kellands Pond, shore'
sitename = 'Kellands_shore'
a = calcTLI(site)
result = pd.concat([result, a], axis=1, join_axes=[TLI_frame.index])

site = 'SQ36148'
sitename1 = 'Lake Opuha'
sitename = 'Opuha'
a = calcTLI(site)
result = pd.concat([result, a], axis=1, join_axes=[TLI_frame.index])

# TLI summary table to csv
result.columns = ['Katrine', 'Sumner','Taylor', 'Sheppard', 'Marion', 'Mason', 'Sarah', 'Grasmere', 'Pearson', 'Hawdon','Lyndon','Georgina', 'Ida','Selfe','Coleridge', 'Evelyn','Catherine', 'Henrietta','Emily', 'MaoriFront','MaoriBack', 'Denny','Heron','Emma','Camp', 'Clearwater', 'McGregor','Middleton', 'Alexandrina', 'Tekapo','Pukaki','Ohau', 'Benmore_Haldon','Benmore_Ahuriri','Benmore_Dam', 'Aviemore','Kellands_mid', 'Kellands_shore', 'Opuha']
#print result
result.to_csv(str(datapath_out)+'TLI_summary_HCL.csv')



