import requests
import time
import xml.etree.ElementTree as ET

# 453129 is ID of the shoreline of Crete island
url = "https://www.openstreetmap.org/api/0.6/relation/453129"
et = ET.fromstring(requests.get(url).content)
rel = et[0]
cnt = 0
t0 = time.time()
f = open('coords.csv', 'w')
for way in rel:
    if way.tag == 'member':
        ref = way.attrib['ref']
        url = f"https://www.openstreetmap.org/api/0.6/way/{ref}"
        etway = ET.fromstring(requests.get(url).content)
        w = etway[0]
        for node in w:
            if node.tag == 'nd':
                cnt += 1
                if cnt % 100 == 0:
                    print(f"{cnt} points {(time.time() - t0)*10:.0f} ms per point")
                    t0 = time.time()
                refnode = node.attrib['ref']
                url = "https://www.openstreetmap.org/api/0.6/node/{}".format(refnode)
                etnode = ET.fromstring(requests.get(url).content)
                n = etnode[0]
                lat = n.attrib['lat']
                lon = n.attrib['lon']
                f.write(f"{lat},{lon}\n")
print("done.")
f.close()
