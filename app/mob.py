from fastapi import FastAPI, Request, Form, Depends,Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .db.models import Login, MEM, TXN, ACT, CRP
from .db.actions import submit_login, save_crp_data, save_mem_data, get_mem_data,get_txn_data, save_txn_data,get_shg_data_byid, get_crp_data_byid, save_act_data, get_cons_rpt
from fastapi.staticfiles import StaticFiles
import starlette.status as status
from starlette.responses import RedirectResponse

from datetime import datetime
from dateutil.relativedelta import relativedelta

mob_app = FastAPI()
mob_templates = Jinja2Templates(directory="templates")

@mob_app.get("/", response_class=HTMLResponse)
async def index(request: Request,response: Response):    
    return mob_templates.TemplateResponse("mob/_index.html",{"request": request, "error":""})

@mob_app.post("/", response_class=HTMLResponse)
async def login(request: Request, login : Login = Depends(Login)):
    try:
        #print(login.userid)
        #print(login.pwd)
        crpid = await submit_login(login.userid,login.pwd)
        #print(crpid)
        #print('crpid')
        if (crpid != ""):            
            #return RedirectResponse('/mob/shgs/' + crpid,status_code=status.HTTP_302_FOUND)
            return mob_templates.TemplateResponse("mob/_home.html",{"request": request, "crpid":crpid})
        else:
            return mob_templates.TemplateResponse("mob/_index.html",{"request": request, "error":"Invalid Login Credentails"})
    except Exception as e:
        print('Exception')
        print (e)

@mob_app.get("/back/{crpid}", response_class=HTMLResponse)
async def get_home(request: Request,crpid:str):
    return mob_templates.TemplateResponse("mob/_home.html",{"request": request, "crpid":crpid})

@mob_app.get("/crpt/{crpid}", response_class=HTMLResponse)
async def get_cons_report(request: Request,crpid:str):
    st_date = datetime.now().replace(day=1)
    en_date = st_date + relativedelta(months=1)
    rpt_info = get_cons_rpt(crpid,st_date,en_date)
    #print (rpt_info)
    return mob_templates.TemplateResponse("mob/rpt_cons.html",{"request": request, "crpid":crpid, "rpt_info":rpt_info})

@mob_app.post("/crpt/{crpid}", response_class=HTMLResponse)
async def get_cons_report(request: Request,crpid:str):
    form_data = await request.form()
    form_data = dict(form_data)
    print (form_data)
    format = "%Y-%m-%d"
    st_date = datetime.strptime(form_data["st_date"], format)
    en_date = datetime.strptime(form_data["en_date"], format)
    rpt_info = get_cons_rpt(crpid,st_date,en_date)
    #print (rpt_info)
    return mob_templates.TemplateResponse("mob/rpt_cons.html",{"request": request, "crpid":crpid, "rpt_info":rpt_info})

@mob_app.get("/shgs/{crpid}", response_class=HTMLResponse)
async def get_shg_list(request: Request, crpid:str):
    return mob_templates.TemplateResponse("mob/shg_list.html",{"request": request, "crpid":crpid})

@mob_app.get("/crp/{crpid}", response_class=HTMLResponse)
async def get_crp(request: Request, crpid : str):
    crp_info = await get_crp_data_byid(crpid)
    return mob_templates.TemplateResponse("mob/crp_details.html",{"request": request,"crpid":crpid, "crp_info" : crp_info})

@mob_app.post("/crp/{crpid}", response_class=HTMLResponse)
async def save_crp(request: Request,crpid : str, CRP = Depends(CRP)):
    crp_info = await save_crp_data(CRP)
    return RedirectResponse('/mob/shgs/' + crpid,status_code=status.HTTP_302_FOUND)

@mob_app.get("/mems/{shgid}", response_class=HTMLResponse)
async def get_mem_list(request: Request, shgid:str):
    shg_info = await get_shg_data_byid(shgid)
    print(shg_info)
    return mob_templates.TemplateResponse("mob/mem_list.html",{"request": request, "shgid":shgid, "crpid":shg_info['crp_id']})

