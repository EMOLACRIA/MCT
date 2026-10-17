import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
AbstractButton {
    id: root
    property string symbol: ""
    property string hint: ""
    property real iconLevel: 100
    property bool iconCharging: false
    property color iconColor: destructive ? Theme.danger : Theme.brass
    property bool selected: false
    property bool destructive: false
    implicitHeight: 42
    implicitWidth: Math.max(42, contentItem.implicitWidth + 28)
    padding: 12
    hoverEnabled: true
    activeFocusOnTab: true
    Accessible.name: text || symbol
    opacity: enabled ? 1 : .38
    SurfaceHint {visible:root.visible && root.hovered && text!=="";text:root.hint}
    background: Rectangle {
        color: root.down || root.selected ? Theme.selectedSurface : root.hovered || root.activeFocus ? Theme.raised : "transparent"
        border.color: root.selected || root.activeFocus ? Theme.brass : root.hovered ? Theme.line : "transparent"
        border.width: 1
        Behavior on color { ColorAnimation { duration:Theme.duration(Theme.quickMotion) } }
    }
    contentItem: Item {
        implicitWidth: content.implicitWidth
        implicitHeight: 20
        RowLayout {
            id: content
            anchors.centerIn: parent
            width: Math.min(implicitWidth, Math.max(root.symbol !== "" ? 20 : 0, parent.width))
            spacing: root.symbol !== "" && root.text !== "" ? 10 : 0
            Glyph {
                objectName: "buttonGlyph"
                visible: root.symbol !== ""; symbol: root.symbol
                ink: root.iconColor; level: root.iconLevel; charging: root.iconCharging
                Layout.preferredWidth: 20; Layout.preferredHeight: 20
                Layout.minimumWidth: 20; Layout.minimumHeight: 20
                Layout.alignment: Qt.AlignVCenter
            }
            Text {
                visible: root.text !== ""; text: root.text; textFormat: Text.PlainText
                color: root.destructive ? Theme.danger : Theme.ink
                font.family: Theme.bodyFont; font.pixelSize:Theme.fontSize(13)
                Layout.fillWidth: true; Layout.minimumWidth: 0
                Layout.alignment: Qt.AlignVCenter; elide: Text.ElideRight
            }
        }
    }
}
