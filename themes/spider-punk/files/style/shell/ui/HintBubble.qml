import QtQuick
Rectangle {
    id:root
    required property string text
    implicitWidth:Math.min(360,label.implicitWidth+16)
    implicitHeight:label.implicitHeight+16
    color:Theme.raised;border.color:Theme.line
    Text {
        id:label;x:8;y:8;width:Math.max(0,parent.width-16)
        text:root.text;textFormat:Text.PlainText;wrapMode:Text.Wrap
        color:Theme.ink;font.family:Theme.bodyFont;font.pixelSize:Theme.fontSize(11)
    }
}
