"""Teste de verificação (correção automática)
    da tarefa 1 do curso AppInventor
    
    Fernando S. Pacheco - 2022
"""

import logging
from parseaia import Project
from parse.classes import OutMsg                                                                                                                                                         

logger = logging.getLogger(__name__)

def parse_tarefa1(filename):
    outmsg = OutMsg()
    mp = Project(filename)
    logger.info("Tarefa 1: avaliando arquivo %s", filename)

    # Check number of screens
    if len(mp.screens) == 1:
        outmsg.success.append("Tem uma tela")
    else:
        outmsg.fail.append("Número de telas não é um")

    # Check if screen 1 has at least 1 button
    ok = False
    for comp in mp.screens[0].UI.Properties.Components:
        if comp.Type == "Button":
            outmsg.success.append("Tela tem um botão")
            ok = True
    if ok == False:
        outmsg.fail.append("Tela não tem um botão")

    # Check if screen 1 has at least 1 sound
    ok = False
    for comp in mp.screens[0].UI.Properties.Components:
        if comp.Type == "Sound":
            outmsg.success.append("Tela tem um objeto de áudio (som)")
            ok = True
    if ok == False:
        outmsg.fail.append("Tela não tem um objeto de áudio (som)")

    #Check if audio file is incorporated in the .aia
    ok = False
    for audio in mp.audio:
        if (audio.samples > 0):
            outmsg.success.append("Tem um arquivo de áudio (som) incorporado")
            # TODO: Formato? Está ligado ao objeto?
            ok = True
    if ok == False:
        outmsg.fail.append("Não tem um arquivo de áudio (som) incorporado")

    # Check if app has an icon
    # TODO: está procurando só na screen[0]. É suficiente?
    try:
        if mp.screens[0].UI.Properties.Icon:
            outmsg.success.append("App tem um ícone")
    except:
        outmsg.fail.append("App não tem um ícone")

    # Check if button has click
    ok = False
    for block in mp.screens[0].Code.blocks:
        try:
            if (block.component_type == "Button" and block.event_name == "Click"):
                outmsg.success.append("Script tem um botão com evento clique")
                ok = True
                break
        except AttributeError:
            ok = False
    if ok == False:
        outmsg.fail.append("Script não tem um botão com evento clique")

    #Check if button is associated to an image
    ok = False
    for block in mp.screens[0].UI.Properties.Components:
        if (block.Type == "Button" and block.Image != None):
            outmsg.success.append("Botão está associado a uma imagem")
            ok = True
    if ok == False:
        outmsg.fail.append("Botão está associado a uma imagem")

    #Check if app has a label
    ok = False
    for block in mp.screens[0].UI.Properties.Components:
        if (block.Type == "Label" and block.Text != None):
            outmsg.success.append("App tem uma legenda (label)")
            ok = True
    if ok == False:
        outmsg.fail.append("App tem uma legenda (label)")

    # Check if sound has method play
    ok = False
    for block in mp.screens[0].Code.blocks:
        if block.type == "component_event":
            for statement in block.statements:
                try:
                    if statement.child.mutation.component_type == "Sound" and statement.child.mutation.method_name == "Play":
                        outmsg.success.append("Script tem um som com método play")
                        ok = True
                        break
                except AttributeError:
                    ok = False
    if ok == False:
        outmsg.fail.append("Script não tem um som com método play")
   

    return outmsg

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

