from lib import *
from backend import *


class AddData_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.addData_window = ui_addData_window.Ui_MainWindow()
        self.addData_window.setupUi(self) 

        self.addData_window.addRow_btn.clicked.connect(lambda: self.addRow())
        self.addData_window.addData_btn.clicked.connect(lambda: self.commitData())

        self.checkCondition = CheckCondition()
        self.database_manager= DatabaseManager()
        self.checkList = []
        self.dataTable = []

    def addRow(self):
        noRow= self.addData_window.addData_table.rowCount()
        self.addData_window.addData_table.insertRow(noRow)
    
    def commitData(self):
        #If there are a row which miss information
        noRow= self.addData_window.addData_table.rowCount()
        checkVal = True
        for i in range(noRow):
            for j in range(28):
                
                if self.addData_window.addData_table.item(i, j).text() == None:
                    checkVal = False
                    break
            if checkVal == False:
                break
        if checkVal == False:
            print("You need fill all information!")
        else: 
            # ---------------------------------------
            # Check condition of inputting data value 
            for i in range (noRow):
                self.checkList.clear()
                for j in range(28):
                    self.checkList.append(self.addData_window.addData_table.item(i, j).text())
                if self.checkCondition.checkCondition(self.checkList) != "":
                    checkVal = False
        # Import data into SQL Server
        if checkVal == False:
            print(self.checkCondition.checkCondition(self.checkList))
        else:
            for i in range (noRow):
                self.checkList.clear()
                for j in range(28):
                    self.checkList.append(self.addData_window.addData_table.item(i, j).text())
                self.dataTable.append(self.checkList)
            self.database_manager.add_function(self.dataTable)
            self.dataTable.clear()
            self.close()


class home(QMainWindow):
    def __init__(self):
        super().__init__()
        # Display the screen
        self.homePage = ui_home.Ui_MainWindow()
        self.homePage.setupUi(self) 

        # Declare Manager Task Class
        self.database_manager = DatabaseManager()
        self.csv_handler = CSVHandler()
        self.checkCondition = CheckCondition()

        # Update database with real time
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: self.database_manager.updateDB())
        self.timer.start(5000)

        # Begin Function
        self.connectBtn()


        # Declare other 
        self.DATableList = []

    def connectBtn(self):      
        self.homePage.openCSV_btn.clicked.connect(lambda: self.openCSVProcess())
        self.homePage.add_btn.clicked.connect(lambda: self.open_addData_window())
        self.database_manager.deleteDB()

    def openCSVProcess(self):
        self.database_manager.importCSV_SQL(self.csv_handler.open_csv_file())
        self.importSQL_Table()

    def importSQL_Table(self):
        # Pre-tranform
        self.DATableList.clear()
        self.database_manager.updateDB()

        # Import customerTable, dateTable, factTable into DATableList
        for row in range(len(self.database_manager.factTable)):
            self.DATableList.append([]) #Create row in array
            # fill date into col from 0 - 6
            for col in range(7):
                self.DATableList[row].append(self.database_manager.customerTable[row][col])
            # fill date into col 7
            date = str(self.database_manager.dateTable[row][2]) + "/" +str(self.database_manager.dateTable[row][3]) + "/" +str(self.database_manager.dateTable[row][1]) 
            self.DATableList[row].append(date)
            # fill date into col 8
            self.DATableList[row].append(self.database_manager.factTable[row][20])
            # fill col 9 - 14
            for col in range(7,13):
                self.DATableList[row].append(self.database_manager.factTable[row][col])
            # fill col 15 - 19
            for col in range(2,7):
                self.DATableList[row].append(self.database_manager.factTable[row][col])
            # fill col 20 - 26
            for col in range(13,20):
                self.DATableList[row].append(self.database_manager.factTable[row][col])
            # fill col 27
            self.DATableList[row].append(self.database_manager.factTable[row][1])

        # Convert array into
        self.homePage.da_table.setRowCount(0)
        for i in range(len(self.DATableList)):
            rowPosition = self.homePage.da_table.rowCount()
            self.homePage.da_table.insertRow(rowPosition)
            for j in range(28):
                self.homePage.da_table.setItem(rowPosition, j+2, QTableWidgetItem(str(self.DATableList[i][j])))
        for row in range(self.homePage.da_table.rowCount()):
            button = QPushButton("Edit")
            self.homePage.da_table.setCellWidget(row, 0, button)
            button.clicked.connect(lambda _, row = row: self.editData(row))
        for row in range(self.homePage.da_table.rowCount()):
            button = QPushButton("Delete")
            self.homePage.da_table.setCellWidget(row, 1, button)    
            button.clicked.connect(lambda _, row = row: self.deleteData(int(self.homePage.da_table.item(row,2).text())))
        
        # item editting is disable
        for row in range(self.homePage.da_table.rowCount()):
            for column in range(2, self.homePage.da_table.columnCount()):
                item = self.homePage.da_table.item(row, column)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)

    def editData(self, row):
        edit_button = self.homePage.da_table.cellWidget(row, 0)
        edit_button.setText("Save")
        yellow_brush = QBrush(QColor("yellow"))
        for i in range(3,30):
            item=self.homePage.da_table.item(row, i)
            item.setBackground(yellow_brush)
            item.setFlags(item.flags() | Qt.ItemIsEditable)
        edit_button.clicked.connect(lambda _, row=row: self.saveData_afterEdit(row))
    
    def saveData_afterEdit(self, row):
        filterList = []
        checkList = []

        # Create a list including editting data of row => Check condition
        for col in range (2, 30):
            checkList.append(self.homePage.da_table.item(row,col).text())
        
            if self.checkCondition.checkCondition(checkList) == "": # Check the valid of editting data
                for row in range(self.homePage.da_table.rowCount()):
                    filterList.append([])
                    for col in range(2,30):
                        filterList[row].append(self.homePage.da_table.item(row, col).text()) 
                # Save Data after editting in database
                self.database_manager.saveData_afterEdit(filterList)
                # Re-display data on the screen after saving
                self.importSQL_Table()
                # Notify save successfully!
                self.noti("Save successfully!")
            else: 
                self.noti(self.checkCondition.checkCondition(checkList))

    def deleteData(self, userId):
        self.database_manager.delete_function(userId)     
        self.importSQL_Table()

    #================================================================================================================================================
    #METHOD TO OPEN ORTHER WINDOW
    def open_addData_window(self):
        self.addData_window = AddData_Window()
        self.addData_window.show()
        #self.edit_item_window.closed.connect(lambda: self.update_main_window(itemfilter, task))

    def closeEvent(self, event):
        # Ask the user if they want to delete before closing the window
        reply = QMessageBox.question(self, 'Message', 'Do you want to exist?', 
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # Perform the delete operation of the DatabaseManager
            self.database_manager.deleteDB()
            event.accept()
        else:
            # Ngăn không cho đóng cửa sổ
            event.ignore()
    
    def noti(self, notification):
        noti = QMessageBox()
        noti.setWindowTitle("Notification Window")
        noti.setIcon(QMessageBox.Information)
        noti.setText(notification)
        noti.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = home()
    window.setWindowTitle('My Software')
    window.setGeometry(100, 100, 2000, 1800)
    window.show()
    sys.exit(app.exec_())