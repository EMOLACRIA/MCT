import QtQuick
import QtQuick.Layouts
RowLayout {
    id:root;objectName:"panelHeader"
    required property string title
    required property string symbol
    property int titleSize:20
    property string statusText:""
    property Component extraAction:null
    signal closed()
    Layout.fillWidth:true
    Image {source:Theme.portraitFor(root.symbol);smooth:false;fillMode:Image.PreserveAspectFit;Layout.preferredWidth:38;Layout.preferredHeight:34}
    Text {
        Layout.fillWidth:true;Layout.minimumWidth:0
        text:root.title;textFormat:Text.PlainText;elide:Text.ElideRight
        color:Theme.ink;font.family:Theme.displayFont;font.pixelSize:Theme.fontSize(root.titleSize)
    }
    Text { font.family:Theme.bodyFont;visible:text!=="";text:root.statusText;color:Theme.brass;font.pixelSize:Theme.fontSize(10);font.letterSpacing:1.5}
    Loader {
        sourceComponent:root.extraAction;visible:active;active:sourceComponent!==null
        Layout.preferredWidth:item ? item.implicitWidth : 0
        Layout.preferredHeight:item ? item.implicitHeight : 0
    }
    ActionButton {
        objectName:"closePanel";symbol:"close";Layout.preferredWidth:36;Layout.preferredHeight:36;padding:8
        Accessible.name:"Close "+root.title
        onClicked:root.closed()
    }
}
