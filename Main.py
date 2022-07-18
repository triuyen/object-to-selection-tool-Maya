########################################################################################################################################

import maya.cmds as cmds
import sys, imp
from PySide2.QtCore import Qt
from PySide2 import QtCore, QtGui,QtWidgets
from shiboken2 import  wrapInstance

#######################################################################################################################################################################"

import maya.OpenMayaUI as omui

#################################################################################################


#####################################################################################################
# 
#   Creation of Main Window 
#
###################################################################################################

def maya_main_window():

    # keep the GUI Window in front despite the fact that you click on Maya viewport general
    # Return Maya main window as an object

    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance( int(main_window_ptr), QtWidgets.QWidget)

#####################################################################################################
# 
#   Main Class for joint creation GUI
#
###################################################################################################

class GUI(QtWidgets.QDialog):


    def __init__(self, parent = maya_main_window()) :

        super(GUI, self).__init__(parent)

        self.setWindowTitle( "TnT create_from_selection Tool")
        self.setMinimumWidth(400)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layout()

        self.create_connections()
    
    #####################################################################################################
    # 
    #   Widgets Creation function
    #
    ###################################################################################################

    def create_widgets(self):

        # joints create in middle of selection #########################################

        
        self.radius= QtWidgets.QLineEdit("1")

        # name of the input ###################################################################################""

        self.name= QtWidgets.QLineEdit("name")
        
        self.combo = QtWidgets.QComboBox()
        self.second_obj= QtWidgets.QLineEdit("object to be placed")

        self.create_replace_btn = QtWidgets.QPushButton(" Replace selection with ")
        self.create_fromselect_btn = QtWidgets.QPushButton( " Place object " )


    #####################################################################################################
    # 
    #   Layout Creation function
    #
    ###################################################################################################

    def create_layout(self):
        
        # Vertical Layout  
        create_creation_layout = QtWidgets.QVBoxLayout();
        create_creation_layout.addWidget( self.create_fromselect_btn )
        ##################################################################### 

        create_NAME_layout = QtWidgets.QHBoxLayout();
        create_NAME_layout.addWidget(self.name)
        create_NAME_layout.addWidget(self.radius)

        create_combo_layout = QtWidgets.QHBoxLayout();
        create_combo_layout.addWidget(self.combo)

        create_second_mesh_layout = QtWidgets.QVBoxLayout();
        create_second_mesh_layout.addWidget(self.second_obj)

        # the form for the name box dialog ######################################

        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow(create_creation_layout)

        form_layout.addRow(" Name & Radius", create_NAME_layout )
        form_layout.addRow(self.combo.insertItems(3,["joints","mesh", "Locator"]),create_combo_layout)
        form_layout.addItem(create_second_mesh_layout)

        ############################################################
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)

    def get_info_name_type(self):
      
            self.radius = self.radius.text()

            self.name = self.name.text()

            self.cb = self.combo.itemText(True)

            return self.radius, self.name, self.cb

    def create_connections(self):

        self.create_fromselect_btn.pressed.connect(self.create_joints)
        #self.create_fromselect_btn.click()

        pass

    ################################## FUNCTIONS #############################################################################"
    # 
    #   Get Info Function
    # 
    # ##########################################################################################################################

    def create_joints(self): # create the joint in the middle of selection
        
        self.rad = float(self.radius.text())
        self.naming = str(self.name.text())
        self.cb = str(self.combo.currentText())
        self.second = str(self.second_obj.text())
     
        vertex_sel = cmds.ls(sl=True)

        if vertex_sel == []:
            print(" nothing selected , please make selection ")
            pass

        elif self.cb == "Locator" :

            cluster_ = cmds.cluster(vertex_sel)
            cmds.select(d=True)
            loc = cmds.spaceLocator(n=self.naming)
            constr = cmds.parentConstraint(cluster_, loc , mo=False)
            cmds.delete(constr, cluster_)

            print("Locator created")

        elif self.cb == "mesh" :
            
            cluster_ = cmds.cluster(vertex_sel)
            cmds.select(d=True)

            second_mesh = cmds.ls(self.second)
            dupli = cmds.duplicate(second_mesh)

            constr = cmds.parentConstraint(cluster_, dupli , mo=False)
            cmds.delete(constr, cluster_)

            print("Locator created")
        else:
            cluster_ = cmds.cluster(vertex_sel)
            cmds.select(d=True)
            jnt = cmds.joint(n= self.naming, rad = self.rad)
            constr = cmds.parentConstraint(cluster_,jnt, mo=False)
            cmds.delete(constr, cluster_)

            print('joints created')

        cmds.select(d=True)

    def create_locator(self): # create the space locator in the middle of selection

        vertex_sel = cmds.ls(sl=True)
        cluster_ = cmds.cluster(vertex_sel)
        cmds.select(d=True)
        jnt = cmds.spaceLocator()
        constr = cmds.parentConstraint(cluster_,jnt, mo=False)
        cmds.delete(constr, cluster_)
    

    def create_sticky(radius):
        pass
        

    
    
if __name__ == "__main__":


    try:
        GUI.close() 
        GUI.deleteLater()
    
    except:
        pass

    test_dialog = GUI()
    test_dialog.show()

  
