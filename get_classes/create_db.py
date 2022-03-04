import sqlite3
db = sqlite3.connect('classes.db')
db.cursor()
db.execute('CREATE TABLE IF NOT EXISTS "classes" ("id" INTEGER, "class_name" TEXT,PRIMARY KEY("id" AUTOINCREMENT));')
db.close()