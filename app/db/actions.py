#import os
#f = open(os.getcwd() + 'data/crps.txt')
from .models import Location,CRP, CRPView,SHG, SHGView, MEM, MEMView, TXN, ACT
from deta import Deta
from datetime import datetime, timezone, timedelta
from pathlib import Path
import json

with open(Path('static/js/dat/act_mas.json'), "r", encoding='utf-8') as read_file:
    print("Reading ACT JSON")
    act_dat = json.load(read_file)

deta = Deta('c0kikqv6_W1vwXcv4uDi6zQn2xJvcurxa3h8LSvRK') # configure your Deta project
crp_tbl = deta.Base('crps')
shg_tbl = deta.Base('shgs')
mem_tbl = deta.Base('mems')
txn_tbl = deta.Base('txns')
act_tbl = deta.Base('acts')
loc_drive = deta.Drive('dat')

def fetch_all(tab,qry):
    _list = tab.fetch(qry)
    _items = _list.items
    while _list.last:
        _list = tab.fetch(qry,last=_list.last)
        _items += _list.items
        
    return _items


def load_loc_dict():
    #with open(Path('static/js/dat/loc_mas.json'), "r", encoding='utf-8') as read_file:
    #    print("Reading JSON serialized Unicode data from file")
    #    loc_dat = json.load(read_file)
     
    loc_file = loc_drive.get('loc_mas.json')
    loc_stream = loc_file.read()
    loc_file.close()
    loc_json = json.loads(loc_stream)
    
    return loc_json

loc_dat = load_loc_dict()

async def get_loc_dict():
    loc_dat = load_loc_dict()    
    return {"data":loc_dat}

async def get_locs():
    #f = open('data/locs.txt')
    #data = json.load(f)
    #return data
    loc_dat = load_loc_dict()
    
    ret_val = []
    for i in loc_dat:
        ret_val.append({"loc_id":i['loc_id'],"loc_desc_en":i['loc_desc_en'],"loc_desc_kn":i['loc_desc_kn']})
    
    return {"data":ret_val}

async def get_vlgs(loc):
    #f = open('data/locs.txt')
    #data = json.load(f)
    #return data

    loc_dat = load_loc_dict()

    ret_val = []
    for j in loc_dat:
        if (j['loc_id'] == loc):
            for i in j['loc_vlgs']:
                ret_val.append({"vlg_id":i['vlg_id'],"vlg_desc_en":i['vlg_desc_en'],"vlg_desc_kn":i['vlg_desc_kn']})
    
    return {"data":ret_val}

async def get_vlg_data(vlg_id):
    loc_dat = load_loc_dict()
    ret_val = []
    for j in loc_dat:
        for i in j['loc_vlgs']:
            if (i['vlg_id'] == vlg_id):
                ret_val.append({"vlg_id":i['vlg_id'],"vlg_desc_en":i['vlg_desc_en'],"vlg_desc_kn":i['vlg_desc_kn']})
    
    return ret_val

async def save_loc_data(loc_data_new : Location):
    try:
        loc_dat = load_loc_dict()

        print ('NEW UPDATE')
        print (loc_data_new)
        is_update = 0
        for j in loc_dat:
            if (j['loc_id'] == loc_data_new.loc_id):
                for i in j['loc_vlgs']:
                    #print (i['vlg_id'])
                    if (i['vlg_id'] == loc_data_new.vlg_id):
                        is_update = 1
                        print ('UPDATING DATA')
                        i['vlg_desc_en'] = loc_data_new.vlg_desc_en
                        i['vlg_desc_kn'] = loc_data_new.vlg_desc_kn
                
                if (is_update == 0):
                    print ('INSERTING DATA')
                    j['loc_vlgs'].append({"vlg_id":loc_data_new.vlg_id,"vlg_desc_en":loc_data_new.vlg_desc_en,"vlg_desc_kn":loc_data_new.vlg_desc_kn})
                    
        #with open(Path('static/js/dat/loc_mas.json'), "w") as outfile:
        #    json.dump(loc_dat, outfile, indent=4)    
       
        loc_drive.put('loc_mas.json', json.dumps(loc_dat))
        
        loc_dat = load_loc_dict()
       
    except Exception as e:
        print (e)


