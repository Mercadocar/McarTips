#!/usr/bin/env python
import pika
import os
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Script to create cluster required resources:

# TODO - Create databases using loop
# TODO - Pass informations through env variables.

try:  
    rabbitmq_host = os.environ['POC_TELEPRECO_RABBITMQ_HA_SERVICE_HOST']

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
except KeyError: 
    print ("RabbitMQ not found, proceeding...")

try:  
    postgres_host = os.environ['POC_TELEPRECO_POSTGRESQL_SERVICE_HOST']
    postgres_username = 'postgres'
    postgres_psw = 'postgres'

    db_1_name = 'atendimento'
    db_2_name = 'orcamento'

    # Create required Postgres Databases.
    con = psycopg2.connect(dbname='postgres',
        user=postgres_username, host=postgres_host,
        password=postgres_psw)

    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()

    cur.execute("SELECT datname FROM pg_database;")

    list_database = cur.fetchall()

    if (db_1_name,) in list_database:
        print("'{}' Database already exist".format(db_1_name))
    else:
        print("'{}' Database not exist...Creating..".format(db_1_name))
        cur.execute(sql.SQL("CREATE DATABASE {}").format(
            sql.Identifier(db_1_name))
        )

    if (db_2_name,) in list_database:
        print("'{}' Database already exist".format(db_2_name))
    else:
        print("'{}' Database not exist...Creating..".format(db_2_name))
        cur.execute(sql.SQL("CREATE DATABASE {}").format(
            sql.Identifier(db_2_name))
        )
except KeyError: 
    print ("Postgres not found, proceeding...")





