"""Teste de verificação (correção automática)
    das atividades do curso AppInventor
    
    Fernando S. Pacheco - 2022
"""

import logging
from parseaia import Project
from parse.classes import OutMsg                                                                                                                                                         

logger = logging.getLogger(__name__)

def check4Buttons(scr, outmsg):
    # Check if screen 2 has at least 4 buttons
    ok = False
    numButtons=0
    nameButtons=""
    if type(scr.UI.Properties.Components) is list:
        complist = scr.UI.Properties.Components
        for arrangement in complist:
            try:
                for comp in arrangement.Components:
                    if comp.Type == "Button":
                        numButtons = numButtons + 1
                        nameButtons = nameButtons + " " + comp.Name
            except:
                continue
    if numButtons>=4:
        outmsg.success.append("Tela "+scr.UI.Properties.Name+" tem "+str(numButtons)+" botões: "+nameButtons)
    else:
        outmsg.fail.append("Tela "+scr.UI.Properties.Name+" tem "+str(numButtons)+" botão. Deveria ter, no mínimo, 4")

def checkNotifiers(scr, outmsg):        
    # Check if screen 2 has one notifier
    ok = False
    numNotifiers=0
    if type(scr.UI.Properties.Components) is list:
        complist = scr.UI.Properties.Components
        try:
            for comp in complist:
                if comp.Type == "Notifier":
                    numNotifiers = numNotifiers + 1
        except:
            ok=False
    if numNotifiers == 1:
        outmsg.success.append("Tela "+scr.UI.Properties.Name+" tem "+str(numNotifiers)+" notificador")
    else:
        outmsg.fail.append("Tela "+scr.UI.Properties.Name+" tem "+str(numNotifiers)+" notificador. Deveria ter 1")
        
def check2Sounds(scr, outmsg):
    # Check if screen 2 has at least 2 sounds
    numAudioFiles=0
    for comp in scr.UI.Properties.Components:
        if comp.Type == "Sound":
            numAudioFiles = numAudioFiles + 1
    if numAudioFiles == 2:
        outmsg.success.append("Tela "+scr.UI.Properties.Name+" tem 2 objetos de áudio (som)")
    else:
        outmsg.fail.append("Tela "+scr.UI.Properties.Name+" tem "+str(numAudioFiles)+" objetos de áudio (som). Deveria ter 2")
        
def parse_tarefa2(filename):
    outmsg = OutMsg()
    #TODO: read validation_code from a file
    outmsg.validation_code = '112233'
    mp = Project(filename)
    logger.info("Tarefa 2: avaliando arquivo %s", filename)

    # Check number of screens
    if len(mp.screens) == 1:
        outmsg.success.append("Tem uma tela")
    else:
        outmsg.fail.append("Número de telas não é um")

    # Check if screen 1 has at least 1 button
    # INFO: Screen1 is always the first screen
    ok = False
    for comp in mp.Screen1.UI.Properties.Components:
        if comp.Type == "Button":
            outmsg.success.append("Tela tem um botão")
            ok = True
    if ok == False:
        outmsg.fail.append("Tela não tem um botão")

    # Check if screen 1 has at least 1 sound
    ok = False
    for comp in mp.Screen1.UI.Properties.Components:
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
    # INFO: If present, the icon is at Screen1
    try:
        if mp.Screen1.UI.Properties.Icon:
            outmsg.success.append("App tem um ícone")
    except:
        outmsg.fail.append("App não tem um ícone")

    # Check if button at Screen1 has click
    ok = False
    for block in mp.Screen1.Code.blocks:
        try:
            if (block.component_type == "Button" and block.event_name == "Click"):
                outmsg.success.append("Script tem um botão com evento clique")
                ok = True
                break
        except AttributeError:
            ok = False
    if ok == False:
        outmsg.fail.append("Script não tem um botão com evento clique")

    #Check if button is associated to an image (at Screen1)
    ok = False
    for block in mp.Screen1.UI.Properties.Components:
        try:
            if (block.Type == "Button" and block.Image != None):
                outmsg.success.append("Botão está associado a uma imagem")
                ok = True
                break
        except AttributeError:
            ok = False
    if ok == False:
        outmsg.fail.append("Botão não está associado a uma imagem")

    #Check if app has a label at Screen1
    ok = False
    for block in mp.Screen1.UI.Properties.Components:
        if (block.Type == "Label" and block.Text != None):
            outmsg.success.append("App tem uma legenda (label)")
            ok = True
    if ok == False:
        outmsg.fail.append("App tem uma legenda (label)")

    # Check if sound has method play at Screen1
    ok = False
    for block in mp.Screen1.Code.blocks:
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

