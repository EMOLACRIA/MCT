const fs=require('fs'),assert=require('assert'),path=require('path');
const source=fs.readFileSync(path.resolve(__dirname,'../payload/style/shell/LiveContext.qml'),'utf8');
const funcs=[];const re=/function\s+(\w+)\s*\(([^)]*)\)\s*\{/g;let match;
while((match=re.exec(source))){let i=re.lastIndex,depth=1,quote=null,escaped=false;
 for(;i<source.length&&depth;i++){let c=source[i];if(quote){if(escaped)escaped=false;else if(c==='\\')escaped=true;else if(c===quote)quote=null;}else if(c==='"'||c==="'"||c==='`')quote=c;else if(c==='{')depth++;else if(c==='}')depth--;}
 funcs.push('root.'+match[1]+'=function('+match[2]+'){'+source.slice(re.lastIndex,i-1)+'};');re.lastIndex=i;
}
const events=[],scheduled=[];
global.Qt={formatDateTime:()=> '18:10',callLater:f=>f(),LeftButton:1,RightButton:2,MiddleButton:4};
global.Hyprland={usingLua:true,dispatch:c=>events.push(c)};
global.Pipewire={nodes:{values:[]}};
global.DesktopEntries={byId:()=>null};
global.Quickshell={shellPath:x=>x,env:()=>'/home/fixture',execDetached:x=>events.push(x)};
global.historyFile={text:()=>JSON.stringify({dnd:false,unread:1,history:[{key:'stored',app:'Old',title:'Previous notification',body:'saved',time:'17:00',actions:[{id:'dead',text:'expired action'}]}]})};
global.saveTimer={restart:()=>events.push('persist')};
function timerFactory(r,v){const timer={...v,running:false,destroyed:false,start(){this.running=true;},stop(){this.running=false;},destroy(){this.destroyed=true;}};scheduled.push(timer);return timer;}
global.expiry={createObject:timerFactory};
// Preserve the Timer component default which createObject inherits in real QML.
const toastInterval=Number(source.match(/id:toastExpiry\s+Timer\s*\{[^}]*interval:(\d+)/)[1]);
global.toastExpiry={createObject:(r,v)=>timerFactory(r,{interval:toastInterval,...v})};
const watchers=[];global.notificationWatcher={createObject:(r,v)=>watchers.push(v)};
global.SystemTray={items:{values:[]}};
const root={historyLoaded:false,history:[],unread:0,doNotDisturb:false,toasts:[],liveNotifications:{},notificationGenerations:{},notificationTimers:{},toastTimers:{},workspaces:[{id:9,count:1,active:true,monitor:'eDP-1'}],audioAvailable:true,sink:{audio:{volume:.5,muted:false}},microphoneAvailable:true,microphone:{audio:{volume:.8,muted:false}},feedbackRequested:(...v)=>events.push(v),lastError:'',networkSettingsAvailable:true};
Object.defineProperties(root,{volume:{get:()=>Math.round(root.sink.audio.volume*100)},muted:{get:()=>root.sink.audio.muted},microphoneMuted:{get:()=>root.microphone.audio.muted}});
new Function('root','with(root){'+funcs.join('\n')+'}')(root);
root.copyText('0.333333333333');assert.strictEqual(Quickshell.clipboardText,'0.333333333333');
root.restoreHistory();assert(root.history.length===1&&root.history[0].actions.length===0);
function note(id,opts={}){const callbacks=[];return {id,appName:'Files',summary:'Copy complete',body:'<b>Done</b>',actions:[],tracked:false,transient:false,lastGeneration:false,expireTimeout:5000,callbacks,closed:{connect:f=>callbacks.push(f)},dismiss(){callbacks.forEach(f=>f(1));},expire(){callbacks.forEach(f=>f(2));},...opts};}
const n=note(8);root.receive(n);assert(n.tracked&&root.history.length===2&&root.toasts.length===1&&root.history[0].body==='Done');
const key=root.history[0].key;const generation=root.notificationGenerations[key];
const firstTimer=root.notificationTimers[key],firstToast=root.toastTimers[key],beforeUnread=root.unread;
assert(firstTimer.interval===5000&&firstTimer.running);
assert(firstToast.interval===4500&&firstToast.running);
n.summary='Copy 75%';n.body='Updated';root.receive(n);
assert(root.history.length===2&&root.notificationGenerations[key]===generation+1);
assert(root.history[0].title==='Copy 75%'&&root.toasts[0].body==='Updated');
assert(root.unread===beforeUnread&&n.callbacks.length===1&&watchers.filter(w=>w.notification===n).length===1);
assert(firstTimer.destroyed&&!firstTimer.running&&firstToast.destroyed&&!firstToast.running);
assert(scheduled.find(t=>t.notificationKey===key&&t.generation===generation));
root.toggleDnd();assert(root.toasts.length===0);root.receive(note(9));assert(root.history.length===3&&root.toasts.length===0);
root.toggleDnd();root.receive(note(10,{transient:true}));assert(root.history.length===3&&root.toasts.length===1);
root.markRead();assert(root.unread===0);
let invoked=false;const action={identifier:'open',text:'Open',invoke(){invoked=true;}};const actionable=note(11,{actions:[action]});root.receive(actionable);const actionKey=root.history[0].key;root.notificationAction(actionKey,'open');assert(invoked);
actionable.expire();assert(root.history[0].actions.length===0&&!root.liveNotifications[actionKey]);
assert(!root.notificationTimers[actionKey]&&!root.toastTimers[actionKey]&&!root.notificationGenerations[actionKey]);
root.dismissHistory(key);assert(!root.history.some(h=>h.key===key));root.clearHistory();assert(root.history.length===0&&root.unread===0&&root.toasts.length===0);
root.setVolume(150);assert(root.volume===100);root.toggleMute();assert(root.muted);root.toggleMicrophone();assert(root.microphoneMuted);
root.activateWorkspace(9);assert(events.includes('hl.dsp.focus({workspace=9})'));
root.setBrightness(0);assert(events.some(e=>Array.isArray(e)&&e[2]==='brightness'&&e[3]==='0'));
root.sessionAction('bad');assert(!events.some(e=>Array.isArray(e)&&e.includes('bad')));
for(const [id,timeout,expected] of [[20,-1,4500],[21,120,120],[22,0,0]]) {
 const message=note(id,{expireTimeout:timeout});root.receive(message);
 const k=Object.keys(root.liveNotifications).find(k=>root.liveNotifications[k]===message);
 if(expected===0)assert(!root.notificationTimers[k]);else assert(root.notificationTimers[k].interval===expected);
 message.expire();assert(!root.notificationTimers[k]&&!root.toastTimers[k]);
}
const changing=note(23);root.receive(changing);const count=root.history.length;
changing.transient=true;root.receive(changing);assert(root.history.length===count-1);
const menuEvents=[],window={id:'bar'};
SystemTray.items.values=[{hasMenu:true,onlyMenu:false,display:(...v)=>menuEvents.push(['menu',...v]),activate:()=>menuEvents.push(['activate']),secondaryActivate:()=>menuEvents.push(['secondary']),scroll:(...v)=>menuEvents.push(['scroll',...v])}];
root.trayClick(0,Qt.RightButton,window,12,32);assert.deepStrictEqual(menuEvents.pop(),['menu',window,12,32]);
root.trayClick(0,Qt.LeftButton,window,12,32);assert.deepStrictEqual(menuEvents.pop(),['activate']);
root.trayClick(0,Qt.MiddleButton,window,12,32);assert.deepStrictEqual(menuEvents.pop(),['secondary']);
root.trayScroll(0,120);assert.deepStrictEqual(menuEvents.pop(),['scroll',120,false]);
SystemTray.items.values[0].onlyMenu=true;root.trayClick(0,Qt.LeftButton,window,12,32);assert(menuEvents.pop()[0]==='menu');
// Only currently listed, valid addresses may reach either dispatcher syntax.
root.windows=[{id:'0xabc'}];
const capture={id:'native-toplevel'};
Hyprland.toplevels={values:[{address:'abc',wayland:capture}]};
let refreshCount=0;Hyprland.refreshToplevels=()=>refreshCount++;
root.refreshWindows();assert.strictEqual(refreshCount,1);
assert.strictEqual(root.windowCapture('0xabc'),capture);
assert.strictEqual(root.windowCapture('0xdead'),null);
root.activateWindow('0xabc');assert.strictEqual(events.pop(),'hl.dsp.focus({window="address:0xabc"})');
Hyprland.usingLua=false;root.activateWindow('0xabc');assert.strictEqual(events.pop(),'focuswindow address:0xabc');
const beforeInvalid=events.length;
for(const id of ['0xdead','0xabc"})','bad',null])root.activateWindow(id);
assert.strictEqual(events.length,beforeInvalid);
root.windows=[];root.activateWindow('0xabc');assert.strictEqual(events.length,beforeInvalid);
console.log('PASS: window activation/capture/refresh routing; notification millisecond/default/persistent timeouts, update deduplication, unread count, timer cleanup, archive/DND/actions/transient filtering, tray routing and Lua dispatch.');
