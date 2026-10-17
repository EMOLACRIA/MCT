import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
OrnamentFrame {
    id:root
    required property var note
    required property var backend
    implicitHeight:body.implicitHeight+32
    ColumnLayout {
        id:body; x:16; y:16; width:parent.width-32; spacing:8
        RowLayout {
            Glyph { symbol:"bell"; width:17; height:17 }
            Text { font.family:Theme.bodyFont; Layout.fillWidth:true; text:root.note.app; textFormat:Text.PlainText; elide:Text.ElideRight; color:Theme.brass; font.pixelSize:Theme.fontSize(10)}
            ActionButton { objectName:"dismissToast-"+root.note.key; symbol:"close"; width:24; height:24; padding:4; onClicked:backend.dismissToast(note.key) }
        }
        Text { font.family:Theme.bodyFont; Layout.fillWidth:true; text:root.note.title; textFormat:Text.PlainText; wrapMode:Text.WordWrap; maximumLineCount:2; elide:Text.ElideRight; color:Theme.ink; font.pixelSize:Theme.fontSize(14)}
        Text { font.family:Theme.bodyFont; Layout.fillWidth:true; visible:text!==""; text:root.note.body; textFormat:Text.PlainText; wrapMode:Text.WordWrap; maximumLineCount:3; elide:Text.ElideRight; color:Theme.muted; font.pixelSize:Theme.fontSize(12)}
        NotificationActions {width:body.width;actions:root.note.actions || [];notificationKey:root.note.key;backend:root.backend}
    }
}
