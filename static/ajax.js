function log(message) {
    console.log.apply(console, message);
}

function elem(selector) {
    return document.querySelector(selector);
}

function ajax(method, url, data, callback) {

    var request = new XMLHttpRequest();
    request.open(method, url);
    request.setRequestHeader('Content-Type', 'application/json');
    request.onreadystatechange = function () {
        if (request.readyState === 4) {
            callback(r.response);
        }
    }
    data = JSON.stringify(data);
    request.send(data);
}

function ajaxGet(url, callback) {
    ajax('GET', url, '', callback);
}

function ajaxPost(url, data, callback) {
    ajax('POST', url, data, callback);
}
