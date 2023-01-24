var app_session = {
  login_role: '',
  login_userid : '',
  login_user_name : '',
  curr_crp :'',
  curr_shg : '',
  curr_mem : '',
  curr_loc : '',
  curr_vlg : ''
};
var purDict;
$.getJSON('/static/js/dat/act_mas.json?v.10', function(result){
	purDict = result;
	console.log('purDict Loaded...');
});	

function initLOCJson(){
	$.get('/api/loc_dict', function(result){
		locDict = result['data'];
		console.log('locDict API Loaded...');
	});		
}

var locDict;
initLOCJson();

//$.getJSON('/static/js/dat/loc_mas.json?v.09c', function(result){
//	locDict = result;
//	console.log('locDict Loaded...');
//});	

function init(mod){
	if (mod === "HOME") loadHOME();
	if (mod === "LOC") loadLOCData();
	if (mod === "VLG") initVLG();
	if (mod === "CRP") loadCRPList();
	if (mod === "newCRP") newCRP();
	if (mod === "SHG") loadSHGList();
	if (mod === "newSHG") newSHG();
	if (mod === "MEM") loadMEMList();
	if (mod === "MemInfo") loadMEMInfo();
	if (mod === "TxnInfo") loadTXNInfo();
	if (mod === "rpt.status") loadReport('status');
	
	setLang(langCode);
	mapAction();
};
function load(type, ID){
	if (type === "VLG") {
		//alert(ID);
		app_session.curr_vlg = ID;		
		loadPage('/web/vlg/' + app_session.curr_vlg,'app-main','VLG');
	}
	if (type === "CRP") {
		app_session.curr_crp = ID;app_session.curr_shg = '';app_session.curr_mem = '';
		loadPage('/web/crp/' + app_session.curr_crp,'app-main','SHG');
	}
	if (type === "SHG") {
		app_session.curr_shg = ID;app_session.curr_mem = '';
		loadPage('/web/shg/' + app_session.curr_shg,'app-main','MEM');
	}
	if (type === "MEM") {
		app_session.curr_mem = ID;
		loadPage('/web/mem/' + app_session.curr_mem	,'app-main','MemInfo')
	}
	if (type === "TXN") {
		app_session.curr_txn = ID;
		loadPage('/web/txn/' + app_session.curr_txn	,'app-main','TxnInfo')
	}
	//alert('currCRP:' + app_session.curr_crp + ' | currSHG:' + app_session.curr_shg + ' | curr MEM :'+ app_session.curr_mem)
}

function delSHG(shg_id){
	loadPage('/web/shg/del/' + shg_id,'app-main','SHG');
}

function delMEM(mem_id, shg_id){
	loadPage('/web/mem/del/' + mem_id,'app-main','MEM');
}

function loadHOME(){
	loadPage('/web/crps','app-main','CRP');
}

function loadLOC(clr){
	if (clr === 1)
		app_session.curr_loc = '';
	
	loadPage('/web/vlgs','app-main','LOC');
}

function loadLOCData(){
	initLOCJson();
	loadLOCList();
	loadVLGList();
}
function loadLOCList(){
	$('#loc_list').empty();
	$.each(locDict, function(i, item) {
		$('<option>').val(item.loc_id).text((langCode === 'en') ? item.loc_desc_en : item.loc_desc_kn).appendTo('#loc_list');
	});	
	
	if (app_session.curr_loc !== '') $('#loc_list').val(app_session.curr_loc)
}

function loadVLGList(){
	app_session.curr_loc = $('#loc_list').val();
	app_session.curr_vlg = '';
	//alert(loc);
	
	$('#vlglist').DataTable( {
		destroy: true,
		responsive: true,
		"ajax": "/api/vlgs/" + app_session.curr_loc,
		columns: [
			{
				data: 'vlg_id',
				render: function(data, type,row) {
					if (type === 'display') {
						let link = "load('VLG','" + row.vlg_id + "')";
						return '<a href="#" onclick="'+ link +'">' + data + '</a>';
					}
					 
					return data;
				}
				
			},
			{data: 'vlg_desc_en'},
			{data: 'vlg_desc_kn'}
		],				
		paging: false,
	} );	
};