def get_desc(type,id):    
    if (type == 'C'):
        name = ''        
        for i in loc_dat:
            if (i['loc_id'] == id):
                name = i['loc_desc_en']
    
    if (type == 'V'):
        name = ''        
        for c in loc_dat:
            for v in c['loc_vlgs']:
                if (v['vlg_id'] == id):
                    name = v['vlg_desc_en']

    if (type == 'P'):
        name = ''        
        for i in act_dat:
            if (i['pur_id'] == id):
                name = i['pur_desc_en']

    return name

async def submit_login(userid, pwd):
    crps = crp_tbl.fetch({"crp_phone": userid, "crp_pwd": pwd})
    print (crps.count)
    if (crps.count == 1):
        return crps.items[0]["crp_id"]
    else :
        return ""

async def get_crps(mode):
    crplist = crp_tbl.fetch({"crp_mode": mode})
    retval = {"data" : crplist.items }
    return retval

#async def get_crp_data_byph(phno):
#    try:
#        #print ('Entering get_crp_data')
#        crplist = crp_tbl.fetch({"crp_phone": phno})        
#        return crplist.items[0]
#    except Exception as e:
#        print (e)

async def get_crp_data_byid(crpid):
    try:
        #print ('Entering get_crp_data')
        crplist = crp_tbl.fetch({"crp_id": crpid})        
        return crplist.items[0]
    except Exception as e:
        print (e)

async def check_crp_phone(crp_phone):
        crp_data = crp_tbl.fetch({"crp_phone": crp_phone})
        if (crp_data.count == 1):
            return 'DUP-PHONE'
        elif (crp_data.count > 1):
            return 'MUL-PHONE'
        else:
            return 'NEW-PHONE'

async def save_crp_data(crp_data : CRP):
    try:
        #crp_tbl.put(crp_data)
        data = json.loads(crp_data.json())
        crp_info = CRPView(**data)
            
        crpval = crp_tbl.fetch({"crp_id": crp_info.crp_id})
        if (crpval.count == 1):
            crp_info.crp_amtdisbursed = crpval.items[0]['crp_amtdisbursed']
            crp_info.crp_amtcollected = crpval.items[0]['crp_amtcollected']
            crp_info.crp_lastactivity = crpval.items[0]['crp_lastactivity']

            if (crp_info.crp_totalamt != crpval.items[0]['crp_totalamt']):
                #crp_info.crp_amtinhand = crp_info.crp_amtinhand + crp_info.crp_totalamt - crpval.items[0]['crp_totalamt']
                crp_info.crp_amtinhand = crp_info.crp_totalamt - crp_info.crp_amtdisbursed + crp_info.crp_amtcollected
            else:
                crp_info.crp_amtinhand = crpval.items[0]['crp_amtinhand']
            
            tbldata = json.loads(crp_info.json())
            crp_tbl.put(tbldata,crpval.items[0]['key'])
        else:
            tbldata = json.loads(crp_info.json())
            crp_tbl.put(tbldata) 
    except Exception as e:
        print (e)
   
async def get_shg_data_byid(shgid):
    try:
        shglist = shg_tbl.fetch({"shg_id": shgid})        
        return shglist.items[0]
    except Exception as e:
        print (e)

async def get_shgs(crpid):
    try:
        shglist = shg_tbl.fetch({"crp_id": crpid}) 
        retval = {"data" : shglist.items }
        return retval
    except Exception as e:
        print (e)

