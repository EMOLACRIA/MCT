//@ pragma UseQApplication
import QtQuick
import Quickshell
ShellRoot {
    id:root
    property var candidate:null
    function finish() {
        if(!candidate)return;
        if(candidate.status===Component.Ready) {console.log("Desktop QML validated");Qt.exit(0);}
        else if(candidate.status===Component.Error) {console.error(candidate.errorString());Qt.exit(1);}
    }
    Component.onCompleted: {
        candidate=Qt.createComponent("shell.qml",Component.Asynchronous);
        candidate.statusChanged.connect(finish);finish();
    }
    Timer { interval:10000; running:true; onTriggered: {console.error("QML validation timed out");Qt.exit(1);} }
}
