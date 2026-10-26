"""Build one map data file per chapter from Natural Earth 10m layers.

Region-agnostic: pass a config JSON with bbox [W,S,E,N] and focus ADM0_A3.
Output: flat lon/lat arrays per layer. Polygons are never clipped; whole
features that touch the view are kept (simplified). Lines are trimmed to an
expanded box only, which cannot create fake borders.

usage: python3 -I build_region.py <ne_dir> <config.json> <out.json>
"""
import json, sys, math

ne, cfg_path, out_path = sys.argv[1:4]
cfg = json.load(open(cfg_path))
W, S, E, N = cfg["bbox"]
PAD = cfg.get("pad", 2.0)
FOCUS = cfg["focus"]
TOL = cfg.get("tol", 0.012)       # simplification tolerance, degrees
TOL_FAR = cfg.get("tol_far", 0.05)
lat0 = (S + N) / 2
kx = math.cos(math.radians(lat0))

def load(name):
    return json.load(open(f"{ne}/{name}.geojson"))["features"]

def rdp(pts, tol):
    if len(pts) < 3: return pts
    keep = [False] * len(pts); keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        a, b = stack.pop()
        ax, ay = pts[a][0] * kx, pts[a][1]; bx, by = pts[b][0] * kx, pts[b][1]
        dx, dy = bx - ax, by - ay; L = math.hypot(dx, dy)
        best, bi = -1, -1
        for i in range(a + 1, b):
            px, py = pts[i][0] * kx, pts[i][1]
            d = abs(dy * px - dx * py + bx * ay - by * ax) / L if L else math.hypot(px - ax, py - ay)
            if d > best: best, bi = d, i
        if best > tol:
            keep[bi] = True; stack += [(a, bi), (bi, b)]
    return [p for p, k in zip(pts, keep) if k]

def flat(pts): return [round(v, 3) for p in pts for v in p[:2]]

def bb(coords):
    xs = [c[0] for c in coords]; ys = [c[1] for c in coords]
    return min(xs), min(ys), max(xs), max(ys)

def touches(b, pad=0.0):
    return not (b[2] < W - pad or b[0] > E + pad or b[3] < S - pad or b[1] > N + pad)

def polys(geom):
    if geom is None: return []
    return [geom["coordinates"]] if geom["type"] == "Polygon" else geom["coordinates"] if geom["type"] == "MultiPolygon" else []

def lines(geom):
    if geom is None: return []
    return [geom["coordinates"]] if geom["type"] == "LineString" else geom["coordinates"] if geom["type"] == "MultiLineString" else []

def poly_rings(geom, near_only=True):
    """Whole polygons (no clipping); drop parts that never come near the view."""
    out = []
    for poly in polys(geom):
        outer = poly[0]
        b = bb(outer)
        if near_only and not touches(b, PAD): continue
        tol = TOL if touches(b, 0) else TOL_FAR
        rings = []
        for r in poly:
            s = rdp(r, tol)
            if len(s) >= 4: rings.append(flat(s))
        if rings: out.append(rings)
    return out

def line_runs(geom, tol=None):
    """Split lines into runs inside the padded box, then simplify."""
    out = []
    for ln in lines(geom):
        run = []
        for p in ln:
            if W - PAD <= p[0] <= E + PAD and S - PAD <= p[1] <= N + PAD: run.append(p)
            else:
                if len(run) > 1: out.append(run)
                run = []
        if len(run) > 1: out.append(run)
    return [flat(rdp(r, tol or TOL)) for r in out]

def prop(f, *keys):
    for k in keys:
        v = f["properties"].get(k)
        if v not in (None, ""): return v
    return None

data = {"name": cfg["name"], "bbox": cfg["bbox"], "focus": FOCUS, "source": "Natural Earth 10m (public domain)"}

land = []
for f in load("ne_10m_admin_0_countries"):
    a3 = prop(f, "ADM0_A3", "adm0_a3")
    rings = poly_rings(f["geometry"])
    if rings: land.append({"a3": a3, "name": prop(f, "NAME_EN", "NAME"), "focus": a3 == FOCUS, "p": rings})
