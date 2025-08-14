from previsao_aluguel.services.previsao_service import prever_alugueis

if __name__ == '__main__':
    data_teste = '2025-07-08'
    try:
        previsao, margem_erro = prever_alugueis(data_teste)
        print(f"Previsão para {data_teste}: {previsao}")
        print(f"Margem de erro: {margem_erro}")
    except Exception as e:
        print("Erro:", e)
