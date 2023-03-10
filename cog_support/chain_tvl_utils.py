import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_chains():
    response = requests.get('https://api.llama.fi/chains')
    data = response.json()
    chains = set(chain['name'] for chain in data)
    return chains

def get_chain_tvl():
    chains = get_chains()
    historical_data = []
    total_tvl = 0 
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(get_chain_tvl_helper, chain): chain for chain in chains}
        for future in as_completed(futures):
            chain = futures[future]
            try:
                result = future.result()
                if result:
                    historical_data.append(result)
                    total_tvl += result['TVL']
            except Exception as e:
                print(f"{e} raised at {chain}.")      
    df = pd.DataFrame(historical_data)
    df['TVL %'] = df['TVL'] / total_tvl * 100
    df['TVL'] = df['TVL'].apply(lambda x: round(x / 1e9, 4))
    df = df.sort_values(by="TVL", ascending=False)
    column_to_move = df.pop('TVL %')
    df.insert(2, 'TVL %', column_to_move )
    df = df.head(35)
    return df

def get_chain_tvl_helper(chain):
    try:
        response = requests.get(f'https://api.llama.fi/v2/historicalChainTvl/{chain}')
        tvl_data = response.json()
        if not tvl_data:
            return None
        current_tvl = tvl_data[-1]['tvl']
        historical_entry = {'chain': chain, 'TVL': current_tvl}
        for i, days in enumerate([7, 14, 30, 60, 90]):
            if len(tvl_data) < days + 1:
                historical_entry[f'{days}d'] = None
            else:
                previous_tvl = tvl_data[-days-1]['tvl']
                percent_change = ((current_tvl - previous_tvl) / previous_tvl) * 100
                historical_entry[f'{days}d'] = round(percent_change, 4)
        return historical_entry
    except Exception as e:
        pass
        # raise Exception(f"{e} raised at {chain}.")
    
def split_df(df, chunk_size=8):
    chunks = []
    for i in range(0, len(df), chunk_size):
        chunks.append(df.iloc[i:i+chunk_size])
    return chunks

def chunks(lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i + n]