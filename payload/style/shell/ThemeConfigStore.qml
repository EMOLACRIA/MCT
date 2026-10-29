import QtQuick
import Quickshell
import Quickshell.Io
import "ui"
// Runs the theme settings helper; one request at a time, latest queued request wins.
Scope {
    id:root
    property alias state:model
    property string queuedAction:""
    property var queuedArgs:null
    ThemeConfigState {id:model;onRequested:(action,args)=>root.run(action,args)}
    function run(action,args) {
        if(worker.running) {queuedAction=action;queuedArgs=args;return;}
        if(action!=="read")model.busy=true;
        worker.command=["python3",Quickshell.shellPath("../scripts/theme_config.py"),action].concat(args || []);
        worker.running=true;
    }
    Process {
        id:worker
        stdout:StdioCollector {onStreamFinished: {try {model.accept(JSON.parse(text));} catch(e) {model.fail("Theme settings helper returned an invalid response.");}}}
        onRunningChanged:if(running)deadline.restart();else deadline.stop()
        onExited:(exitCode,exitStatus)=> {if(exitCode!==0)model.fail("Theme settings helper failed. Check shell.log.");if(root.queuedAction!=="")continueQueue.restart();}
    }
    // A file chooser can stay open for a while; everything else answers quickly.
    Timer {id:deadline;interval:620000;onTriggered:model.fail("Theme settings helper did not answer.")}
    Timer {id:continueQueue;interval:0;onTriggered: {const a=root.queuedAction,b=root.queuedArgs;root.queuedAction="";root.queuedArgs=null;root.run(a,b);}}
    Component.onCompleted:run("read",[])
}
