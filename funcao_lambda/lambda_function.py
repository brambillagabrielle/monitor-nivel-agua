import boto3
import os
import json
from datetime import datetime
from decimal import Decimal

# variáveis de ambiente
QUEUE_NAME = os.environ["QUEUE_NAME"]
TOPIC_ARN = os.environ["TOPIC_ARN"]
TABLE_NAME = os.environ["TABLE_NAME"]

# cria clientes para os serviços que vão ser utilizados
sns = boto3.client('sns')
dynamodb = boto3.resource('dynamodb')

# função que vai executar quando o trigger for acionado (evento do SQS)
def lambda_handler(event, context):
   
    messages = event['Records']

    for message in messages:
        
        # separa os dados enviados na mensagem recebida pelo SQS
        timestamp = datetime.now()
        dados = message['body'].split("|")
        nivelColetado = round(float(dados[0]), 2)
        alteracao = int(dados[1])
        
        try:
            # se for uma alteracao (1), vai enviar um e-mail para o SNS
            if alteracao:
                dataFormatada = timestamp.strftime("%d/%m/%Y, %H:%M:%S")
                mensagemEmail = ('Olá!\n' + 
                'Uma alteração foi identificada no nosso sensor relativo ao nível de água.' +
                f'\nA coleta do dia {dataFormatada} indica que o nível da água está atualmente em {nivelColetado} cm.' +
                '\nAtt.')
                # publica a mensagem no tópico SNS, para ser enviada por e-mail
                snsResponse = sns.publish(
                    TopicArn=TOPIC_ARN,
                    Message=mensagemEmail,
                    Subject=f'Identificada alteração no nível da água ({dataFormatada})'
                )
                print(f'Mensagem enviada ao SNS: {json.dumps(snsResponse, indent=4)}')
            
            # escreve na tabela do DynamoDB as informações recebidas
            table = dynamodb.Table(TABLE_NAME)
            dynamodbResponse = table.put_item(Item=json.loads(json.dumps({'timestamp': timestamp.isoformat(), 
                'nivel_coletado': nivelColetado}), parse_float=Decimal))
            print(f'Mensagem enviada ao DynamoDB: {json.dumps(dynamodbResponse, indent=4)}')
        
            return dynamodbResponse
    
        except Exception as e:
            print(e)