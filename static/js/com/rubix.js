var langs = ['en', 'kn'];
langCode = 'en';
var langDict;

const formatDate = d => [
    d.getFullYear(),
    (d.getMonth() + 1).toString().padStart(2, '0'),
    d.getDate().toString().padStart(2, '0')
].join('-');

var translate = function (jsdata)
{	
	console.log('translate called...');
	var date = new Date(), y = date.getFullYear(), m = date.getMonth();
	$("[tkey]").each (function (index)
	{
		var strTr = jsdata [$(this).attr ('tkey')];
	    $(this).html (strTr);
	});

	$("[def_today]").each (function (index)
	{
		if ($(this).val === "") $(this).val(formatDate(new Date()));
	});

	//$("[def_mst]").each (function (index)
	//{
	//	alert($(this).val());
	//	var firstDay = new Date(y, m, 1);		
	//	if ($(this).val() === "") $(this).val(formatDate(firstDay));
	//});

	//$("[def_men]").each (function (index)
	//{
	//	var lastDay = new Date(y, m + 1, 0);
	//	if ($(this).val() === "") $(this).val(formatDate(lastDay));
	//});

	//TODO : Mobile app icon tooltips to be translated.
	//$("[ttip]").each (function (index)
	//{
	//	var strTr = jsdata [$(this).attr ('ttip')];
	//    $(this).attr("title", strTr);;
	//});
}
function loadLang(plangCode){
	langCode = plangCode;	
	$.getJSON('/static/lang/'+langCode+'.json?v0.7', function(result){
		langDict = result;
		setLang(langDict);
		console.log('langLoad done...');
	});		
}

function setLang(plangCode){
	translate(langDict);
}

function loadPage(actionUrl, replaceDiv, initMod){
	history.pushState(actionUrl + ":" + replaceDiv + ":" + initMod, "", "");
	//console.log('FORWARD ACTION is ' + actionUrl + ":" + replaceDiv + ":" + initMod);
	//window.localStorage.setItem('currpage', actionUrl + ":" + replaceDiv + ":" + initMod);
	do_loadPage(actionUrl, replaceDiv, initMod);
}

function do_loadPage(actionUrl, replaceDiv, initMod){	
    $.ajax({
      url: actionUrl,
      method: 'GET',
      success: function(data) {
		var container = document.getElementById(replaceDiv);
		container.innerHTML = data;
		init(initMod);
      },
    });	
}

function mapAction(){
$('.app-form').on("submit", function(event) {
    event.preventDefault();
	$(this).find(":submit").attr('disabled', 'disabled');

    var actionUrl = $(this).attr('action');
    var formData = $(this).serialize();
    var replaceDiv = $(this).attr('replace');
    var initMod = $(this).attr('mod');

	//alert(formData);
    $.ajax({
      url: actionUrl,
      method: 'POST',
      //dataType: 'json',
      data: formData,
      success: function(data) {
		var container = document.getElementById(replaceDiv);
		container.innerHTML = data;
		init(initMod);
      },
    });
  });
}
loadLang('en');
mapAction();

window.addEventListener('popstate', onPopState);

function onPopState(e) {
	let state = e.state;
	console.log(state);
	if (state !== null) {
		x_reload(state);
	}
	//else {
	//	history.back();
	//}

}

function x_reload(state){
	
	arr_state = state.split(":");
	p_actionUrl = arr_state[0];
	p_replaceDiv = arr_state[1]; 
	p_initMod = arr_state[2];
	
	console.log('p_actionUrl is ' + p_actionUrl);
	console.log('p_replaceDiv is ' + p_replaceDiv);
	console.log('p_initMod is ' + p_initMod);
	
	do_loadPage(p_actionUrl, p_replaceDiv, p_initMod);
}


// Good article on HistoryAPI state management.
//https://medium.com/@george.norberg/history-api-getting-started-36bfc82ddefc