import QtQuick
import "../ui"
import QtQuick.Controls
import QtQuick.Layouts
Item {
    id:root
    required property var backend
    required property var uiState
    function activate() { root.forceActiveFocus();backend.markRead(); }
    ColumnLayout {
        anchors.fill:parent; spacing:16
        PanelHeader {title:"Notifications";symbol:"bell";onClosed:uiState.close()}
        RowLayout {
            Layout.fillWidth:true
            ActionButton { Layout.fillWidth:true; Layout.minimumWidth:0; text:backend.doNotDisturb ? "Do not disturb: on" : "Do not disturb: off"; symbol:"moon"; selected:backend.doNotDisturb; onClicked:backend.toggleDnd(); hint:text }
            Item { Layout.fillWidth:true }
            ActionButton { text:"Clear"; enabled:backend.history.length>0; onClicked:backend.clearHistory() }
        }
        ListView {
            id:historyList; objectName:"notificationHistory"; Layout.fillWidth:true; Layout.fillHeight:true; clip:true; model:backend.history; spacing:10
            ScrollBar.vertical:ScrollBar {}
            delegate: Rectangle {
                id:entry; required property var modelData
                width:historyList.width; height:noteColumn.implicitHeight+28; color:Theme.raised; border.color:Theme.line
                ColumnLayout {
                    id:noteColumn; x:14; y:14; width:parent.width-28; spacing:8
                    RowLayout {
                        Text { font.family:Theme.bodyFont; text:entry.modelData.app; textFormat:Text.PlainText; elide:Text.ElideRight; color:Theme.brass; font.pixelSize:Theme.fontSize(10); Layout.fillWidth:true }
                        Text { font.family:Theme.bodyFont; text:entry.modelData.time; color:Theme.muted; font.pixelSize:Theme.fontSize(10)}
                        ActionButton { symbol:"close"; width:25; height:25; padding:4; onClicked:backend.dismissHistory(entry.modelData.key) }
                    }
                    Text { font.family:Theme.bodyFont; Layout.fillWidth:true; text:entry.modelData.title; textFormat:Text.PlainText; wrapMode:Text.WordWrap; color:Theme.ink; font.pixelSize:Theme.fontSize(14)}
                    Text { font.family:Theme.bodyFont; Layout.fillWidth:true; visible:text!==""; text:entry.modelData.body; textFormat:Text.PlainText; wrapMode:Text.WordWrap; color:Theme.muted; font.pixelSize:Theme.fontSize(12); maximumLineCount:5; elide:Text.ElideRight }
                    NotificationActions {width:noteColumn.width;actions:entry.modelData.actions || [];notificationKey:entry.modelData.key;backend:root.backend}
                }
            }
            Text { anchors.centerIn:parent; visible:historyList.count===0; text:"Nothing here yet"; color:Theme.muted; font.family:Theme.displayFont; font.pixelSize:Theme.fontSize(20)}
        }
    }
}
