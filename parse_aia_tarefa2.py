#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Teste de verificação (correção automática)
    de script do curso AppInventor
    
    Fernando S. Pacheco - 2022
"""

import argparse
import logging
from parseaia import Project                                                                                                                                                         

cmparser = argparse.ArgumentParser(description='Parse Tarefa2 para curso AppInventor.')
cmparser.add_argument("-t", "--tarefa", dest="tarefa_id", choices=['1', '2', '3', '4'], help="Id da tarefa a avaliar")
cmparser.add_argument("-f", "--file", dest="file_name", help="Nome do arquivo. Default temporário: App_Oficina2_3.aia")
cmparser.add_argument("-l", "--log", dest="logLevel", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], help="Set the logging level")

args = cmparser.parse_args()
if args.logLevel:
    logging.basicConfig(level=getattr(logging, args.logLevel), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

if args.file_name == None:
    args.file_name = "App_Oficina2_3.aia"

mp = Project(args.file_name)
logger.info("Avaliando arquivo %s", args.file_name)

if args.tarefa_id:
    logger.info("Avaliando tarefa 2")

# Check number of screens
if (len(mp.screens) == 1):
    print("OK  : Tem uma tela")
else:
    print("FAIL: Número de telas não é um")

# Check if screen 1 has at least 1 button
ok = False
for comp in mp.screens[0].UI.Properties.Components:
    if (comp.Type == "Button"):
        print("OK  : Tela tem um botão")
        ok = True
if (ok == False):
    print("FAIL: Tela não tem um botão")

# Check if screen 1 has at least 1 sound
ok = False
for comp in mp.screens[0].UI.Properties.Components:
    if (comp.Type == "Sound"):
        print("OK  : Tela tem um objeto de áudio (som)")
        ok = True
if (ok == False):
    print("FAIL: Tela não tem um objeto de áudio (som)")

#Check if audio file is incorporated in the .aia
ok = False
for audio in mp.audio:
    if (audio.samples > 0):
        print("OK  : Tem um arquivo de áudio (som) incorporado")
        # TODO: Formato? Está ligado ao objeto?
        ok = True
if (ok == False):
    print("FAIL: Não tem um arquivo de áudio (som) incorporado")

# Check if app has an icon
# TODO: está procurando só na screen[0]. É suficiente?
try:
    if mp.screens[0].UI.Properties.Icon:
        print("OK  : App tem um ícone")
except:
    print("FAIL  : App não tem um ícone")

# Check if button has click
ok = False
for block in mp.screens[0].Code.blocks:
    if (block.component_type == "Button" and block.event_name == "Click"):
        print("OK  : Script tem um botão com evento clique")
        ok = True
if (ok == False):
    print("FAIL: Script não tem um botão com evento clique")

#Check if button is associated to an image
ok = False
for block in mp.screens[0].UI.Properties.Components:
    if (block.Type == "Button" and block.Image != None):
        print("OK  : Botão está associado a uma imagem")
        ok = True
if (ok == False):
    print("FAIL: Botão está associado a uma imagem")

#Check if app has a label
ok = False
for block in mp.screens[0].UI.Properties.Components:
    if (block.Type == "Label" and block.Text != None):
        print("OK  : App tem uma legenda (label)")
        ok = True
if (ok == False):
    print("FAIL: App tem uma legenda (label)")

# Check if sound has method play
ok = False
for block in mp.screens[0].Code.blocks:
    if block.type == "component_event":
        for statement in block.statements:
            if statement.child.mutation.component_type == "Sound" and statement.child.mutation.method_name == "Play":
                print("OK  : Script tem um som com método play")
                ok = True
if (ok == False):
    print("FAIL: Script não tem um som com método play")


"""    
Arquivo exemplo Tarefa2
https://codebeautify.org/xmlviewer

<xml
	xmlns="http://www.w3.org/1999/xhtml">
	<block type="component_event" id="$:7Zo}[,[6%y]_Xv9T`?" x="-1418" y="-674">
		<mutation component_type="Button" is_generic="false" instance_name="Bt_som" event_name="Click"></mutation>
		<field name="COMPONENT_SELECTOR">Bt_som</field>
		<statement name="DO">
			<block type="component_method" id="QkPhkLZ[|{-+uF*ZNn-{">
				<mutation component_type="Sound" method_name="Play" is_generic="false" instance_name="SOm_cao"></mutation>
				<field name="COMPONENT_SELECTOR">SOm_cao</field>
			</block>
		</statement>
	</block>
	<yacodeblocks ya-version="213" language-version="34"></yacodeblocks>
</xml>
"""

