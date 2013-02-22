// javascript:c=document.createElement('script');c.type='text/javascript';c.src='file:///marklet.js?ts='+new Date().getTime();document.getElementsByTagName('HEAD')[0].appendChild(c);

// load our own jQuery from googleapis CDN
javascript:(function(e,a,g,h,f,c,b,d){if(!(f=e.jQuery)||g>f.fn.jquery||h(f)){c=a.createElement("script");c.type="text/javascript";c.src="https://ajax.googleapis.com/ajax/libs/jquery/"+g+"/jquery.min.js";c.onload=c.onreadystatechange=function(){if(!b&&(!(d=this.readyState)||d=="loaded"||d=="complete")){h((f=e.jQuery).noConflict(1),b=1);f(c).remove()}};a.documentElement.childNodes[0].appendChild(c)}})(window,document,"1.3.2",function($,L){

// prevent duplicate loads

// getXPath

// display simple floating UI with data

$("*").bind('click', function(el) {

	x = []
	t = el.target;
	while (t != undefined && t.nodeName != "HTML") {
		node = t.nodeName;
		// XXX as soon as we find a node with an id or class, we can probably break to save 
		// unnecessary paths...
		if (t.id != "") node += "#" + t.id;
		else if (t.className != "") node += "." + t.className; // XXX multiple classes? replace(" ", ",");
		x[x.length] = node;
		t = t.parentNode;
	}

	xpath = x.reverse().join(" > ");
	alert(xpath);
	console.log(xpath);

	// maybe we shouldnt override their event handlers? 
	event.preventDefault();

	return false;
});

});

