import requests
from credentials import APP_KEY, APP_SECRET
import json

def get_all_accounts():

    url = 'https://app.omie.com.br/api/v1/geral/contacorrente/'

    headers = {
        'Content-type': 'application/json',
    }

    json_data = {
        'call': 'ListarContasCorrentes',
        'app_key': APP_KEY,
        'app_secret': APP_SECRET,
        'param': [
            {
                'pagina': 1,
                'registros_por_pagina': 100,
                'apenas_importado_api': 'N',
            },
        ],
    }

    response = requests.post(url, headers=headers, json=json_data, timeout=10)
    
    if response.status_code == 200:
        return response.json()
        
    else:
        #print("teste")
        print(response.text)
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None


def get_all_accounts_statement(start_date, end_date, acc_code):
    #Date Format: DD/MM/YYYY 
    
    url = 'https://app.omie.com.br/api/v1/financas/extrato/'

    headers = {
        'Content-type': 'application/json',
    }

    json_data = {
        'call': 'ListarExtrato',
        'app_key': APP_KEY,
        'app_secret': APP_SECRET,
        'param': [
            {
                'nCodCC': acc_code,
                'cCodIntCC': '',
                'dPeriodoInicial': start_date,
                'dPeriodoFinal': end_date,
            },
        ],
    }
    #print("omie info request started")
    #print(url)
    response = requests.post(url, headers=headers, json=json_data)
    #print("omie info request finished")

    
    if response.status_code == 200:
        return response.json()
        
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None

    

