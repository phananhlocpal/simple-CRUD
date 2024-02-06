from lib import *

class CheckCondition:
    def __init__(self):
        self.databaseManager = DatabaseManager()

    def checkCondition(self, checkList: list):
        # Check condition of inputting data value 
        noti = ""
        print(checkList)
        if checkList != []:
            duplicates = self.databaseManager.db.execute("SELECT userId, COUNT(*) as count FROM Dim_Customer GROUP BY userId HAVING COUNT(*) > 1").fetchall()
            if checkList[0].isdigit() == False or len(duplicates) > 0:
                noti += "Id is invalid or exsit in database!\n" 
            elif checkList[1].isdigit() == False:
                noti += "yearBirthday must be a number\n"
            elif checkList[4].isdigit() == False:
                noti += "income must be a number.\n"
            elif checkList[5].isdigit() == False:
                noti += "kidhome must be a number.\n"
            elif checkList[6].isdigit() == False:
                noti += "Teenhome must be a number.\n"
            elif checkList[8].isdigit() == False:
                noti += "recency must be a number.\n"
            elif checkList[9].isdigit() == False:

                noti += "MntWines must be a number.\n"
            elif checkList[10].isdigit() == False:
                checkVal = False
                noti += "MntFruits must be a number.\n"
            elif checkList[11].isdigit() == False:
                checkVal = False
                noti += "MntMeatProducts must be a number.\n"
            elif checkList[12].isdigit() == False:
                checkVal = False
                noti += "MntFishProducts must be a number.\n"
            elif checkList[13].isdigit() == False:
                checkVal = False
                noti += "MntSweetProducts must be a number.\n"
            elif checkList[14].isdigit() == False:
                checkVal = False
                noti += "MntGoldProds must be a number.\n"
            elif checkList[15].isdigit() == False:
                checkVal = False
                noti += "NumDealsPurchases must be a number.\n"
            elif checkList[16].isdigit() == False:
                checkVal = False
                noti += "NumWebPurchases must be a number.\n"
            elif checkList[17].isdigit() == False:
                checkVal = False
                noti += "NumCatalogPurchases must be a number.\n"
            elif checkList[18].isdigit() == False:
                checkVal = False
                noti += "NumStorePurchases must be a number.\n"
            elif checkList[19].isdigit() == False:
                noti += "NumWebVisitsMonth must be a number.\n"
            elif self.checkBool(checkList[20]) == False:
                noti += "AcceptedCmp3 must be a number (0 or 1).\n"
            elif self.checkBool(checkList[21]) == False:
                checkVal = False
                noti += "AcceptedCmp4 must be a number.\n"
            elif self.checkBool(checkList[22]) == False:
                checkVal = False
                noti += "AcceptedCmp5 must be a number.\n"
            elif self.checkBool(checkList[23]) == False:
                checkVal = False
                noti += "AcceptedCmp1 must be a number.\n"
            elif self.checkBool(checkList[24]) == False:
                checkVal = False
                noti += "AcceptedCmp2 must be a number.\n"
            elif self.checkBool(checkList[25]) == False:
                checkVal = False
                noti += "Response must be a number.\n"
            elif self.checkBool(checkList[26]) == False:
                checkVal = False
                noti += "Complain must be a number.\n"

            try:
                datetime.strptime(checkList[7], "%m/%d/%Y")
                pass
            except ValueError:
                noti += "Date needs format dd/mm/yyyy.\n"
            
        return noti

    def checkBool(self, text: str):
        if text == "True" or text == "False" or int(text) == 1 or int(text) == 0:
            return True
        else: return False

