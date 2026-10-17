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
            Text { Layout.fillWidth:true; text:root.note.app; textFormat:Text.PlainText; elide:Text.ElideRight; color:Theme.brass; font.pixelSize:10 }
            ActionButton { symbol:"close"; width:24; height:24; padding:4; onClicked:backend.dismissToast(note.key) }
        }
        Text { Layout.fillWidth:true; text:root.note.title; textFormat:Text.PlainText; wrapMode:Text.WordWrap; maximumLineCount:2; elide:Text.ElideRight; color:Theme.ink; font.pixelSize:14 }
        Text { Layout.fillWidth:true; visible:text!==""; text:root.note.body; textFormat:Text.PlainText; wrapMode:Text.WordWrap; maximumLineCount:3; elide:Text.ElideRight; color:Theme.muted; font.pixelSize:12 }
        Flow {
            width:body.width; spacing:6
            Repeater { model:root.note.actions || []; delegate:ActionButton { required property var modelData; text:modelData.text; height:32; onClicked:backend.notificationAction(root.note.key,modelData.id) } }
        }
    }
}
