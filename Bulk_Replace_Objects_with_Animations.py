from maya import cmds

def onTransferclick(*args): # Core Script Working
	
	transfer_value = []
	transfer_trans = cmds.checkBox("Trf_Trns", query=True, value=True)
	tranfer_rot = cmds.checkBox("Trf_Rot", query=True, value=True)
	transfer_scl = cmds.checkBox("Trf_Scl", query=True, value=True)
	if transfer_trans:
		transfer_value.append('tx')
		transfer_value.append('ty')
		transfer_value.append('tz')
	if tranfer_rot:
		transfer_value.append('rx')
		transfer_value.append('ry')
		transfer_value.append('rz')
	if transfer_scl:
		transfer_value.append('sx')
		transfer_value.append('sy')
		transfer_value.append('sz')
	
	#it stores the value of geomentry type as copy or instance
	geotype = cmds.radioCollection("Geometry_Type", query=True, select=True)
	geotypemode = cmds.radioButton(geotype, query=True, data=True)
	
	keepSourceConn = False
	inConn = True
	# First we check the radio collection to see which radio button is selected
	radio = cmds.radioCollection("Transfer_Type", query=True, select=True)
	# Then we use the radio button to see what its text says to get its value
	mode = cmds.radioButton(radio, query=True, data=True)
	if mode == -3:
		keepSourceConn=False
	else:
		keepSourceConn=True
	
	inConn = cmds.checkBox("animation", query=True, value=True)
	
	nlist =cmds.ls(sl=True)
	if len(nlist)>1 : #check is there any objects selected
		objectlist = cmds.ls(selection=True)
		lastselected = cmds.ls(selection=True, tail=1)
		Group = cmds.group( em=True, name='Transfered_Objects1' )
		objectlist.pop()
		
		for transfered in objectlist: #Duplicate objects and then transfer attribute to the duplicated objects
			if geotypemode == -3: #it checks that geo type as copy or instance and performe the function as required
				duplicatedobj = cmds.instance( lastselected )
			else:
				duplicatedobj = cmds.duplicate( lastselected, rr=True )
			#duplicatedobj = duplicatedas
			cmds.copyAttr(transfered, duplicatedobj, inConnections=inConn, keepSourceConnections=keepSourceConn, values=True, attribute=transfer_value)
			cmds.parent(duplicatedobj, Group)
	else: # if noting is selected then pass an error
		cmds.error( "Noting is Selected: Select at least 2 or more objects" )

radio_E_D = True

def diable_n_enable_radio(radio_E_D):
	radio_E_D = not radio_E_D
	cmds.refresh(currentView=True, force=True)
	#print(radio_E_D)

def hepWindow(*args): # show help window if that button is clicked from window
	hepWindowname = "Help"
	if cmds.window(hepWindowname, query=True, exists=True):
		cmds.deleteUI(hepWindowname)
	cmds.window(hepWindowname, menuBar=True, menuBarVisible=True, width=300, height=70, sizeable=False)
	cmds.showWindow(hepWindowname)
	cmds.columnLayout( adjustableColumn=True)
	cmds.text(label="First select all the object you want to replace")
	cmds.text(label="and then select the oblject you want to replace with")
	cmds.text(label="and then click on transfer button")
	cmds.text(label="Scripted by Ankush Gupta")
	cmds.text(label="artstation:(https://www.artstation.com/ankushgupta)")

def showWindow(): # Main UI for the script
    name = "BROA" #Bulk replace oblect with animation
    if cmds.window(name, query=True, exists=True):
        cmds.deleteUI(name)
    cmds.window(name, menuBar=True, menuBarVisible=True, width=300, height=100)
    helpMenu = cmds.menu( label='Help')
    cmds.menuItem( label='Help on Bulk Replace Objects with Animations', command=(hepWindow) )
    cmds.showWindow()
    
    colum = cmds.columnLayout( adjustableColumn=True)
    cmds.frameLayout( label="General Option", width=300, collapsable=True )
    cmds.columnLayout()
    
    cmds.rowLayout( numberOfColumns=2,columnWidth2=(120, 120), columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0)])
    cmds.text( label="Transfer:  ")
    cmds.checkBox( "Trf_Trns" ,label="Translate",value=True )
    cmds.setParent('..')
    cmds.rowLayout( numberOfColumns=2,columnWidth2=(120, 120), columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0)])
    cmds.text( label="")
    cmds.checkBox( "Trf_Rot" ,label="Rotate",value=True )
    cmds.setParent('..')
    cmds.rowLayout( numberOfColumns=2,columnWidth2=(120, 120), columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0)])
    cmds.text( label="")
    cmds.checkBox( "Trf_Scl" ,label="Scale",value=True )
    
    
    cmds.setParent('..')
    cmds.rowLayout( numberOfColumns=2,columnWidth2=(120, 120), columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0)])
    cmds.text( label="Geometry type:  ")
    cmds.radioCollection("Geometry_Type")
    cmds.radioButton( label="Copy", select=True, collection="Geometry_Type" )
    cmds.setParent('..')
    cmds.rowLayout( numberOfColumns=2,columnWidth2=(120, 120), columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0)])
    cmds.text( label="")
    cmds.radioButton( label="Instance", collection="Geometry_Type")
    
    cmds.setParent('..')
    cmds.rowLayout( numberOfColumns=2,columnWidth2=(120, 120), columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0)])
    cmds.text( label="In connections:  ")
    cmds.checkBox( "animation" ,label="",value=True, changeCommand=(diable_n_enable_radio) )   
    cmds.setParent('..')
    cmds.rowLayout( numberOfColumns=2,columnWidth2=(120, 120), columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0)])
    cmds.radioCollection("Transfer_Type")
    cmds.text( label=" ")
    cmds.radioButton( label="Share with source", select=True, collection="Transfer_Type", enable=radio_E_D )
    cmds.setParent('..')
    cmds.rowLayout( numberOfColumns=2,columnWidth2=(120, 120), columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0)])
    cmds.text( label="")
    cmds.radioButton( label="Tranfer form source", collection="Transfer_Type", enable=radio_E_D)
    
    cmds.setParent(colum)
    cmds.button( label="Transfer", command =(onTransferclick) )
    
showWindow()

# Scripted by Ankush Gupta [artstation:(https://www.artstation.com/ankushgupta)]

