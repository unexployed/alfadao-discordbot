import json
import requests

def get_audit_chain_ids():
    with open('cog_support/chain_ids.json' , "r") as json_file:
        chain_ids_list = json.load(json_file)
    return chain_ids_list

list_security = ['is_open_source', 'mintable', 'can_take_back_ownership', 
                 'creator_address', 'creator_balance', 'creator_percent', 
                 'owner_address', 'owner_balance', 'hidden_owner', 
                 'selfdestruct', 'external_calls', 'is_honeypot', 
                 'cannot_sell_all', 'slippage_modifiable','transfer_pausable', 
                 'is_blacklisted', 'is_proxy', 'is_whitelisted',
                'holder_count', 'owner_change_balance', 'is_true_token', 
                'is_airdrop_scam', 'trust_list', 'other_potential_risks', 
                 'cannot_sell_all', 'slippage_modifiable', 'transfer_pausable',
                'dex', 'is_anti_whale', 'anti_whale_modifiable', 'buy_tax', 'sell_tax','lp_holders']

def ping_audit_api(chain, contract):
    response = requests.get('https://api.gopluslabs.io/api/v1/token_security/{}?contract_addresses={}'.format(chain, contract))
    data = response.json()
    return data['result']

def filter_security(data:dict):
    contract_address = next(iter(data))
    data = data[contract_address]
    matched_data = {}
    for key in list_security:
        if key in data:
            value = data[key]
            if value == '0':
                value = 'False'
            elif value == '1':
                value = 'True'
            elif key == 'lp_holders':
                holders = [
                    {
                        'address': holder['address'],
                        'tag': holder['tag'],
                        'percentage_locked': holder['percent'],
                        'unlock_date': holder['locked_detail'][0]['end_time']
                    }
                    for holder in data['lp_holders'] if holder['tag'] == 'UniCrypt'
                ]
                value = holders or 'No locked liquidity in Unicrypt'
            matched_data[key] = value
    return matched_data

# data = ping_audit_api(1, '0xbb9fd9fa4863c03c574007ff3370787b9ce65ff6')
# filtered = filter_security(data)
# print(filtered['dex'])
