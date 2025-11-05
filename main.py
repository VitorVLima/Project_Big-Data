import pandas as pd
import glob
import os # Us

import pandas as pd
import glob
import os

def combinar_arquivos(pasta_entrada: str, 
                             padrao_arquivos: str, 
                             arquivo_saida: str, 
                             adicionar_origem: bool = False,
                             ignore_index: bool = True):
    """
    Combina múltiplos arquivos (CSV ou Excel) de uma pasta em um único DataFrame
    e salva o resultado.

    Argumentos:
    pasta_entrada -- O caminho para a pasta contendo os arquivos.
    padrao_arquivos -- O padrão para encontrar os arquivos (ex: "*.csv", "relatorio_*.xlsx").
    arquivo_saida -- O nome (ou caminho completo) do arquivo final a ser salvo.
    adicionar_origem -- Se True, adiciona uma coluna 'origem_arquivo' com o nome
                        do arquivo de onde cada linha veio.
    ignore_index -- Se True, reinicia o índice do DataFrame final.
    
    Retorna:
    Um DataFrame do pandas contendo todos os dados combinados, ou None se
    nenhum arquivo for encontrado.
    """
    
    # Determina o caminho completo para a busca
    caminho_busca = os.path.join(pasta_entrada, padrao_arquivos)
    lista_de_arquivos = glob.glob(caminho_busca)

    if not lista_de_arquivos:
        print(f"Aviso: Nenhum arquivo encontrado com o padrão '{padrao_arquivos}' em '{pasta_entrada}'.")
        return None

    # Determina a função de leitura com base na extensão
    extensao = padrao_arquivos.split('.')[-1].lower()
    if extensao == 'csv':
        funcao_leitura = pd.read_csv
    elif extensao in ['xlsx', 'xls']:
        funcao_leitura = pd.read_excel
    else:
        print(f"Erro: Extensão de arquivo '{extensao}' não suportada.")
        return None

    # Processa os arquivos
    lista_de_dfs = []
    print(f"Encontrados {len(lista_de_arquivos)} arquivos. Processando...")

    for arquivo in lista_de_arquivos:
        try:
            df_temp = funcao_leitura(arquivo)
            
            if adicionar_origem:
                nome_do_arquivo = os.path.basename(arquivo)
                df_temp['origem_arquivo'] = nome_do_arquivo
            
            lista_de_dfs.append(df_temp)
        except Exception as e:
            print(f"Erro ao ler o arquivo {arquivo}: {e}")

    if not lista_de_dfs:
        print("Nenhum arquivo pôde ser lido com sucesso.")
        return None

    # Concatena todos os DataFrames
    df_final = pd.concat(lista_de_dfs, ignore_index=ignore_index)

    # Salva o arquivo final
    caminho_saida_completo = os.path.join(pasta_entrada, arquivo_saida)
    try:
        if arquivo_saida.endswith('.csv'):
            df_final.to_csv(caminho_saida_completo, index=False)
        elif arquivo_saida.endswith('.xlsx'):
            df_final.to_excel(caminho_saida_completo, index=False)
        else:
            print(f"Aviso: Extensão do arquivo de saída não reconhecida, salvando como CSV.")
            df_final.to_csv(caminho_saida_completo, index=False)
            
        print(f"\nSucesso! Arquivos combinados e salvos em: {caminho_saida_completo}")
        print(f"Total de linhas combinadas: {len(df_final)}")
        
    except Exception as e:
        print(f"Erro ao salvar o arquivo final: {e}")

    return df_final



caminho_do_arquivo = "DataSet/Dados_Mortalidade.csv"

# Tente carregar o arquivo
try:
    # Se for um arquivo CSV:
    df = pd.read_csv(caminho_do_arquivo)

except FileNotFoundError:
    print(f"Erro: O arquivo não foi encontrado em '{caminho_do_arquivo}'")
except Exception as e:
    print(f"Ocorreu um erro ao ler o arquivo: {e}")