async def save_shg_data(shg_data : SHG):
    try:
        data = json.loads(shg_data.json())
        shg_info = SHGView(**data)
        #print(shg_info)
        shgval = shg_tbl.fetch({"shg_id": shg_info.shg_id})
        if (shgval.count == 1):            
            tbldata = json.loads(shg_info.json())
            shg_tbl.put(tbldata,shgval.items[0]['key'])
        else:
            tbldata = json.loads(shg_info.json())
            shg_tbl.put(tbldata) 
    except Exception as e:
        print (e)

async def del_shg_data(shgid):
    shglist = shg_tbl.fetch({"shg_id": shgid})
    delcount = shg_tbl.delete(shglist.items[0]['key'])
    print ('DELETING SHG - ',shglist.items[0]['key'])
    return delcount
    
async def get_mems(shgid):
    memlist = mem_tbl.fetch({"shg_id": shgid})
    retval = {"data" : memlist.items }
    return retval

async def get_mem_data(memid):
    try:
        #print ('Entering get_crp_data')
        memlist = mem_tbl.fetch({"mem_id": memid})        
        return memlist.items[0]
    except Exception as e:
        print (e)

async def del_mem_data(memid):
    memlist = fetch_all(mem_tbl,{"mem_id": memid})
    delcount = mem_tbl.delete(memlist[0]['key'])
    print ('DELETING MEM - ',memlist[0]['key'])
    
    shgval = shg_tbl.fetch({"shg_id": memlist[0]['shg_id']})
    if (shgval.count == 1):
        new_shg_memcount = int(shgval.items[0]['shg_memcount']) - 1
        new_shg_lastactivity = datetime.now().strftime("%d/%m/%Y")
        shg_updates = {"shg_memcount": new_shg_memcount, "shg_lastactivity" : new_shg_lastactivity}
        shg_tbl.update(shg_updates, shgval.items[0]["key"]) 
        print('SHG UPDATED WITH MEMBER COUNT......')
    
    return delcount

async def get_txn_data(txnid):
    try:
        #txnlist = txn_tbl.fetch({"txn_id": txnid})        
        #return txnlist.items[0]
        txnlist = fetch_all(txn_tbl,{"txn_id": txnid})
        return txnlist[0]
    except Exception as e:
        print (e)

async def save_mem_data(mem_data : MEM):
    try:
        #crp_tbl.put(crp_data)
        data = json.loads(mem_data.json())
        mem_info = MEMView(**data)
        
        memval = mem_tbl.fetch({"mem_id": mem_info.mem_id})
        if (memval.count == 1):
            mem_info.mem_amtrec = memval.items[0]['mem_amtrec']
            mem_info.mem_amtret = memval.items[0]['mem_amtret']
            mem_info.mem_amtout = memval.items[0]['mem_amtout']
            mem_info.mem_lastactivity = memval.items[0]['mem_lastactivity']
        
            tbldata = json.loads(mem_info.json())
            mem_tbl.put(tbldata,memval.items[0]['key'])
        else:
            tbldata = json.loads(mem_info.json())
            mem_tbl.put(tbldata) 
            print('ADDING NEW MEMBER......')
            shgval = shg_tbl.fetch({"shg_id": mem_info.shg_id})
            if (shgval.count == 1):
                new_shg_memcount = int(shgval.items[0]['shg_memcount']) + 1
                new_shg_lastactivity = datetime.now().strftime("%d/%m/%Y")
                shg_updates = {"shg_memcount": new_shg_memcount, "shg_lastactivity" : new_shg_lastactivity}
                shg_tbl.update(shg_updates, shgval.items[0]["key"]) 
                print('SHG UPDATED WITH MEMBER COUNT......')
                
    except Exception as e:
        print (e)

async def get_txns(memid):
    try:
        txnlist = fetch_all(txn_tbl,{"mem_id": memid})
        retval = {"data" : txnlist }
        return retval
    except Exception as e:
        print (e)

