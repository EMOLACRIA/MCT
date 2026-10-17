import QtQuick
Item {
    id:root
    objectName:"demoContext"
    visible:false
    property var hardware:({cpuName:"Intel Core Ultra · Processor",cpuUsage:18.4,cpuTemp:54,memoryUsed:11.2,memoryTotal:32,memoryPercent:35,diskUsed:284,diskTotal:953,diskPercent:30,uptime:4.2,temperatures:[{name:"coretemp · Package",value:54,unit:"°C"},{name:"coretemp · Core 0",value:48,unit:"°C"},{name:"nvme · Composite",value:39,unit:"°C"}],fans:[{name:"CPU fan",value:1800,unit:"RPM"}],gpus:[{name:"NVIDIA GeForce RTX",state:"Sleeping"},{name:"Intel Graphics",state:"Active · 8% load"}],error:""})
    property bool previewMode:true
    property string clock:"17:55"
    property string date:"WEDNESDAY · 14 OCTOBER"
    property string focusedScreenName:"preview"
    property string activeWindowId:"0x101"
    property var windows:[
        {id:"0x101",title:"Terminal",appName:"Kitty",icon:"",workspaceLabel:"4",monitor:"eDP-1",focusOrder:0},
        {id:"0x102",title:"Project files",appName:"Dolphin",icon:"",workspaceLabel:"9",monitor:"eDP-1",focusOrder:1},
        {id:"0x103",title:"Documentation",appName:"Browser",icon:"",workspaceLabel:"2",monitor:"DP-1",focusOrder:2},
        {id:"0x104",title:"Music library",appName:"Spotify",icon:"",workspaceLabel:"10",monitor:"eDP-1",focusOrder:3}]
    function activateWindow(id) {if(windows.some(w=>w.id===id)) {lastAction="Preview · Focus "+id;activeWindowId=id;}}
    property var workspaces:[{id:1,count:2,active:false},{id:2,count:1,active:false},{id:3,count:0,active:false},{id:4,count:3,active:true},{id:5,count:0,active:false},{id:6,count:0,active:false},{id:7,count:0,active:false},{id:8,count:0,active:false},{id:9,count:1,active:false},{id:10,count:0,active:false}]
    property var applications:[{id:"kitty",name:"Kitty",comment:"Terminal emulator",icon:""},{id:"dolphin",name:"Dolphin",comment:"File manager",icon:""},{id:"zen",name:"Zen Browser",comment:"Browse the web",icon:""},{id:"godot",name:"Godot",comment:"Game engine",icon:""},{id:"blender",name:"Blender",comment:"3D modelling",icon:""},{id:"code",name:"Visual Studio Code",comment:"Code editor",icon:""},{id:"spotify",name:"Spotify",comment:"Music",icon:""}]
    property var trayItems:[]
    property int volume:48
    property bool muted:false
    property bool audioAvailable:true
    property bool microphoneAvailable:true
    property bool microphoneMuted:true
    property int brightness:62
    property var audioDevices:[{id:1,name:"Built-in speakers",selected:true},{id:2,name:"Headphones",selected:false}]
    property bool batteryCharging:true
    property bool batteryFull:false
    property int battery:78
    property string batteryText:"Battery · 78%"
    property string powerText:"Charging"
    property string network:"Home Wi-Fi · Connected"
    property bool networkSettingsAvailable:true
    property string lastError:""
    property bool doNotDisturb:false
    property int unread:2
    property var history:[{key:"1",app:"Calendar",title:"Afternoon plans",body:"Your next event starts in 15 minutes.",time:"17:40",actions:[]},{key:"2",app:"Files",title:"Transfer complete",body:"All files were copied successfully.",time:"17:32",actions:[]},{key:"3",app:"System",title:"Headphones connected",body:"Audio output is ready.",time:"17:20",actions:[]}]
    property var toasts:[]
    property string mediaTitle:"A Quiet Evening"
    property string mediaArtist:"Local music library"
    property string mediaArt:""
    property bool mediaPlaying:true
    property bool canPrevious:true
    property bool canNext:true
    property bool canPlayPause:true
    property var players:[{id:"sample",name:"Music",selected:true}]
    property string lastAction:""
    signal feedbackRequested(string kind,int level,bool muted)
    function workspaceActive(id,screen) { return workspaces.some(w=>w.id===id && w.active); }
    function activateWorkspace(id) { workspaces=workspaces.map(w=>({id:w.id,count:w.count,active:w.id===id})); }
    function launchApplication(id) { lastAction="Preview · Open " + id; }
    function trayClick() {}
    function trayScroll() {}
    function setVolume(v) { volume=v;feedbackRequested("volume",v,muted); }
    function setMicrophoneVolume(v) {feedbackRequested("microphone",v,microphoneMuted);}
    function toggleMute() { muted=!muted;feedbackRequested("volume",volume,muted); }
    function toggleMicrophone() { microphoneMuted=!microphoneMuted;feedbackRequested("microphone",100,microphoneMuted); }
    function setBrightness(v) { brightness=v;feedbackRequested("brightness",v,false); }
    function selectAudio(id) { audioDevices=audioDevices.map(d=>({id:d.id,name:d.name,selected:d.id===id})); }
    function openNetworkSettings() { lastAction="Preview · Network settings"; }
    function markRead() { unread=0; }
    function toggleDnd() { doNotDisturb=!doNotDisturb; }
    function clearHistory() { history=[];unread=0; }
    function dismissHistory(key) { history=history.filter(n=>n.key!==key); }
    function notificationAction() {}
    function dismissToast() { toasts=[]; }
    function sessionAction(code) { lastAction="Preview · " + code + " selected"; }
    function mediaCommand(code) { if(code==="toggle")mediaPlaying=!mediaPlaying;else lastAction="Preview · " + code + " track"; }
    function selectPlayer() {}
}
