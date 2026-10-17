import QtQuick
import "../logic/Preferences.js" as Preferences
Item {
    id:root;visible:false;objectName:"preferencesState"
    property var values:Preferences.defaults()
    property bool ephemeral:false
    property bool ready:true
    property bool saving:false
    property bool sourceValid:true
    property string error:""
    property string notice:""
    property string path:"Preview · memory only"
    property string diagnostics:""
    property var terminals:[{id:"kitty",name:"Kitty",available:true},{id:"alacritty",name:"Alacritty",available:true},{id:"foot",name:"Foot",available:true}]
    signal writeRequested(string action,var candidate)
    function fail(message) {saving=false;ready=true;error=message;notice="";}
    function request(key,value) {
        if(!ready || saving)return;
        if(!sourceValid) {fail("Reset unreadable preferences first; the original file will be retained.");return;}
        if(!Object.prototype.hasOwnProperty.call(Preferences.schema.fields,key)) {fail("Unknown preference");return;}
        const next=Object.assign({},values);next[key]=value;
        const problem=Preferences.validate(next);if(problem) {fail(problem);return;}
        saving=true;error="";notice="";writeRequested("save",next);
    }
    function reset() {if(!saving) {saving=true;error="";writeRequested("reset",Preferences.defaults());}}
    function accept(packet) {
        saving=false;ready=true;
        if(packet.path)path=packet.path;
        if(packet.terminals)terminals=packet.terminals;
        if(packet.sourceValid!==undefined)sourceValid=packet.sourceValid;
        if(packet.values && (packet.ok || packet.action==="read")) {
            const problem=Preferences.validate(packet.values);if(problem) {fail(problem);return;}
            values=packet.values;
        }
        error=packet.error || "";
        if(packet.diagnostics)diagnostics=packet.diagnostics;
        notice=packet.ok && packet.action==="save" ? (ephemeral ? "Preview updated" : "Saved") : packet.ok && packet.action==="reset" ? (ephemeral ? "Preview defaults restored" : "Defaults restored"+(packet.backup ? " · previous file retained" : "")) : "";
    }
}
