import QtQuick
import QtQuick.Controls
FocusScope {
    id: root
    required property var state
    signal closeRequested()
    implicitWidth: 1600; implicitHeight: 1000
    focus: true
    readonly property color accent: state.selected && state.selected.accent ? state.selected.accent : "#c7b28b"
    readonly property real edge: width < 700 ? 20 : 64
    readonly property real photoHeight: Math.min(230, height * (height < 600 ? .24 : .28))
    readonly property real railHeight: photoHeight + 136
    readonly property real axisY: Math.round(height * .5)
    readonly property real expandedWidth: Math.min(430, width * .54)
    readonly property real collapsedWidth: Math.max(126, Math.min(210, width * .22))
    readonly property bool pixelTitle: !!state.selected && !!state.selected.fontSource && titleFace.status === FontLoader.Ready
    FontLoader { id: titleFace; source: root.state.selected && root.state.selected.fontSource ? root.state.selected.fontSource : root.state.monoFontSource }
    function revealSelection() {
        for (let i = 0; i < rail.count; ++i) {
            const card = rail.itemAtIndex(i);
            if (card && card.entry.id === state.selectedId) {
                rail.positionViewAtIndex(i, ListView.Contain);
                return;
            }
        }
    }
    Connections { target: root.state; function onSelectedIdChanged() { Qt.callLater(root.revealSelection); } }
    Keys.onPressed: event => {
        if (event.key === Qt.Key_Escape) {
            if (state.rollbackArmed) state.rollbackArmed = false;
            else closeRequested();
            event.accepted = true;
        } else if (event.key === Qt.Key_Left || event.key === Qt.Key_Right || event.key === Qt.Key_Tab) {
            state.navigate(event.key === Qt.Key_Left || (event.modifiers & Qt.ShiftModifier) ? -1 : 1);
            event.accepted = true;
        } else if (event.key === Qt.Key_Return || event.key === Qt.Key_Enter || event.key === Qt.Key_Space) {
            state.activate(state.selectedId); event.accepted = true;
        }
    }
    Rectangle { anchors.fill: parent; color: "#bb03070c" }
    MouseArea { anchors.fill: parent; onClicked: {root.closeRequested();root.forceActiveFocus();} }
    Text {
        x: root.edge; y: root.height < 600 ? 20 : root.height * .13
        text: "WORLD SELECT"; color: root.accent
        font.family: "monospace"; font.pixelSize: 11 * root.state.fontScale; font.letterSpacing: 4
    }
    Text {
        x: root.edge; y: (root.height < 600 ? 20 : root.height * .13) + 30
        text: root.state.selected ? root.state.selected.name : "Themes"
        textFormat: Text.PlainText; color: "#eceee8"
        font.family: root.pixelTitle ? titleFace.name : "serif"
        font.pixelSize: Math.min(root.height < 600 ? 30 : root.pixelTitle ? 38 : 48, root.width * (root.height < 600 ? .045 : .055)) * root.state.fontScale
    }
    Rectangle {
        objectName: "themeSpine"
        x: root.edge; y: root.axisY; width: parent.width - 2 * root.edge; height: 1
        color: root.accent; opacity: .36
    }
    ListView {
        id: rail
        objectName: "themeRail"
        x: root.edge; y: root.axisY - root.photoHeight - 26
        width: root.width - 2 * root.edge; height: root.railHeight
        orientation: ListView.Horizontal; spacing: 28; clip: true
        boundsBehavior: Flickable.StopAtBounds
        contentX: 0
        header: Item {width: Math.max(0, (rail.width - root.expandedWidth - (root.state.themes.length - 1) * (root.collapsedWidth + rail.spacing)) / 2); height: 1}
        footer: Item {width: rail.headerItem ? rail.headerItem.width : 0; height: 1}
        model: root.state.themes
        delegate: PickerCard {
            required property var modelData
            entry: modelData
            selected: root.state.selectedId === entry.id
            active: root.state.activeTheme !== null && root.state.activeTheme.id === entry.id && root.state.activeTheme.version === entry.version
            locked: root.state.busy; reduceMotion: root.state.reduceMotion; fontScale: root.state.fontScale
            expandedWidth: root.expandedWidth; collapsedWidth: root.collapsedWidth; previewHeight: root.photoHeight
            onHighlighted: {root.state.choose(entry.id);root.forceActiveFocus();}
            onActivated: {root.state.activate(entry.id);root.forceActiveFocus();}
        }
    }
    ScrollView {
        id: statusArea
        x: root.edge; y: root.axisY + 125
        width: root.width - 2 * root.edge; height: Math.max(30, root.height - y - 110)
        contentWidth: availableWidth; clip: true
        Text {
        objectName: "pickerStatus"
        width: statusArea.availableWidth
        text: root.state.pending ? "A previous switch needs recovery. Run bash theme.sh recover."
            : root.state.stateError || root.state.message || (!root.state.ready ? "Loading themes…" : root.state.selected && !root.state.selected.valid ? root.state.selected.error : "")
        color: root.state.failed || root.state.pending || root.state.stateError ? "#f0aaaa" : root.accent
        font.pixelSize: 13 * root.state.fontScale; wrapMode: Text.Wrap; textFormat: Text.PlainText
        }
    }
    Row {
        x: root.edge; anchors.bottom: parent.bottom; anchors.bottomMargin: root.height < 600 ? 20 : 40
        spacing: 22
        Text {text: "← →  EXPLORE"; color: "#83949e"; font.family: "monospace"; font.pixelSize: 10}
        Text {text: "ENTER  SWITCH"; color: "#83949e"; font.family: "monospace"; font.pixelSize: 10}
        Text {text: "ESC  CLOSE"; color: "#83949e"; font.family: "monospace"; font.pixelSize: 10}
    }
    Text {
        id: restore
        objectName: "rollbackTheme"
        anchors.right: parent.right; anchors.rightMargin: root.edge
        anchors.bottom: parent.bottom; anchors.bottomMargin: root.height < 600 ? 42 : 40
        text: root.state.rollbackArmed ? "CONFIRM RESTORE" : "RESTORE LAST"
        color: root.state.rollbackArmed ? root.accent : "#83949e"
        font.family: "monospace"; font.pixelSize: 10
        visible: root.state.canRollback
        MouseArea {anchors.fill:parent;anchors.margins:-10;enabled:!root.state.blocked;cursorShape:Qt.PointingHandCursor;onClicked:{root.state.run("rollback");root.forceActiveFocus();}}
    }
}
