import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
Item {
    id:root
    required property var backend
    required property var uiState
    function activate() { root.forceActiveFocus(); }
    ColumnLayout {
        anchors.fill:parent; spacing:20
        RowLayout {
            Glyph { symbol:"music"; width:25; height:25 }
            Text { text:"Now playing"; color:Theme.ink; font.family:Theme.displayFont; font.pixelSize:Theme.fontSize(26); Layout.fillWidth:true }
            ActionButton { symbol:"close"; width:36; height:36; padding:8; onClicked:uiState.close() }
        }
        Rectangle {
            Layout.alignment:Qt.AlignHCenter; width:142; height:142; color:Theme.raised; border.color:Theme.line
            Image { id:cover; anchors.fill:parent; anchors.margins:1; source:backend.mediaArt; fillMode:Image.PreserveAspectCrop; asynchronous:true }
            Glyph { anchors.centerIn:parent; width:60; height:60; symbol:"tree"; visible:cover.status!==Image.Ready }
        }
        ColumnLayout {
            Layout.fillWidth:true; spacing:6
            Text { Layout.fillWidth:true; text:backend.mediaTitle || "No active player"; textFormat:Text.PlainText; wrapMode:Text.WordWrap; maximumLineCount:2; elide:Text.ElideRight; color:Theme.ink; font.family:Theme.displayFont; font.pixelSize:Theme.fontSize(22); horizontalAlignment:Text.AlignHCenter }
            Text { Layout.fillWidth:true; text:backend.mediaArtist; textFormat:Text.PlainText; elide:Text.ElideRight; color:Theme.muted; font.pixelSize:Theme.fontSize(12); horizontalAlignment:Text.AlignHCenter }
        }
        RowLayout {
            Layout.alignment:Qt.AlignHCenter; spacing:18
            ActionButton { symbol:"previous"; enabled:backend.canPrevious; onClicked:backend.mediaCommand("previous") }
            ActionButton { symbol:backend.mediaPlaying ? "pause" : "play"; width:54; height:48; padding:15; enabled:backend.canPlayPause; onClicked:backend.mediaCommand("toggle") }
            ActionButton { symbol:"next"; enabled:backend.canNext; onClicked:backend.mediaCommand("next") }
        }
        Flow {
            Layout.fillWidth:true; spacing:5
            Repeater { model:backend.players; delegate:ActionButton { required property var modelData; text:modelData.name; selected:modelData.selected; onClicked:backend.selectPlayer(modelData.id) } }
        }
        Item { Layout.fillHeight:true }
    }
}