function loadNEWVLG(){
	app_session.curr_vlg = '';
	loadPage('/web/newvlg/' + $('#loc_list').val(),'app-main','VLG');
}

function initVLG(){
	loadLOCList();
	//alert('init new Village Form');
	$('#loc_list').val(app_session.curr_loc)
	$('#hdnlocid').val(app_session.curr_loc)
	
	if (app_session.curr_vlg === '')
		set_vlg_id(app_session.curr_loc);
	
}

function set_vlg_id(loc_id){
	//Generate ID : Get MaxID for Loc --> Remove 5 chars --> increment --> pad to 3 --> add back first 5 chars.
	var curr_max_id = 'C00.V00'
	$.each(locDict, function(i, item) {
		if (item.loc_id === loc_id){
			$.each(item.loc_vlgs, function(i, subitem) {
				//console.log(subitem.vlg_id);
				if (subitem.vlg_id > curr_max_id) 
					curr_max_id = subitem.vlg_id
				//$('<option>').val(subitem.vlg_id).text((langCode === 'en') ? subitem.vlg_desc_en : subitem.vlg_desc_kn).appendTo('#vlg_list');
			});
		}			
	});	
	new_max_id = curr_max_id.slice(0,5) + String(parseInt(curr_max_id.slice(5)) + 1).padStart(3, '0');
	console.log(new_max_id);
	$('#vlgid').val(new_max_id);
}
$.fn.dataTable.ext.buttons.newCRP = {
	className: 'btn btn-primary',
 
	action: function ( e, dt, node, config ) {
		loadPage('/web/crp/new','app-main','newCRP');
	}
};	

function loadCRPList(){
	$('#crplist').DataTable( {
		responsive: true,
		"ajax": "/api/crps/" + $('#_mode').val(),
		columns: [
			{
				data: 'crp_name',
				render: function(data, type,row) {
					if (type === 'display') {
						let link = "load('CRP','" + row.crp_id + "')";
						return '<a href="#" onclick="'+ link +'">' + data + '</a>';
					}
					 
					return data;
				}
				
			},
			{data: 'crp_phone'},
			{
				data: 'crp_loc',
				render : function(data,type){
					if (type === 'display') {
						return get_loc_desc(data);
						//return data;
					}
					 
					return data;				
				}
			},
			{data: 'crp_totalamt'},
			{data: 'crp_amtinhand'},
			{data: 'crp_amtdisbursed'},
			{data: 'crp_amtcollected'},
			{ 
				data: null,                       
				render: function(data,type,row) { return (data['crp_amtdisbursed'] - data['crp_amtcollected'])}
			},			
			{data: 'crp_lastactivity'}
		],				
		paging: false,
		dom: 'fBrt',
		buttons: [
			{
				extend: 'newCRP',
				text: '<span tkey="new">New</span>'
			}
		]				
	} );	
};

function newCRP(){
	$('#crp_mode').val($('#_mode').val())
	//alert($('#crp_mode').val());
	const crpid = document.querySelector('#crpid');
	crpid.value = 'CRP-' + Math.floor(Date.now() / 1000);
	console.log('Calling LOC list');
	get_loc_list();	
}

function newSHG(){
	const shgid = document.querySelector('#shgid');
	shgid.value = 'SHG-' + Math.floor(Date.now() / 1000);	
	
	get_loc_list();
	$("#loc_list").val($('#crp_loc').val());
	get_vlg_list($('#crp_loc').val());
}

$.fn.dataTable.ext.buttons.newSHG = {
	className: 'btn btn-primary',
 
	action: function ( e, dt, node, config ) {
		loadPage('/web/shg/new/' + app_session.curr_crp,'app-main','newSHG');
		//window.location = '/web/shg/new/' + crpid;
	}
};	

