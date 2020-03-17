#!/usr/bin/env python
import pika
import os
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Script to create cluster required resources:

# Defining Variables

postgres_username = 'postgres'
postgres_psw = 'postgres'
postgres_host = os.environ['POC_TELEPRECO_POSTGRESQL_SERVICE_HOST']
rabbitmq_host = os.environ['POC_TELEPRECO_RABBITMQ_SERVICE_HOST']

# Create required RabbitMQ Queues and Exchanges.

connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))
channel = connection.channel()

channel.exchange_declare(exchange='Pessoa', exchange_type='direct')
channel.queue_declare(queue='PessoaAtualizadaEvent', durable=True)
channel.queue_bind(exchange='Pessoa', queue='PessoaAtualizadaEvent', routing_key='')

channel.exchange_declare(exchange='Orcamento', exchange_type='fanout')
channel.queue_declare(queue='OrcamentoGeradoEvent', durable=True)
channel.queue_bind(exchange='Orcamento', queue='OrcamentoGeradoEvent', routing_key='')

channel.exchange_declare(exchange='PessoaCriada', exchange_type='fanout')
channel.queue_declare(queue='PessoaCriadaEvent', durable=True)
channel.queue_bind(exchange='PessoaCriada', queue='PessoaCriadaEvent', routing_key='')

connection.close()

# Create required Postgres Databases.

con = psycopg2.connect(dbname='postgres',
    user=postgres_username, host=postgres_host,
    password=postgres_psw)

con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = con.cursor()

cur.execute(sql.SQL("CREATE DATABASE {}").format(
    sql.Identifier('atendimento'))
)
cur.execute(sql.SQL("CREATE DATABASE {}").format(
    sql.Identifier('orcamento'))
)