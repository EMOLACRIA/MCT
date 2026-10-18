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
        PanelHeader {title:"Now playing";symbol:"music";onClosed:uiState.close()}
        Flickable {
            id:mediaScroll; objectName:"mediaScroll"
            Layout.fillWidth:true; Layout.fillHeight:true; clip:true
            contentHeight:mediaContent.implicitHeight; boundsBehavior:Flickable.StopAtBounds
            function reveal(item) {
                const p=item.mapToItem(mediaContent,0,0);
                contentY=Math.max(0,Math.min(p.y,Math.max(contentY,p.y+item.height-height)));
            }
            ScrollBar.vertical:ScrollBar {}
            ColumnLayout {
                id:mediaContent; width:mediaScroll.width; spacing:20
                RowLayout {
                    Layout.fillWidth:true;spacing:18
                    Rectangle {
                        Layout.preferredWidth:112;Layout.preferredHeight:112;color:Theme.raised;border.color:Theme.line
                        Image {id:cover;anchors.fill:parent;anchors.margins:1;source:backend.mediaArt || Theme.wallpaper;fillMode:Image.PreserveAspectCrop;smooth:false;asynchronous:true}
                        Glyph {anchors.centerIn:parent;width:40;height:40;symbol:"music";visible:cover.status!==Image.Ready}
                    }
                    ColumnLayout {
                        Layout.fillWidth:true;Layout.minimumWidth:0;spacing:10
                        Text {Layout.fillWidth:true;text:backend.mediaTitle || "No active player";textFormat:Text.PlainText;wrapMode:Text.WordWrap;maximumLineCount:3;elide:Text.ElideRight;color:Theme.ink;font.family:Theme.displayFont;font.pixelSize:Theme.fontSize(18)}
                        Text {Layout.fillWidth:true;text:backend.mediaArtist;textFormat:Text.PlainText;elide:Text.ElideRight;color:Theme.muted;font.family:Theme.bodyFont;font.pixelSize:Theme.fontSize(11)}
                    }
                }
                RowLayout {
                    Layout.alignment:Qt.AlignHCenter; spacing:18
                    ActionButton { symbol:"previous"; enabled:backend.canPrevious; onClicked:backend.mediaCommand("previous") }
                    ActionButton { symbol:backend.mediaPlaying ? "pause" : "play"; width:54; height:48; padding:15; enabled:backend.canPlayPause; onClicked:backend.mediaCommand("toggle") }
                    ActionButton { symbol:"next"; enabled:backend.canNext; onClicked:backend.mediaCommand("next") }
                }
                Flow {
                    Layout.fillWidth:true; spacing:5
                    Repeater {
                        model:backend.players
                        delegate:ActionButton {
                            required property var modelData; objectName:"mediaPlayer-"+modelData.id
                            width:Math.min(implicitWidth,mediaContent.width); text:modelData.name; selected:modelData.selected
                            onClicked:backend.selectPlayer(modelData.id)
                            onActiveFocusChanged:if(activeFocus)mediaScroll.reveal(this)
                            hint:text
                        }
                    }
                }
            }
        }
    }
}
