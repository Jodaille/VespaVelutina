import sys
import os
from datetime import datetime
import pymysql.cursors
import pymysql

#CREATE TABLE `snapshots`.`snapshots` ( `id` INT UNSIGNED NOT NULL AUTO_INCREMENT , `camera` VARCHAR(50) NOT NULL , `filename` VARCHAR(255) NOT NULL , `created_at` DATETIME NOT NULL , PRIMARY KEY (`id`) ) ENGINE = InnoDB;

class SaveImage:
    camera = ''
    imagepath = ''
    filename = ''
    file_name = ''
    date_string = ''
    datetime = datetime

    def __init__(self, imagepath):
        self.imagepath = imagepath
        self.parseImagePath(imagepath)
        dateTime = self.datetimeFromString(self.date_string)
        self.dateTimeForMysql(dateTime)

    def parseImagePath(self, imagepath):
        self.filename = os.path.basename(imagepath)
        self.file_name = os.path.splitext(self.filename)[0]
        self.camera = '/'.join(self.file_name.split("_")[1::])
        self.date_string = self.filename.split("_")[0]

    def datetimeFromString(self, date_string):
        date_time_obj = datetime.strptime(date_string, '%Y-%m-%d-%H%M%S')
        return date_time_obj

    def dateTimeForMysql(self, dateTime):
        self.datetime_string = dateTime.strftime('%Y-%m-%d %H:%M:%S')
        return self.datetime_string

    def description(self):
        return "filename: {} \nfile_name: {} \ncamera: {} \ndatetime: {}".format(self.filename, self.file_name, self.camera, self.datetime_string)

    def exists(self, connection):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `snapshots` WHERE `filename`=%s"
            cursor.execute(sql, (self.filename,))
            result = cursor.fetchone()
            if(result):
                return result['id']
            else:
                return False

    def save(self, connection):
        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `snapshots` (`filename`,`camera`, `created_at`) VALUES (%s, %s,%s)"
                cursor.execute(sql, (self.filename, self.camera ,self.datetime_string))
                print("id {} ".format(cursor.lastrowid))
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()

        finally:
            connection.close()

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='snapshots',
                             password='snapshots',
                             db='snapshots',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

imagepath = sys.argv[1]
Image = SaveImage(imagepath)
print(Image.description())
id_image = Image.exists(connection)
if (id_image == False):
    print(Image.save(connection))
else:
    print('Already exists {}'.format(id_image))
