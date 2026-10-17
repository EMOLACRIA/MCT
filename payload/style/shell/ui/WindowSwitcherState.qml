import QtQuick
Item {
    id:root
    visible:false
    property var windows:[]
    property string activeWindowId:""
    property var recent:[]
    property bool active:false
    property string screenName:""
    property string originId:""
    property string selectedId:""
    property var order:[]
    readonly property var entries:order.map(id=>windows.find(w=>w.id===id)).filter(w=>!!w)
    readonly property int selectedIndex:entries.findIndex(w=>w.id===selectedId)
    readonly property var selected:entries.find(w=>w.id===selectedId) || null
    signal committed(string windowId)
    function remember(id) {
        if(id && windows.some(w=>w.id===id))recent=[id].concat(recent.filter(v=>v!==id));
    }
    function reconcile() {
        const ids=windows.map(w=>w.id);
        recent=recent.filter(id=>ids.indexOf(id)>=0);
        if(!active) {remember(activeWindowId);return;}
        const oldIndex=Math.max(0,order.indexOf(selectedId));
        order=order.filter(id=>ids.indexOf(id)>=0).concat(ids.filter(id=>order.indexOf(id)<0));
        if(!order.length) {cancel();return;}
        if(order.indexOf(selectedId)<0)selectedId=order[Math.min(oldIndex,order.length-1)];
    }
    onWindowsChanged:reconcile()
    onActiveWindowIdChanged: {
        remember(activeWindowId);
        if(active && activeWindowId && activeWindowId!==originId)cancel();
    }
    function begin(direction,screen) {
        if(active) {step(direction);return;}
        reconcile();
        const ranked=windows.slice().sort((a,b)=>{
            const ai=recent.indexOf(a.id),bi=recent.indexOf(b.id);
            if(ai>=0 || bi>=0)return (ai<0 ? 1e9 : ai)-(bi<0 ? 1e9 : bi);
            const af=a.focusOrder>=0 ? a.focusOrder : 1e9,bf=b.focusOrder>=0 ? b.focusOrder : 1e9;
            return af-bf || a.id.localeCompare(b.id);
        });
        if(!ranked.length)return;
        order=ranked.map(w=>w.id);originId=activeWindowId;screenName=screen || "";
        let index=order.indexOf(originId);
        if(index<0)index=direction<0 ? 0 : -1;
        selectedId=order[(index+(direction<0 ? -1 : 1)+order.length)%order.length];
        active=true;
    }
    function step(direction) {
        if(!active || !order.length)return;
        const index=order.indexOf(selectedId);
        selectedId=order[(Math.max(0,index)+(direction<0 ? -1 : 1)+order.length)%order.length];
    }
    function choose(id) {if(active && order.indexOf(id)>=0)selectedId=id;}
    function cancel() {active=false;order=[];selectedId="";originId="";screenName="";}
    function commit() {
        if(!active)return;
        const id=selectedId,valid=windows.some(w=>w.id===id);
        cancel();
        if(valid)committed(id);
    }
}
