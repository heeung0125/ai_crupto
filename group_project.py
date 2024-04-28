import time
import requests
import pandas as pd

while True:
    response = requests.get('https://api.bithumb.com/public/orderbook/BTC_KRW/?count=5')
    book = response.json()
    data = book['data']

    bids = pd.DataFrame(data['bids']).apply(pd.to_numeric, errors='coerce')  # FutureWarning 수정
    bids.sort_values('price', ascending=False, inplace=True)
    bids.reset_index(drop=True, inplace=True)
    bids['type'] = 0  # bid를 0으로 지정

    asks = pd.DataFrame(data['asks']).apply(pd.to_numeric, errors='coerce')  # FutureWarning 수정
    asks.sort_values('price', ascending=True, inplace=True)
    asks.reset_index(drop=True, inplace=True)
    asks['type'] = 1  # ask를 1으로 지정

    df = pd.concat([bids, asks])

    timestamp = time.strftime('%Y%m%d%H%M%S')  # 파일 이름 수정
    filename = f'orderbook_{timestamp}.csv'
    
    # CSV 파일에 헤더 추가
    with open(filename, 'w') as f:
        f.write('price,quantity,type,timestamp\n')
    
    df.to_csv(filename, mode='a', index=False, header=False)

    print(f'Orderbook saved to {filename}')

    time.sleep(5)
