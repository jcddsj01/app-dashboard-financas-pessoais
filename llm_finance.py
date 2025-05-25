import ofxparse
import pandas as pd
import os
from datetime import datetime

df = pd.DataFrame()
for extrato in os.listdir("extratos"):
    with open(f'extratos/{extrato}', encoding='utf-8') as ofx_file:
        ofx = ofxparse.OfxParser.parse(ofx_file)

    transactions_data = []
    for account in ofx.accounts:
        for transaction in account.statement.transactions:
            transactions_data.append({
                "Data": transaction.date,
                "Valor": transaction.amount,
                "Descrição": transaction.memo,
                "ID": transaction.id,
            })

    df_temp = pd.DataFrame(transactions_data)
    df_temp["Valor"] = df_temp["Valor"].astype(float)
    df_temp["Data"] = df_temp["Data"].apply(lambda x: x.date())
    df = pd.concat([df, df_temp])

# ---------------------------
# LLM
# from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
# from langchain_core.output_parsers.string import StrOutputParser
# from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

template = """
Você é um analista de dados, trabalhando em um projeto de limpeza de dados.
Seu trabalho é escolher uma categoria adequada para cada lançamento financeiro
que vou te enviar.

Todos são transações financeiras de uma mesma pessoa física.

Escolha uma dentre as seguintes categorais:
- Alimentação
- Receitas
- Saúde
- Mercado
- Educação
- Compras
- Transporte
- Investimento
- Transferência para terceiros
- Telefone
- Moradia

Escolha a categoria deste item:
{text}

Responda apenas com a catergoria.
"""

prompt = PromptTemplate.from_template(template=template)
chat = ChatGroq(model="llama-3.1-8b-instant")
chain = prompt | chat

category = []
for transaction in list(df["Descrição"].values):
    category += [chain.invoke(transaction).content]
    
df["Categoria"] = category
df.to_csv("finances.csv", index=False, encoding="utf-8-sig")