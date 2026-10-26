import json, math, sys
d=json.load(open(sys.argv[1]))
def rings_of(p): return [[(r[i],r[i+1]) for i in range(0,len(r),2)] for r in p]
def inring(x,y,r):
    c=False
    for i in range(len(r)):
        x1,y1=r[i];x2,y2=r[i-1]
        if (y1>y)!=(y2>y) and x < (x2-x1)*(y-y1)/(y2-y1)+x1: c=not c
    return c
def inpoly(x,y,poly):
    rs=rings_of(poly); return inring(x,y,rs[0]) and not any(inring(x,y,h) for h in rs[1:])
def land_at(lon,lat):
    for f in d['land']:
        for p in f['p']:
            if inpoly(lon,lat,p): return f['a3']
    return None
def lake_at(lon,lat):
    for f in d['lakes']:
        for p in f['p']:
            if inpoly(lon,lat,p): return f['name']
def river_dist(name,lon,lat):
    best=9
    for f in d['rivers']:
        if f['name']!=name: continue
        for r in f['l']:
            for i in range(0,len(r),2): best=min(best,math.hypot((r[i]-lon)*math.cos(math.radians(lat)),r[i+1]-lat))
    return best
checks=[("Lake Maracaibo centre is water",land_at(-71.6,9.8) is None),
("Maracaibo city is on land (VEN)",land_at(-71.64,10.65)=="VEN"),
("Strait of Maracaibo near 10.9N is water",land_at(-71.6,10.95) is None),
("Gulf of Venezuela is water",land_at(-71.2,11.5) is None),
("Paraguaná peninsula is land",land_at(-70.05,11.85)=="VEN"),
("Caracas is land",land_at(-66.9,10.49)=="VEN"),
("Sea just north of La Guaira is water",land_at(-66.9,10.75) is None),
("Margarita Island is VEN land",land_at(-63.9,11.0)=="VEN"),
("Gulf of Paria is water",land_at(-62.0,10.4) is None),
("Trinidad is TTO",land_at(-61.3,10.45)=="TTO"),
("Aruba is ABW",land_at(-69.97,12.52)=="ABW"),
("Curacao is CUW",land_at(-68.95,12.15)=="CUW"),
("Lake Valencia is a lake",lake_at(-67.73,10.18)),
("Guri reservoir is a lake",lake_at(-62.9,7.6)),
("Orinoco passes Ciudad Bolivar (<0.1 deg)",river_dist("Orinoco",-63.55,8.13)<0.1),
("Orinoco passes Puerto Ayacucho (<0.15 deg)",river_dist("Orinoco",-67.6,5.66)<0.15),
("Orinoco reaches the delta coast (<0.05 deg)",river_dist("Orinoco",-61.12,8.95)<0.05),
("Apure passes San Fernando (<0.1)",river_dist("Apure",-67.47,7.89)<0.1),
("Caroni meets Orinoco near Ciudad Guayana (<0.15)",river_dist("Caroní",-62.65,8.33)<0.15),
]
for t in sys.argv[2:]:
    pass
bad=0
for name,ok in checks:
    print(("PASS " if ok else "FAIL ")+name+("" if ok is True else f" -> {ok}")); bad+= not ok
for lon,lat,nm in [(-60.074,9.099,'Atlantic label'),(-66.876,10.876,'Caribbean label'),(-60.984,8.799,'Boca Grande label')]:
    print(nm,'land=',land_at(lon,lat))
sys.exit(bad)