function loadSHGList(){
	get_loc_list();
	$('#shglist').DataTable( {
		responsive: true,
		"ajax": "/api/shgs/" + app_session.curr_crp,
		columns: [
			{
				data: 'shg_name',
				render: function(data, type, row) {
					if (type === 'display') {
						let link = "load('SHG','" + row.shg_id + "');";
						return '<a href="#" onclick="'+ link +'">' + data + '</a>';
					}
					 
					return data;
				}
			},
			{
				data: 'shg_vlg',
				render : function(data,type){
					if (type === 'display') {
						return get_vlg_desc(data);
						//return data;
					}
					 
					return data;				
				}
			},
			{data: 'shg_memcount'},
			{data: 'shg_amtdisbursed'},
			{data: 'shg_amtcollected'},
			{ 
				data: null,                       
				render: function(data,type,row) { return (data['shg_amtdisbursed'] - data['shg_amtcollected'])}
			},
			{data: 'shg_lastactivity'}
		],				
		dom: 'fBrtip',
		buttons: [
			{
				extend: 'newSHG',
				text: '<span tkey="new">New</span>'
			}
		]				
	} );

	$("#crp_loc_desc").val(get_loc_desc($('#crp_loc').val()));
	$("#crp_loc_desc_form").val(get_loc_desc($('#crp_loc').val()));

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
		paging: false			
	} );

	$("#shg_loc_desc").val(get_loc_desc($('#shg_loc').val()));
	$("#shg_vlg_desc").val(get_vlg_desc($('#shg_vlg').val()));

	$("#shg_loc_desc_form").val(get_loc_desc($('#shg_loc').val()));
	$("#shg_vlg_desc_form").val(get_vlg_desc($('#shg_vlg').val()));
	
}

function loadMEMInfo(){
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
		paging: false,
		order: [[1, 'desc']],
		"initComplete": function(settings, json) {
			//alert(langCode);
			setLang(langCode);
		}
	} );
	
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
		paging: false,
		order: [[1, 'desc']]
	} );
	
	$('#pur_desc').val(get_pur_desc($('#mem_pur_id').val()))
	
}

function loadTXNInfo(){
	
}

function get_pur_desc(pur_id){
	ret_val = 'Unknown..';
	$.each(purDict, function(i, item) {
		if (item.pur_id === pur_id) ret_val = (langCode === 'en') ? item.pur_desc_en : item.pur_desc_kn;
	});	
	return ret_val
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

function loadReport(rptname){		
	if (rptname === 'status'){
		console.log('So fa so good...');
		var table = $('#rpt_status').DataTable( {
			responsive: true,
			dom: 'Brt',
			ajax: "/api/rpt/summary/" + $('#_mode').val(),
			columns: [
				{data: 'crp_loc_name'},
				{data: 'crp_name'},
				{data: 'tot_mem'},
				{data: 'c_mem_dis'},
				{data: 'c_amt_dis'},
				{data: 'c_amt_col'}
			],
			paging: false,
			order: [[ 0, 'asc' ]],
			buttons: ['csv']
	
		});
		
		table.on('xhr.dt', function ( e, settings, json, xhr ) {
			//console.log('AJAX Done...');
			//console.log(json);

			var tot_mem = 0; var act_mem = 0; var amt_d = 0; var amt_c = 0;
			for ( var i=0, ien=json.data.length ; i<ien ; i++ ) {
				tot_mem += json.data[i].tot_mem;
				act_mem += json.data[i].c_mem_dis;
				amt_d += json.data[i].c_amt_dis;
				amt_c += json.data[i].c_amt_col;
			}
			//console.log(tot_mem);	
			document.querySelector('#tot_mem').innerHTML = tot_mem;
			document.querySelector('#act_mem').innerHTML = act_mem;
			document.querySelector('#amt_d').innerHTML = amt_d.toLocaleString('hi-IN', { style: 'currency', currency: 'INR' });
			document.querySelector('#amt_c').innerHTML = amt_c.toLocaleString('hi-IN', { style: 'currency', currency: 'INR' });
			
			//var my_val = table.column(3).data().sum();
			//console.log($(this).column(3).data().sum());
		});
	}
};