data["land"] = land

data["admin0"] = [r for f in load("ne_10m_admin_0_boundary_lines_land") for r in line_runs(f["geometry"])]
data["coast"] = [r for f in load("ne_10m_coastline") for r in line_runs(f["geometry"])]
data["admin1"] = [r for f in load("ne_10m_admin_1_states_provinces_lines")
                  if prop(f, "adm0_a3", "ADM0_A3") == FOCUS for r in line_runs(f["geometry"])]

states = []
for f in load("ne_10m_admin_1_states_provinces"):
    if prop(f, "adm0_a3") != FOCUS: continue
    nm = cfg.get("state_names", {}).get(prop(f, "name_en", "name") or "", prop(f, "name_en", "name"))
    if not nm: continue
    states.append({"name": nm, "lon": round(f["properties"]["longitude"], 3), "lat": round(f["properties"]["latitude"], 3)})
data["states"] = states

lakes = []
for f in load("ne_10m_lakes"):
    rings = poly_rings(f["geometry"])
    if not rings: continue
    b = bb([c for p in polys(f["geometry"]) for c in p[0]])
    if not touches(b, 0): continue
    lakes.append({"name": prop(f, "name_en", "name"), "rank": f["properties"].get("scalerank"), "p": rings})
data["lakes"] = lakes

rivers = []
for f in load("ne_10m_rivers_lake_centerlines"):
    nm = prop(f, "name_en", "name"); rk = f["properties"].get("scalerank") or 99
    inc = next((x for x in cfg.get("river_include", []) if x["name"] == nm and x["rank"] == rk), None)
    if rk > cfg.get("river_rank", 7) and not inc: continue
    runs = line_runs(f["geometry"])
    if runs: rivers.append({"name": inc.get("rename", nm) if inc else nm, "rank": rk, "l": runs})
data["rivers"] = rivers

roads = []
for f in load("ne_10m_roads"):
    if f["properties"].get("type") not in cfg.get("road_types", ["Major Highway"]): continue
    if cfg.get("roads_focus_only", True) and prop(f, "sov_a3", "SOV_A3") not in (FOCUS, None) and f["properties"].get("continent") is None:
        pass
    runs = line_runs(f["geometry"], TOL * 1.5)
    runs = [r for r in runs if any(W <= r[i] <= E and S <= r[i + 1] <= N for i in range(0, len(r), 2))]
    if runs: roads.extend(runs)
data["roads"] = roads

places = []
for f in load("ne_10m_populated_places_simple"):
    p = f["properties"]; lon, lat = f["geometry"]["coordinates"][:2]
    if not (W <= lon <= E and S <= lat <= N): continue
    sr = p.get("scalerank", 99)
    if sr > cfg.get("place_rank", 6): continue
    places.append({"name": p.get("name") or p.get("nameascii"), "lon": round(lon, 3), "lat": round(lat, 3), "rank": sr,
                   "cap": p.get("featurecla", "").startswith("Admin-0 capital"), "a3": p.get("adm0_a3")})
data["places"] = sorted(places, key=lambda x: x["rank"])

marine = []
for f in load("ne_10m_geography_marine_polys"):
    pts = [c for poly in polys(f["geometry"]) for c in poly[0] if W <= c[0] <= E and S <= c[1] <= N]
    if len(pts) < 3: continue
    marine.append({"name": prop(f, "name_en", "name"), "lon": round(sum(c[0] for c in pts) / len(pts), 3),
                   "lat": round(sum(c[1] for c in pts) / len(pts), 3), "rank": f["properties"].get("scalerank")})
if "marine" in cfg: marine = cfg["marine"]
data["marine"] = marine

json.dump(data, open(out_path, "w"), separators=(",", ":"))
print({k: (len(v) if isinstance(v, list) else v) for k, v in data.items()})