async def save_txn_data(txn_info : TXN):
    try:
        #data = json.loads(txn_data.json())
        #txn_info = TXNView(**data)
        tbldata = json.loads(txn_info.json())
        
        #Update mem data to reflect the txn
        mem_data = mem_tbl.fetch({"mem_id": txn_info.mem_id})
        shg_data = shg_tbl.fetch({"shg_id": mem_data.items[0]["shg_id"]})
        crp_data = crp_tbl.fetch({"crp_id": shg_data.items[0]["crp_id"]})
        txn_val = fetch_all(txn_tbl,{"txn_id": txn_info.txn_id})
        
        old_txn_type = 'NONE'
        new_txn_type = txn_info.txn_type
        if (len(txn_val) == 1):
            txn_data = txn_val[0]
            old_txn_type = txn_data["txn_type"]
            
        adj_txn_amt = float(txn_info.txn_amt)
        print ("Old Txn Type", old_txn_type)

        if (new_txn_type == 'txn_disbursed'):            
            #Disburse - money goes from crp to mem
            if (old_txn_type == 'txn_disbursed'):
                adj_txn_amt = float(txn_info.txn_amt) - float(txn_data["txn_amt"])       

            new_crp_amtdisbursed = float(crp_data.items[0]["crp_amtdisbursed"]) + adj_txn_amt
            new_crp_amtinhand = float(crp_data.items[0]["crp_amtinhand"]) - adj_txn_amt
            new_crp_lastactivity = datetime.now().strftime("%d/%m/%Y")
            crp_updates = {"crp_amtdisbursed": new_crp_amtdisbursed, "crp_amtinhand" : new_crp_amtinhand, "crp_lastactivity" : new_crp_lastactivity}
            
            new_shg_amtdisbursed = float(shg_data.items[0]["shg_amtdisbursed"]) + adj_txn_amt
            new_shg_lastactivity = datetime.now().strftime("%d/%m/%Y")
            shg_updates = {"shg_amtdisbursed": new_shg_amtdisbursed, "shg_lastactivity" : new_shg_lastactivity}
            
            new_mem_amtrec = float(mem_data.items[0]["mem_amtrec"]) + adj_txn_amt
            new_mem_amtout = float(mem_data.items[0]["mem_amtout"]) + adj_txn_amt
            new_mem_lastactivity = datetime.now().strftime("%d/%m/%Y")
            mem_updates = {"mem_amtrec": new_mem_amtrec, "mem_amtout" : new_mem_amtout, "mem_lastactivity" : new_mem_lastactivity}
                            
        elif (new_txn_type == 'txn_collected'):        
            #Collect
            if (old_txn_type == 'txn_collected'):
                adj_txn_amt = float(txn_info.txn_amt) - float(txn_data["txn_amt"])

            print ("Step B")
            new_crp_amtcollected = float(crp_data.items[0]["crp_amtcollected"]) + adj_txn_amt
            new_crp_amtinhand = float(crp_data.items[0]["crp_amtinhand"]) + adj_txn_amt
            new_crp_lastactivity = datetime.now().strftime("%d/%m/%Y")
            crp_updates = {"crp_amtcollected": new_crp_amtcollected, "crp_amtinhand" : new_crp_amtinhand, "crp_lastactivity" : new_crp_lastactivity}

            new_shg_amtcollected = float(shg_data.items[0]["shg_amtcollected"]) + adj_txn_amt
            new_shg_lastactivity = datetime.now().strftime("%d/%m/%Y")
            shg_updates = {"shg_amtcollected": new_shg_amtcollected, "shg_lastactivity" : new_shg_lastactivity}
            
            new_mem_amtret = float(mem_data.items[0]["mem_amtret"]) + adj_txn_amt
            new_mem_amtout = float(mem_data.items[0]["mem_amtout"]) - adj_txn_amt
            new_mem_lastactivity = datetime.now().strftime("%d/%m/%Y")
            mem_updates = {"mem_amtret": new_mem_amtret, "mem_amtout" : new_mem_amtout, "mem_lastactivity" : new_mem_lastactivity}
            
            if (new_mem_amtout == 0):
              await clr_dues(txn_info)
        else:
            print ('Save Due - No Action')
        
        if (len(txn_val) == 1):
            print ('Updating Txn', new_txn_type)
            txn_tbl.put(tbldata,txn_val[0]['key'])
        else:
            print ('Adding Txn', tbldata)
            txn_tbl.put(tbldata)
            #print (mem_updates)
            if (old_txn_type == 'NONE' and new_txn_type == 'txn_disbursed'):
                print ('Generating Dues')
                await gen_dues(txn_info)
        
        print (new_txn_type)
        if (new_txn_type != 'txn_due'):            
            crp_tbl.update(crp_updates, crp_data.items[0]["key"]) 
            shg_tbl.update(shg_updates, shg_data.items[0]["key"]) 
            mem_tbl.update(mem_updates, mem_data.items[0]["key"]) 
            print ('Updating MemInfo', mem_data.items[0]["mem_id"])
        
        #Update crp data to reflect the txn
        
    except Exception as e:
        print (e)

