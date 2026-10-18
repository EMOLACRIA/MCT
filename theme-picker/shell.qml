//@ pragma UseQApplication
import QtQuick
import Quickshell
import Quickshell.Io
ShellRoot {
    id: root
    property string response: ""
    property string errors: ""
    PickerState { id: model; onRequested: (action, theme) => root.run(action, theme) }
    function run(action, theme) {
        response = ""; errors = "";
        worker.command = ["python3", Quickshell.shellPath("../theme_picker.py"), action].concat(theme ? [theme] : []);
        worker.running = true;
    }
    Process {
        id: worker
        stdout: StdioCollector { onStreamFinished: root.response = text }
        stderr: StdioCollector { onStreamFinished: root.errors = text }
        onExited: (exitCode, exitStatus) => completion.restart()
        onRunningChanged: if (!running && model.busy) completion.restart()
    }
    Timer {
        id: completion; interval: 0
        onTriggered: {
            try { model.accept(JSON.parse(root.response)); }
            catch (e) { model.fail(root.errors || "The theme helper stopped without a response. Refresh to check the desktop state."); }
            if (!window.visible) Qt.quit();
        }
    }
    FloatingWindow {
        id: window
        title: "Themes"; visible: true
        implicitWidth: 1080; implicitHeight: 760
        minimumSize: Qt.size(480, 400)
        onVisibleChanged: if (!visible && !model.busy) Qt.quit()
        PickerView { anchors.fill: parent; state: model; onCloseRequested: window.visible = false }
    }
    Component.onCompleted: model.run("catalog")
}
