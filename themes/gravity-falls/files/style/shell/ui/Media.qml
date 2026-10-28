import QtQuick
import QtQuick.Layouts
import "../surfaces"
MediaSurface {
    id:mediaSkin
    metadataComponent:Component {
                RowLayout {
                    Layout.fillWidth:true;spacing:16
                    Rectangle {
                        Layout.preferredWidth:84;Layout.preferredHeight:84;color:Theme.raised;border.color:Theme.line
                        Image {id:cover;anchors.fill:parent;anchors.margins:1;source:mediaSkin.backend.mediaArt || Theme.wallpaper;fillMode:Image.PreserveAspectCrop;smooth:true;asynchronous:true}
                        Glyph {anchors.centerIn:parent;width:40;height:40;symbol:"music";visible:cover.status!==Image.Ready}
                    }
                    ColumnLayout {
                        Layout.fillWidth:true;Layout.minimumWidth:0;spacing:10
                        Text {Layout.fillWidth:true;text:mediaSkin.backend.mediaTitle || "No active player";textFormat:Text.PlainText;wrapMode:Text.WordWrap;maximumLineCount:2;elide:Text.ElideRight;color:Theme.ink;font.family:Theme.displayFont;font.pixelSize:Theme.fontSize(16)}
                        Text {Layout.fillWidth:true;text:mediaSkin.backend.mediaArtist;textFormat:Text.PlainText;elide:Text.ElideRight;color:Theme.muted;font.family:Theme.bodyFont;font.pixelSize:Theme.fontSize(11)}
                    }
                }
    }
}
