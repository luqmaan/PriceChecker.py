
// Called when the user clicks on the browser action.
chrome.browserAction.onClicked.addListener(function(tab) {
    console.log(tab);
    console.log("clickedweofijewoifj");
    chrome.tabs.executeScript(tab.id, {
        file: "jquery.min.js"
    }, function() {
        chrome.tabs.insertCSS(tab.id, {
            file: "marklet.css"
        }, function() {
            chrome.tabs.executeScript(tab.id, {
                file: "marklet.js"
            });
        });
    });
});