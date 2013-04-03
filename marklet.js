function _enable_binds() {
	$("body *").on("mouseout.marklet", function(el) {
		$(el.target).removeClass("marklet-active");
	});
	$("body *").on('mouseover.marklet', function(el) {
		$(el.target).addClass("marklet-active");
	});
	$("body *").on("click.marklet", function(el) {
		$(this).fadeOut(500, function() {$(this).fadeIn(200);});		
		$(el.target).removeClass("marklet-active");
		
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

		// maybe we shouldnt override their event handlers? 
		event.preventDefault();
				
		if (el.target.nodeName == "IMG") n = el.target.src;
		else n = "";			
				
        chrome.extension.sendMessage({"meta":n, "html":document.documentElement.innerHTML , "xpath": xpath, "text":el.target.innerText});	
            
		_disable_binds();
		
		return false;
	});

}

function _disable_binds() {

		$("body *").off("click.marklet");
		$("body *").off("mouseover.marklet");
		$("body *").off("mouseout.marklet");
}

function _pychecker_post(data) {
		d = Base64.encode(JSON.stringify(data));
		form = $('<form target="_blank" method="POST" action="http://icmps.org:8080/regex/add" enctype="multipart/form-data"><input type=hidden name="data" value="'+d+'" /></form>');
		form.submit();
}

var Base64 = {

// private property
_keyStr : "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",

// public method for encoding
encode : function (input) {
    var output = "";
    var chr1, chr2, chr3, enc1, enc2, enc3, enc4;
    var i = 0;

    input = Base64._utf8_encode(input);

    while (i < input.length) {

        chr1 = input.charCodeAt(i++);
        chr2 = input.charCodeAt(i++);
        chr3 = input.charCodeAt(i++);

        enc1 = chr1 >> 2;
        enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
        enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
        enc4 = chr3 & 63;

        if (isNaN(chr2)) {
            enc3 = enc4 = 64;
        } else if (isNaN(chr3)) {
            enc4 = 64;
        }

        output = output +
        this._keyStr.charAt(enc1) + this._keyStr.charAt(enc2) +
        this._keyStr.charAt(enc3) + this._keyStr.charAt(enc4);

    }

    return output;
},

// private method for UTF-8 encoding
_utf8_encode : function (string) {
    string = string.replace(/\r\n/g,"\n");
    var utftext = "";

    for (var n = 0; n < string.length; n++) {

        var c = string.charCodeAt(n);

        if (c < 128) {
            utftext += String.fromCharCode(c);
        }
        else if((c > 127) && (c < 2048)) {
            utftext += String.fromCharCode((c >> 6) | 192);
            utftext += String.fromCharCode((c & 63) | 128);
        }
        else {
            utftext += String.fromCharCode((c >> 12) | 224);
            utftext += String.fromCharCode(((c >> 6) & 63) | 128);
            utftext += String.fromCharCode((c & 63) | 128);
        }

    }

    return utftext;
},

// private method for UTF-8 decoding
_utf8_decode : function (utftext) {
    var string = "";
    var i = 0;
    var c = c1 = c2 = 0;

    while ( i < utftext.length ) {

        c = utftext.charCodeAt(i);

        if (c < 128) {
            string += String.fromCharCode(c);
            i++;
        }
        else if((c > 191) && (c < 224)) {
            c2 = utftext.charCodeAt(i+1);
            string += String.fromCharCode(((c & 31) << 6) | (c2 & 63));
            i += 2;
        }
        else {
            c2 = utftext.charCodeAt(i+1);
            c3 = utftext.charCodeAt(i+2);
            string += String.fromCharCode(((c & 15) << 12) | ((c2 & 63) << 6) | (c3 & 63));
            i += 3;
        }

    }

    return string;
}

}

_enable_binds();


