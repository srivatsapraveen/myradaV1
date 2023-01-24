from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .db.models import Location, Login, CRP, SHG, TXN
from .db.actions import get_vlg_data,save_loc_data,save_crp_data,get_crp_data_byid, get_mem_data, save_shg_data, get_shg_data_byid, reset_data, get_txn_data, save_txn_data, del_shg_data, del_mem_data
import starlette.status as status 
from starlette.responses import RedirectResponse
import json

web_app = FastAPI()
web_app.mount("/static", StaticFiles(directory="static"), name="static")
web_templates = Jinja2Templates(directory="templates")

myTab = {
	'train@myrada.org':{'pwd':'pass-train','mode':'train'},
	'test@myrada.org':{'pwd':'pass-test','mode':'test'},
	'admin@myrada.org':{'pwd':'pass-live-111','mode':'live'},
	'blradmin@myrada.org':{'pwd':'pass-live-999','mode':'live'}
}

@web_app.get("/", response_class=HTMLResponse)
async def index(request: Request, msg:str = ''):
    return web_templates.TemplateResponse("web/_index.html",{"request": request, "error":msg})

@web_app.post("/", response_class=HTMLResponse)
async def login(request: Request, login : Login = Depends(Login)):
#async def login(request: Request):
    
    if (login.userid in myTab):
        if (myTab[login.userid]['pwd'] == login.pwd):
            print(myTab[login.userid]['mode'])
            return web_templates.TemplateResponse("web/_home.html",{"request": request,"mode":myTab[login.userid]['mode']})
        else:
            return web_templates.TemplateResponse("web/_index.html",{"request": request, "error":"Invalid Login Credentails"})
    else:
        return web_templates.TemplateResponse("web/_index.html",{"request": request, "error":"Invalid Login Credentails"})

@web_app.get("/vlgs", response_class=HTMLResponse)
async def get_vlg_list(request: Request,mode: str = 'live'):
    return web_templates.TemplateResponse("web/vlg_list.html",{"request": request})

@web_app.get("/newvlg/{loc_id}", response_class=HTMLResponse)
async def get_new_vlg(request: Request, loc_id : str):
    return web_templates.TemplateResponse("web/vlg_add.html",{"request": request, "loc_id" : loc_id, "vlg_info": ""})

@web_app.get("/vlg/{vlg_id}", response_class=HTMLResponse)
async def get_vlg(request: Request, vlg_id : str):
    try:
        vlg_dat = await get_vlg_data(vlg_id)
        vlg_info = vlg_dat[0]
        return web_templates.TemplateResponse("web/vlg_add.html",{"request": request, "loc_id" : vlg_id[0: 3], "vlg_info" : vlg_info})
    except Exception as e:
        print (e)
       
@web_app.post("/vlg/new", response_class=HTMLResponse)
async def save_crp(request: Request, vlg_info : Location = Depends(Location)):
    #print (vlg_info)
    await save_loc_data (vlg_info)
    return RedirectResponse('/web/vlgs/',status_code=status.HTTP_302_FOUND)
    
@web_app.get("/crps", response_class=HTMLResponse)
async def get_crp_list(request: Request,mode: str = 'live'):
    return web_templates.TemplateResponse("web/crp_list.html",{"request": request})

@web_app.get("/crp/new", response_class=HTMLResponse)
async def get_new_crp(request: Request):
    return web_templates.TemplateResponse("web/crp_add.html",{"request": request})

@web_app.post("/crp/{acttype}", response_class=HTMLResponse)
async def save_crp(request: Request, acttype : str, crp_info : CRP = Depends(CRP)):
    #async def save_crp(request: Request, acttype : str):
    #data = await request.form()
    #print (json.dumps(data)      )
    await save_crp_data(crp_info)
    if (acttype == 'new'):
        return RedirectResponse('/web/crps',status_code=status.HTTP_302_FOUND)
    else:
        return RedirectResponse('/web/crp/' + crp_info.crp_id,status_code=status.HTTP_302_FOUND)
        

