import QtQuick
import "../logic/Calculator.js" as Calculator
Item {
    id: root
    objectName:"launcher"
    required property var backend
    required property var uiState
    readonly property var calculation:Calculator.calculate(uiState.search)
    property string copiedText:""
    onCalculationChanged: {copiedText="";copyFeedback.stop();}
    readonly property var applications: {
        const terms=uiState.search.trim().toLocaleLowerCase().split(/\s+/).filter(t=>t.length);
        return backend.applications.filter(a=>terms.every(t=>(a.name+" "+a.comment).toLocaleLowerCase().indexOf(t)>=0));
    }
    readonly property var entries: {
        const apps=applications.map(a=>({kind:"application",id:a.id,name:a.name,comment:a.comment,icon:a.icon}));
        return calculation.state==="ready" ? [{kind:"calculation",name:calculation.text}].concat(apps) : apps;
    }
    property int selectedIndex:0
    onEntriesChanged:selectedIndex=entries.length ? 0 : -1
    signal focusRequested()
    function activate() {focusRequested();}
    function copyResult() {
        if(calculation.state!=="ready")return;
        backend.copyText(calculation.text);copiedText=calculation.text;copyFeedback.restart();activate();
    }
    function openSelected() {
        const entry=entries[selectedIndex];if(!entry)return;
        if(entry.kind==="calculation")copyResult();
        else {backend.launchApplication(entry.id);uiState.close();}
    }
    function moveSelection(direction) {
        if(entries.length)selectedIndex=Math.max(0,Math.min(entries.length-1,selectedIndex+direction));
    }
    Timer {id:copyFeedback;interval:1600;onTriggered:root.copiedText=""}
}
