import QtQuick
import QtQuick.Controls
ToolTip {
    id:root;objectName:"surfaceHint"
    padding:8
    implicitWidth:Math.min(360,contentItem.implicitWidth+leftPadding+rightPadding)
    contentItem:Text {
        text:root.text;textFormat:Text.PlainText;wrapMode:Text.Wrap
        color:Theme.ink;font.family:Theme.bodyFont;font.pixelSize:Theme.fontSize(11)
    }
    background:Rectangle {color:Theme.raised;border.color:Theme.line}
}
