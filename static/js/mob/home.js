var app_session = {
  login_role: '',
  login_userid : '',
  login_user_name : '',
  curr_crp :'',
  curr_shg : '',
  curr_mem : ''
};
var purDict;
$.getJSON('/static/js/dat/act_mas.json?v.10', function(result){
	purDict = result;
	console.log('purDict Loaded...');
});	

var locDict;
$.getJSON('/api/loc_dict', function(result){
	locDict = result['data'];
	console.log('locDict API Loaded...');
});	

//$.getJSON('/static/js/dat/loc_mas.json?v.09c', function(result){
//	locDict = result;
//	console.log('locDict Loaded...');
//});	

function init(mod){
	if (mod === "HOME") loadHOME();
	if (mod === "SHG") loadSHGList();
	if (mod === "newMEM") newMEM();
	if (mod === "MEM") loadMEMList();
	if (mod === "MEMHOME") loadMEMHOME();
	if (mod === "TXN") loadTXNList();
	if (mod === "newTXN") newTXN();
	if (mod === "ACT") loadACTList();
	if (mod === "newACT") newACT();
	if (mod === "MEMInfo") loadMEMinfo();
	if (mod === "CRPInfo") loadCRPInfo();
	
	setLang(langCode);	
	mapAction();
};

function load(type, ID){
	if (type === "SHG") {
		app_session.curr_shg = ID;app_session.curr_mem = '';
		loadPage('/mob/mems/' + app_session.curr_shg,'app-main','MEM');
	}
	if (type === "MEM") {
		app_session.curr_mem = ID;
		//alert(app_session.curr_mem);		
		loadPage('/mob/mem/home/' + app_session.curr_mem,'app-page','MEMHOME')
	}
	if (type === "TXN") {
		loadPage('/mob/txn-edit/' + ID,'app-main','none')
	}
	if (type === "BACK") {
		app_session.curr_mem = '';
		loadPage('/mob/back/' + app_session.curr_crp,'app-page','');
		do_loadPage('/mob/mems/' + app_session.curr_shg,'app-main','MEM');
	}
	//alert('currCRP:' + app_session.curr_crp + ' | currSHG:' + app_session.curr_shg + ' | curr MEM :'+ app_session.curr_mem)
}

function newMEM(){
	const memid = document.querySelector('#memid');
	memid.value = 'MEM-' + Math.floor(Date.now() / 1000);
	get_pur_list();	
	get_pur_amt($('#pur_list').val());	
	$('#pur_list').on('change',function(){
		get_pur_amt($('#pur_list').val());
	});	
}

function newTXN(){
	const txnid = document.querySelector('#txnid');
	txnid.value = 'TXN-' + Math.floor(Date.now() / 1000);	
}
function newACT(){
	const actid = document.querySelector('#actid');
	actid.value = 'ACT-' + Math.floor(Date.now() / 1000);	

	get_pur_list();	
	$("#pur_list").val($('#mem_pur_id').val());
	get_act_list($('#mem_pur_id').val());
	
}
function loadHOME(){
	app_session.curr_crp = document.querySelector('#crpid').value;
	//alert(app_session.curr_crp);				
	loadPage('/mob/shgs/' + app_session.curr_crp,'app-main','SHG');
}

function loadMEMHOME(){
	//alert('Loading txns..' + app_session.curr_mem);
	do_loadPage('/mob/txns/' + app_session.curr_mem,'app-main','TXN');
}

function loadCRPInfo(){
	$("#crp_loc_desc").val(get_loc_desc($('#crp_loc').val()));
}

function loadMEMinfo(){
	console.log('Loading MEMInfo...' + $('#mem_pur_id').val());
	get_pur_list();	
	$("#pur_list").val($('#mem_pur_id').val());
}

function loadSHGList(){
	$('#shglist').DataTable( {
		responsive: true,
		"ajax": "/api/shgs/" + app_session.curr_crp,
		columns: [
			{
				data: 'shg_name',
				render: function(data, type, row) {
					if (type === 'display') {
						let link = "load('SHG','" + row.shg_id + "');";
						return '<a href="#" onclick="'+ link +'">' + data + ' (' + row.shg_vlg.slice(4) + ')</a>';
					}
					 
					return data;
				}
			},
			{
				data: 'shg_vlg',
				render : function(data,type){
					if (type === 'display') {
						return get_vlg_desc(data) + ' (' + data.slice(4) + ')';
						//return data;
					}
					 
					return data;				
				}
			},
			{data: 'shg_fullname'},
			{
				data: 'shg_loc',
				render : function(data,type){
					if (type === 'display') {
						return get_loc_desc(data);
						//return data;
					}
					 
					return data;				
				}
			},
			{data: 'shg_memcount'},
			{data: 'shg_amtdisbursed'},
			{data: 'shg_amtcollected'},
			{data: 'shg_lastactivity'}
		],				
		paging: false,
		dom: 'frt'						
	} );	
}