async def gen_dues(txn_info : TXN):
    try:
        dur = 13
        new_txn_id = txn_info.txn_id        
        new_txn_info = txn_info
        tmp_amt = round(txn_info.txn_amt / (dur - 1))
        last_amt = txn_info.txn_amt - (tmp_amt * (dur - 2))
        curr_date = txn_info.txn_date
        for x in range(dur):
            new_txn_info.txn_id = new_txn_id + '-' + str(x).rjust(2,"0")
            new_txn_info.mem_id = txn_info.mem_id
            new_txn_info.txn_type = 'txn_due'
            if (x < (dur - 2)) : 
                new_txn_info.txn_amt = tmp_amt
            else : 
                new_txn_info.txn_amt = last_amt

            curr_date = await get_next_month(curr_date)
            new_txn_info.txn_date = curr_date
            due_data = json.loads(new_txn_info.json())
            txn_tbl.put(due_data)

            #print(x)
            #print(new_txn_info.txn_id)
            #print(new_txn_info.mem_id)
            #print(new_txn_info.txn_type)
            #print(new_txn_info.txn_amt)
            #print(new_txn_info.txn_date)
            

    except Exception as e:
        print (e)

async def clr_dues(txn_info : TXN):
    try:
        txn_data = fetch_all(txn_tbl,{"mem_id": txn_info.mem_id, "txn_type" : "txn_due"})        
        for t_txn in txn_data:
            print(t_txn['txn_id'],t_txn['key'])
            txn_tbl.delete(t_txn['key'])
                    
    except Exception as e:
        print (e)
async def get_next_month(dt:datetime):
    return (dt.replace(day=1) + timedelta(days=32)).replace(day=1)

async def get_acts(memid):
    try:
        actlist = act_tbl.fetch({"mem_id": memid})
        retval = {"data" : actlist.items }
        return retval
    except Exception as e:
        print (e)

async def save_act_data(act_info : ACT):
    try:
        tbldata = json.loads(act_info.json())
        act_tbl.put(tbldata) 
        
    except Exception as e:
        print (e)