class DatabaseManager:
    def __init__(self):
        self.connectSQLDB()
        self.updateDB()
        
    def connectSQLDB(self):
        #Connect to SQL Database
        connection = pyodbc.connect('DRIVER = {ODBC Driver 18 for SQL Server}; SERVER=PAL; DATABASE=marketingDA; DSN=InventorySaleManagement; Trusted_Connection=yes; encrypt=yes; TrustServerCertificate=yes')
        self.db = connection.cursor()

        self.columns = self.db.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'FACT';").fetchall()

    def generate_random_key(self):
        existing_keys = self.db.execute("SELECT userId FROM FACT").fetchall()
        while True:
            random_key = random.randint(1, 1000000)
            if random_key not in existing_keys:
                break
        return random_key
    
    def generate_random_dateId(self):
        existing_keys = self.db.execute("SELECT dateId FROM FACT").fetchall()
        while True:
            random_key = random.randint(1, 1000000)
            if random_key not in existing_keys:
                break
        return random_key
    
    def importCSV_SQL(self, dataTable):
        self.dateId = 1
        for row in range(len(dataTable)):
            self.db.execute("INSERT INTO Dim_Customer VALUES (?, ?, ?, ?, ?, ?, ?, ?)", dataTable[row][0],dataTable[row][1],dataTable[row][2],dataTable[row][3],dataTable[row][4],dataTable[row][5],dataTable[row][6],dataTable[row][27])
            
            #Insert data into Dim_Date
                # Getting the day, month, and year from the datetime object
            date_object = datetime.strptime(dataTable[row][7], '%m/%d/%Y')  # Adjust the format if needed
            day = date_object.day
            month = date_object.month
            year = date_object.year

            insert_query = f"INSERT INTO Dim_Date VALUES (?, ?, ?, ?)"  
            self.db.execute(insert_query, self.dateId ,year, month,day)

            #Insert data into Dim_Date
            insert_query = f"INSERT INTO FACT VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )"  
            self.db.execute(insert_query, dataTable[row][0], self.dateId, dataTable[row][15],dataTable[row][16], dataTable[row][17],dataTable[row][18],dataTable[row][19],dataTable[row][9],dataTable[row][10],dataTable[row][11],dataTable[row][12],dataTable[row][13],dataTable[row][14],dataTable[row][20],dataTable[row][21],dataTable[row][22],dataTable[row][23],dataTable[row][24],dataTable[row][25],dataTable[row][26],dataTable[row][8])
            self.dateId +=1
        self.db.commit()
    
    def saveData_afterEdit(self, dataTable):
        update_query = "UPDATE FACT SET "
        column_names = [column[0] for column in self.columns]
        print(column_names)
        for i in range(2,21):
            update_query += str(column_names[i]) + " = ?,"
        update_query = update_query.rstrip(",")
        update_query += " WHERE userId = ?"
        print(update_query)

        for row in range(len(dataTable)):
            self.db.execute("UPDATE Dim_Customer SET yearBirth = ?, education = ?, maritalStatus = ?, income = ?, kidhome = ?,  teenhome = ?, country = ? WHERE userId = ?", dataTable[row][1],dataTable[row][2],dataTable[row][3],dataTable[row][4],dataTable[row][5],dataTable[row][6],dataTable[row][27], dataTable[row][0],)
            
            dateId = self.db.execute("SELECT dateId FROM FACT WHERE userId = ?", dataTable[row][0]).fetchone()[0]
            #Insert data into Dim_Date
                # Getting the day, month, and year from the datetime object
            date_object = datetime.strptime(dataTable[row][7], '%m/%d/%Y')  # Adjust the format if needed
            day = date_object.day
            month = date_object.month
            year = date_object.year

            insert_query = f"UPDATE Dim_Date SET yearEnroll = ?, monthEroll = ?, dayEnroll = ? WHERE dateId = ?"  
            self.db.execute(insert_query, year, month,day, dateId)

            #Insert data into Dim_Date
           
            self.db.execute(update_query, dataTable[row][15],dataTable[row][16], dataTable[row][17],dataTable[row][18],dataTable[row][19],dataTable[row][9],dataTable[row][10],dataTable[row][11],dataTable[row][12],dataTable[row][13],dataTable[row][14],dataTable[row][20],dataTable[row][21],dataTable[row][22],dataTable[row][23],dataTable[row][24],dataTable[row][25],dataTable[row][26],dataTable[row][8], dataTable[row][0])
        self.db.commit()

    def deleteDB(self):
        self.db.execute("DELETE FROM FACT") 
        self.db.execute("DELETE FROM Dim_Date")
        self.db.execute("DELETE FROM Dim_Customer")
        self.db.commit()
        
    def updateDB(self):
        self.factTable = self.db.execute("SELECT * FROM FACT").fetchall()
        self.dateTable = self.db.execute("SELECT * FROM Dim_Date").fetchall()
        self.customerTable = self.db.execute("SELECT * FROM Dim_Customer").fetchall()
        print(self.customerTable)

    def add_function(self, dataTable):
        for row in range(len(dataTable)):
            userId = self.generate_random_key()
            dateId = self.generate_random_dateId()
            print("Hello")
            self.db.execute("INSERT INTO Dim_Customer VALUES (?, ?, ?, ?, ?, ?, ?, ?)", userId,dataTable[row][1],dataTable[row][2],dataTable[row][3],dataTable[row][4],dataTable[row][5],dataTable[row][6],dataTable[row][27])
            
            #Insert data into Dim_Date
                # Getting the day, month, and year from the datetime object
            date_object = datetime.strptime(dataTable[row][7], '%m/%d/%Y')  # Adjust the format if needed
            day = date_object.day
            month = date_object.month
            year = date_object.year

            insert_query = f"INSERT INTO Dim_Date VALUES (?, ?, ?, ?)"  
            self.db.execute(insert_query,  dateId,year, month,day)

            #Insert data into Dim_Date
            insert_query = f"INSERT INTO FACT VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )"  
            self.db.execute(insert_query, userId, dateId, dataTable[row][15],dataTable[row][16], dataTable[row][17],dataTable[row][18],dataTable[row][19],dataTable[row][9],dataTable[row][10],dataTable[row][11],dataTable[row][12],dataTable[row][13],dataTable[row][14],dataTable[row][20],dataTable[row][21],dataTable[row][22],dataTable[row][23],dataTable[row][24],dataTable[row][25],dataTable[row][26],dataTable[row][8])
        self.db.commit()
    

    def delete_function(self, userId):
        dateId = self.db.execute("SELECT dateId FROM FACT WHERE userId = ?", userId).fetchone()[0]
        self.db.execute("DELETE FROM FACT WHERE userId = ?", userId)
        self.db.execute("DELETE FROM Dim_Customer WHERE userId = ?", userId)
        self.db.execute("DELETE FROM Dim_Date WHERE dateId = ?", dateId)
        self.db.commit()

    def edit_function(self, editCustomer_dict: dict, editDate_dict: dict, editFACT_dict: dict):
        # Edit Dim_Customer table
        update_sql = "UPDATE Dim_Customer SET "
        placeholders = []
        values = []

        for key, value in editCustomer_dict.items():
            if key == 1:
                # Nếu là userId, ta bỏ qua việc thêm vào câu lệnh UPDATE và lưu giá trị userId riêng
                self.user_id_value = editCustomer_dict["userId"]
            else:
                placeholders.append(f"{key} = ?")
                values.append(value)

        # Kết hợp các placeholders và thêm vào câu lệnh SQL
        update_sql += ", ".join(placeholders)
        update_sql += " WHERE userId = ?"

        # Thêm giá trị của userId vào danh sách các giá trị cần cập nhật
        values.append(self.user_id_value)

        # Thực hiện câu lệnh UPDATE
        self.db.execute(update_sql, values)
        self.db.commit()
        # -------------------------------------------------
        # Edit Dim_Date table
        update_sql = "UPDATE Dim_Date SET "
        placeholders = []
        values = []

        for key, value in editDate_dict.items():
            if key == 1:
                # Nếu là userId, ta bỏ qua việc thêm vào câu lệnh UPDATE và lưu giá trị userId riêng
                self.user_id_value = editDate_dict["dateId"]
            else:
                placeholders.append(f"{key} = ?")
                values.append(value)

        # Kết hợp các placeholders và thêm vào câu lệnh SQL
        update_sql += ", ".join(placeholders)
        update_sql += " WHERE userId = ?"

        # Thêm giá trị của userId vào danh sách các giá trị cần cập nhật
        values.append(self.user_id_value)

        # Thực hiện câu lệnh UPDATE
        self.db.execute(update_sql, values)
        self.db.commit()
        # -------------------------------------------------
        # Edit FACT table
        update_sql = "UPDATE FACT SET "
        placeholders = []
        values = []

        for key, value in editFACT_dict.items():
            if key == 1:
                # Nếu là userId, ta bỏ qua việc thêm vào câu lệnh UPDATE và lưu giá trị userId riêng
                self.user_id_value = editFACT_dict["dateId"]
            else:
                placeholders.append(f"{key} = ?")
                values.append(value)

        # Kết hợp các placeholders và thêm vào câu lệnh SQL
        update_sql += ", ".join(placeholders)
        update_sql += " WHERE userId = ?"

        # Thêm giá trị của userId vào danh sách các giá trị cần cập nhật
        values.append(self.user_id_value)

        # Thực hiện câu lệnh UPDATE
        self.db.execute(update_sql, values)
        self.db.commit()


    def filter_function(self):
        pass

class CSVHandler():
    def __init__(self):
        self.database_manager = DatabaseManager()

    def open_csv_file(self):
        option = QFileDialog.Option()
        self.file_path, _ = QFileDialog.getOpenFileName(None, "Open File", "", "*.csv", options=option)

        # Đọc file CSV và lưu vào DataFrame
        df = pd.read_csv(self.file_path)

        #Xóa các cột bị trống dữ liệu
        df.dropna(subset=[' Income '], inplace=True)

        # Chuyển đổi dữ liệu trong cột 'Income' về kiểu int và xử lý các giá trị non-finite
        df[' Income '] = df[' Income '].replace({'\$': '', ',': '', '\.': ''}, regex=True).astype(int)

        self.filter_list = df.values.tolist()
        return self.filter_list
     
    def save_csv_file(self, file_path, data):
        pass