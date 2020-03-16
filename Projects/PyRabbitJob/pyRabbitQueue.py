#!/usr/bin/env python
import pika
import os

connection = pika.BlockingConnection(pika.ConnectionParameters(os.environ['POC_TELEPRECO_RABBITMQ_SERVICE_HOST']))
channel = connection.channel()

channel.exchange_declare(exchange='Pessoa',
                         exchange_type='direct')

channel.queue_declare(queue='PessoaAtualizadaEvent', durable=True)

channel.queue_bind(exchange='Pessoa',
                   queue='PessoaAtualizadaEvent',
                   routing_key='')

channel.exchange_declare(exchange='Orcamento',
                         exchange_type='fanout')

channel.queue_declare(queue='OrcamentoGeradoEvent', durable=True)

channel.queue_bind(exchange='Orcamento',
                   queue='OrcamentoGeradoEvent',
                   routing_key='')

channel.exchange_declare(exchange='PessoaCriada',
                         exchange_type='fanout')

channel.queue_declare(queue='PessoaCriadaEvent', durable=True)

channel.queue_bind(exchange='PessoaCriada',
                   queue='PessoaCriadaEvent',
                   routing_key='')

connection.close()
