import QtQuick
import QtQuick.Controls
FocusScope {
    id: root
    required property var state
    property var enlarged: null
    signal closeRequested()
    implicitWidth: 1080; implicitHeight: 760
    focus: true
    function revealSelection() {
        for (let i = 0; i < themeCards.count; ++i) {
            const card = themeCards.itemAt(i);
            if (card && card.entry.id === state.selectedId) {
                const flick = scroll.contentItem;
                const top = cards.y + card.y;
                if (top < flick.contentY) flick.contentY = top;
                else if (top + card.height > flick.contentY + flick.height)
                    flick.contentY = Math.min(top, Math.max(0, flick.contentHeight - flick.height));
                return;
            }
        }
    }
    Connections {
        target: root.state
        function onSelectedIdChanged() { Qt.callLater(root.revealSelection); }
    }
    Keys.onPressed: event => {
        if (event.key === Qt.Key_Escape) {
            if (enlarged) enlarged = null;
            else if (state.rollbackArmed) state.rollbackArmed = false;
            else if (!state.busy) closeRequested();
            event.accepted = true;
        } else if (!enlarged && (event.key === Qt.Key_Left || event.key === Qt.Key_Right)) {
            state.navigate(event.key === Qt.Key_Right ? 1 : -1); event.accepted = true;
        }
    }
    Rectangle { anchors.fill: parent; color: "#0c141c" }
    ScrollView {
        id: scroll
        objectName: "themePickerScroll"
        anchors { top: parent.top; left: parent.left; right: parent.right; bottom: footer.top }
        anchors.margins: root.width < 700 ? 20 : 32
        anchors.bottomMargin: 20
        clip: true
        enabled: root.enlarged === null
        contentWidth: availableWidth
        Column {
            width: scroll.availableWidth; spacing: 20
            Row {
                width: parent.width
                Column {
                    width: parent.width - refresh.width - 16; spacing: 7
                    Text { text: "Themes"; color: "#f2f5f7"; font.pixelSize: 32; font.bold: true }
                    Text {
                        width: parent.width; text: "A different world. Your shortcuts and preferences stay with you."
                        color: "#a8b8c5"; font.pixelSize: 14; wrapMode: Text.WordWrap
                    }
                }
                PickerButton { id: refresh; objectName: "refreshThemes"; text: "Refresh"; enabled: !root.state.busy; onClicked: root.state.run("catalog") }
            }
            Grid {
                id: cards
                width: parent.width; columns: width >= 740 ? 2 : 1; spacing: 16
                Repeater {
                    id: themeCards
                    model: root.state.themes
                    PickerCard {
                        required property var modelData
                        entry: modelData; width: (cards.width - (cards.columns - 1) * cards.spacing) / cards.columns
                        selected: root.state.selectedId === entry.id
                        active: root.state.activeTheme !== null && root.state.activeTheme.id === entry.id && root.state.activeTheme.version === entry.version
                        locked: root.state.busy
                        onChosen: {root.state.choose(entry.id); root.forceActiveFocus();}
                        onEnlarge: {root.enlarged = entry; root.forceActiveFocus();}
                    }
                }
            }
            Text {
                width: parent.width
                visible: root.state.ready && root.state.themes.length === 0
                text: "No theme packages were found in this checkout."; color: "#f0afaf"; wrapMode: Text.WordWrap
            }
            Rectangle {
                width: parent.width; implicitHeight: scopeText.implicitHeight + 28
                radius: 8; color: "#131f29"; border.color: "#2b3d4b"
                Text {
                    id: scopeText
                    x: 14; y: 14; width: parent.width - 28
                    text: "Desktop · wallpaper · lock screen · Kitty colours\nDolphin, Spotify, the login screen and terminal emblem use their separate installers. Open docs/THEME_PICKER.md for those commands."
                    color: "#bac9d4"; font.pixelSize: 13; wrapMode: Text.WordWrap; lineHeight: 1.25
                }
            }
        }
    }
    Column {
        id: footer
        enabled: root.enlarged === null
        anchors { left: parent.left; right: parent.right; bottom: parent.bottom }
        anchors.margins: root.width < 700 ? 20 : 32
        spacing: 12
        ScrollView {
            id: statusScroll
            width: parent.width; height: Math.min(84, statusText.implicitHeight)
            clip: true; contentWidth: availableWidth
            Text {
                id: statusText; objectName: "pickerStatus"
                width: statusScroll.availableWidth
                text: root.state.pending ? "An interrupted switch needs recovery. Run bash theme.sh recover before continuing."
                    : root.state.stateError || root.state.message || (root.state.isActive ? "This theme is active." : "Select a theme, then check compatibility before applying.")
                color: root.state.failed || root.state.pending || root.state.stateError ? "#f0afaf" : "#c7d7e2"
                font.pixelSize: 14; wrapMode: Text.Wrap; textFormat: Text.PlainText
                Accessible.role: Accessible.StaticText
            }
        }
        Flow {
            width: parent.width; spacing: 10
            PickerButton { objectName: "checkTheme"; text: "Check compatibility"; enabled: root.state.canCheck; onClicked: root.state.run("check") }
            PickerButton { objectName: "applyTheme"; text: "Apply theme"; primary: true; enabled: root.state.canApply; onClicked: root.state.run("apply") }
            PickerButton {
                objectName: "rollbackTheme"
                text: root.state.rollbackArmed ? "Confirm restore" : "Previous theme"
                enabled: !root.state.blocked && root.state.canRollback
                onClicked: root.state.run("rollback")
            }
        }
        Text {
            width: parent.width; visible: root.state.busy || root.state.rollbackArmed
            text: root.state.busy ? "Keep this window open while the desktop switches."
                  : "Restore the last theme snapshot? This keeps your shortcuts and preferences. Esc cancels."
            color: "#a8b8c5"; font.pixelSize: 12; wrapMode: Text.WordWrap
        }
    }
    Rectangle {
        anchors.fill: parent; visible: root.enlarged !== null; color: "#f50a1016"; z: 10
        MouseArea { anchors.fill: parent; onClicked: {root.enlarged = null; root.forceActiveFocus();} }
        Image {
            anchors.fill: parent; anchors.margins: 24; anchors.bottomMargin: 78
            source: root.enlarged ? root.enlarged.preview : ""
            fillMode: Image.PreserveAspectFit
        }
        PickerButton {
            objectName: "closeThemeImage"
            anchors.horizontalCenter: parent.horizontalCenter; anchors.bottom: parent.bottom; anchors.bottomMargin: 20
            text: "Close image"; onClicked: {root.enlarged = null; root.forceActiveFocus();}
        }
    }
}
