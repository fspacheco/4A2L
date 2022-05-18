#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Teste de verificação (correção automática)
    de scripts do curso AppInventor
    
    Fernando S. Pacheco - 2022
"""

import argparse
import logging
from parse.classes import OutMsg
from parse.parse_tarefas import *


cmparser = argparse.ArgumentParser(description='Verifica Tarefas para curso AppInventor.')
cmparser.add_argument("-t", "--tarefa", dest="tarefaId", choices=['2', '3', '4'], help="Id da tarefa a avaliar")
cmparser.add_argument("-f", "--file", dest="filename", help="Nome do arquivo. Default temporário: App_Oficina2_3.aia")
cmparser.add_argument("-l", "--log", dest="logLevel", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], help="Set the logging level")

args = cmparser.parse_args()
if args.logLevel:
    logging.basicConfig(level=getattr(logging, args.logLevel), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

if args.filename == None:
    args.filename = "../App_Oficina2_3.aia"

outmsg = OutMsg()

if args.tarefaId != None:
    args.tarefaId = int(args.tarefaId)
    
logger.debug("Tarefa ID: %s", args.tarefaId)

if args.tarefaId == 2:
    logger.debug("Start to evaluate Tarefa 2: %s", args.filename)
    outmsg = parse_tarefa2(args.filename)

if args.tarefaId == 3:
    logger.debug("Start to evaluate Tarefa 3: %s", args.filename)
    outmsg = parse_tarefa3(args.filename)    

if args.tarefaId == 4:
    logger.debug("Start to evaluate Tarefa 4: %s", args.filename)
    outmsg = parse_tarefa4(args.filename)

print("SUCCESS")
for msg in outmsg.success:
    print("PASS : ", msg)

print("ERROR")
for msg in outmsg.fail:
    print("FAIL : ", msg)
print("========")
