//@ pragma UseQApplication
import QtQuick
import Quickshell
import Quickshell.Io
import Quickshell.Wayland
import Quickshell.Hyprland
ShellRoot {
    id: root
    property bool opened: true
    property string screenName: ""
    property string response: ""
    property string errors: ""
    readonly property var focusedScreen: Quickshell.screens.find(s => s.name === (Hyprland.focusedMonitor ? Hyprland.focusedMonitor.name : "")) || Quickshell.screens[0] || null
    readonly property var selectedScreen: Quickshell.screens.find(s => s.name === screenName) || focusedScreen
    PickerState {
        id: model
        onRequested: (action, theme) => root.run(action, theme)
        onApplied: closeAfterSwitch.restart()
    }
    function toggle() {
        closeAfterSwitch.stop();
        opened = !opened;
        if (opened) {
            screenName = focusedScreen ? focusedScreen.name : "";
            closeDesktopPanel.running = true;
            if (!model.busy) model.run("catalog");
        }
    }
    function run(action, theme) {
        response = ""; errors = "";
        worker.command = ["python3", Quickshell.shellPath("../theme_picker.py"), action].concat(theme ? [theme] : []);
        worker.running = true;
    }
    IpcHandler {
        target: "themes"
        function toggle(): void {root.toggle();}
        function ping(): string {return "ready";}
    }
    Process {
        id: closeDesktopPanel
        command: ["quickshell", "ipc", "-p", Quickshell.env("HOME") + "/.config/desktop-style/shell", "call", "desktop", "close"]
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
            catch (e) { model.fail(root.errors || "The theme helper stopped. Reopen to read the current desktop state."); }
        }
    }
    Timer { id: closeAfterSwitch; interval: 650; onTriggered: root.opened = false }
    PanelWindow {
        id: window
        visible: root.opened && root.selectedScreen !== null
        screen: root.selectedScreen
        anchors { top: true; bottom: true; left: true; right: true }
        color: "transparent"; exclusionMode: ExclusionMode.Ignore
        WlrLayershell.layer: WlrLayer.Overlay
        WlrLayershell.keyboardFocus: WlrKeyboardFocus.Exclusive
        WlrLayershell.namespace: "desktop-theme-rail"
        PickerView { anchors.fill: parent; state: model; onCloseRequested: root.opened = false }
    }
    Component.onCompleted: {
        screenName = focusedScreen ? focusedScreen.name : "";
        closeDesktopPanel.running = true;
        model.run("catalog");
    }
}
