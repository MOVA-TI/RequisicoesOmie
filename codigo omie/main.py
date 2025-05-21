import pandas as pd
from omie import get_all_accounts, get_all_accounts_statement
from datetime import datetime
import schedule
import time
from sqlalchemy.orm import sessionmaker

from connect import engine
from models import Omie, Base

def get_omie_data():
	acc_list = get_all_accounts()["ListarContasCorrentes"]

	concatenated_movements_df = pd.DataFrame()
	date_now = datetime.now()
	date_now = date_now.strftime('%d/%m/%Y')
	for acc_print in acc_list:
		print(f'{acc_print["nCodCC"]} - {acc_print["descricao"]}\n')

		#max_retries = 3 #máx de tentativas
		#retry_delay = 5 #tempo de espera 5seg

	for acc in acc_list:
		print("\n\n\n-------------------------------")
		print(f'{acc["nCodCC"]} - {acc["descricao"]}\n')
		#acc_info = get_all_accounts_statement("01/01/2022", date_now, acc["nCodCC"])

		acc_info_all = []

		# Loop de 2021 a 2025
		for year in range(2024, 2026):
		    # Limita os meses dependendo do ano
		    if year == 2025:
		        months = range(1, 6)  # Apenas até março
		    else:
		        months = range(1, 13)  # Janeiro a Dezembro

		    for month in months:
		        month_str = f"{month:02d}"
		        print(f"{year}/{month_str} - PENDENTE")

				#retries = 0
                #while retries < max_retries:
                #try:
		        
		        start_time = datetime.now()
		        acc_info = get_all_accounts_statement(
		            f"01/{month_str}/{year}", 
		            f"{'28' if month == 2 else '30' if month in [4, 6, 9, 11] else '31'}/{month_str}/{year}", 
		            acc["nCodCC"]
		        )
		        finish_time = datetime.now()

				#if not acc_info.get('listaMovimentos'): #verifica se a resposta está vazia
                	#raise ValueError("Resposta vazia recebida da API")

		        total_time = finish_time - start_time
		        print(f"{year}/{month_str} - FINALIZADO - {total_time}\n")

				#acc_info_all.extend(acc_info['listaMovimentos'])
                #break  #Sai do loop de tentativas se bem-sucedido
				
				#except (ValueError, Exception) as e:
                    # retries += 1
                    # print(f"Erro na tentativa {retries}: {str(e)}")
                    # if retries == max_retries:
                    #     print(f"Falha após {max_retries} tentativas para {year}/{month_str}")
                    #     acc_info_all.extend([])  #Adiciona lista vazia para continuar
                    #     break
                    #time.sleep(retry_delay) #Espera antes de tentar novamente

		        time.sleep(1)
		        acc_info_all.extend(acc_info['listaMovimentos'])  # Junta tudo em uma lista

		print("-------------------------------\n\n")


		print(acc_info_all)
		print(len(acc_info_all))
		print("------------------------------------------------------------------------------------")
		print(acc_info['listaMovimentos'])
		print(len(acc_info['listaMovimentos']))

		#print("novo")
		#print(acc_info)
		#temp_df = pd.DataFrame(acc_info_all['listaMovimentos'])
		temp_df = pd.DataFrame(acc_info_all)
		temp_df["cDescricao"] = acc_info["cDescricao"]
		temp_df["nCodBanco"] = acc_info["nCodBanco"]
		temp_df["nNumConta"] = acc_info["nNumConta"]
		temp_df["nCodAgencia"] = acc_info["nCodAgencia"]

		concatenated_movements_df = pd.concat([concatenated_movements_df, temp_df])

	concatenated_movements_df.to_csv("planilhas/extrato_contas.csv", index=False, sep = ';', decimal=',')

	return concatenated_movements_df.copy()

def update_omie_data():
	#print('INIT:', datetime.now())
	#print('Getting data from Omie')
	df = get_omie_data()
	#print('Dataframe is right')



	# print(df.head())
	# for col in df.columns:
	# 	print(col, df[col].dtypes, df[col].unique()[:4])

	Base.metadata.drop_all(bind=engine, tables=[Omie.__table__])
	time.sleep(2)
	Base.metadata.create_all(engine)
	db_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
	session = db_session()

	dict_cols = {j: i for i, j in enumerate(df.columns)}
	all_samples = []

	for idx, row in enumerate(df.values):
		omie_ = Omie()
		omie_.id = idx

		for item in dict_cols:
			setattr(omie_, item, row[dict_cols[item]])
		
		all_samples.append(omie_)
	
	session.add_all(all_samples)
	print('comminting ...')
	session.commit()
	session.close()

update_omie_data()

#schedule.every().day.at("23:00").do(update_omie_data)
#schedule.every().day.at("11:00").do(update_omie_data)
#schedule.every().day.at("11:35").do(update_omie_data)
#schedule.every().day.at("05:00").do(update_omie_data)

#while True:
	# update_omie_data()
#	schedule.run_pending()
#	time.sleep(3) # wait 
