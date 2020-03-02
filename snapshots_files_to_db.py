import sys
import os
import glob
from datetime import datetime
import pymysql.cursors
import pymysql

#CREATE TABLE `snapshots`.`snapshots` ( `id` INT UNSIGNED NOT NULL AUTO_INCREMENT , `camera` VARCHAR(50) NOT NULL , `filename` VARCHAR(255) NOT NULL , `created_at` DATETIME NOT NULL , PRIMARY KEY (`id`) ) ENGINE = InnoDB;
# ALTER TABLE `snapshots` ADD `frelon` BOOLEAN NOT NULL DEFAULT FALSE AFTER `filename`;
class SaveImage:
    camera = ''
    imagepath = ''
    filename = ''
    file_name = ''
    date_string = ''
    isfrelon = 0
    datetime = datetime

    def __init__(self, imagepath, hasfrelon):
        self.imagepath = imagepath
        self.parseImagePath(imagepath)
        dateTime = self.datetimeFromString(self.date_string)
        self.dateTimeForMysql(dateTime)
        if(hasfrelon):
            self.isfrelon = 1
            #print("constructor frelon {}".format(self.isfrelon))

    def parseImagePath(self, imagepath):
        self.filename = os.path.basename(imagepath)
        self.file_name = os.path.splitext(self.filename)[0]
        self.camera = '/'.join(self.file_name.split("_")[1::])
        self.date_string = self.filename.split("_")[0]

    def datetimeFromString(self, date_string):
        date_time_obj = datetime.strptime(date_string, '%Y-%m-%d-%H%M%S')
        return date_time_obj

    def isFrelonDetected(self, isfrelon):
        return self.isfrelon

    def dateTimeForMysql(self, dateTime):
        self.datetime_string = dateTime.strftime('%Y-%m-%d %H:%M:%S')
        return self.datetime_string

    def description(self):
        return "filename: {} \nfile_name: {} \ncamera: {} \ndatetime: {}".format(self.filename, self.file_name, self.camera, self.datetime_string)

    def exists(self, connection):
        with connection.cursor() as cursor:
            sql = "SELECT id, frelon FROM `snapshots` WHERE `filename` = %s"

            cursor.execute(sql, (self.filename))
            result = cursor.fetchone()

            if(result):
                cursor.close()
                return result["id"]
            else:
                cursor.close()
                return False

    def save(self, connection):
        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `snapshots` (`filename`,`camera`, `frelon`, `created_at`) VALUES (%s, %s,%s, %s)"
                cursor.execute(sql, (self.filename, self.camera , self.isfrelon, self.datetime_string))
                cursor.close()
                print("save id {} ".format(cursor.lastrowid))
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()

        finally:
            return cursor.lastrowid

    def update(self, connection, id_image):
        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "UPDATE `snapshots` set filename = %s,`camera` = %s , `frelon` = %s , `created_at`=  %s WHERE id = %s"
                cursor.execute(sql, (self.filename, self.camera , self.isfrelon, self.datetime_string, id_image))
                cursor.close()
                #print("update id {} frelon: {} ".format(id_image, self.isfrelon))
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()

        finally:
            return id_image


# Connect to the database
connection = pymysql.connect(host='computervision',
                             user='snapshots',
                             password='snapshots',
                             db='snapshots',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

imagepath = sys.argv[1]
hasfrelon = False
if (len(sys.argv) > 2):
    hasfrelon = True


folders = []
print(imagepath)

files = [f for f in glob.glob(imagepath + "**/*.jpg", recursive=True)]

for f in files:
    print("loop file: {} hasfrelon: {}".format(f, hasfrelon))
    Image = SaveImage(f, hasfrelon)
    id_image = Image.exists(connection)
    if (id_image == False):
        print(Image.save(connection))
    else:
        print('Already exists {}'.format(id_image))
        print(Image.update(connection, id_image))


