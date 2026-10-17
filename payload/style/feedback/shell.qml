import QtQuick
import Quickshell
import Quickshell.Io
import Quickshell.Wayland

Scope {
    id: root
    property string kind: "volume"
    property int level: 0
    property bool muted: false
    property bool showing: false

    IpcHandler {
        target: "feedback"
        function ping(): string { return "ready"; }
        function show(kind: string, level: int, muted: bool): void {
            root.kind = kind;
            root.level = Math.max(0, Math.min(100, level));
            root.muted = muted;
            root.showing = true;
            hideTimer.restart();
        }
    }
    Timer {
        id: hideTimer
        interval: 1400
        onTriggered: root.showing = false
    }
    PanelWindow {
        visible: root.showing
        implicitWidth: 320
        implicitHeight: 72
        color: "transparent"
        anchors.bottom: true
        margins.bottom: 80
        exclusionMode: ExclusionMode.Ignore
        focusable: false
        WlrLayershell.layer: WlrLayer.Overlay
        WlrLayershell.namespace: "desktop-feedback"

        Rectangle {
            anchors.fill: parent
            color: "#ee191a18"
            border.width: 1
            border.color: "#77715e"
            Image { anchors.left: parent.left; anchors.top: parent.top; width: 15; height: 15; source: "../assets/tl.svg" }
            Image { anchors.right: parent.right; anchors.top: parent.top; width: 15; height: 15; source: "../assets/tr.svg" }
            Image { anchors.left: parent.left; anchors.bottom: parent.bottom; width: 15; height: 15; source: "../assets/bl.svg" }
            Image { anchors.right: parent.right; anchors.bottom: parent.bottom; width: 15; height: 15; source: "../assets/br.svg" }
            Text {
                x: 22; y: 15
                color: "#d8d3c5"
                font.family: "serif"
                font.pixelSize: 17
                text: root.kind === "brightness" ? "Brightness" : root.kind === "microphone" ? "Microphone" : "Volume"
            }
            Text {
                anchors.right: parent.right
                anchors.rightMargin: 22
                y: 18
                color: root.muted ? "#ce9582" : "#b5a37c"
                font.pixelSize: 12
                text: root.muted ? "MUTED" : root.level + "%"
            }
            Rectangle {
                x: 22; y: 49; width: parent.width - 44; height: 3
                color: "#45473e"
                Rectangle {
                    width: root.muted ? 0 : parent.width * root.level / 100
                    height: parent.height
                    color: "#b5a37c"
                    Behavior on width { NumberAnimation { duration: 80 } }
                }
            }
        }
    }
}
