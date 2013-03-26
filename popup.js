
function enable() {
	chrome.tabs.getSelected(null, function(tab) {
		$('#url').val( tab.url );
		$('#title').val( tab.title );
		
		port.postMessage({"action":"enable", "tab": tab});
	});
	
}

function disable() {
	chrome.tabs.getSelected(null, function(tab) {		
		port.postMessage({"action":"disable", "tab": tab});
	});
}


function post_online() {
	chrome.tabs.captureVisibleTab(null, {}, function(img) {
		$('#ss').val( img );
		
		$("#frm").submit();
	});
	
	bg = chrome.extension.getBackgroundPage();
	bg._disable();
	
}

$('#save').bind('click', function() {
	post_online();
});
$('#enable').bind('click', function() {
	enable();
});
$('#disable').bind('click', function() {
	disable();
});

var port = chrome.extension.connect({name:"popup"});
// port.onMessage.addListener(function(msg) {}); seemed a little flaky

bg = chrome.extension.getBackgroundPage();

chrome.tabs.getSelected(null, function(tab) {		
	bg.inject(tab);

	$('#url').val( tab.url );
	$('#title').val( tab.title );
	
	if (bg.data.xpath == undefined) return;
	$('textarea[name=xpath]').text( bg.data.xpath );
	$('#text').val( bg.data.text );	
	$("input[name=html]").val( bg.data.html );
	$('#meta').val( bg.data.meta );
	
});

