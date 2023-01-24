#https://github.com/tiangolo/fastapi/issues/2387
from fastapi import Form
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime, timezone

def form_body(cls):
    cls.__signature__ = cls.__signature__.replace(
        parameters=[
            arg.replace(default=Form(...))
            for arg in cls.__signature__.parameters.values()
        ]
    )
    return cls

#usrs : userid, password (for now, admin with fixed pwd - need change pwd and manage users later)    
@form_body
class Login(BaseModel):
    userid : str
    pwd : str

@form_body
class Location(BaseModel):
    loc_id : str
    vlg_id : str
    vlg_desc_en : str
    vlg_desc_kn : str
    
#crps : crpMode(Live/Trng), crpPhoneNo, crpName, crpLocation, crpPortfolio, disbursed, collected, inHand, lastActivity
@form_body
class CRP(BaseModel):
    crp_mode : str
    crp_id : str
    crp_phone : str
    crp_pwd : str
    crp_name : str
    crp_loc : str
    crp_totalamt : int

@form_body
class CRPView(BaseModel):
    crp_mode : str
    crp_id : str
    crp_phone : str
    crp_pwd : str
    crp_name : str
    crp_loc : str
    crp_totalamt : int 
    crp_amtdisbursed : Optional[int] = 0
    crp_amtcollected : Optional[int] = 0
    crp_amtinhand : Optional[int] = 0
    crp_lastactivity : Optional[datetime] = datetime.now().strftime("%d/%m/%Y")
    #= datetime.now().strftime("%d/%m/%Y")
    #crp_lastactivity : Optional[datetime] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

@form_body
class SHG(BaseModel):
    shg_id : str
    crp_id : str
    shg_name : str
    shg_fullname : str
    shg_loc : str
    shg_vlg : str
    shg_memcount : int

class SHGView(BaseModel):
    shg_id : str
    crp_id : str
    shg_name : str
    shg_fullname : str
    shg_loc : str    
    shg_vlg : str
    shg_memcount : int
    shg_amtdisbursed : Optional[int] = 0
    shg_amtcollected : Optional[int] = 0
    shg_lastactivity : Optional[datetime] = datetime.now().strftime("%d/%m/%Y")
        
    
#mems : memID, memName, memLocation, memActivity, memAllotted, recieved, returned, outstanding, lastActivity
@form_body
class MEM(BaseModel):
    mem_id : str
    shg_id : str
    mem_name : str
    mem_spouse : str
    mem_act : str
    mem_totamt : int


class MEMView(BaseModel):
    mem_id : str
    shg_id : str
    mem_name : str
    mem_spouse : str
    mem_act : str
    mem_totamt : int
    mem_amtrec : Optional[int] = 0
    mem_amtret : Optional[int] = 0
    mem_amtout : Optional[int] = 0
    mem_lastactivity : Optional[datetime] = datetime.now().strftime("%d/%m/%Y")

#txns : crpID, memID, txnDate, txnType, txnAmount    
@form_body
class TXN(BaseModel):
    txn_id : str
    mem_id : str
    txn_type : str
    txn_amt : int
    txn_date : date

@form_body
class ACT(BaseModel):
    act_id : str
    mem_id : str
    act_type : str
    act_notes : str
    act_date : date

class LOC(BaseModel):
    cluster : str
    taluk : str
    district : str

        
#locs : locCode, locName
#acts : actCode, actName