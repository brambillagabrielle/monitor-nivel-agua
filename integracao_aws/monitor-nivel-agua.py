import boto3
import serial
from credenciais import keys

# Cria um cliente de SQS com as chaves de acesso criada para o usuário
sqs = boto3.client(
    'sqs',
    aws_access_key_id=keys.get('aws_access_key_id'),
    aws_secret_access_key=keys.get('aws_secret_access_key'),
    region_name='us-east-1'
)

# Define a fila SQS para envio de mensagens
queue_url = 'https://sqs.us-east-1.amazonaws.com/341952761262/fila-coleta-sensor'

# Define a porta serial e o baud rate da conexão com a porta conectada ao Arduino
serial_port = '/dev/ttyUSB0'
baud_rate = 9600

# Variáveis definidas para medir o nível da água e identificar alterações
altura_sensor = 19.24
nivel_padrao = 10.0
variacao = 2.0
nivel_minimo = nivel_padrao - variacao
nivel_maximo = nivel_padrao + variacao

# Loop de conexão com o Arduino
while True:
    try:
        # Conecta o Arduino pela porta serial (USB conectado)
        arduino = serial.Serial(serial_port, baud_rate)
        print('Arduino conectado com sucesso!')
        break
    
    except:
        pass

# Loop principal para coleta das métricas do sensor enviadas pelo Arduino
while True:
    try:
        # Lê uma linha do monitor serial
        leitura = arduino.readline().decode().strip()

        # Realiza o cálculo do nível de água com a leitura do sensor
        nivel_agua = altura_sensor - float(leitura)
        print("Nível identificado da água: " + str(nivel_agua))
        
        # Verifica se ocorreu uma alteração no nível da água em relação à 
        # variação aceitável
        alteracao = 0
        if nivel_agua < nivel_minimo or nivel_agua > nivel_maximo:
            alteracao = 1
            # arduino.write('1'.encode())
            print('Alteração identificada')
        else:
            # arduino.write('0'.encode())
            print('Nivel normal')

        # Envia mensagem para o SQS e espera uma resposta
        response = sqs.send_message(
            QueueUrl=queue_url,
            DelaySeconds=10,
            MessageBody=(
                    f'{nivel_agua}|{alteracao}'
            )
        )

        # Mostra no console a resposta recebida pelo SQS
        print("SQS recebeu a mensagem com ID: " + response['MessageId'])

        # Limpa a comunicação do serial
        arduino.flush()

    except KeyboardInterrupt:
        # Fecha a conexão com o Arduino pela porta serial
        arduino.close()
        print('Conexão fechada com o Arduino!')
        break