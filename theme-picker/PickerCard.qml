import QtQuick
// One rail entry. A family (deltarune + deltarune-*) is one card: the photo shows
// the chosen member and, while the card is open, its members are listed underneath.
Item {
    id: root
    required property var entry
    property var members: [entry]
    property bool selected: false
    property string selectedId: ""
    property string activeId: ""
    property string activeVersion: ""
    property bool locked: false
    property bool reduceMotion: false
    property real fontScale: 1
    property real expandedWidth: 420
    property real collapsedWidth: 180
    property real previewHeight: 220
    readonly property bool family: members.length > 1
    readonly property var shown: {
        for (let i = 0; i < members.length; ++i)
            if (selected && members[i].id === selectedId) return members[i];
        return entry;
    }
    readonly property var activeMember: {
        for (let i = 0; i < members.length; ++i)
            if (members[i].id === activeId) return members[i];
        return null;
    }
    // "active" = the shown member is the installed one (same version).
    readonly property bool active: activeMember !== null && activeMember.id === shown.id && activeMember.version === shown.version
    readonly property bool pixel: !!entry.fontSource
    readonly property color accent: shown.accent || entry.accent || "#c7b28b"
    readonly property string face: pixel && faceLoader.status === FontLoader.Ready ? faceLoader.name : pixel ? "monospace" : "serif"
    readonly property real axis: previewHeight + 26
    width: selected ? expandedWidth : collapsedWidth
    height: axis + (family && selected ? 150 : 110)
    signal highlighted()
    signal activated()
    signal memberHighlighted(string id)
    signal memberActivated(string id)
    FontLoader { id: faceLoader; source: root.entry.fontSource || "" }
    Behavior on width { NumberAnimation { duration: root.reduceMotion ? 0 : 190; easing.type: Easing.OutCubic } }

    Rectangle {
        id: photo
        objectName: "themePhoto-" + root.entry.id
        x: 8; y: root.axis - height - 24; width: root.width - 16
        height: root.selected ? Math.min(root.previewHeight, width / 1.6) : 0
        opacity: root.selected ? 1 : 0; clip: true
        color: root.shown.surface || "#181b18"
        border.color: root.accent; border.width: 1
        Behavior on height { NumberAnimation { duration: root.reduceMotion ? 0 : 190; easing.type: Easing.OutCubic } }
        Behavior on opacity { NumberAnimation { duration: root.reduceMotion ? 0 : 150 } }
        Image {
            objectName: "themeImage-" + root.entry.id
            anchors.fill: parent; anchors.margins: 5
            source: root.shown.preview; fillMode: Image.PreserveAspectFit; asynchronous: true
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
        color: root.activeMember !== null || root.selected ? root.accent : "#111a20"
        border.color: root.entry.valid ? root.accent : "#bd7c7c"; border.width: 1
        Rectangle { anchors.fill: parent; anchors.margins: -4; color: "transparent"; border.color: root.accent; opacity: root.activeMember !== null ? .6 : 0 }
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
        text: !root.shown.valid ? "UNAVAILABLE" : root.active ? "CURRENT"
              : root.selected ? "ENTER TO SWITCH"
              : root.activeMember !== null && root.family ? "CURRENT · " + root.activeMember.name.toUpperCase() : ""
        color: root.accent; font.family: "monospace"; font.pixelSize: 10 * root.fontScale
        font.letterSpacing: 2; horizontalAlignment: Text.AlignHCenter
    }
    MouseArea {
        objectName: "selectTheme-" + root.entry.id
        anchors.fill: parent; hoverEnabled: true; enabled: !root.locked
        cursorShape: root.shown.valid && !root.active ? Qt.PointingHandCursor : Qt.ArrowCursor
        onEntered: root.highlighted()
        onClicked: root.activated()
        Accessible.role: Accessible.Button
        Accessible.name: root.entry.name
        Accessible.onPressAction: root.activated()
    }
    // Members of an open family, under the card. Hover chooses, click switches.
    Row {
        objectName: "themeMembers-" + root.entry.id
        anchors.horizontalCenter: parent.horizontalCenter
        y: root.axis + 96; spacing: 24
        visible: root.family && root.selected
        Repeater {
            model: root.family ? root.members : []
            Item {
                id: member
                required property var modelData
                readonly property bool chosen: modelData.id === root.selectedId
                readonly property bool installed: modelData.id === root.activeId
                width: label.implicitWidth; height: 30
                Text {
                    id: label
                    y: 4
                    text: member.modelData.name; textFormat: Text.PlainText
                    color: !member.modelData.valid ? "#bd8888" : member.chosen ? "#f5f2e9" : "#83949e"
                    font.family: root.face; font.pixelSize: (root.pixel ? 13 : 16) * root.fontScale
                }
                Rectangle {
                    anchors.horizontalCenter: parent.horizontalCenter; y: label.y + label.height + 3
                    width: member.chosen ? label.width : 0; height: 2; color: member.modelData.accent || root.accent
                    Behavior on width { NumberAnimation { duration: root.reduceMotion ? 0 : 120 } }
                }
                Rectangle {
                    visible: member.installed
                    anchors.verticalCenter: label.verticalCenter; x: -11
                    width: 5; height: 5; rotation: 45; color: member.modelData.accent || root.accent
                }
                MouseArea {
                    objectName: "selectMember-" + member.modelData.id
                    anchors.fill: parent; anchors.margins: -6; hoverEnabled: true; enabled: !root.locked
                    cursorShape: member.modelData.valid && !member.installed ? Qt.PointingHandCursor : Qt.ArrowCursor
                    onEntered: root.memberHighlighted(member.modelData.id)
                    onClicked: root.memberActivated(member.modelData.id)
                    Accessible.role: Accessible.Button
                    Accessible.name: member.modelData.name
                    Accessible.onPressAction: root.memberActivated(member.modelData.id)
                }
            }
        }
    }
}
