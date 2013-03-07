(function($) {

	// display simple floating UI with data
	$("body *").on("mouseover.marklet", function(el) {
		$(el.target).addClass("marklet-active");
	});
	$("body *").on("mouseout.marklet", function(el) {
		$(el.target).removeClass("marklet-active");
	});

	$("body *").on('click.marklet', function(el) {

		$(this).fadeOut(500, function() {$(this).fadeIn(200);});
		$(this).removeClass("marklet-active");

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

		$("body *").off("click.marklet");
		$("body *").off("mouseover.marklet");
		$("body *").off("mouseout.marklet");

		return false;
	});


})(jQuery);