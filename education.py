from bs4 import BeautifulSoup
import requests
import pandas as pd

url = "http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm"

r = requests.get(url)

soup = BeautifulSoup(r.content)

import sqlite3 as lite

con = lite.connect('education.db')
cur = con.cursor()

with con:
	cur.execute("drop table if exists Edu_Life")
	cur.execute('CREATE TABLE Edu_Life ( Country_or_area STR, Year INT, Total INT, Men INT, Women INT);')

for tr in soup("table")[6]("table")[2]("tr")[4:]:
	td = tr("td")
	with con:
		cur.execute("INSERT INTO Edu_Life VALUES (?,?,?,?,?)", (td[0].text, int(td[1].text), int(td[4].text), int(td[7].text), int(td[10].text) ))

df = pd.read_sql_query("SELECT * FROM Edu_Life ORDER BY Total",con,index_col='Country_or_area')

print df

df["Total"].mean()
df["Men"].mean()
df["Women"].mean()

import mtplotlib.pyplot as plt

plt.bar(range(len(df)),df["Men"])
plt.show()

import csv
import math
import numpy as np

con = lite.connect('education.db')
cur = con.cursor()

with open('ny.gdp.mktp.cd_Indicator_en_csv_v2.csv','rU') as inputFile:
	header = next(inputFile)
	inputReader = csv.reader(inputFile)
	for line in inputReader:
		with con:
			cur.execute("DROP TABLE IF EXISTS gdp")
			cur.execute('CREATE TABLE gdp ( country_name STR, _1999 REAL, _2000 REAL, _2001 REAL, _2002 INT, _2003 INT, _2004 INT, _2005 INT, _2006 INT, _2007 INT, _2008 INT, _2009 INT, _2010 INT);')
			cur.execute("INSERT INTO gdp VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (line[0], line[43], math.log(line[44]), line[45], line[46], line[47], line[48], line[49], line[50], line[51], line[52], line[53], line[54] ))

with con:
	cur.execute("SELECT country_name, _2000 FROM gdp INNER JOIN Edu_Life ON country_name = Country_or_area;")

df = pd.read_sql_query("SELECT * FROM Edu_Life ORDER BY _2000",con,index_col='Country_or_area')

print df

df = pd.read_sql_query("SELECT * FROM Edu_Life ORDER BY _2000",con,index_col='Country_or_area')
	np.correlate(_2000, Total)