async def get_summary_report(mode):
    #start = time.time()
    i = 0
    t_dict = []
    tbl_crps = crp_tbl.fetch({"crp_mode": mode})
    tbl_shgs_tot = shg_tbl.fetch({"shg_memcount?ne" : 0, "shg_memcount?ne" : "0"})
    _tbl_mems = mem_tbl.fetch({"mem_amtrec?ne" : "0", "mem_amtrec?ne" : 0})
    
    tbl_mems_tot = _tbl_mems.items

    while _tbl_mems.last:
      _tbl_mems = mem_tbl.fetch({"mem_amtrec?ne" : "0", "mem_amtrec?ne" : 0}, last=_tbl_mems.last)
      tbl_mems_tot += _tbl_mems.items
    
    #print ("TOTAL MEMBERS IS ", len(tbl_mems_tot))

    for t_crp in tbl_crps.items:
      #print (t_crp["crp_id"])
      c_tot_mem = 0
      c_amt_dis = 0
      c_amt_col = 0      
      c_mem_dis = 0
      # The below stupid query is needed as excel upload converts numbers to text randomly.
      #tbl_shgs = shg_tbl.fetch({"crp_id": t_crp["crp_id"],"shg_memcount?ne" : 0, "shg_memcount?ne" : "0"})
      tbl_shgs = [x for x in tbl_shgs_tot.items if x['crp_id'] == t_crp["crp_id"]]
      #tbl_shgs = shg_tbl.fetch({"crp_id": t_crp["crp_id"]})
      #print (tbl_shgs.count)
      for t_shg in tbl_shgs:
        #print (t_shg["shg_name"])
        #print (t_shg["shg_memcount"])
        c_tot_mem = c_tot_mem + int(t_shg["shg_memcount"])        
        c_amt_dis = c_amt_dis + float(t_shg["shg_amtdisbursed"])
        c_amt_col = c_amt_col + float(t_shg["shg_amtcollected"])
        
        # This actually is not needed (as there is no excel upload for this), but I just got a bit paranoid.
        #tbl_mems = mem_tbl.fetch({"shg_id": t_shg["shg_id"],"mem_amtrec?ne" : "0", "mem_amtrec?ne" : 0})
        tbl_mems = [x for x in tbl_mems_tot if x['shg_id'] == t_shg["shg_id"]]        
        c_mem_dis = c_mem_dis + len(tbl_mems)
        
      t_dict.append({"crp_loc_name" : get_desc('C',t_crp["crp_loc"]),"crp_name" : t_crp["crp_name"],"tot_mem" : c_tot_mem, "c_mem_dis" : c_mem_dis, "c_amt_dis" : c_amt_dis,"c_amt_col" : c_amt_col  })
      #t_dict.append({"crp_loc_name" : t_crp["crp_loc"],"crp_name" : t_crp["crp_name"],"tot_mem" : c_tot_mem, "c_mem_dis" : c_mem_dis, "c_amt_dis" : c_amt_dis,"c_amt_col" : c_amt_col  })
         
    #print(f'Time Smry2: {time.time() - start}')  
    retval = {"data" : t_dict }
    return retval

async def get_summary_report_old(mode):
    #start = time.time()
    i = 0
    t_dict = []
    tbl_crps = crp_tbl.fetch({"crp_mode": mode})
    
    for t_crp in tbl_crps.items:
      #print (t_crp["crp_id"])
      c_tot_mem = 0
      c_amt_dis = 0
      c_amt_col = 0      
      c_mem_dis = 0
      # The below stupid query is needed as excel upload converts numbers to text randomly.
      tbl_shgs = shg_tbl.fetch({"crp_id": t_crp["crp_id"],"shg_memcount?ne" : 0, "shg_memcount?ne" : "0"})
      #tbl_shgs = shg_tbl.fetch({"crp_id": t_crp["crp_id"]})
      #print (tbl_shgs.count)
      for t_shg in tbl_shgs.items:
        #print (t_shg["shg_name"])
        #print (t_shg["shg_memcount"])
        c_tot_mem = c_tot_mem + int(t_shg["shg_memcount"])        
        c_amt_dis = c_amt_dis + float(t_shg["shg_amtdisbursed"])
        c_amt_col = c_amt_col + float(t_shg["shg_amtcollected"])
        
        # This actually is not needed (as there is no excel upload for this), but I just got a bit paranoid.
        tbl_mems = mem_tbl.fetch({"shg_id": t_shg["shg_id"],"mem_amtrec?ne" : "0", "mem_amtrec?ne" : 0})
        c_mem_dis = c_mem_dis + int(tbl_mems.count)
        
      t_dict.append({"crp_loc_name" : get_desc('C',t_crp["crp_loc"]),"crp_name" : t_crp["crp_name"],"tot_mem" : c_tot_mem, "c_mem_dis" : c_mem_dis, "c_amt_dis" : c_amt_dis,"c_amt_col" : c_amt_col  })
         
    #print(f'Time: {time.time() - start}')  
    retval = {"data" : t_dict }
    return retval

