function loadFiles(i, files, tab) {
    setTimeout(function() {
        if (i === files.length)
            return;

        var fname = files[i];
        var typeregex = /\.([0-9a-z]+)(?:[\?#]|$)/i;
        var ftype = fname.match(typeregex);

        console.log(Date.now() + " " + fname);

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

// Called when the user clicks on the extension icon.
chrome.browserAction.onClicked.addListener(function(tab) {

    var files = ["jquery.min.js", "marklet.css",  "jquery.xpath.min.js", "marklet.js"];

    loadFiles(0, files, tab);

});

