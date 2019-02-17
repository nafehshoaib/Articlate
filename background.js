var API_KEY = ''

// chrome.runtime.onInstalled.addListener(function() {

// });

// http makes an HTTP request and calls callback with parsed JSON.
var http = function (method, url, body, cb) {
    var xhr = new XMLHttpRequest();
    xhr.open(method, url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
      if (xhr.readyState !== 4) { return; }
      if (xhr.status >= 400) {
        notify('API request failed');
        console.log('XHR failed', xhr.responseText);
        return;
      }
      cb(JSON.parse(xhr.responseText));
    };
    xhr.send(body);
};

http('GET', chrome.runtime.getURL('config.json'), '', function (obj) {
    API_KEY = obj.key;
    document.dispatchEvent(new Event('config-loaded'));
});

// detect makes a NLP API request with the API key.
var articlate = function (type, article, cb) {
    var url = 'https://language.googleapis.com/v1/documents:analyzeEntities?key=' + API_KEY;
    var data = {
      "document": {
          article
      },
      encodingType: type
    };
    http('POST', url, JSON.stringify(data), cb);
};

chrome.contextMenus.create({
    id: "articlate-article-link",
    title: 'Articlate Article',
    contexts: ['link'],
    onclick: function (link) {
        displayPopup()
        // articlate('UTF16', link, function (data) {
        //     var entities = data.responses;
        //     displayPopup(entities);
        // });
    }
});

var createWordle = function(entitities, cb) {
    cb(generateWordleImage(entitities));
}

var displayPopup = function () {
    newWindow = window.open("/wordletest.html", null, "toolbar=no,menubar=no,location=no");
    //newWindow.document.write("<img src='" + wordle + "'/>");
}