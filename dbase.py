from flask import *
import datetime
import hashlib

class dbase:

    def __init__(self, connectDB):
        self.__connectDB = connectDB
        self.__cursorDB = connectDB.cursor()


    def setScore(self, data, id):
        self.__cursorDB.execute(f"UPDATE Scores SET Score = {data} WHERE User_id = {id} ")
        self.__connectDB.commit()


    def getUserByEmail(self, email):
        self.__cursorDB.execute(f"SELECT * FROM Users WHERE Email = '{email}' LIMIT 1")
        result = self.__cursorDB.fetchone()

        if not result:
            print("User don't found")
            return False
        return result

    def top_players(self):
        self.__cursorDB.execute('SELECT ROW_NUMBER() OVER(ORDER BY Score DESC) AS rowid, * FROM Scores ')
        result = self.__cursorDB.fetchall()
        return result

    def score(self, userID):
        self.__cursorDB.execute(f'SELECT Score FROM Scores WHERE User_id = {userID} LIMIT 1')
        result1 = self.__cursorDB.fetchone()

        with open('score.json', 'w') as score:
            data = {'score': result1[0]}
            json.dump(data, score)
        return result1


    def registration(self, data):

        for em in self.__cursorDB.execute('SELECT Email FROM Users'):
            if data['email'] == em[0]:
                flash('Вы уже зарегистрированы', category='fail')
                return redirect(url_for('sign_up'))

        if data['email'] == '' or data['password'] == '' or data['repeat_password'] == '':
            flash('Вы заполнили не все поля!!!', category='fail')
            return False
        elif data['password'] != data['repeat_password']:
            flash('Пароли не совпадают', category='fail')
            return False
        elif len(data['password']) < 8:
            flash('Пароль < 8 символов', category='fail')
            return False

        hash_object = hashlib.md5(data['password'].encode())

        date = datetime.datetime.now()
        date = str(date.day) + '/' + str(date.month) + '/' + str(date.year)

        self.__cursorDB.execute("INSERT INTO Users (Email, Password, RegistrationDate) VALUES (?, ?, ?)", (data['email'], hash_object.hexdigest(), date))
        self.__cursorDB.execute("INSERT INTO Scores (Score) VALUES (0)")
        self.__connectDB.commit()

        flash('Вы успешно зарегистрировались!', category='success')
        return True

    def getUser(self, userID):
        self.__cursorDB.execute(f'SELECT * FROM Users WHERE id = { userID } LIMIT 1' )
        result = self.__cursorDB.fetchone()
        if not result:
            print("User don't found")
            return False
        return result

