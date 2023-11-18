import time
from estrategias import *
from backtesting_functions import monkey_test, mp_backtest, mp_walk_forward
from rsubsets import rSubset
start = time.time()

available_coins = ['MATIC', 'ETH', 'AVAX', 'LINK','SOL', 'ADA', 'BNB', 'BTC']

source = 'sqlite:///crypto_15m_from_2019.db' 
settings = {   
    'tickers_list': rSubset(available_coins,(1,)),
    'fecha_desde_bt': ['2022-11-24'],
    'fecha_hasta_bt': ['2023-01-01'],
    'interval': ['2H'],
    'position_size_st': [1.00],
    'short_selling': [True],
    'time_stop': [0],
    'stop_selection': ['seteado'],
    'trailing': [False],
    'comision': [0.00035], 
    'stop_loss': [0.015, 0.025],
    'take_profit': [0.03,0.05,0.1],
    'show_daily_results': [False]
}
account_sets = {
    'init_account': 100,
    'account_margin': 1,
    'open_positions_long': {},
    'open_positions_short': {},
    'current_size': '',
    'available': ''
}
strategy = add_estrategia_momentum
strategy_sets = {
    'fast_lag':[8,10,12],
    'slow_lag':[24,30,36]
}

#sólo para walk forward:
steps = [(180,60)]

#sólo para monkey_test:
monkey_sets = {
    'random_entries': True,
    'random_exits': False,
    'pasadas': 100
}

if __name__ == '__main__':
    metricas, results = mp_backtest(
                                source,
                                settings,
                                account_sets,
                                strategy,
                                strategy_sets,
                                #steps,
                                save_to='bt_momo_diciembre'
                                )

    finish = time.time()
    print(str(round(finish-start,1)) +' segundos de ejecución')

