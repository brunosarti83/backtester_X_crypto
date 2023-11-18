import config
from binance.client import Client
client = Client(config.API_KEY, config.API_SECRET)
import pandas as pd
from datetime import datetime, timedelta
import time
from sqlalchemy import create_engine
import concurrent.futures
start = time.time()

def unit_OHLC(token1, token2, interval, fecha_desde, fecha_hasta):

    timeframe = {'1m' :  Client.KLINE_INTERVAL_1MINUTE, '3m' : Client.KLINE_INTERVAL_3MINUTE,'5m' : Client.KLINE_INTERVAL_5MINUTE,'15m' : Client.KLINE_INTERVAL_15MINUTE,'30m' : Client.KLINE_INTERVAL_30MINUTE,'1h' : Client.KLINE_INTERVAL_1HOUR,'2h' : Client.KLINE_INTERVAL_2HOUR,'4h' : Client.KLINE_INTERVAL_4HOUR,'6h' : Client.KLINE_INTERVAL_6HOUR,'8h' : Client.KLINE_INTERVAL_8HOUR,'12h' : Client.KLINE_INTERVAL_12HOUR,'1d' : Client.KLINE_INTERVAL_1DAY}
    
    ticker = token1 + token2
    #candles = client.get_historical_klines(ticker, timeframe[interval],fecha_aux,fecha_hasta)
    candles = client.futures_historical_klines_generator(ticker, timeframe[interval],fecha_desde,fecha_hasta)
    data = pd.DataFrame(candles, columns = ['timestamp', 'Open','High','Low','Close','Volume','Col1','Col2','Col3','Col4','Col5','Col6'])
    data = data.drop(['Col1','Col2','Col3','Col4','Col5','Col6'],axis =1)
    
    if len(data) != 0:
        data['timestamp']=data['timestamp']/1000
        data['timestamp'] = [datetime.fromtimestamp(x) for x in data['timestamp']] #transformamos los timestamp en datetime
        data = data.set_index('timestamp')
        data['Open'] = data['Open'].astype(float)
        data['High'] = data['High'].astype(float)
        data['Low'] = data['Low'].astype(float)
        data['Close'] = data['Close'].astype(float)
        data['Volume'] = data['Volume'].astype(float)

        data = data.dropna()

        data['Date'] = data.index

    return token1, data


tickers_list = ['ADA','ETH','BNB','LINK','MATIC','AVAX','BTC','SOL'] 
token2 = 'USDT'

interval = '5m'

fecha_desde = '2018-12-01' #esta es para pedir los datos
fecha_hasta = '2022-10-01' #esta es para pedir datos pero también es donde termina obviamente el BT ya que solo hay datos hasta ahí

file_name = 'crypto_5m_prueba'



with concurrent.futures.ThreadPoolExecutor() as e: 
    engine = create_engine('sqlite:///'+file_name+'.db')
    thread_list = []
    for token1 in tickers_list:
        t1 = e.submit(unit_OHLC, token1, token2, interval, fecha_desde, fecha_hasta)
        thread_list.append(t1)
    
    for thread in thread_list:
        resultado = thread.result()
        token, data = resultado
        data.to_sql(token,engine)

    test = pd.read_sql('ADA','sqlite:///'+file_name+'.db').set_index('timestamp')
    print(test)

    #test = pd.read_csv('ADA_prueba_1m_agosto.csv')
    #test['timestamp'] = pd.to_datetime(test['timestamp'],format='%Y-%m-%d %H:%M:%S')
    #test = test.set_index('timestamp')
    #print(test)

    #ADA_4_hour = test.resample('4H',base=1).agg({'Open':'first','High':'max','Low':'min','Close':'last','Volume':'sum','Date':'first'})
    #print(ADA_4_hour)

    print('finalizado {}'.format(time.time() - start))