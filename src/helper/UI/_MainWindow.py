# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/helper/UI/mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(699, 528)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/app_blue.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setMidLineWidth(0)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName("splitter")
        self.tabWidget = QtWidgets.QTabWidget(self.splitter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.tabWidget.setFont(font)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.claimText = QtWidgets.QTextEdit(self.tab)
        self.claimText.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.claimText.setObjectName("claimText")
        self.horizontalLayout_3.addWidget(self.claimText)
        self.tabWidget.addTab(self.tab, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.tab_3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(-1, 0, -1, -1)
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setVerticalSpacing(3)
        self.gridLayout.setObjectName("gridLayout")
        self.figureText = QtWidgets.QTextEdit(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.figureText.sizePolicy().hasHeightForWidth())
        self.figureText.setSizePolicy(sizePolicy)
        self.figureText.setMinimumSize(QtCore.QSize(0, 0))
        self.figureText.setMaximumSize(QtCore.QSize(150, 16777215))
        self.figureText.setObjectName("figureText")
        self.gridLayout.addWidget(self.figureText, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.tab_3)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.tab_3)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.descriptionText = QtWidgets.QTextEdit(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.descriptionText.sizePolicy().hasHeightForWidth())
        self.descriptionText.setSizePolicy(sizePolicy)
        self.descriptionText.setObjectName("descriptionText")
        self.gridLayout.addWidget(self.descriptionText, 1, 0, 1, 1)
        self.gridLayout.setColumnStretch(0, 3)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setRowStretch(1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.tab_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.abstractText = QtWidgets.QTextEdit(self.tab_2)
        self.abstractText.setObjectName("abstractText")
        self.horizontalLayout_2.addWidget(self.abstractText)
        self.tabWidget.addTab(self.tab_2, "")
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 3, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.resultText = QtWidgets.QTextBrowser(self.layoutWidget)
        self.resultText.setObjectName("resultText")
        self.verticalLayout.addWidget(self.resultText)
        self.horizontalLayout_4.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 699, 22))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        self.menu_H = QtWidgets.QMenu(self.menubar)
        self.menu_H.setObjectName("menu_H")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setIconSize(QtCore.QSize(24, 24))
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.widgetToolBar = QtWidgets.QToolBar(MainWindow)
        self.widgetToolBar.setObjectName("widgetToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.widgetToolBar)
        self.loginAction = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/login_blue.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.loginAction.setIcon(icon1)
        self.loginAction.setObjectName("loginAction")
        self.closeAction = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/close_blue.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.closeAction.setIcon(icon2)
        self.closeAction.setObjectName("closeAction")
        self.copyAction = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/copy_blue.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.copyAction.setIcon(icon3)
        self.copyAction.setObjectName("copyAction")
        self.cutAction = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/cut_blue.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cutAction.setIcon(icon4)
        self.cutAction.setObjectName("cutAction")
        self.pasteAction = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/paste_blue.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pasteAction.setIcon(icon5)
        self.pasteAction.setObjectName("pasteAction")
        self.searchAction = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/search_blue.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.searchAction.setIcon(icon6)
        self.searchAction.setObjectName("searchAction")
        self.cmpAction = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icons/cmp_blue.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmpAction.setIcon(icon7)
        self.cmpAction.setObjectName("cmpAction")
        self.deadlineAction = QtWidgets.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icons/calendar_blue.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.deadlineAction.setIcon(icon8)
        self.deadlineAction.setObjectName("deadlineAction")
        self.archiveAction = QtWidgets.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/icons/archive_blue.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.archiveAction.setIcon(icon9)
        self.archiveAction.setObjectName("archiveAction")
        self.docAction = QtWidgets.QAction(MainWindow)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/icons/doc_blue.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.docAction.setIcon(icon10)
        self.docAction.setObjectName("docAction")
        self.aboutAction = QtWidgets.QAction(MainWindow)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/icons/about_blue.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.aboutAction.setIcon(icon11)
        self.aboutAction.setObjectName("aboutAction")
        self.settingAction = QtWidgets.QAction(MainWindow)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/icons/setting_blue.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.settingAction.setIcon(icon12)
        self.settingAction.setObjectName("settingAction")
        self.menu.addAction(self.loginAction)
        self.menu.addSeparator()
        self.menu.addAction(self.closeAction)
        self.menu_2.addAction(self.copyAction)
        self.menu_2.addAction(self.cutAction)
        self.menu_2.addAction(self.pasteAction)
        self.menu_2.addSeparator()
        self.menu_2.addAction(self.searchAction)
        self.menu_3.addAction(self.cmpAction)
        self.menu_3.addAction(self.deadlineAction)
        self.menu_3.addAction(self.archiveAction)
        self.menu_3.addSeparator()
        self.menu_3.addAction(self.settingAction)
        self.menu_H.addAction(self.docAction)
        self.menu_H.addAction(self.aboutAction)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_H.menuAction())
        self.toolBar.addAction(self.cmpAction)
        self.toolBar.addAction(self.deadlineAction)
        self.toolBar.addAction(self.archiveAction)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.settingAction)
        self.toolBar.addAction(self.loginAction)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        self.closeAction.triggered.connect(MainWindow.close) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Helper-专利审查助手"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "权利要求书"))
        self.label.setText(_translate("MainWindow", "说明书:"))
        self.label_2.setText(_translate("MainWindow", "附图:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "说明书及附图"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "摘要"))
        self.label_3.setText(_translate("MainWindow", "查找结果:"))
        self.menu.setTitle(_translate("MainWindow", "账户(&A)"))
        self.menu_2.setTitle(_translate("MainWindow", "编辑(&E)"))
        self.menu_3.setTitle(_translate("MainWindow", "工具(&T)"))
        self.menu_H.setTitle(_translate("MainWindow", "帮助(&H)"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.widgetToolBar.setWindowTitle(_translate("MainWindow", "toolBar_2"))
        self.loginAction.setText(_translate("MainWindow", "登录(&L)"))
        self.loginAction.setToolTip(_translate("MainWindow", "登录"))
        self.loginAction.setStatusTip(_translate("MainWindow", "登录i系统账号以获取审查数据"))
        self.closeAction.setText(_translate("MainWindow", "关闭(&E)"))
        self.closeAction.setToolTip(_translate("MainWindow", "关闭此应用"))
        self.copyAction.setText(_translate("MainWindow", "复制(&C)"))
        self.copyAction.setToolTip(_translate("MainWindow", "复制"))
        self.copyAction.setShortcut(_translate("MainWindow", "Ctrl+C"))
        self.cutAction.setText(_translate("MainWindow", "剪切(&T)"))
        self.cutAction.setToolTip(_translate("MainWindow", "剪切"))
        self.cutAction.setShortcut(_translate("MainWindow", "Ctrl+X"))
        self.pasteAction.setText(_translate("MainWindow", "粘贴(&P)"))
        self.pasteAction.setToolTip(_translate("MainWindow", "粘贴"))
        self.pasteAction.setShortcut(_translate("MainWindow", "Ctrl+V"))
        self.searchAction.setText(_translate("MainWindow", "查找(&S)"))
        self.searchAction.setToolTip(_translate("MainWindow", "查找"))
        self.searchAction.setShortcut(_translate("MainWindow", "Ctrl+F"))
        self.cmpAction.setText(_translate("MainWindow", "文本比较(&B)"))
        self.cmpAction.setToolTip(_translate("MainWindow", "文本比较"))
        self.cmpAction.setStatusTip(_translate("MainWindow", "打开文本比较器"))
        self.deadlineAction.setText(_translate("MainWindow", "周期管理(&Z)"))
        self.deadlineAction.setToolTip(_translate("MainWindow", "周期管理"))
        self.deadlineAction.setStatusTip(_translate("MainWindow", "查看和管理案件审查周期"))
        self.archiveAction.setText(_translate("MainWindow", "结案数据(&J)"))
        self.archiveAction.setToolTip(_translate("MainWindow", "结案数据"))
        self.archiveAction.setStatusTip(_translate("MainWindow", "查看当月结案数据"))
        self.docAction.setText(_translate("MainWindow", "使用说明(&D)"))
        self.docAction.setToolTip(_translate("MainWindow", "打开使用说明"))
        self.aboutAction.setText(_translate("MainWindow", "关于(&A)"))
        self.aboutAction.setToolTip(_translate("MainWindow", "关于此应用"))
        self.settingAction.setText(_translate("MainWindow", "设置(&S)"))
        self.settingAction.setToolTip(_translate("MainWindow", "设置"))
        self.settingAction.setStatusTip(_translate("MainWindow", "设置"))
import resources_rc
