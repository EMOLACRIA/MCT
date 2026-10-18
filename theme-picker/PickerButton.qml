import QtQuick
import QtQuick.Controls
Button {
    id: root
    property bool primary: false
    implicitHeight: 42
    implicitWidth: Math.max(110, contentItem.implicitWidth + 30)
    font.pixelSize: 14
    font.family: "sans-serif"
    contentItem: Text {
        text: root.text; font: root.font
        color: !root.enabled ? "#697581" : root.primary ? "#10161c" : "#f2f5f7"
        horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter
    }
    background: Rectangle {
        radius: 7
        color: root.primary ? (root.enabled ? "#bed7e5" : "#26313c") : root.down ? "#293947" : root.hovered ? "#23303c" : "#18232d"
        border.color: root.activeFocus ? "#ffffff" : "#384a59"
        border.width: root.activeFocus ? 2 : 1
    }
}
