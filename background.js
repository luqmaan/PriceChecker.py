function loadFiles(i, files, tab) {
    setTimeout(function() {
        if (i === files.length)
            return;

        var fname = files[i];
        var typeregex = /\.([0-9a-z]+)(?:[\?#]|$)/i;
        var ftype = fname.match(typeregex);

//        console.log(Date.now() + " " + fname);

        switch (ftype[1]) {
        case "css":
            chrome.tabs.insertCSS(tab.id, {
                file: fname
            }, loadFiles(i+1, files, tab));
            break;
        case "js":
            chrome.tabs.executeScript(tab.id, {
                file: fname
            }, loadFiles(i+1, files, tab));
            break;
        default:
            console.error("Unexpected file extension: " + ftype);
            break;
        }
    }, 300);
}

function inject(tab) {
    var files = ["jquery.min.js", "marklet.css",  "jquery.xpath.min.js", "marklet.js"];
    loadFiles(0, files, tab);
}

var data = {};

// XXX also check for any kind of feed declaration on the page and save it

chrome.browserAction.onClicked.addListener(function(tab) {
	data.tab = tab;
	
	chrome.tabs.captureVisibleTab(tab.windowid, {}, function(img) {
		data.ss = img;
		inject(tab);			
	});
});

chrome.extension.onMessage.addListener(function(request, sender) {

        data.request = request;
		
		//minify function
		fakePostCode = fakePost.toString().replace(/(\n|\t)/gm,'');
		chrome.tabs.create({"url" : "javascript:"+fakePostCode+"; fakePost('"+Base64.encode(JSON.stringify(data))+"');"});
		
		//chrome.tabs.create({url:"http://icmps.org:8080/regex/add/?data="+c});		
		return;
		
		c = "_pychecker_post("+JSON.stringify(data)+")";				
		chrome.tabs.executeScript(data.tab.id, {code:c});
		
});

function fakePost(d) {   
    var form = document.createElement("form");
    form.setAttribute("method", "post");
    form.setAttribute("action", "http://icmps.org:8080/regex/add");    
	form.setAttribute("enctype", "multipart/form-data");
    var hiddenField = document.createElement("input");
    hiddenField.setAttribute("type", "hidden");
    hiddenField.setAttribute("name", "data");
    hiddenField.setAttribute("value", d );
    form.appendChild(hiddenField);
    document.body.appendChild(form);
    form.submit();
};

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
