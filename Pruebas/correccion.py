import utils

v1 = [{
  "_id": {
    "$oid": "6376d4eb39750000fb000ecd"
  },
  "hora": "2022/11/17/ 21:42:19",
  "Id_tag": ":CCF957966B2C",
  "Id_ant": "PID=0403:6015 SER=D200BZVHA",
  "RSSI": "-45",
  "Ang_azimuth": "50",
  "Ang_elevacion": "-21",
  "Canal": "39",
  "Altura_ant": "134"
},{
  "_id": {
    "$oid": "6376d4eb39750000fb000ece"
  },
  "hora": "2022/11/17/ 21:42:19",
  "Id_tag": ":CCF957966AC9",
  "Id_ant": "PID=0403:6015 SER=D200BZVHA",
  "RSSI": "-59",
  "Ang_azimuth": "33",
  "Ang_elevacion": "-22",
  "Canal": "37",
  "Altura_ant": "134"
},{
  "_id": {
    "$oid": "6376d4ed39750000fb000ecf"
  },
  "hora": "2022/11/17/ 21:42:21",
  "Id_tag": ":CCF957966B2C",
  "Id_ant": "PID=0403:6015 SER=D200BZVHA",
  "RSSI": "-45",
  "Ang_azimuth": "-50",
  "Ang_elevacion": "-20",
  "Canal": "39",
  "Altura_ant": "134"
},{
  "_id": {
    "$oid": "6376d4ed39750000fb000ed0"
  },
  "hora": "2022/11/17/ 21:42:21",
  "Id_tag": ":CCF957966B2C",
  "Id_ant": "PID=0403:6015 SER=D200BZVHA",
  "RSSI": "-50",
  "Ang_azimuth": "-51",
  "Ang_elevacion": "-20",
  "Canal": "38",
  "Altura_ant": "134"
}]
v2 = [{
  "_id": {
    "$oid": "6376d4eb39750000fb000ecd"
  },
  "hora": "2022/11/17/ 21:42:19",
  "Id_tag": ":CCF957966B2C",
  "Id_ant": "PID=0403:6015 SER=D200BZVHA",
  "RSSI": "-45",
  "Ang_azimuth": "50",
  "Ang_elevacion": "-21",
  "Canal": "39",
  "Altura_ant": "134"
},{
  "_id": {
    "$oid": "6376d4ef39750000fb000ed3"
  },
  "hora": "2022/11/17/ 21:42:23",
  "Id_tag": ":CCF957966AC9",
  "Id_ant": "PID=0403:6015 SER=D200BZVHA",
  "RSSI": "-59",
  "Ang_azimuth": "33",
  "Ang_elevacion": "-22",
  "Canal": "37",
  "Altura_ant": "134"
},{
  "_id": {
    "$oid": "6376d4ed39750000fb000ecf"
  },
  "hora": "2022/11/17/ 21:42:21",
  "Id_tag": ":CCF957966B2C",
  "Id_ant": "PID=0403:6015 SER=D200BZVHA",
  "RSSI": "-45",
  "Ang_azimuth": "-50",
  "Ang_elevacion": "-20",
  "Canal": "39",
  "Altura_ant": "134"
},{
  "_id": {
    "$oid": "6376d4ef39750000fb000ed3"
  },
  "hora": "2022/11/17/ 21:42:23",
  "Id_tag": ":CCF957966AC9",
  "Id_ant": "PID=0403:6015 SER=D200BZVHA",
  "RSSI": "-59",
  "Ang_azimuth": "33",
  "Ang_elevacion": "-22",
  "Canal": "37",
  "Altura_ant": "134"
}]
v3 = []

for r in v1:
    for s in v2:
        print(s)
        if(r['Canal']==s['Canal']):
            v3.append(r)
            v3.append(s)
            v2.remove(s)

print("~"*50)
print(v1)
print(v2)
print(v3)
print(len(v3))
x = int(len(v3)/2)
print("~"*50)


### Pruebas con el rango

D_ant_tag = 130

print(type(x))
for t in range(int(len(v3)/2)):
    print("~"*50)
    print(v3[2*t])
    print(v3[(2*t)+1])
    print(v3[2*t]['Ang_azimuth'])
    a,b = utils.CalculoAngulo(v3[2*t]['Ang_azimuth'],v3[(2*t)+1]['Ang_azimuth'])
    print(a)
    print(b)
    D_B,D_A = utils.Distancia_ant_tag(D_ant_tag,v3[2*t]['Ang_azimuth'],v3[(2*t)+1]['Ang_azimuth'])
    print(D_A)
    print(D_B)
  