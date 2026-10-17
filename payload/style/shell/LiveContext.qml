import QtQuick
import Quickshell
import Quickshell.Io
import Quickshell.Hyprland
import Quickshell.Services.Pipewire
import Quickshell.Services.Mpris
import Quickshell.Services.UPower
import Quickshell.Services.SystemTray
import Quickshell.Services.Notifications
import "ui"

Scope {
    id:root
    property bool hardwareMonitoring:false
    property var hardware:({})
    onHardwareMonitoringChanged:if(hardwareMonitoring && !hardwareProcess.running)hardwareProcess.running=true
    Process {
        id:hardwareProcess
        command:["python3",Quickshell.shellPath("hardware.py")]
        stdout:StdioCollector { onStreamFinished: {try {root.hardware=JSON.parse(text);} catch(e) {console.warn("Hardware read failed: "+e);} } }
    }
    Timer {interval:2000;running:root.hardwareMonitoring;repeat:true;onTriggered:if(!hardwareProcess.running)hardwareProcess.running=true}
    property bool previewMode:false
    property bool ready:false
    property date now:new Date()
    readonly property string clock:Qt.formatDateTime(now,"HH:mm")
    readonly property string date:Qt.formatDateTime(now,"dddd · dd MMMM").toUpperCase()
    readonly property string focusedScreenName:Hyprland.focusedMonitor ? Hyprland.focusedMonitor.name : ""
    readonly property var workspaces: Array.from({length:10},(_,i)=>{
        const w=Hyprland.workspaces.values.find(w=>w.id===i+1);
        return {id:i+1,count:w ? w.toplevels.values.length : 0,active:w ? w.active : false,monitor:w && w.monitor ? w.monitor.name : ""};
    })
    readonly property var applications:DesktopEntries.applications.values.map(e=>({id:e.id,name:e.name,comment:e.genericName || e.comment || "",icon:e.icon ? Quickshell.iconPath(e.icon,true) : ""})).sort((a,b)=>a.name.localeCompare(b.name))
    readonly property var trayItems:SystemTray.items.values.map(i=>({icon:i.icon,title:i.tooltipTitle || i.title || i.id}))
    readonly property var sink:Pipewire.defaultAudioSink
    readonly property var microphone:Pipewire.defaultAudioSource
    readonly property bool audioAvailable:!!(sink && sink.ready && sink.audio)
    readonly property bool microphoneAvailable:!!(microphone && microphone.ready && microphone.audio)
    readonly property int volume:audioAvailable ? Math.round(sink.audio.volume*100) : 0
    readonly property bool muted:audioAvailable ? sink.audio.muted : false
    readonly property bool microphoneMuted:microphoneAvailable ? microphone.audio.muted : false
    readonly property var audioDevices:Pipewire.nodes.values.filter(n=>!n.isStream && n.isSink && n.audio).map(n=>({id:n.id,name:n.description || n.nickname || n.name,selected:!!sink && n.id===sink.id}))
    property var extra:({brightness:-1,network:"Offline",networkSettingsAvailable:false})
    readonly property int brightness:extra.brightness
    readonly property string network:extra.network
    readonly property bool networkSettingsAvailable:extra.networkSettingsAvailable
    readonly property int battery:UPower.displayDevice.ready && UPower.displayDevice.isLaptopBattery ? Math.round(UPower.displayDevice.percentage*100) : -1
    readonly property bool batteryCharging:UPower.displayDevice.ready && UPower.displayDevice.state===UPowerDeviceState.Charging
    readonly property bool batteryFull:UPower.displayDevice.ready && UPower.displayDevice.state===UPowerDeviceState.FullyCharged
    readonly property string batteryText:battery>=0 ? "Battery · " + battery + "%" : "Battery unavailable"
    readonly property string powerText:batteryCharging ? "Charging" : batteryFull ? "Fully charged · plugged in" : UPower.onBattery ? "On battery" : "Plugged in · not charging"
    property string lastError:""
    property string selectedPlayer:""
    readonly property var player:Mpris.players.values.find(p=>p.dbusName===selectedPlayer) || Mpris.players.values.find(p=>p.isPlaying) || Mpris.players.values[0] || null
    readonly property string mediaTitle:player ? player.trackTitle || player.identity : ""
    readonly property string mediaArtist:player ? player.trackArtist : ""
    readonly property string mediaArt:player ? player.trackArtUrl : ""
    readonly property bool mediaPlaying:!!player && player.isPlaying
    readonly property bool canPrevious:!!player && player.canGoPrevious
    readonly property bool canNext:!!player && player.canGoNext
    readonly property bool canPlayPause:!!player && player.canTogglePlaying
    readonly property var players:Mpris.players.values.map(p=>({id:p.dbusName,name:p.identity,selected:!!player && p.dbusName===player.dbusName}))
    property bool doNotDisturb:false
    property int unread:0
    property var history:[]
    property var toasts:[]
    property var liveNotifications:({})
    property var notificationGenerations:({})
    property var notificationTimers:({})
    property var toastTimers:({})
    property bool historyLoaded:false
    signal feedbackRequested(string kind,int level,bool muted)

    Timer { interval:1000; running:true; repeat:true; onTriggered:root.now=new Date() }
    PwObjectTracker { objects:Pipewire.nodes.values.filter(n=>!n.isStream && n.audio) }
    Process {
        id:statusProcess
        command:["python3",Quickshell.shellPath("status.py")]
        stdout:StdioCollector { onStreamFinished: {try {root.extra=JSON.parse(text);} catch(e) {console.warn("Status read failed: " + e);} } }
        Component.onCompleted:running=true
    }
    Timer { interval:2000; running:true; repeat:true; onTriggered:if(!statusProcess.running)statusProcess.running=true }
    FileView {
        id:historyFile
        path:Quickshell.env("HOME")+"/.local/state/desktop-style/notifications.json"
        blockLoading:true; printErrors:false; atomicWrites:true
        onSaveFailed:root.lastError="Notification history could not be saved."
    }
    Timer { id:saveTimer; interval:200; onTriggered:historyFile.setText(JSON.stringify({version:1,dnd:root.doNotDisturb,unread:root.unread,history:root.history.slice(0,100)})) }
    Component {
        id:expiry
        Timer { required property string notificationKey; required property int generation; onTriggered: {if(root.notificationGenerations[notificationKey]===generation) {delete root.notificationTimers[notificationKey];root.expireNotification(notificationKey);}destroy();} }
    }
    Component {
        id:toastExpiry
        Timer { required property string notificationKey; required property int generation; interval:4500; onTriggered: {if(root.notificationGenerations[notificationKey]===generation) {delete root.toastTimers[notificationKey];root.toasts=root.toasts.filter(n=>n.key!==notificationKey);}destroy();} }
    }
    Component {
        id:notificationWatcher
        NotificationWatcher { onUpdated:root.receive(notification) }
    }
    NotificationServer {
        id:server
        bodySupported:true; actionsSupported:true; imageSupported:false
        persistenceSupported:true; bodyMarkupSupported:false; keepOnReload:true
        onNotification:n=>root.receive(n)
    }
    function restoreHistory() {
        if(historyLoaded)return;
        historyLoaded=true;
        try {
            const saved=JSON.parse(historyFile.text() || "{}");
            doNotDisturb=!!saved.dnd;
            const stored=Array.isArray(saved.history) ? saved.history.filter(n=>n && typeof n.key==="string" && typeof n.title==="string").slice(0,100).map(n=>({key:n.key,sourceId:n.sourceId,app:String(n.app || "Notification").slice(0,200),title:n.title.slice(0,300),body:String(n.body || "").slice(0,2000),time:String(n.time || ""),actions:[]})) : [];
            history=history.concat(stored).slice(0,100);unread=Math.max(0,Math.min(history.length,Number(saved.unread)||0));
        } catch(e) { console.warn("Notification history read failed: " + e); }
    }
    function persist() { if(historyLoaded)saveTimer.restart(); }
    function workspaceActive(id,screen) { return workspaces.some(w=>w.id===id && w.active && (!screen || w.monitor===screen)); }
    function activateWorkspace(id) {
        if(id<1 || id>10)return;
        Hyprland.dispatch(Hyprland.usingLua ? "hl.dsp.focus({workspace="+id+"})" : "workspace "+id);
    }
    function launchApplication(id) {
        const entry=DesktopEntries.byId(id);if(!entry)return;
        if(entry.runInTerminal)Quickshell.execDetached({command:["kitty","--"].concat(Array.from(entry.command)),workingDirectory:entry.workingDirectory || Quickshell.env("HOME")});
        else entry.execute();
    }
    function trayClick(index,button,window,x,y) {
        const item=SystemTray.items.values[index];if(!item)return;
        if((button===Qt.RightButton || item.onlyMenu) && item.hasMenu && window)item.display(window,x,y);
        else if(button===Qt.MiddleButton)item.secondaryActivate();else if(button===Qt.LeftButton)item.activate();
    }
    function trayScroll(index,delta) { const item=SystemTray.items.values[index];if(item)item.scroll(delta,false); }
    function setVolume(value) {
        if(!audioAvailable)return;
        sink.audio.volume=Math.max(0,Math.min(100,value))/100;
        Qt.callLater(()=>root.feedbackRequested("volume",root.volume,root.muted));
    }
    function setMicrophoneVolume(value) {if(microphoneAvailable) {microphone.audio.volume=Math.max(0,Math.min(100,value))/100;Qt.callLater(()=>root.feedbackRequested("microphone",Math.round(root.microphone.audio.volume*100),root.microphoneMuted));}}
    function toggleMute() { if(audioAvailable) {sink.audio.muted=!sink.audio.muted;Qt.callLater(()=>root.feedbackRequested("volume",root.volume,root.muted));} }
    function toggleMicrophone() { if(microphoneAvailable) {microphone.audio.muted=!microphone.audio.muted;Qt.callLater(()=>root.feedbackRequested("microphone",Math.round(root.microphone.audio.volume*100),root.microphoneMuted));} }
    function selectAudio(id) { const node=Pipewire.nodes.values.find(n=>n.id===id && !n.isStream && n.isSink && n.audio);if(node)Pipewire.preferredDefaultAudioSink=node; }
    function runAction(kind,value) { lastError="";Quickshell.execDetached(["python3",Quickshell.shellPath("actions.py"),kind,String(value===undefined || value===null ? "" : value)]); }
    function setBrightness(value) { runAction("brightness",Math.round(value)); }
    function openNetworkSettings() { if(networkSettingsAvailable)runAction("network",""); }
    function sessionAction(code) { if(["lock","suspend","logout","restart","poweroff"].indexOf(code)>=0)runAction("session",code); }
    function selectPlayer(id) { selectedPlayer=id; }
    function mediaCommand(code) { if(!player)return;if(code==="toggle" && canPlayPause)player.togglePlaying();else if(code==="previous" && canPrevious)player.previous();else if(code==="next" && canNext)player.next(); }
    function stopNotificationTimer(timers,key) {
        const timer=timers[key];delete timers[key];
        if(timer) {timer.stop();timer.destroy();}
    }
    function notificationTimeout(value) {
        // QuickShell 0.3.1 forwards the D-Bus millisecond value unchanged.
        const timeout=Number(value);
        if(!Number.isFinite(timeout) || timeout<0)return 4500;
        return Math.min(2147483647,Math.max(0,Math.round(timeout)));
    }
    function receive(n) {
        restoreHistory();n.tracked=true;
        let oldKey=Object.keys(liveNotifications).find(k=>liveNotifications[k] && liveNotifications[k].id===n.id);
        const firstTracking=oldKey===undefined;
        if(!oldKey && n.lastGeneration) {const old=history.find(h=>h.sourceId===n.id);if(old)oldKey=old.key;}
        const key=oldKey || String(Date.now())+":"+n.id;
        const generation=(notificationGenerations[key] || 0)+1;notificationGenerations[key]=generation;
        stopNotificationTimer(notificationTimers,key);stopNotificationTimer(toastTimers,key);
        liveNotifications[key]=n;
        const note={key:key,sourceId:n.id,app:String(n.appName || "Notification").slice(0,200),title:String(n.summary || "").slice(0,300),body:String(n.body || "").replace(/<[^>]*>/g,"").slice(0,2000),time:Qt.formatDateTime(new Date(),"HH:mm"),actions:n.actions.map(a=>({id:a.identifier,text:a.text}))};
        if(!n.transient) {history=[note].concat(history.filter(h=>h.key!==key)).slice(0,100);if(firstTracking && !n.lastGeneration)unread=Math.min(100,unread+1);persist();}
        else if(history.some(h=>h.key===key)) {history=history.filter(h=>h.key!==key);unread=Math.min(unread,history.length);persist();}
        if(!doNotDisturb && !n.lastGeneration) {toasts=[note].concat(toasts.filter(t=>t.key!==key)).slice(0,3);const timer=toastExpiry.createObject(root,{notificationKey:key,generation:generation});toastTimers[key]=timer;timer.start();}
        if(firstTracking) {
            notificationWatcher.createObject(root,{notification:n});
            n.closed.connect(()=>{
                if(liveNotifications[key]!==n)return;
                stopNotificationTimer(notificationTimers,key);stopNotificationTimer(toastTimers,key);
                delete notificationGenerations[key];
                delete liveNotifications[key];toasts=toasts.filter(t=>t.key!==key);
                history=history.map(h=>h.key===key ? {key:h.key,sourceId:h.sourceId,app:h.app,title:h.title,body:h.body,time:h.time,actions:[]} : h);persist();
            });
        }
        const timeout=notificationTimeout(n.expireTimeout);
        if(timeout!==0) {const timer=expiry.createObject(root,{notificationKey:key,generation:generation,interval:timeout});notificationTimers[key]=timer;timer.start();}
    }
    function expireNotification(key) {const n=liveNotifications[key];if(n)n.expire();}
    function markRead() {unread=0;persist();}
    function toggleDnd() {doNotDisturb=!doNotDisturb;if(doNotDisturb)toasts=[];persist();}
    function dismissToast(key) { const n=liveNotifications[key];if(n)n.dismiss();toasts=toasts.filter(t=>t.key!==key); }
    function dismissHistory(key) {dismissToast(key);history=history.filter(h=>h.key!==key);unread=Math.min(unread,history.length);persist();}
    function clearHistory() {Object.keys(liveNotifications).forEach(k=>{const n=liveNotifications[k];if(n)n.dismiss();});history=[];toasts=[];unread=0;persist();}
    function notificationAction(key,id) {const n=liveNotifications[key];if(!n)return;const action=n.actions.find(a=>a.identifier===id);if(action)action.invoke();}
    Component.onCompleted: {restoreHistory();ready=true;}
}
