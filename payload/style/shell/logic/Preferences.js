.pragma library
// The JSON block is also read by scripts/preferences.py. Keep it strict JSON.
// schema begin
var schema = {
  "version": 1,
  "fields": {
    "fontScale": {"type":"number","default":1,"min":0.9,"max":1.2},
    "reduceMotion": {"type":"boolean","default":false},
    "surfaceOpacity": {"type":"number","default":0.96,"min":0.75,"max":1},
    "barFloating": {"type":"boolean","default":true},
    "barShowDate": {"type":"boolean","default":true},
    "barShowTray": {"type":"boolean","default":true},
    "centerPanels": {"type":"boolean","default":false},
    "osdPosition": {"type":"string","default":"bottom","enum":["bottom","top"]},
    "terminal": {"type":"string","default":"kitty","enum":["kitty","alacritty","foot"]},
    "fileManager": {"type":"string","default":"org.kde.dolphin.desktop","pattern":"^[A-Za-z0-9][A-Za-z0-9_.-]*\\.desktop$"}
  }
};
// schema end
function defaults() {
    var result={};Object.keys(schema.fields).forEach(key=>result[key]=schema.fields[key].default);return result;
}
function validate(values) {
    if(!values || typeof values!=="object" || Array.isArray(values))return "Expected a preference object";
    var keys=Object.keys(values);
    if(keys.length!==Object.keys(schema.fields).length)return "Preference fields are missing or unknown";
    for(var i=0;i<keys.length;i++) {
        var key=keys[i],rule=schema.fields[key],value=values[key];
        if(!Object.prototype.hasOwnProperty.call(schema.fields,key) || typeof value!==rule.type)return "Invalid preference: "+key;
        if(rule.type==="number" && (!Number.isFinite(value) || value<rule.min || value>rule.max))return "Out of range: "+key;
        if(rule.enum && rule.enum.indexOf(value)<0)return "Unsupported preference: "+key;
        if(rule.pattern && (/[\r\n]/.test(value) || value.length>180 || !(new RegExp(rule.pattern)).test(value)))return "Invalid application ID";
    }
    return "";
}