# Recursively count compType elements, e.g., Button
# Works also for elements inside Arrangements (that is, inside a list of components)
def countComponents(compObj, compType):
    total = 0  
    for comp in compObj:
        if hasattr(comp, "Components"):
            total = total + countComponents(comp.Components, compType)
        else:
            if comp.Type == compType:
                total = total + 1
    return total

# Recursively check if Buttons have associated Image
def checkButtonImage(compObj, scrName, outmsg):
    total = 0  
    for comp in compObj:
        if hasattr(comp, "Components"):
            checkButtonImage(compObj=comp.Components, scrName=scrName, outmsg=outmsg)
        else:
            if comp.Type == "Button":
                if hasattr(comp, "Image") and comp.Image != None:
                    outmsg.success.append(scrName+" Botão "+comp.Name+" tem imagem associada")
                else:
                    outmsg.fail.append(scrName+" Botão "+comp.Name+" não tem imagem associada")

def checkScreenButtonImage(scr, outmsg):
    checkButtonImage(compObj=scr.UI.Properties.Components, scrName=scr.UI.Properties.Name, outmsg=outmsg)    

def parse_tarefa3(filename):
    outmsg = OutMsg()
    mp = Project(filename)
    logger.info("Tarefa 3: avaliando arquivo %s", filename)

    # Check if app has an icon
    # INFO: If present, the icon is at Screen1
    try:
        if mp.Screen1.UI.Properties.Icon:
            outmsg.success.append("App tem um ícone")
    except:
        outmsg.fail.append("App não tem um ícone")

    # Check number of screens
    if len(mp.screens) >= 5:
        outmsg.success.append("Tem "+str(len(mp.screens))+" telas")
    else:
        outmsg.fail.append("Tem "+str(len(mp.screens))+" telas. Deveria ter 5 ou mais")
     
    # Check if screen 1 has at least 2 buttons anywhere in the screen
    # INFO: Screen1 is always the first screen
    numButtons=countComponents(mp.Screen1.UI.Properties.Components, "Button")
    if numButtons>=2:
        outmsg.success.append("Tela 1 tem "+str(numButtons)+" botões")
    else:
        outmsg.fail.append("Tela 1 tem "+str(numButtons)+" botão. Deveria ter, no mínimo, 2") 
        
    #Check if audio file is incorporated in the .aia
    numAudioFiles=0
    for audio in mp.audio:
        numAudioFiles = numAudioFiles + 1
    if (numAudioFiles >= 5):
        outmsg.success.append("Tem "+str(numAudioFiles)+" arquivos de áudio (som) incorporados")
    else:
        outmsg.fail.append("Só tem "+str(numAudioFiles)+" arquivos de áudio. Deveria ter, no mínimo, 5")

    # Check if Screen1 has 2 buttons with click
    ok = False
    numButtons = 0
    for block in mp.Screen1.Code.blocks:
        try:
            if (block.component_type == "Button" and block.event_name == "Click"):
                numButtons = numButtons + 1
        except AttributeError:
            ok = False
    if numButtons >= 2:
                outmsg.success.append("Os "+str(numButtons)+" botões da Tela 1 tem evento clique")
    else:
        outmsg.fail.append("Tela 1 não tem 2 botões com evento clique")

    # Check if Screen1 / Button has action to open another screen
    ok = False
    for block in mp.Screen1.Code.blocks:
        try:
            if (block.component_type == "Button" and block.event_name == "Click"):
                if block.statements[0].child.type == "controls_openAnotherScreen":
                    outmsg.success.append("Tela 1 tem um botão que abre uma outra janela")
                    ok=True
                    break
        except AttributeError:
            ok = False
    if ok == False:
        outmsg.fail.append("Tela 1 não tem um botão que abre uma outra tela")

    # Check if Screen1 / Button has action to exit app
    ok = False
    for block in mp.Screen1.Code.blocks:
        try:
            if (block.component_type == "Button" and block.event_name == "Click"):
                if block.statements[0].child.type == "controls_closeApplication":
                    outmsg.success.append("Tela 1 tem um botão que fecha o aplicativo")
                    ok=True
                    break
        except AttributeError:
            ok = False
    if ok == False:
        outmsg.fail.append("Tela 1 não tem um botão que fecha o aplicativo")        

    #Check for screens
    for scr in mp.screens:
        if scr.UI.Properties.Name == "Screen1":
            continue
        check4Buttons(scr, outmsg)
        checkNotifiers(scr, outmsg)
        check2Sounds(scr, outmsg)
        checkScreenButtonImage(scr, outmsg)
          
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

