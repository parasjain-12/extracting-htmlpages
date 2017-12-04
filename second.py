#!/usr/bin/python
import pandas as pd
import os
import time
from datetime import datetime
from time import mktime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
style.use("dark_background")
import re

path = "intraQuarter"

def Key_Status(gather="Total Debt/Equity (mrq)"):
	statspath = path+'/_KeyStats'
	stock_list = [x[0] for x in os.walk(statspath)]
	df =  pd.DataFrame(columns = ['Date',
					'Unix',
					'Ticker',
					'DE Ratio',
					'Price',
					'stock_p_change',
					'SP500',
					'sp500_change',
					'Differnece'])
	sp_data = pd.DataFrame.from_csv('YAHOO-INDEX_GSPC.csv')
	tickerlist = []

	for each_dir in stock_list[1:25]:
		#print(each_dir)
		
		filename = os.listdir(each_dir)
		triger = each_dir.split('/_KeyStats/')[1]
		tickerlist.append(triger)
		starting_stock_value = False
		starting_sp500_value = False
		if len(filename)>0:
			for page in filename:
				date_stamp = datetime.strptime(page,"%Y%m%d%H%M%S.html")
				unix_stamp = time.mktime(date_stamp.timetuple())
				full_file_path = each_dir+'/'+page
				#print(date_stamp,unix_stamp)
				#print(full_file_path)
				source =open(full_file_path,'r').read()
				try:
					try:
						value = float(source.split(gather +':</td><td class="yfnc_tabledata1">' )[1].split('</td>')[0])
					except Exception as e:
						print(str(e),page,triger)
						
						
					
					try:
						sp_date = datetime.fromtimestamp(unix_stamp).strftime('%Y-%m-%d')
						row = sp_data[(sp_data.index==sp_date)]
						sp_value = float(row['Adj Close'])
						
					except:
						sp_date = datetime.fromtimestamp(unix_stamp-259200).strftime('%Y-%m-%d')
						row = sp_data[(sp_data.index==sp_date)]
						sp_value = float(row['Adj Close'])
						
					stock_price = float(source.split('</small><big><b>')[1].split('</b></big>')[0])
					if not starting_stock_value:
						starting_stock_value = stock_price
					if not starting_sp500_value:
						starting_sp500_value = sp_value

					#print("stock Price : ",stock_price,"ticker : ",triger)
					stock_p_change = ((stock_price - starting_stock_value)/starting_stock_value)*100
					sp500_change = ((sp_value - starting_sp500_value)/starting_sp500_value)*100
					
					df=df.append({'Date':date_stamp,
						'Unix':unix_stamp,
						'Ticker':triger,
						'DE Ratio':value,
						'Price':stock_price,
						'stock_p_change':stock_p_change,
						'SP500':sp_value,
						'sp500_change':sp500_change,
						'Differnece':(stock_p_change-sp500_change)},ignore_index=True)
				except Exception as e:
					pass

	for each_ticker in tickerlist:
		try:
			
			plot_df = df[(df['Ticker']==each_ticker)]
			
			plot_df = plot_df.set_index(['Date'])
			
			plot_df['Differnece'].plot(label = each_ticker)
			plt.legend()
		except:
			
			pass
	plt.show()
	save = gather.replace(' ','').replace('/','').replace('(','').replace(')','')+('.csv')
	print(save)
	df.to_csv(save)


Key_Status()
