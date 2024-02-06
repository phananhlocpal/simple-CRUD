from lib import *

class home(QMainWindow):
    def __init__(self):
        super().__init__()
        # Display the screen
        self.homePage = ui_home.Ui_MainWindow()
        self.homePage.setupUi(self) 
        self.factTable = db.execute("SELECT * FROM FACT").fetchall()
        self.dateTable = db.execute("SELECT * FROM Dim_Date").fetchall()
        self.customerTable = db.execute("SELECT * FROM Dim_Customer").fetchall()

        # Declare list, dict, class from classTask
     
        #Update database
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: self.updateDB())
        #self.timer.timeout.connect(self.format_list_staff)
        self.timer.start(5000)

        # Call design and connect functions
        #self.designComboBox()
        self.connect()
     

    def updateDB(self):
        self.raw_fact = db.execute("SELECT * FROM FACT")
        self.raw_date = db.execute("SELECT * FROM Dim_Date")
        self.raw_customer = db.execute("SELECT * FROM Dim_Customer")
        self.factTable = self.raw_fact.fetchall()
        self.dateTable = self.raw_fact.fetchall()
        self.customerTable = self.raw_fact.fetchall()

    def connect(self):
        
        # Interact in the stackedWidget
            # 1. Click the button
      
        self.homePage.openCSV_btn.clicked.connect(lambda: self.middleman_openCSV()) # Click "Create Supplier Button" in page "Create Supplier"
    
    #================================================================================================================================================
    # MIDDLEMAN METHOD
    def middleman_openCSV(self):
        self.updateDB()
    
    def middleman_openCSV(self):
        option = QFileDialog.Option()
        file, _ = QFileDialog.getOpenFileName(None, "Open File", "", "*.csv", options=option)
        # Đọc file CSV và lưu vào DataFrame
        df = pd.read_csv(file)

        filter_list = df.values.tolist()

        self.addToTable(filter_list)

    # 3. Table
    #<===> 3.1 List Item Table
    def addToTable(self, filter_list: list):
        self.updateDB()
        if filter_list == []:
            self.noti("The system doesnt have any invoice.")
        else:
            self.homePage.da_table.setRowCount(0)
            for i in range(len(filter_list)):
                rowPosition = self.homePage.da_table.rowCount()
                self.homePage.da_table.insertRow(rowPosition)
                for j in range(39):
                    self.homePage.da_table.setItem(rowPosition, j, QTableWidgetItem(str(filter_list[i][j])))
                
    #================================================================================================================================================
    # DEFAUT PAGE
    # 1. Create Item
    def default_createItem(self):
        self.homePage.NameItem.setText("")
        self.homePage.descriptionItem.setText("")
        self.homePage.priceItem.setText("")
   
    #================================================================================================================================================
    # FUNCTION TO CREATE SOMETHING
    # 1. Create BE (BE and BE_detail)
    def createBE(self):
        if self.homePage.BECreateUserId.text() == "":
            self.noti("You must input UserId!")
        else:
            try:
                userId, userName = str(self.homePage.BECreateUserId.text()).split(" - ")
                self.BE_label.createBE(self.homePage.BECreateId.text(), userId)
                for i in range (self.homePage.CreateBETable.rowCount()):
                    self.BE_Detail_label.createBE_Detail(int(self.homePage.BECreateId.text()),int(self.homePage.CreateBETable.item(i,0).text()),int(self.homePage.CreateBETable.cellWidget(i,2).value()))
                self.noti('Buying Entry imported successfully!')
                self.defaut_createBE() 
            except ValueError:
                self.noti('Value Error!')
            except Exception as e:
                self.noti(f'Have error: {e}!')
    # 2. Create Invoice (Invoice and Invoice_detail)
    def createInvoice(self):
        itemInvoice_list = []
        if self.homePage.itemInvoice.rowCount == 0:
            self.noti("You must input item before creating invoices!")
        else:
            if self.homePage.findCustomerInvoiceInput.text() == "":
                customerId = ""
            else: customerId, customerName = str(self.homePage.findCustomerInvoiceInput.text()).split(" - ")
            invoiceId = len(self.invoice_label.invoiceTable) + 10001
            totalDisplay = self.totalDisplay()
            self.invoice_label.createInvoice(invoiceId, self.homePage.methodInvoice.currentText(), int(totalDisplay), customerId, "1000")
            for i in range (self.homePage.itemInvoice.rowCount()):
                spinBox = self.homePage.itemInvoice.cellWidget(i, 3)
                value = spinBox.value()
                itemInvoice_dict = {"itemId": int(self.homePage.itemInvoice.item(i, 0).text()), "deviation": -int(value)}
                itemInvoice_list.append(itemInvoice_dict)
                self.invoiceDetail_label.createInvoice_Detail(invoiceId, int(self.homePage.itemInvoice.item(i, 0).text()), int(value), int(self.homePage.itemInvoice.item(i, 4).text()))
            self.invoiceDetail_label.updateStock_afterSELL(invoiceId, itemInvoice_list)
            self.noti("Create invoice successfully!")
            self.defaut_createInvoice()
    

    #===============================================================================================================================================
    # FUNCTION TO FILTER
    # 1. List Items
    def LIFilter(self):
        Itemfilter = []
        # Get the selected label, supplier, and status values
        label_value = self.homePage.LILabel.currentText()
        supplier_value = self.homePage.LISupplier.currentText()
        status_value = self.homePage.LIStatus.currentText()
        # Check if "All" is selected for any of the filters
        if label_value == "All":
            label_value = None
        if supplier_value == "All":
            supplier_value = None
        if status_value == "All":
            status_value = None
        # Generate the filter based on the selected values
        if label_value is not None and supplier_value is not None and status_value is not None:
            Itemfilter = list(filter(lambda x: x[3] == label_value and x[5] == int(db.execute(f"SELECT Id FROM Suplier WHERE Name = '{supplier_value}'").fetchone()[0]) and x[7] == (1 if status_value == "Available" else 0), self.item_label.itemTable))
        elif label_value is not None and supplier_value is not None and status_value is None:
            Itemfilter = list(filter(lambda x: x[3] == label_value and x[5] == int(db.execute(f"SELECT Id FROM Suplier WHERE Name = '{supplier_value}'").fetchone()[0]), self.item_label.itemTable))
        elif label_value is not None and supplier_value is None and status_value is not None:
            Itemfilter = list(filter(lambda x: x[3] == label_value and x[7] == (1 if status_value == "Available" else 0), self.item_label.itemTable))
        elif label_value is not None and supplier_value is None and status_value is None:
            Itemfilter = list(filter(lambda x: x[3] == label_value, self.item_label.itemTable))
        elif label_value is None and supplier_value is not None and status_value is not None:
            Itemfilter = list(filter(lambda x: x[5] == int(db.execute(f"SELECT Id FROM Suplier WHERE Name = '{supplier_value}'").fetchone()[0]) and x[7] == (1 if status_value == "Available" else 0), self.item_label.itemTable))
        elif label_value is None and supplier_value is not None and status_value is None:
            Itemfilter = list(filter(lambda x: x[5] == int(db.execute(f"SELECT Id FROM Suplier WHERE Name = '{supplier_value}'").fetchone()[0]), self.item_label.itemTable))
        elif label_value is None and supplier_value is None and status_value is not None:
            Itemfilter = list(filter(lambda x: x[7] == (1 if status_value == "Available" else 0), self.item_label.itemTable))
        else:
            Itemfilter = self.item_label.itemTable

        return Itemfilter
    # 2. List Customers
    def LCFilter(self):
        self.customer_label.update_db()
        customerfilter = []
        text = str(self.homePage.LCFindCustomer.text())
        if " - " in text:
            customerId, customerName = text.split(" - ")
            phone = db.execute(f"SELECT Phone FROM Customer WHERE Id = {customerId}").fetchone()[0]
            email = db.execute(f"SELECT Email FROM Customer WHERE Id = {customerId}").fetchone()[0]
            address = db.execute(f"SELECT Address FROM Customer WHERE Id = {customerId}").fetchone()[0]
            customerfilter = [(customerId, customerName, phone, email, address)]
        return customerfilter
    # 3. List Invoices
    def invoiceFilter(self):
        self.invoice_label.update_db()
        invoiceFilter = []
        displayTest = ""
        check = True
        text = str(self.homePage.listInvoiceFindInput.text())
        if text != "":
            if " - " in text:
                customerId, customerName = text.split(" - ")
                customerId_test = db.execute("SELECT * FROM Customer WHERE Id = ?", customerId).fetchone()[0]
                customerName_test = db.execute("SELECT Name FROM Customer WHERE Id = ?", customerId).fetchone()[0]
                if not customerId_test or not customerName_test:
                    check = False
                    displayTest += "The customer information input is invalid.\n"
        date_to = self.homePage.dateInvoiceTo.dateTime().toPyDateTime()
        date_from = self.homePage.dateInvoiceFrom.dateTime().toPyDateTime()
        if date_from > date_to:
            check = False
            displayTest += "Start date must be before end date.\n"
        if check == False:
            displayTest += "Please re-input!"
            self.noti(displayTest)
        else:
            for i in range (len(self.invoice_label.invoiceTable)):
                date_str = db.execute("SELECT BuyingDate FROM Invoice WHERE Id = ?", (self.invoice_label.invoiceTable[i][0])).fetchone()[0]
                date_obj = datetime.datetime.strptime(date_str.strftime('%d/%m/%Y'), '%d/%m/%Y')
                if text == "":
                    if self.invoice_label.invoiceTable[i][1].date() >= date_from.date() and self.invoice_label.invoiceTable[i][1].date() <= date_to.date():
                        invoiceFilter.append(self.invoice_label.invoiceTable[i])
                else:
                    if int(customerId) == self.invoice_label.invoiceTable[i][4]:
                        if self.invoice_label.invoiceTable[i][1] >= date_from and self.invoice_label.invoiceTable[i][1] <= date_to:
                            invoiceFilter.append(self.invoice_label.invoiceTable[i])
        return invoiceFilter
    # 4. List BE
    def BEFilter(self):
        self.BE_label.update_db()
        listBEFilter = []
        draft = []
        displayTest = ""
        check = True
        cre_date_to = self.homePage.CredateBETo.dateTime().toPyDateTime()
        cre_date_from = self.homePage.CredateBEFrom.dateTime().toPyDateTime()
        if self.homePage.statusBECB.currentText() == "Confirmed":
            status = 1
        elif self.homePage.statusBECB.currentText() == "Not confirmed":
            status = 0
        else: status = 2
        if cre_date_from > cre_date_to:
            check = False
            displayTest += "With creation day, start date must be before end date.\n"
        if check == False:
            displayTest += "Please re-input!"
            self.noti(displayTest)
            
        else:
            
            for i in range (len(self.BE_label.BETable)):
                if status == 2:
                    if self.BE_label.BETable[i][1].date() >= cre_date_from.date() and self.BE_label.BETable[i][1].date() <= cre_date_to.date():
                        listBEFilter.append(self.BE_label.BETable[i])
                else:
                    if self.BE_label.BETable[i][1].date() >= cre_date_from.date() and self.BE_label.BETable[i][1].date() <= cre_date_to.date() and self.BE_label.BETable[i][3] == status:
                        draft.append(self.BE_label.BETable[i])
                    listBEFilter = list(filter(lambda x: x[3] == status, draft))
        return listBEFilter
    # 5. Stock
    def stockFilter(self):
        stockFilter = []
        # Get the selected label, supplier, and status values
        label_value = self.homePage.SMLabel.currentText()
        supplier_value = self.homePage.SMSupplier.currentText()
        status_value = self.homePage.SMStatus.currentText()
        # Check if "All" is selected for any of the filters
        if label_value == "All":
            label_value = None
        if supplier_value == "All":
            supplier_value = None
        if status_value == "All":
            status_value = None
        # Generate the filter based on the selected values
        if label_value is not None and supplier_value is not None and status_value is not None:
            stockFilter = list(filter(lambda x: x[3] == label_value and x[5] == int(db.execute(f"SELECT Id FROM Suplier WHERE Name = '{supplier_value}'").fetchone()[0]) and x[7] == (1 if status_value == "Available" else 0), self.item_label.itemTable))
        elif label_value is not None and supplier_value is not None and status_value is None:
            stockFilter = list(filter(lambda x: x[3] == label_value and x[5] == int(db.execute(f"SELECT Id FROM Suplier WHERE Name = '{supplier_value}'").fetchone()[0]), self.item_label.itemTable))
        elif label_value is not None and supplier_value is None and status_value is not None:
            stockFilter = list(filter(lambda x: x[3] == label_value and x[7] == (1 if status_value == "Available" else 0), self.item_label.itemTable))
        elif label_value is not None and supplier_value is None and status_value is None:
            stockFilter = list(filter(lambda x: x[3] == label_value, self.item_label.itemTable))
        elif label_value is None and supplier_value is not None and status_value is not None:
            stockFilter = list(filter(lambda x: x[5] == int(db.execute(f"SELECT Id FROM Suplier WHERE Name = '{supplier_value}'").fetchone()[0]) and x[7] == (1 if status_value == "Available" else 0), self.item_label.itemTable))
        elif label_value is None and supplier_value is not None and status_value is None:
            stockFilter = list(filter(lambda x: x[5] == int(db.execute(f"SELECT Id FROM Suplier WHERE Name = '{supplier_value}'").fetchone()[0]), self.item_label.itemTable))
        elif label_value is None and supplier_value is None and status_value is not None:
            stockFilter = list(filter(lambda x: x[7] == (1 if status_value == "Available" else 0), self.item_label.itemTable))
        else:
            stockFilter = self.item_label.itemTable

        return stockFilter

    #================================================================================================================================================
    # FUNCTON TO FIND THE INFORMATION
    # 1. Item
    def FindItem(self):
        itemfilter = []
        text = str(self.homePage.LIFindItem.text())
        if " - " in text:
            itemId, itemName = text.split(" - ")
            try:
                description = db.execute(f"SELECT Description FROM Item WHERE Id = {itemId}").fetchone()[0]
                label = db.execute(f"SELECT Label FROM Item WHERE Id = {itemId}").fetchone()[0]
                price = db.execute(f"SELECT Price FROM Item WHERE Id = {itemId}").fetchone()[0]
                status = db.execute(f"SELECT Status FROM Item WHERE Id = {itemId}").fetchone()[0]
                unitId = db.execute(f"SELECT UnitId FROM Item WHERE Id = {itemId}").fetchone()[0]
                supplierId = db.execute(f"SELECT SupplierId FROM Item WHERE Id = {itemId}").fetchone()[0]
                itemfilter = [(itemId, itemName, description, label, unitId, supplierId, price, status)]
            except ValueError:
                self.noti("Value Error!")
            except Exception as e:
                self.noti(f"Error: {e}")
        return itemfilter
    # 2. Invoice (from inputting customer information)
    def findInvoice(self):
        invoiceFilter = []
        text = str(self.homePage.listInvoiceFindInput.text())
        if " - " in text:
            customerId, customerName = text.split(" - ")
            for i in range(len(self.invoice_label.invoiceTable)):
                invoice_draft = ()
                if self.invoice_label.invoiceTable[i][4] == int(customerId):
                    invoice_draft = (self.invoice_label.invoiceTable[i][0], self.invoice_label.invoiceTable[i][1], self.invoice_label.invoiceTable[i][2], self.invoice_label.invoiceTable[i][3], self.invoice_label.invoiceTable[i][4], self.invoice_label.invoiceTable[i][5])
                    invoiceFilter.append(invoice_draft)
        return invoiceFilter
    # 3. Stock
    def FindItemStock(self):
        stockFilter = []
        text = str(self.homePage.SMFindItem.text())
        if " - " in text:
            itemId, itemName = text.split(" - ")
            try:
                description = db.execute(f"SELECT Description FROM Item WHERE Id = {itemId}").fetchone()[0]
                label = db.execute(f"SELECT Label FROM Item WHERE Id = {itemId}").fetchone()[0]
                price = db.execute(f"SELECT Price FROM Item WHERE Id = {itemId}").fetchone()[0]
                status = db.execute(f"SELECT Status FROM Item WHERE Id = {itemId}").fetchone()[0]
                unitId = db.execute(f"SELECT UnitId FROM Item WHERE Id = {itemId}").fetchone()[0]
                supplierId = db.execute(f"SELECT SupplierId FROM Item WHERE Id = {itemId}").fetchone()[0]
                stockFilter = [(itemId, itemName, description, label, unitId, supplierId, price, status)]
            except ValueError:
                self.noti("Value Error!")
            except Exception as e:
                self.noti(f"Error: {e}")
        return stockFilter

    #================================================================================================================================================
    # UPDATE DATA
    # 1. Spinboxes data
    def update_spinboxes(self):
        for spinbox in self.spinboxes:
            spinbox.valueChanged.connect(self.updateTotal)
    # 2. Total Price each item when update amount
    def updateTotal(self):
        # get the spinbox that triggered the signal
        spinbox = self.sender()
        # get the row and column index of the spinbox in the table
        row = self.homePage.itemInvoice.indexAt(spinbox.pos()).row()
        column = self.homePage.itemInvoice.indexAt(spinbox.pos()).column()
        # calculate the new total value based on the spinbox value and price
        price = int(self.homePage.itemInvoice.item(row, 2).text())
        amount = spinbox.value()
        total = price * amount
        # update the total value in the table
        self.homePage.itemInvoice.setItem(row, 4, QTableWidgetItem(str(total)))
        self.totalDisplay()
    # 3. Stock Data
    def updateStock(self):
        check = True
        displayTest = ""
        # 3.1. Check the condition
        if self.homePage.UpdateStockTable.rowCount() == 0:
            check = False
            displayTest += "You haven't inputted any product to update yet.\n"
        if self.homePage.UpdateStockReason == "":
            check = False
            displayTest += "You haven't inputted reason to update yet.\n"
        if check == False:
            displayTest += "Please re-input."
            self.noti(displayTest)
        else:
            try:
                for i in range (self.homePage.UpdateStockTable.rowCount()):
                    amount = int(self.homePage.UpdateStockTable.item(i,2).text())
                    itemId= int(self.homePage.UpdateStockTable.item(i,0).text())
                    try:
                        db.execute("UPDATE STOCK SET amount = ? WHERE itemId = ?", (amount, itemId))
                        db.commit()
                    except ValueError:
                        self.noti("Value Error!")
                    except Exception as e:
                        self.noti(f"Error: {e}")
            except ValueError:
                self.noti("Value Error!")
            except Exception as e:
                self.noti(f"Error: {e}")
            self.default_updateStock()
            self.noti("Updated successfully!")

    #================================================================================================================================================
    # DISPLAY SOMETHING INFORMATION ON THE SCREEN 
    # 1. Display Customer information when enter find the customer in "CREATE AN INVOICE"
    def customerDisplay(self):
        customerID, customerName = str(self.homePage.findCustomerInvoiceInput.text()).split(" - ")
        try:
            customerPhone = db.execute("SELECT Phone FROM Customer WHERE Id = ?", customerID).fetchone()[0]
            customerEmail = db.execute("SELECT Email FROM Customer WHERE Id = ?", customerID).fetchone()[0]
            self.homePage.customerInfo.setText(f"1. Customer ID: {customerID}\n2. Customer Name: {customerName}\n3. Customer Phone Number: {customerPhone}\n4. Customer Email: {customerEmail}")
        except ValueError:
            self.noti("Value Error!")
        except Exception as e:
            self.noti(f"Error: {e}")
    # 2. Display the total when user input the item in "CREATE AN INVOICE"
    def totalDisplay(self):
        totalPrice = 0
        for i in range(self.homePage.itemInvoice.rowCount()):
            totalPrice += int(self.homePage.itemInvoice.item(i, 4).text())
            totalPrice_display = locale.currency(totalPrice, grouping=True).replace(",00", "")
        self.homePage.totalInvoice.setText(str(totalPrice_display))
        return totalPrice

    #================================================================================================================================================    
    # FUNCTION TO ADD ITEM INTO THE TABLE
    def deleteLineInput(self, lineInput: QLineEdit):
        lineInput.setText("")
        
    def pre_addTable(self, table: QTableWidgetItem, lineInput: QLineEdit, task):
        # Get the selected text from the completer
        
        if lineInput.text() == "":
            self.noti("You must input the item id!")
        else:
            # Split the selected text into Item ID and name
            item_id, item_name = str(lineInput.text()).split(" - ")

            # Define the amount cell
            if item_id in self.product_counts:
                self.product_counts[item_id] += 1
            else:
                self.product_counts[item_id] = 1

            if task == "CreateBE": 
                self.addTable_detail_BE(table,  item_id, item_name)
            elif task == "Invoice":
                self.addTable_detail_Invoice(table,  item_id, item_name)
            elif task == "UpdateStock":
                self.addTable_detail_UpdateStock(table, item_id, item_name)
        self.deleteLineInput(lineInput)
    # 1. Add to "Create BE" Table      
    def addTable_detail_BE(self, table: QTableWidgetItem, item_id, item_name):
        # If the item is not in the table, add it to the end
        check = False
        for i in range(table.rowCount()):
            if table.item(i, 0).text() == item_id:  
                amount = table.cellWidget(i, 2).value() + 1
                table.cellWidget(i, 2).setValue(amount)
                check = True
        
        if check == False:    
            row_position = table.rowCount()
            table.insertRow(row_position)
            table.setItem(row_position, 0, QTableWidgetItem(item_id))
            table.setItem(row_position, 1, QTableWidgetItem(item_name))
            spinbox = QSpinBox(table) # Create spinBox for amount value
            spinbox.setRange(1, 999)
            spinbox.setValue(1)
            table.setCellWidget(row_position, 2, spinbox)
    # 2. Add to "Create an invoice" Table
    def addTable_detail_Invoice(self, table: QTableWidgetItem, item_id, item_name):
        # If the item is not in the table, add it to the end
        check = False
        for i in range(table.rowCount()):
            if table.item(i, 0).text() == item_id:  
                amount = table.cellWidget(i, 3).value() + 1
                table.cellWidget(i, 3).setValue(amount)
                total = int(table.cellWidget(i, 3).value()) * int(table.item(i, 2).text())
                table.setItem(i,4, QTableWidgetItem(str(total)))
                check = True
        
        if check == False:
            row_position = table.rowCount()
            table.insertRow(row_position)
            table.setItem(row_position, 0, QTableWidgetItem(item_id))
            table.setItem(row_position, 1, QTableWidgetItem(item_name))
            price = db.execute(f"SELECT Price FROM Item WHERE Id = {item_id}").fetchone()[0]
            table.setItem(row_position, 2, QTableWidgetItem(str(price)))
            spinbox = QSpinBox(table) # Create spinBox for amount value
            spinbox.setRange(1, 999)
            spinbox.setValue(1)
            self.spinboxes.append(spinbox)
            table.setCellWidget(row_position, 3, spinbox)
            total = int(table.cellWidget(row_position, 3).value()) * int(table.item(row_position, 2).text())
            table.setItem(row_position,4, QTableWidgetItem(str(total)))
            self.update_spinboxes()
        
        self.totalDisplay()
    # 3. Add to "Update Stock Modifier" Table
    def addTable_detail_UpdateStock(self, table: QTableWidgetItem, item_id, item_name):
        #check if the item is not in table, create new row
        check = False
        for i in range(table.rowCount()):
            if table.item(i, 0).text() == item_id:  
                check = True
        if check == False:
            row_position = table.rowCount()
            table.insertRow(row_position)
            table.setItem(row_position, 0, QTableWidgetItem(item_id))
            table.setItem(row_position, 1, QTableWidgetItem(item_name))
  
    #================================================================================================================================================
   
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = home()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(window)
    widget.resize(800,600)
    widget.show()
    sys.exit(app.exec())