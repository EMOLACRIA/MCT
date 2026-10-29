import QtQuick
// Draft of the theme settings (shared layout + the active theme's overrides).
// Nothing reaches the desktop until apply(); applying is a normal theme switch.
Item {
    id:root;visible:false;objectName:"themeConfigState"
    readonly property var roles:["accent","surface","raised","selection","text","secondary","line","warning"]
    readonly property var roleLabels:({accent:"Accent",surface:"Surface",raised:"Raised",selection:"Selection",text:"Text",secondary:"Secondary",line:"Line",warning:"Warning"})
    readonly property var alphaRoles:["surface","raised","line","selection"]
    readonly property int quoteMax:18
    property bool ephemeral:false
    property bool ready:false
    property bool busy:false
    property string error:""
    property string notice:""
    property string path:""
    property var config:empty()
    property var draft:empty()
    property var active:null
    property var defaults:null
    property bool lockQuote:false
    property var applied:null
    property var lastApply:null
    property string wallpaper:""
    property string customWallpaper:""
    property string quoteImagePath:""
    property int wallpaperRevision:0
    signal requested(string action,var args)

    function empty() {return {version:1,layout:{themeOwn:true,gapsIn:5,gapsOut:14,border:2,rounding:8},themes:{}};}
    function clone(value) {return JSON.parse(JSON.stringify(value));}
    readonly property string themeId:active ? active.id : ""
    readonly property var entry:themeId!=="" && draft.themes[themeId] ? draft.themes[themeId] : ({})
    readonly property var savedEntry:themeId!=="" && config.themes[themeId] ? config.themes[themeId] : ({})
    readonly property bool dirty:JSON.stringify(strip(draft))!==JSON.stringify(strip(config))
    readonly property bool canApply:ready && !busy && active!==null && quoteProblem==="" && (dirty || applied===false)
    readonly property int changeCount:{
        let n=entry.colors ? Object.keys(entry.colors).length : 0;
        if(entry.quote)n++;
        if(entry.wallpaper && (entry.wallpaper.desktop || entry.wallpaper.lock))n++;
        if(!draft.layout.themeOwn)n++;
        return n;
    }
    readonly property var quoteLines:entry.quote ? entry.quote : (defaults ? defaults.quote : [])
    readonly property string quoteProblem:entry.quote ? checkQuote(entry.quote) : ""

    // quoteImage is bookkeeping written by the helper, not a user choice.
    function strip(value) {const v=clone(value);for(const k in v.themes)delete v.themes[k].quoteImage;return v;}
    function edit(change) {
        if(themeId==="")return;
        const next=clone(draft),current=next.themes[themeId] || {};
        change(current,next);
        for(const key of ["colors"])if(current[key] && Object.keys(current[key]).length===0)delete current[key];
        if(Object.keys(current).length===0 || (Object.keys(current).length===1 && current.quoteImage))delete next.themes[themeId];
        else next.themes[themeId]=current;
        draft=next;notice="";error="";
    }
    function color(role) {
        if(entry.colors && entry.colors[role])return entry.colors[role];
        return defaults && defaults.colors ? defaults.colors[role] : String(Theme.ink);
    }
    function isChanged(role) {return !!(entry.colors && entry.colors[role]);}
    function setColor(role,value) {
        edit(e=> {
            e.colors=e.colors || {};
            if(!value || (defaults && value.toLowerCase()===defaults.colors[role]))delete e.colors[role];
            else e.colors[role]=value.toLowerCase();
        });
    }
    function checkQuote(lines) {
        if(lines.length<1 || lines.length>2)return "Use one or two rows.";
        for(const line of lines) {
            if(line.trim()==="" || line.length>quoteMax)return "Each row needs 1-"+quoteMax+" characters.";
            // The helper re-checks with the exact rule; this catches what Hyprlock/markup would misread.
            if(line!==line.trim() || line.indexOf("  ")>=0 || /[<>&$#\\"`{}\[\]|*_=+^~@%\/\x00-\x1f]/.test(line))return "Use letters, digits, spaces and . , ! ? ' - : ; ( ) only.";
        }
        return "";
    }
    function setQuote(first,second) {
        const lines=[first,second].filter(l=>l!=="");
        const same=defaults && JSON.stringify(lines)===JSON.stringify(defaults.quote);
        edit(e=> {if(same || lines.length===0)delete e.quote;else e.quote=lines;});
    }
    function setWallpaper(desktop,lock) {edit(e=> {if(!desktop && !lock)delete e.wallpaper;else e.wallpaper={desktop:desktop,lock:lock};});}
    function setLayout(key,value) {const next=clone(draft);next.layout[key]=Math.round(value);draft=next;notice="";}
    function setThemeOwn(own) {
        const next=clone(draft);next.layout.themeOwn=own;
        // Start from the active theme's own values the first time the shared layout is used.
        if(!own && config.layout.themeOwn && defaults)for(const key in defaults.layout)next.layout[key]=defaults.layout[key];
        draft=next;notice="";
    }
    function layoutValue(key) {return draft.layout.themeOwn && defaults ? defaults.layout[key] : draft.layout[key];}
    function resetTheme() {edit(e=> {for(const key in e)delete e[key];});}
    function discard() {draft=clone(config);notice="";error="";}
    function reload() {requested("read",[]);}
    function pick() {if(!busy)requested("pick",[]);}
    function importWallpaper(file) {
        if(busy || themeId==="")return;
        const clean=String(file).replace(/^file:\/\//,"").trim();
        if(clean===""){error="Choose or paste an image path.";return;}
        requested("wallpaper",[themeId,clean]);
    }
    function apply(rendered) {
        if(!canApply)return;
        busy=true;error="";notice="";
        requested("apply",[JSON.stringify(draft)].concat(rendered ? ["rendered"] : []));
    }
    function fail(message) {busy=false;ready=true;error=message;notice="";}
    function accept(packet) {
        busy=false;ready=true;
        const keepDraft=packet.action==="wallpaper" || packet.action==="pick";
        const previous=draft;
        if(packet.path!==undefined)path=packet.path;
        if(packet.config)config=packet.config;
        active=packet.active || null;defaults=packet.defaults || null;
        lockQuote=!!packet.lockQuote;applied=packet.applied===undefined ? null : packet.applied;
        lastApply=packet.lastApply || null;
        wallpaper=packet.wallpaper || "";customWallpaper=packet.customWallpaper || "";quoteImagePath=packet.quoteImagePath || "";
        draft=keepDraft ? previous : clone(config);
        error=packet.error || "";
        if(packet.action==="wallpaper" && packet.ok) {wallpaperRevision++;setWallpaper(true,true);notice="Image ready · apply to use it";}
        if(packet.action==="pick" && packet.picked)importWallpaper(packet.picked);
        if(packet.action==="apply" && packet.ok)notice=ephemeral ? "Preview · settings stay in this window" : "Applying · the shell restarts for a moment";
    }
}