@web_app.get("/crp/{crp_id}", response_class=HTMLResponse)
async def get_crp_shgs(request: Request, crp_id : str):
    try:
        crp_info = await get_crp_data_byid(crp_id)
        return web_templates.TemplateResponse("web/crp_details.html",{"request": request, "crp_info" : crp_info})
    except Exception as e:
        print (e)

@web_app.get("/shg/{shg_id}", response_class=HTMLResponse)
async def get_shg_mems(request: Request, shg_id : str):
    try:
        shg_info = await get_shg_data_byid(shg_id)
        return web_templates.TemplateResponse("web/shg_details.html",{"request": request, "shg_info" : shg_info})
    except Exception as e:
        print (e)

@web_app.get("/shg/new/{crp_id}", response_class=HTMLResponse)
async def get_new_shg(request: Request, crp_id : str):
    crp_info = await get_crp_data_byid(crp_id)
    return web_templates.TemplateResponse("web/shg_add.html",{"request": request, "crp_id" : crp_id, "crp_loc" : crp_info['crp_loc']})

@web_app.post("/shg/{mode}", response_class=HTMLResponse)
async def save_shg(request: Request, mode : str, shg_info : SHG = Depends(SHG)):
    print (shg_info.json())      
    await save_shg_data(shg_info)
    if (mode == 'new'):
        return RedirectResponse('/web/crp/' + shg_info.crp_id,status_code=status.HTTP_302_FOUND)
    else:
        return RedirectResponse('/web/shg/' + shg_info.shg_id,status_code=status.HTTP_302_FOUND)

@web_app.get("/shg/del/{shg_id}", response_class=HTMLResponse)
async def del_shg(request: Request, shg_id : str):
    shg_info = await get_shg_data_byid(shg_id) 
    if (shg_info["shg_memcount"] == 0):
        print('DELETING SHG : ',shg_id)
        i = await del_shg_data(shg_id)
        
    return RedirectResponse('/web/crp/' + shg_info["crp_id"],status_code=status.HTTP_302_FOUND)
        
@web_app.get("/mem/del/{mem_id}", response_class=HTMLResponse)
async def del_mem(request: Request, mem_id : str):    
    mem_info = await get_mem_data(mem_id)
    if (mem_info["mem_amtrec"] == 0):
        #print('DELETING MEMBER : ',mem_id)
        i = await del_mem_data(mem_id)
        #print ('DELETED COUNT : ',i)
            
    return RedirectResponse('/web/shg/' + mem_info["shg_id"],status_code=status.HTTP_302_FOUND)
        
@web_app.get("/mem/{mem_id}", response_class=HTMLResponse)
async def get_mem_txns(request: Request, mem_id : str):
    mem_info = await get_mem_data(mem_id)
    return web_templates.TemplateResponse("web/mem_details.html",{"request": request, "mem_info" : mem_info})

@web_app.get("/txn/{txn_id}", response_class=HTMLResponse)
async def get_txn_info(request: Request, txn_id : str):
    txn_info = await get_txn_data(txn_id)
    print(txn_info['mem_id'])
    mem_info = await get_mem_data(txn_info['mem_id'])    
    return web_templates.TemplateResponse("web/txn_details.html",{"request": request, "mem_info" : mem_info, "txn_info" : txn_info})

@web_app.post("/txn", response_class=HTMLResponse)
async def save_txn(request: Request,txn_info : TXN = Depends(TXN)):
    try:
        await save_txn_data(txn_info)
        return RedirectResponse('/web/mem/' + txn_info.mem_id,status_code=status.HTTP_302_FOUND)
    except Exception as e:
        print (e)

@web_app.get("/rpt/summary", response_class=HTMLResponse)
async def get_rpt_summary(request: Request,mode: str = 'live'):
    return web_templates.TemplateResponse("web/rpt_status.html",{"request": request})


@web_app.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    return RedirectResponse('/web',status_code=status.HTTP_302_FOUND)
