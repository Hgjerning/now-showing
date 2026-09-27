import data, turtle, numpy as np, pandas as pd, json
out={}
for R in ["US","EU","WD","DK"]:
    o=data.load(R); r=o["ret"].loc[:"2019-12-31"]; e=o["elig"].loc[:"2019-12-31"]
    res={}
    for c,b in [(0.001,0.005),(0,0)]:
        turtle.COST, turtle.BORROW = c,b
        x=0.5*turtle.run(r,e,system=1)["ret"]+0.5*turtle.run(r,e,system=2)["ret"]
        res["net" if c else "gross"]=float(x.mean()*252)
    out[R]=res; print(R,res)
turtle.COST, turtle.BORROW = 0.001,0.005
json.dump(out,open("../results/turtle_cost_check.json","w"))
