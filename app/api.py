from fastapi import FastAPI, Request
from .db.actions import get_loc_dict,get_locs,get_vlgs,get_acts, get_crps, get_shgs, get_mems, get_txns, get_acts, get_json_data, get_summary_report

api_app = FastAPI()

@api_app.get("/loc_dict")
async def loc_dict():
    data = await get_loc_dict()
    return data

@api_app.get("/locs")
async def locs():
    data = await get_locs()
    return data

@api_app.get("/vlgs/{loc}")
async def vlgs(loc):
    data = await get_vlgs(loc)
    return data

@api_app.get("/acts")
async def acts():
    data = await get_acts()
    return data

@api_app.get("/crps/{mode}")
async def crps(mode):
    data = await get_crps(mode)
    return data
    
@api_app.get("/crp/{phone}")
async def crp_check(phone):
    data = await check_crp_phone(phone)
    return data

@api_app.get("/shgs/{crpid}")
async def shgs(crpid):
    data = await get_shgs(crpid)
    return data

@api_app.get("/mems/{shgid}")
async def mems(shgid):
    data = await get_mems(shgid)
    return data

@api_app.get("/txns/{memid}")
async def txns(memid):
    data = await get_txns(memid)
    return data

@api_app.get("/acts/{memid}")
async def acts(memid):
    data = await get_acts(memid)
    return data

@api_app.get("/all/{mode}")
async def all_data(mode):
    data = await get_json_data(mode)
    return data

@api_app.get("/rpt/summary/{mode}")
async def rpt_summary(mode):
    data = await get_summary_report(mode)
    return data

