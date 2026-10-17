import QtQuick
import Quickshell
import Quickshell.Io
import "ui"
Scope {
    id:root
    property alias state:model
    property string queuedAction:""
    property var queuedCandidate:null
    PreferencesState {id:model;ready:false;onWriteRequested:(action,candidate)=>root.run(action,candidate)}
    function run(action,candidate) {
        if(worker.running) {queuedAction=action;queuedCandidate=candidate;return;}
        model.saving=true;
        worker.command=["python3",Quickshell.shellPath("../scripts/preferences.py"),action].concat(action==="save" ? [JSON.stringify(candidate)] : []);
        worker.running=true;
    }
    Process {
        id:worker
        stdout:StdioCollector {onStreamFinished: {try {model.accept(JSON.parse(text));} catch(e) {model.fail("Preference helper returned an invalid response.");}}}
        onRunningChanged: {if(running)deadline.restart();else {deadline.stop();checkCompletion.restart();}}
        onExited:(exitCode,exitStatus)=> {if(exitCode!==0)model.fail("Preference helper failed. Check shell.log.");if(root.queuedAction!=="")continueQueue.restart();}
    }
    Timer {id:deadline;interval:10000;onTriggered:model.fail("Preference operation is taking too long. Reload to check the stored value.")}
    Timer {id:checkCompletion;interval:0;onTriggered:if(!worker.running && model.saving) {model.fail("Preference helper did not return a result. Check shell.log.");if(root.queuedAction!=="")continueQueue.restart();}}
    Timer {id:continueQueue;interval:0;onTriggered: {const action=root.queuedAction,candidate=root.queuedCandidate;root.queuedAction="";root.queuedCandidate=null;root.run(action,candidate);}}
    Component.onCompleted:run("read",null)
}