async def get_crp_report(crp_id):
    #start = time.time()
    i = 0
    t_dict = []
    s_dict = []
    
    #print (t_crp["crp_id"])
    c_tot_mem = 0
    c_amt_dis = 0
    c_amt_col = 0      
    c_mem_dis = 0
    # The below stupid query is needed as excel upload converts numbers to text randomly.
    tbl_shgs = shg_tbl.fetch({"crp_id": crp_id,"shg_memcount?ne" : 0, "shg_memcount?ne" : "0"})
    for t_shg in tbl_shgs.items:
      #print (t_shg["shg_name"])
      #print (t_shg["shg_memcount"])
      c_tot_mem = c_tot_mem + int(t_shg["shg_memcount"])        
      c_amt_dis = c_amt_dis + float(t_shg["shg_amtdisbursed"])
      c_amt_col = c_amt_col + float(t_shg["shg_amtcollected"])
        
      # This actually is not needed (as there is no excel upload for this), but I just got a bit paranoid.
      tbl_mems = mem_tbl.fetch({"shg_id": t_shg["shg_id"],"mem_amtrec?ne" : "0", "mem_amtrec?ne" : 0})
      c_mem_dis = c_mem_dis + int(tbl_mems.count)
      
      #for t_mem in tbl_mems.items:
      #  tbl_txns = txn_tbl.fetch({"mem_id": t_mem["mem_id"],"shg_memcount?ne" : 0, "shg_memcount?ne" : "0"})
        
    t_dict.append({"crp_loc_name" : get_desc('C',t_crp["crp_loc"]),"crp_name" : t_crp["crp_name"],"tot_mem" : c_tot_mem, "c_mem_dis" : c_mem_dis, "c_amt_dis" : c_amt_dis,"c_amt_col" : c_amt_col  })
         
    #print(f'Time: {time.time() - start}')  
    retval = {"data" : t_dict }
    return retval
    
   
async def reset_data(mode):
    train_crps = crp_tbl.fetch({"crp_mode": mode})
    for t_crp in train_crps.items:
        print(t_crp['crp_id'],t_crp['key'])
        train_shgs = shg_tbl.fetch({"crp_id": t_crp['crp_id']})
        for t_shg in train_shgs.items:
            print(t_shg['shg_id'],t_shg['key'])
            train_mems = mem_tbl.fetch({"shg_id": t_shg['shg_id']})
            for t_mem in train_mems.items:
                print(t_mem['mem_id'],t_shg['key'])
                train_txns = txn_tbl.fetch({"mem_id": t_mem['mem_id']})
                for t_txn in train_txns.items:
                    print(t_txn['txn_id'],t_txn['key'])
                    txn_tbl.delete(t_txn['key'])
                train_acts = act_tbl.fetch({"mem_id": t_mem['mem_id']})
                for t_act in train_acts.items:
                    print(t_act['act_id'],t_act['key'])
                    act_tbl.delete(t_act['key'])
                
                mem_tbl.delete(t_mem['key'])
            shg_tbl.delete(t_shg['key'])
        crp_tbl.delete(t_crp['key'])
    return 'DONE'
    
        