function loadMEMList(){
	var table = $('#memlist').DataTable( {
		responsive: true,
		"ajax": "/api/mems/" + app_session.curr_shg,
		columns: [
			{
			data: 'mem_name',
			render: function(data, type, row) {
				if (type === 'display') {
					let link = "load('MEM','" + row.mem_id + "');";					
					return '<a href="#" onclick="'+ link +'">' + data + '</a>';
				}
				 
				return data;
			}
		},
		{data: 'mem_spouse'},
		{
			data: 'mem_act',
			render : function(data,type){
				if (type === 'display') {
					return get_pur_desc(data);
					//return data;
				}
				 
				return data;				
			}
		},
		{data: 'mem_totamt'},
		{data: 'mem_amtrec'},
		{data: 'mem_amtret'},
		{data: 'mem_amtout'},
		{data: 'mem_lastactivity'}
		],
		paging: false,
		dom: 'frt'						
		
	} );	
}

function loadTXNList(){
	$('#txnlist').DataTable( {
		responsive: true,
		"ajax": "/api/txns/" + app_session.curr_mem,
		columns: [
			{
			data: 'txn_type',
			render: function(data, type, row) {
				if (type === 'display') {
					let link = "load('TXN','" + row.txn_id + "');";					
					return '<a href="#" onclick="'+ link +'" tkey="' + data + '">' + data + '</a>';
					//return '<a href="#" onclick="'+ link +'">' + data + '</a>';
				}				 
				return data;
				}
			},
			{data: 'txn_date'},
			{data: 'txn_amt'}
		],			
		order: [[1, 'desc']],
		paging: false,
		dom: 'frt',					
		"initComplete": function(settings, json) {
			//alert(langCode);
			setLang(langCode);
		}
  } );
}

function loadACTList(){
	$('#actlist').DataTable( {
		responsive: true,
		"ajax": "/api/acts/" + app_session.curr_mem,
		columns: [
			{
				data: 'act_type',
				render : function(data,type){
					if (type === 'display') {
						return get_act_desc(data);
						//return data;
					}
					 
					return data;				
				}				
			},
			{data: 'act_date'},
			{data: 'act_notes'}
		],
		order: [[1, 'desc']],
		paging: false,
		dom: 'frt'						

	} );
}

function get_pur_list(){
	$('#pur_list').empty();
	$.each(purDict, function(i, item) {
		//console.log(item.pur_desc_en);
		if (item.pur_id !== 'P00')
			$('<option>').val(item.pur_id).text((langCode === 'en') ? item.pur_desc_en : item.pur_desc_kn).appendTo('#pur_list');
	});	
}

function get_pur_amt(pur_id){
	$.each(purDict, function(i, item) {
		if (item.pur_id === pur_id) pur_amount.value = item.pur_amt;
	});	
}

function get_pur_desc(pur_id){
	ret_val = 'Unknown..';
	$.each(purDict, function(i, item) {
		if (item.pur_id === pur_id) ret_val = (langCode === 'en') ? item.pur_desc_en : item.pur_desc_kn;
	});	
	return ret_val
}

function get_act_list(pur_id){
	$('#act_list').empty();
	$.each(purDict, function(i, item) {
		if (item.pur_id === pur_id || item.pur_id === 'P00'){
			$.each(item.pur_act, function(i, subitem) {
				$('<option>').val(subitem.act_id).text((langCode === 'en') ? subitem.act_desc_en : subitem.act_desc_kn).appendTo('#act_list');
			});
		}			
	});	
}

function get_act_desc(act_id){
	ret_val = 'Unknown..';
	$.each(purDict, function(i, item) {
		$.each(item.pur_act, function(i, subitem) {
			//console.log(subitem.act_id);
			if (subitem.act_id === act_id) ret_val = (langCode === 'en') ? subitem.act_desc_en : subitem.act_desc_kn;
		});
	});
	return ret_val;
}

function get_loc_list(){
	$('#loc_list').empty();
	$.each(locDict, function(i, item) {
		$('<option>').val(item.loc_id).text((langCode === 'en') ? item.loc_desc_en : item.loc_desc_kn).appendTo('#loc_list');
	});	
}

function get_loc_desc(loc_id){
	ret_val = 'Unknown..';
	$.each(locDict, function(i, item) {
		if (item.loc_id === loc_id) ret_val = (langCode === 'en') ? item.loc_desc_en : item.loc_desc_kn;
	});	
	return ret_val
}

function get_vlg_list(loc_id){
	$('#vlg_list').empty();
	$.each(locDict, function(i, item) {
		if (item.loc_id === loc_id){
			$.each(item.loc_vlgs, function(i, subitem) {
				$('<option>').val(subitem.vlg_id).text((langCode === 'en') ? subitem.vlg_desc_en : subitem.vlg_desc_kn).appendTo('#vlg_list');
			});
		}			
	});	
}

function get_vlg_desc(vlg_id){
	ret_val = 'Unknown..';
	$.each(locDict, function(i, item) {
		$.each(item.loc_vlgs, function(i, subitem) {
			//console.log(subitem.act_id);
			if (subitem.vlg_id === vlg_id) ret_val = (langCode === 'en') ? subitem.vlg_desc_en : subitem.vlg_desc_kn;
		});
	});
	return ret_val;
}
