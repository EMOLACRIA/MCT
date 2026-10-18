import QtQuick
Rectangle {
    id: root
    required property var entry
    property bool selected: false
    property bool active: false
    property bool locked: false
    signal chosen()
    signal enlarge()
    implicitHeight: column.implicitHeight + 28
    radius: 12
    color: selected ? "#1a2935" : "#121c25"
    border.color: selected ? "#bed7e5" : "#30404d"
    border.width: selected ? 2 : 1
    Column {
        id: column
        x: 14; y: 14; width: parent.width - 28; spacing: 12
        Rectangle {
            width: parent.width; height: Math.min(240, width / 1.6)
            color: "#080d12"; radius: 6; clip: true
            Image {
                objectName: "themeImage-" + root.entry.id
                anchors.fill: parent
                source: root.entry.preview; fillMode: Image.PreserveAspectFit; asynchronous: true
            }
            Text {
                anchors.centerIn: parent; width: parent.width - 32
                visible: !root.entry.valid
                text: "Preview unavailable"; color: "#d5b6b6"; wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignHCenter
            }
            MouseArea {
                objectName: "selectTheme-" + root.entry.id
                anchors.fill: parent; enabled: !root.locked
                cursorShape: Qt.PointingHandCursor
                onClicked: root.chosen()
            }
        }
        Row {
            width: parent.width; spacing: 8
            Text {
                width: parent.width - badge.width - 8
                text: root.entry.name; color: "#f2f5f7"; font.pixelSize: 22; elide: Text.ElideRight
            }
            Rectangle {
                id: badge
                width: root.active ? 58 : 0; height: 24; radius: 4; visible: root.active
                color: "#294637"
                Text { anchors.centerIn: parent; text: "ACTIVE"; color: "#b9eacb"; font.pixelSize: 10; font.bold: true }
            }
        }
        Text {
            width: parent.width; text: root.entry.valid ? "Version " + root.entry.version : root.entry.error
            color: root.entry.valid ? "#a8b8c5" : "#f0afaf"; font.pixelSize: 12; wrapMode: Text.Wrap
        }
        Row {
            width: parent.width; spacing: 8
            PickerButton {
                objectName: "chooseTheme-" + root.entry.id
                text: root.selected ? "Selected" : "Select"; primary: root.selected; enabled: !root.locked
                onClicked: root.chosen()
            }
            PickerButton {
                objectName: "enlargeTheme-" + root.entry.id
                text: "View image"; enabled: root.entry.valid && !root.locked
                onClicked: root.enlarge()
            }
        }
    }
}
