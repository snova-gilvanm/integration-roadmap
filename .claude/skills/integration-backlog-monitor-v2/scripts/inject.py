"""Replace the embedded data block of the published page with WORK/data.json.
usage: WORK=... python3 inject.py page_in.html page_out.html"""
import os, sys, json, re
WORK = os.environ.get("WORK", ".").rstrip("/") + "/"
src, dst = sys.argv[1], sys.argv[2]
h = open(src, encoding="utf-8").read()
D = json.load(open(WORK + "data.json"))
blob = json.dumps(D, separators=(",", ":")).replace("</", "<\\/")
pat = re.compile(r'(<script type="application/json" id="data">)(.*?)(</script>)', re.S)
assert pat.search(h), "data block not found"
h = pat.sub(lambda m: m.group(1) + blob + m.group(3), h, count=1)
if "—" in pat.sub("", h): print("WARNING: em dash in page copy; the owner never wants that character in written text")
open(dst, "w", encoding="utf-8").write(h)
print("ok", len(h), "bytes")
