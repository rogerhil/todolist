function get_query_string() {
    var splited = window.location.href.split('?');
    if (splited.length == 1) {
        return;
    }
    return splited[1].split('#')[0];

}

function get_query_string_params() {
	var qs = get_query_string();
    if (!qs) {
        return {};
    }
	var strparams = qs.split('&');
	var params = {};
	for (var k = 0; k < strparams.length; k++) {
		var sp = strparams[k].split('=');
		params[sp[0]] = unescape(sp[1]).replace(/\+/g,' ');
	}
	return params;
}
