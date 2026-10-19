import QtQuick
Item {
    id: root
    required property var entry
    property bool selected: false
    property bool active: false
    property bool locked: false
    property bool reduceMotion: false
    property real fontScale: 1
    property real expandedWidth: 420
    property real collapsedWidth: 180
    property real previewHeight: 220
    readonly property bool pixel: entry.id === "deltarune"
    readonly property color accent: pixel ? "#00d9ef" : "#c7b28b"
    readonly property string face: pixel && faceLoader.status === FontLoader.Ready ? faceLoader.name : pixel ? "monospace" : "serif"
    readonly property real axis: previewHeight + 26
    width: selected ? expandedWidth : collapsedWidth
    height: axis + 110
    signal highlighted()
    signal activated()
    FontLoader { id: faceLoader; source: root.entry.fontSource || "" }
    Behavior on width { NumberAnimation { duration: root.reduceMotion ? 0 : 190; easing.type: Easing.OutCubic } }

    Rectangle {
        id: photo
        objectName: "themePhoto-" + root.entry.id
        x: 8; y: root.axis - height - 24; width: root.width - 16
        height: root.selected ? Math.min(root.previewHeight, width / 1.6) : 0
        opacity: root.selected ? 1 : 0; clip: true
        color: root.pixel ? "#010b13" : "#181b18"
        border.color: root.accent; border.width: 1
        Behavior on height { NumberAnimation { duration: root.reduceMotion ? 0 : 190; easing.type: Easing.OutCubic } }
        Behavior on opacity { NumberAnimation { duration: root.reduceMotion ? 0 : 150 } }
        Image {
            objectName: "themeImage-" + root.entry.id
            anchors.fill: parent; anchors.margins: 5
            source: root.entry.preview; fillMode: Image.PreserveAspectFit; asynchronous: true
        }
        Rectangle { x: 0; y: 0; width: root.pixel ? 26 : 12; height: 3; color: root.accent }
        Rectangle { anchors.right: parent.right; anchors.bottom: parent.bottom; width: root.pixel ? 26 : 12; height: 3; color: root.accent }
    }
    Rectangle {
        anchors.horizontalCenter: parent.horizontalCenter
        y: photo.y + photo.height; width: 1; height: 24
        color: root.accent; opacity: root.selected ? .7 : 0
    }
    Rectangle {
        objectName: "themeNode-" + root.entry.id
        anchors.horizontalCenter: parent.horizontalCenter
        y: root.axis - height / 2; width: root.selected ? 12 : 7; height: width
        rotation: root.pixel ? 0 : 45
        color: root.active || root.selected ? root.accent : "#111a20"
        border.color: root.entry.valid ? root.accent : "#bd7c7c"; border.width: 1
        Rectangle { anchors.fill: parent; anchors.margins: -4; color: "transparent"; border.color: root.accent; opacity: root.active ? .6 : 0 }
    }
    Text {
        objectName: "themeTitle-" + root.entry.id
        x: 0; y: root.axis + 26; width: parent.width
        text: root.entry.name; textFormat: Text.PlainText
        color: root.entry.valid ? root.selected ? "#f5f2e9" : "#aab5bb" : "#bd8888"
        font.family: root.face; font.pixelSize: (root.pixel ? 19 : 26) * root.fontScale
        horizontalAlignment: Text.AlignHCenter; elide: Text.ElideRight
    }
    Text {
        x: 8; y: root.axis + 65; width: parent.width - 16
        text: !root.entry.valid ? "UNAVAILABLE" : root.active ? "CURRENT" : root.selected ? "ENTER TO SWITCH" : ""
        color: root.accent; font.family: "monospace"; font.pixelSize: 10 * root.fontScale
        font.letterSpacing: 2; horizontalAlignment: Text.AlignHCenter
    }
    MouseArea {
        objectName: "selectTheme-" + root.entry.id
        anchors.fill: parent; hoverEnabled: true; enabled: !root.locked
        cursorShape: root.entry.valid && !root.active ? Qt.PointingHandCursor : Qt.ArrowCursor
        onEntered: root.highlighted()
        onClicked: root.activated()
        Accessible.role: Accessible.Button
        Accessible.name: root.entry.name
        Accessible.onPressAction: root.activated()
    }
}