@mob_app.get("/mem/new/{shgid}", response_class=HTMLResponse)
async def get_new_mem(request: Request, shgid : str):
    return mob_templates.TemplateResponse("mob/mem_add.html",{"request": request, "shgid":shgid})

@mob_app.post("/mem/new", response_class=HTMLResponse)
async def save_new_mem(request: Request,mem_info : MEM = Depends(MEM)):
    try:
        await save_mem_data(mem_info)
        return RedirectResponse('/mob/mems/' + mem_info.shg_id,status_code=status.HTTP_302_FOUND)
    except Exception as e:
        print (e)

@mob_app.get("/mem/home/{memid}", response_class=HTMLResponse)
async def get_mem_home(request: Request, memid : str):
    try:
        mem_info = await get_mem_data(memid)
        return mob_templates.TemplateResponse("mob/mem/_home.html",{"request": request, "mem_info" : mem_info})
    except Exception as e:
        print (e)

@mob_app.get("/mem/{memid}", response_class=HTMLResponse)
async def get_mem(request: Request, memid : str):
    try:
        mem_info = await get_mem_data(memid)
        return mob_templates.TemplateResponse("mob/mem/mem_details.html",{"request": request, "mem_info" : mem_info})
    except Exception as e:
        print (e)

@mob_app.post("/mem/{memid}", response_class=HTMLResponse)
async def save_mem(request: Request, memid : str, mem_info : MEM = Depends(MEM)):
    try:
        #TODO : Update the data
        await save_mem_data(mem_info)
        return RedirectResponse('/mob/txns/' + memid,status_code=status.HTTP_302_FOUND)
    except Exception as e:
        print (e)

@mob_app.get("/txns/{memid}", response_class=HTMLResponse)
async def get_mem_txns(request: Request, memid : str):
    mem_info = await get_mem_data(memid)
    return mob_templates.TemplateResponse("mob/mem/txn_list.html",{"request": request, "mem_info" : mem_info})

@mob_app.get("/txn/{memid}", response_class=HTMLResponse)
async def get_new_txn(request: Request, memid : str):
    mem_info = await get_mem_data(memid)
    return mob_templates.TemplateResponse("mob/mem/txn_add.html",{"request": request, "mem_info" : mem_info})

@mob_app.get("/txn-edit/{txnid}", response_class=HTMLResponse)
async def get_new_txn(request: Request, txnid : str):
    txn_info = await get_txn_data(txnid)
    print(txn_info['mem_id'])
    mem_info = await get_mem_data(txn_info['mem_id'])
    return mob_templates.TemplateResponse("mob/mem/txn_edit.html",{"request": request, "mem_info" : mem_info, "txn_info" : txn_info})

@mob_app.post("/txn", response_class=HTMLResponse)
async def save_mem(request: Request,txn_info : TXN = Depends(TXN)):
    try:
        await save_txn_data(txn_info)
        return RedirectResponse('/mob/txns/' + txn_info.mem_id,status_code=status.HTTP_302_FOUND)
    except Exception as e:
        print (e)
    
@mob_app.get("/acts/{memid}", response_class=HTMLResponse)
async def get_act_txns(request: Request, memid : str):
    mem_info = await get_mem_data(memid)
    return mob_templates.TemplateResponse("mob/mem/act_list.html",{"request": request, "mem_info" : mem_info})

@mob_app.get("/act/{memid}", response_class=HTMLResponse)
async def get_new_act(request: Request, memid : str):
    mem_info = await get_mem_data(memid)
    return mob_templates.TemplateResponse("mob/mem/act_add.html",{"request": request, "mem_info" : mem_info})

@mob_app.post("/act", response_class=HTMLResponse)
async def save_act(request: Request,act_info : ACT = Depends(ACT)):
    try:
        await save_act_data(act_info)
        return RedirectResponse('/mob/acts/' + act_info.mem_id,status_code=status.HTTP_302_FOUND)
    except Exception as e:
        print (e)  
        
@mob_app.get("/about/{crpid}", response_class=HTMLResponse)
async def about(request: Request,response: Response, crpid : str):
    return mob_templates.TemplateResponse("mob/about.html",{"request": request,"crpid":crpid})
        
@mob_app.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    return RedirectResponse('/mob',status_code=status.HTTP_302_FOUND)
