# -*- coding: utf-8 -*-
"""Add the 'test your own strategy' offer box to every published factsheet page.

Run before each push, after add_analytics.py:  python _shared/add_offer.py
Idempotent: an existing block (between the markers) is replaced, so a new PRICE in
offer_config.py reaches every page. Only factsheets/<slug>/index.html pages get it.
"""
import os, sys, time, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import offer_config as C

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A, Z = "<!-- offer:start -->", "<!-- offer:end -->"


def block(place):
    e = html.escape
    js = """
<script>(function(){var P=%r,F=%r,U=%r;
function gc(ev){try{if(window.goatcounter&&window.goatcounter.count)window.goatcounter.count({path:ev,title:ev,event:true})}catch(e){}}
var box=document.getElementById('ns-offer'),seen=false;
if('IntersectionObserver' in window){new IntersectionObserver(function(es,o){es.forEach(function(x){if(x.isIntersecting&&!seen){seen=true;gc('offer-seen-'+P);o.disconnect()}})}).observe(box)}
document.getElementById('ns-offer-open').onclick=function(){gc('offer-click-'+P);if(F){window.open(F,'_blank');return}document.getElementById('ns-offer-form').style.display='block'};
document.getElementById('ns-offer-send').onclick=function(){var r=document.getElementById('ns-offer-rule').value.trim(),m=document.getElementById('ns-offer-mkt').value;
if(r.length<10){document.getElementById('ns-offer-msg').textContent='Describe the rule in a sentence or two first.';return}
var t='Now Showing strategy test request\\nRule: '+r+'\\nMarket: '+m+'\\nSeen on: '+location.pathname;
var go=function(){gc('offer-sent-'+P);document.getElementById('ns-offer-msg').textContent='Copied. Paste it in a LinkedIn message and I will reply with a quote.';window.open(U,'_blank')};
try{navigator.clipboard.writeText(t).then(go,function(){prompt('Copy this text:',t);go()})}catch(e){prompt('Copy this text:',t);go()}}})();</script>""" % (place, C.FORM_URL, C.CONTACT_URL)
    css = ("<style>#ns-offer{border:2px solid #2a78d6;border-radius:10px;padding:16px 18px;margin:28px auto;max-width:760px;width:calc(100% - 32px);box-sizing:border-box;"
           "font-family:-apple-system,Segoe UI,Helvetica,Arial,sans-serif}#ns-offer h3{margin:0 0 6px}"
           "#ns-offer .b{display:inline-block;background:#2a78d6;color:#fff;border:0;border-radius:8px;padding:10px 16px;font-size:15px;cursor:pointer}"
           "#ns-offer small{display:block;opacity:.75;margin-top:8px}#ns-offer textarea,#ns-offer select{width:100%;box-sizing:border-box;"
           "margin:6px 0;padding:8px;font:inherit;border-radius:6px;border:1px solid #bbb;background:transparent;color:inherit}</style>")
    return (A + css + f"""<div id="ns-offer"><h3>{e(C.HEADLINE)}</h3><p>{e(C.PITCH)}</p>
<button class="b" id="ns-offer-open">Test my strategy · {e(C.PRICE)}</button>
<div id="ns-offer-form" style="display:none"><p><b>Your rule in plain words</b> (what to buy, how often, how many stocks):</p>
<textarea id="ns-offer-rule" rows="3" placeholder="e.g. Each month buy the 30 stocks with the highest 6-month return and dividend yield above 2%"></textarea>
<select id="ns-offer-mkt"><option>Any / not sure</option><option>US</option><option>Europe</option><option>UK</option><option>Denmark</option><option>Scandinavia</option><option>World</option></select>
<button class="b" id="ns-offer-send">Copy request and message me on LinkedIn</button><p id="ns-offer-msg"></p></div>
<small>{e(C.SMALL)} No payment is taken here.</small></div>""" + js + Z)


def main():
    t0 = time.time(); n = 0
    print(time.strftime("%H:%M:%S"), "offer price:", C.PRICE)
    fdir = os.path.join(ROOT, "factsheets")
    for slug in sorted(os.listdir(fdir)):
        p = os.path.join(fdir, slug, "index.html")
        if not os.path.isfile(p):
            continue
        s = open(p, encoding="utf-8").read()
        if A in s:
            s = s[:s.index(A)] + s[s.index(Z) + len(Z):]
        i = s.lower().rfind("</body>")
        if i < 0:
            print("  no </body>, skipped:", slug); continue
        s = s[:i] + block("fs-" + slug.split("-")[0]) + s[i:]
        open(p, "w", encoding="utf-8").write(s); n += 1
    print(f"{time.strftime('%H:%M:%S')} done in {time.time()-t0:.1f}s: offer on {n} factsheet pages")


if __name__ == "__main__":
    sys.exit(main())
