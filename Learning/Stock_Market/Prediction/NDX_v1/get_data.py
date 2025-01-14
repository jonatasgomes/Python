from datetime import datetime, timedelta

yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
today = datetime.now().strftime('%Y-%m-%d')
middle_time = '11:30'

# initial_date = input(f"Enter the initial date [{yesterday}]: ") or yesterday
# final_date = input(f"Enter the final date [{today}]: ") or today
# middle_time = input(f"Enter the middle time [{middle_time}]: ") or middle_time

ndx_stocks = {
    'AAPL': 9.33, 'NVDA': 8.67, 'MSFT': 8.12, 'AMZN': 6.0, 'AVGO': 4.51,
    'TSLA': 3.73, 'META': 3.5, 'GOOGL': 2.92, 'GOOG': 2.79, 'COST': 2.66,
    'NFLX': 2.3, 'TMUS': 1.57, 'CSCO': 1.5, 'LIN': 1.26, 'PEP': 1.25,
    'ISRG': 1.25, 'AMD': 1.21, 'ADBE': 1.15, 'INTU': 1.12, 'QCOM': 1.12,
    'TXN': 1.11, 'BKNG': 1.01, 'PLTR': 0.94, 'HON': 0.91, 'AMAT': 0.91,
    'AMGN': 0.9, 'CMCSA': 0.89, 'ADP': 0.75, 'PANW': 0.73, 'GILD': 0.72,
    'MU': 0.71, 'VRTX': 0.68, 'ADI': 0.68, 'SBUX': 0.67, 'MRVL': 0.64,
    'LRCX': 0.62, 'CEG': 0.61, 'APP': 0.61, 'KLAC': 0.59, 'MELI': 0.57,
    'PYPL': 0.54, 'INTC': 0.53, 'CDNS': 0.53, 'CRWD': 0.52, 'CTAS': 0.49,
    'SNPS': 0.49, 'REGN': 0.48, 'MAR': 0.48, 'MDLZ': 0.48, 'FTNT': 0.47,
    'ORLY': 0.44, 'DASH': 0.42, 'ASML': 0.42, 'PDD': 0.41, 'CSX': 0.39,
    'ADSK': 0.39, 'MSTR': 0.39, 'ABNB': 0.36, 'PCAR': 0.36, 'ROP': 0.35,
    'CPRT': 0.34, 'TTD': 0.34, 'WDAY': 0.34, 'NXPI': 0.34, 'FANG': 0.33,
    'ROST': 0.32, 'PAYX': 0.32, 'AEP': 0.32, 'MNST': 0.31, 'CHTR': 0.3,
    'LULU': 0.3, 'DDOG': 0.28, 'AXON': 0.28, 'BKR': 0.27, 'KDP': 0.26,
    'FAST': 0.26, 'TEAM': 0.25, 'AZN': 0.25, 'GEHC': 0.25, 'VRSK': 0.24,
    'ODFL': 0.24, 'EXC': 0.24, 'CTSH': 0.24, 'EA': 0.24, 'XEL': 0.23,
    'KHC': 0.22, 'IDXX': 0.22, 'CCEP': 0.22, 'TTWO': 0.2, 'DXCM': 0.2,
    'MCHP': 0.19, 'ANSS': 0.19, 'ZS': 0.19, 'CSGP': 0.18, 'CDW': 0.16,
    'WBD': 0.15, 'ON': 0.15, 'GFS': 0.15, 'BIIB': 0.14, 'MDB': 0.12,
    'ARM': 0.12
}

try:
    conn = None
finally:
    if conn is not None:
        conn.close()
