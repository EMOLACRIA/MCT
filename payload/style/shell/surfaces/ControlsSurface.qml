import QtQuick
import "../ui"
import QtQuick.Controls
import QtQuick.Layouts
Item {
    id:root
    required property var backend
    required property var uiState
    function activate() { root.forceActiveFocus(); }
    ColumnLayout {
        anchors.fill:parent; spacing:18
        PanelHeader {
            title:"Controls";symbol:"audio";onClosed:uiState.close()
            extraAction:Component {ActionButton {objectName:"openSettings";symbol:"settings";padding:8;onClicked:uiState.toggle("settings",uiState.screenName);hint:"Desktop preferences"}}
        }
        Flickable {
            Layout.fillWidth:true; Layout.fillHeight:true; clip:true; contentHeight:details.implicitHeight; boundsBehavior:Flickable.StopAtBounds
            ScrollBar.vertical:ScrollBar {}
            ColumnLayout {
                id:details; width:parent.width; spacing:18
                Text { font.family:Theme.bodyFont; text:"Sound"; color:Theme.brass; font.pixelSize:Theme.fontSize(11); font.letterSpacing:1.2 }
                LevelControl { Layout.fillWidth:true; label:"Volume"; symbol:backend.muted ? "mute" : "audio"; level:backend.volume; available:backend.audioAvailable; onCommit:percent=>backend.setVolume(percent) }
                RowLayout {
                    Layout.fillWidth:true; spacing:8
                    ActionButton { Layout.fillWidth:true; text:backend.muted ? "Unmute sound" : "Mute sound"; symbol:backend.muted ? "mute" : "audio"; enabled:backend.audioAvailable; selected:backend.muted; onClicked:backend.toggleMute() }
                    ActionButton { Layout.fillWidth:true; text:backend.microphoneMuted ? "Enable mic" : "Mute mic"; symbol:"mic"; enabled:backend.microphoneAvailable; selected:backend.microphoneMuted; onClicked:backend.toggleMicrophone() }
                }
                Text { font.family:Theme.bodyFont; text:"Output device"; color:Theme.muted; font.pixelSize:Theme.fontSize(11)}
                Repeater {
                    model:backend.audioDevices
                    delegate: ActionButton {
                        required property var modelData
                        Layout.fillWidth:true; text:modelData.name; symbol:"audio"; selected:modelData.selected
                        onClicked:backend.selectAudio(modelData.id)
                    }
                }
                Rectangle { Layout.fillWidth:true; height:1; color:Theme.line }
                LevelControl { Layout.fillWidth:true; label:"Brightness"; symbol:"sun"; level:Math.max(0,backend.brightness); available:backend.brightness>=0; onCommit:percent=>backend.setBrightness(percent) }
                Rectangle { Layout.fillWidth:true; height:1; color:Theme.line }
                RowLayout {
                    Glyph { symbol:"battery"; level:backend.battery; charging:backend.batteryCharging; ink:backend.battery>=0 && backend.battery<=15 && !backend.batteryCharging ? Theme.danger : Theme.brass }
                    ColumnLayout {
                        Layout.fillWidth:true; spacing:5
                        Text { font.family:Theme.bodyFont; text:backend.batteryText; color:Theme.ink; font.pixelSize:Theme.fontSize(13)}
                        Text { font.family:Theme.bodyFont; text:backend.powerText; color:Theme.muted; font.pixelSize:Theme.fontSize(11)}
                    }
                }
                RowLayout {
                    Glyph { symbol:"network" }
                    Text { font.family:Theme.bodyFont; Layout.fillWidth:true; text:backend.network; textFormat:Text.PlainText; wrapMode:Text.WordWrap; color:Theme.ink; font.pixelSize:Theme.fontSize(12)}
                    ActionButton { text:"Settings"; enabled:backend.networkSettingsAvailable; onClicked:backend.openNetworkSettings() }
                }
                Text { font.family:Theme.bodyFont; Layout.fillWidth:true; visible:backend.lastError!==""; text:backend.lastError; textFormat:Text.PlainText; wrapMode:Text.WordWrap; color:Theme.danger; font.pixelSize:Theme.fontSize(11)}
            }
        }
    }
}
