import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
Item {
    id:root
    required property var backend
    required property var uiState
    function activate() { root.forceActiveFocus();backend.markRead(); }
    ColumnLayout {
        anchors.fill:parent; spacing:16
        RowLayout {
            Glyph { symbol:"bell"; width:25; height:25 }
            Text { text:"Notifications"; color:Theme.ink; font.family:Theme.displayFont; font.pixelSize:Theme.fontSize(26); Layout.fillWidth:true }
            ActionButton { symbol:"close"; width:36; height:36; padding:8; onClicked:uiState.close() }
        }
        RowLayout {
            Layout.fillWidth:true
            ActionButton { Layout.fillWidth:true; Layout.minimumWidth:0; text:backend.doNotDisturb ? "Do not disturb: on" : "Do not disturb: off"; symbol:"moon"; selected:backend.doNotDisturb; onClicked:backend.toggleDnd(); ToolTip.visible:hovered; ToolTip.text:text }
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
                        Text { text:entry.modelData.app; textFormat:Text.PlainText; elide:Text.ElideRight; color:Theme.brass; font.pixelSize:Theme.fontSize(10); Layout.fillWidth:true }
                        Text { text:entry.modelData.time; color:Theme.muted; font.pixelSize:Theme.fontSize(10)}
                        ActionButton { symbol:"close"; width:25; height:25; padding:4; onClicked:backend.dismissHistory(entry.modelData.key) }
                    }
                    Text { Layout.fillWidth:true; text:entry.modelData.title; textFormat:Text.PlainText; wrapMode:Text.WordWrap; color:Theme.ink; font.pixelSize:Theme.fontSize(14)}
                    Text { Layout.fillWidth:true; visible:text!==""; text:entry.modelData.body; textFormat:Text.PlainText; wrapMode:Text.WordWrap; color:Theme.muted; font.pixelSize:Theme.fontSize(12); maximumLineCount:5; elide:Text.ElideRight }
                    Flow {
                        width:noteColumn.width; spacing:6
                        Repeater {
                            model:entry.modelData.actions || []
                            delegate: ActionButton { required property var modelData; objectName:"notificationAction-"+modelData.id; width:Math.min(implicitWidth,noteColumn.width); text:modelData.text; height:32; onClicked:backend.notificationAction(entry.modelData.key,modelData.id); ToolTip.visible:hovered; ToolTip.text:text }
                        }
                    }
                }
            }
            Text { anchors.centerIn:parent; visible:historyList.count===0; text:"Nothing here yet"; color:Theme.muted; font.family:Theme.displayFont; font.pixelSize:Theme.fontSize(20)}
        }
    }
}
