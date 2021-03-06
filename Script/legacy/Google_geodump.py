import codecs
import json
import sqlite3

conn = sqlite3.connect(r'E:\3.9.0\Python1.sqlite')
cur = conn.cursor()

cur.execute('SELECT * FROM Locations')
fhand = codecs.open(r'F:\How to be a good qingnian\Learn\Python\M code\geodata\where.js','w', "utf-8")
fhand.write("myData = [\n")
count = 0
for row in cur :
    data = row[1].decode()
    try: js = json.loads(data)
    except: continue

    if not('status' in js and js['status'] == 'OK') : continue

    lat = js["results"][0]["geometry"]["location"]["lat"]
    lng = js["results"][0]["geometry"]["location"]["lng"]
    if lat == 0 or lng == 0 : continue
    where = js['results'][0]['formatted_address']
    where = where.replace("'","")
    try :
        print(where, lat, lng)

        count = count + 1
        if count > 1 : fhand.write(",\n")
        output = "["+str(lat)+","+str(lng)+", '"+where+"']"
        fhand.write(output)
    except:
        continue

fhand.write("\n];\n")
cur.close()
fhand.close()
print (count, "records written to where.js")
print ("Open where.html to view the data in a browser")
