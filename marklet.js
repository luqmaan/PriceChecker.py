// javascript:c=document.createElement('script');c.type='text/javascript';c.src='file://localhost/Users/lolcat/dev/PriceChecker.py/marklet.js?ts='+new Date().getTime();document.getElementsByTagName('HEAD')[0].appendChild(c);

// prevent duplicate loads

// getXPath

// display simple floating UI with data
$("body *").on("mouseover", function(el) {
	$(el.target).addClass("marklet-active");
});
$("body *").on("mouseout", function(el) {
	$(el.target).removeClass("marklet-active");
});

$("body *").on('click', function(el) {
	var x = [],
		t = el.target;

	while (t !== undefined && t.nodeName !== "HTML") {
		var node = t.nodeName;
		// XXX as soon as we find a node with an id or class, we can probably break to save 
		// unnecessary paths...
		if (t.id !== "") {
			node += "#" + t.id;
		} else if (t.className !== "") {
			node += "." + t.className; // XXX multiple classes? replace(" ", ",");	
		}
		x[x.length] = node;
		t = t.parentNode;
	}

	var xpath = x.reverse().join(" > ");
	console.log(xpath);

	// maybe we shouldnt override their event handlers? 
	event.preventDefault();

	return false;
});


// });