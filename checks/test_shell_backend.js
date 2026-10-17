const fs=require('fs'),assert=require('assert');
const source=fs.readFileSync('build/desktop-style/payload/style/shell/LiveContext.qml','utf8');
const funcs=[];const re=/function\s+(\w+)\s*\(([^)]*)\)\s*\{/g;let match;
while((match=re.exec(source))){let i=re.lastIndex,depth=1,quote=null,escaped=false;
 for(;i<source.length&&depth;i++){let c=source[i];if(quote){if(escaped)escaped=false;else if(c==='\\')escaped=true;else if(c===quote)quote=null;}else if(c==='"'||c==="'"||c==='`')quote=c;else if(c==='{')depth++;else if(c==='}')depth--;}
 funcs.push('root.'+match[1]+'=function('+match[2]+'){'+source.slice(re.lastIndex,i-1)+'};');re.lastIndex=i;
}
const events=[],scheduled=[];
global.Qt={formatDateTime:()=> '18:10',callLater:f=>f(),RightButton:2,MiddleButton:4};
global.Hyprland={usingLua:true,dispatch:c=>events.push(c)};
global.Pipewire={nodes:{values:[]}};
global.DesktopEntries={byId:()=>null};
global.Quickshell={shellPath:x=>x,env:()=>'/home/fixture',execDetached:x=>events.push(x)};
global.historyFile={text:()=>JSON.stringify({dnd:false,unread:1,history:[{key:'stored',app:'Old',title:'Previous notification',body:'saved',time:'17:00',actions:[{id:'dead',text:'expired action'}]}]})};
global.saveTimer={restart:()=>events.push('persist')};
global.expiry={createObject:(r,v)=>scheduled.push(v)};global.toastExpiry={createObject:(r,v)=>scheduled.push(v)};
const root={historyLoaded:false,history:[],unread:0,doNotDisturb:false,toasts:[],liveNotifications:{},notificationGenerations:{},workspaces:[{id:9,count:1,active:true,monitor:'eDP-1'}],audioAvailable:true,sink:{audio:{volume:.5,muted:false}},microphoneAvailable:true,microphone:{audio:{volume:.8,muted:false}},feedbackRequested:(...v)=>events.push(v),lastError:'',networkSettingsAvailable:true};
Object.defineProperties(root,{volume:{get:()=>Math.round(root.sink.audio.volume*100)},muted:{get:()=>root.sink.audio.muted},microphoneMuted:{get:()=>root.microphone.audio.muted}});
new Function('root','with(root){'+funcs.join('\n')+'}')(root);
root.restoreHistory();assert(root.history.length===1&&root.history[0].actions.length===0);
function note(id,opts={}){const callbacks=[];return {id,appName:'Files',summary:'Copy complete',body:'<b>Done</b>',actions:[],tracked:false,transient:false,lastGeneration:false,expireTimeout:5,closed:{connect:f=>callbacks.push(f)},dismiss(){callbacks.forEach(f=>f(1));},expire(){callbacks.forEach(f=>f(2));},...opts};}
const n=note(8);root.receive(n);assert(n.tracked&&root.history.length===2&&root.toasts.length===1&&root.history[0].body==='Done');
const key=root.history[0].key;const generation=root.notificationGenerations[key];root.receive(n);assert(root.history.length===2&&root.notificationGenerations[key]===generation+1);
assert(scheduled.find(t=>t.notificationKey===key&&t.generation===generation));
root.toggleDnd();assert(root.toasts.length===0);root.receive(note(9));assert(root.history.length===3&&root.toasts.length===0);
root.toggleDnd();root.receive(note(10,{transient:true}));assert(root.history.length===3&&root.toasts.length===1);
root.markRead();assert(root.unread===0);
let invoked=false;const action={identifier:'open',text:'Open',invoke(){invoked=true;}};const actionable=note(11,{actions:[action]});root.receive(actionable);const actionKey=root.history[0].key;root.notificationAction(actionKey,'open');assert(invoked);
actionable.expire();assert(root.history[0].actions.length===0&&!root.liveNotifications[actionKey]);
root.dismissHistory(key);assert(!root.history.some(h=>h.key===key));root.clearHistory();assert(root.history.length===0&&root.unread===0&&root.toasts.length===0);
root.setVolume(150);assert(root.volume===100);root.toggleMute();assert(root.muted);root.toggleMicrophone();assert(root.microphoneMuted);
root.activateWorkspace(9);assert(events.includes('hl.dsp.focus({workspace=9})'));
root.setBrightness(0);assert(events.some(e=>Array.isArray(e)&&e[2]==='brightness'&&e[3]==='0'));
root.sessionAction('bad');assert(!events.some(e=>Array.isArray(e)&&e.includes('bad')));
console.log('PASS: production JS notification archive/DND/actions/expiry generations/transient filtering, stored history, sound clamps and Lua dispatch.');