async def get_json_data(mode):
    train_crps = crp_tbl.fetch({"crp_mode": mode})
    ret_val = []
    for t_crp in train_crps.items:
        print(t_crp['crp_id'],t_crp['key'])
        ret_crp = t_crp
        ret_crp["shgs"] = []
        train_shgs = shg_tbl.fetch({"crp_id": t_crp['crp_id']})
        for t_shg in train_shgs.items:
            print(t_shg['shg_id'],t_shg['key'])
            ret_shg = t_shg
            ret_shg["mems"] = []
            train_mems = mem_tbl.fetch({"shg_id": t_shg['shg_id']})
            for t_mem in train_mems.items:
                print(t_mem['mem_id'],t_shg['key'])
                ret_mem = t_mem
                ret_mem["txns"] = []
                ret_mem["acts"] = []
                train_txns = txn_tbl.fetch({"mem_id": t_mem['mem_id']})
                for t_txn in train_txns.items:
                    print(t_txn['txn_id'],t_txn['key'])
                    ret_mem["txns"].append(t_txn)
                train_acts = act_tbl.fetch({"mem_id": t_mem['mem_id']})
                for t_act in train_acts.items:
                    print(t_act['act_id'],t_act['key'])
                    ret_mem["acts"].append(t_act)
                
                ret_shg["mems"].append(ret_mem)
            ret_crp["shgs"].append(ret_shg)            
        ret_val.append(ret_crp)        

    return ret_val
    
    
def get_cons_rpt(crp_id, s_date, e_date):
    #start = time.time()
    st_date = s_date.strftime("%Y-%m-%d")
    en_date = e_date.strftime("%Y-%m-%d")
    
    due_amt = 0    
    col_amt = 0
    dis_amt = 0
    t_dict = []
    t_i = 0
    m_i = 0
    s_i = 0
    c_i = 0
    
    tbl_shgs = shg_tbl.fetch({"crp_id": crp_id,"shg_memcount?ne" : 0, "shg_memcount?ne" : "0"})
    #tbl_mems = mem_tbl.fetch({"mem_amtrec?gt" : 0, "mem_amtout?gt" : 0})
    tbl_mems = mem_tbl.fetch({"mem_amtrec?gt" : 0})
    mem_items = tbl_mems.items
    while tbl_mems.last:
      tbl_mems = mem_tbl.fetch({"mem_amtrec?gt" : 0},last=tbl_mems.last)
      mem_items += tbl_mems.items
    
    tbl_txns = txn_tbl.fetch({"txn_date?gte" : st_date, "txn_date?lt" : en_date})
    txn_items = tbl_txns.items
    while tbl_txns.last:
      tbl_txns = txn_tbl.fetch({"txn_date?gte" : st_date, "txn_date?lt" : en_date},last=tbl_txns.last)
      txn_items += tbl_txns.items
  
    #print (txn_items.count)
    
    for t_txn in txn_items:
      t_i = t_i + 1
      #print (t_i)
      _memid = t_txn["mem_id"]
#      g_shg_for_txn(tbl_mems.items,_memid)      
      for t_mem in mem_items:
        if(t_mem["mem_id"] == _memid):
          m_i = m_i + 1
          #print (m_i)
          _shgid = t_mem["shg_id"]
          for t_shg in tbl_shgs.items:
            if (t_shg["shg_id"] == _shgid and t_shg["crp_id"] == crp_id):
              s_i = s_i + 1
              #print (s_i)
              #print (t_shg["crp_id"])
              t_dict.append({"txn_type" : t_txn["txn_type"],"txn_amt" : t_txn["txn_amt"],"txn_date" : t_txn["txn_date"],"mem_name":t_mem["mem_name"], "shg_name":t_shg["shg_name"]})         
              if(t_txn["txn_type"] == "txn_due"):
                due_amt = due_amt + t_txn["txn_amt"]
              if(t_txn["txn_type"] == "txn_collected"):
               col_amt = col_amt + t_txn["txn_amt"]
              if(t_txn["txn_type"] == "txn_disbursed"):
                dis_amt = dis_amt + t_txn["txn_amt"]
              
    ret_val = {"col_amt":col_amt, "dis_amt":dis_amt, "due_amt" : due_amt, "st_date":st_date, "en_date":en_date, "txn_details" : t_dict}
    #print(f'You have dues of Rs{due_amt}, collection of Rs {col_amt} and disbursements of {dis_amt} between {st_date} and {en_date} ')
    #print(f'Time: {time.time() - start}')       
    return ret_val