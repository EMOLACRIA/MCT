import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Window
FocusScope {
    id:root
    objectName:"windowSwitcher"
    required property var controller
    property Component previewComponent:null
    visible:controller.active
    focus:visible
    property bool hadWindowFocus:false
    readonly property bool windowActive:Window.window ? Window.window.active : false
    onWindowActiveChanged: {
        if(windowActive)hadWindowFocus=true;
        else if(hadWindowFocus && controller.active)controller.cancel();
    }
    onVisibleChanged: {
        hadWindowFocus=visible && windowActive;
        if(visible)Qt.callLater(()=>{if(root.visible)root.forceActiveFocus();});
    }
    Keys.onPressed:event=> {
        if(event.key===Qt.Key_Tab || event.key===Qt.Key_Backtab) {controller.step(event.key===Qt.Key_Backtab || (event.modifiers & Qt.ShiftModifier) ? -1 : 1);event.accepted=true;}
        else if(event.key===Qt.Key_Left || event.key===Qt.Key_Up) {controller.step(-1);event.accepted=true;}
        else if(event.key===Qt.Key_Right || event.key===Qt.Key_Down) {controller.step(1);event.accepted=true;}
        else if(event.key===Qt.Key_Return || event.key===Qt.Key_Enter) {controller.commit();event.accepted=true;}
        else if(event.key===Qt.Key_Escape) {controller.cancel();event.accepted=true;}
    }
    Keys.onReleased:event=> {if(event.key===Qt.Key_Alt && !event.isAutoRepeat) {controller.commit();event.accepted=true;}}
    Rectangle {anchors.fill:parent;color:"#880c0d0b"}
    MouseArea {anchors.fill:parent;onClicked:controller.cancel()}
    OrnamentFrame {
        id:frame;objectName:"windowSwitcherFrame"
        anchors.centerIn:parent
        width:Math.max(200,Math.min(parent.width-40,960))
        height:Math.max(180,Math.min(parent.height-80,590))
        MouseArea {anchors.fill:parent}
        ColumnLayout {
            anchors.fill:parent;anchors.margins:24;spacing:16
            RowLayout {
                Glyph {symbol:"windows";width:24;height:24}
                Text {text:"Windows";font.family:Theme.displayFont;font.pixelSize:27;color:Theme.ink;Layout.fillWidth:true}
                Text {text:controller.entries.length+" open";color:Theme.brass;font.pixelSize:11}
            }
            RowLayout {
                Layout.fillWidth:true;Layout.fillHeight:true;spacing:22
                ListView {
                    id:list;objectName:"windowSwitcherList"
                    Layout.fillWidth:true;Layout.preferredWidth:500;Layout.fillHeight:true;clip:true;spacing:5
                    model:controller.entries;currentIndex:controller.selectedIndex
                    onCurrentIndexChanged:if(currentIndex>=0)positionViewAtIndex(currentIndex,ListView.Contain)
                    ScrollBar.vertical:ScrollBar {}
                    delegate:Item {
                        id:row;required property var modelData
                        width:list.width;height:72
                        Rectangle {anchors.fill:parent;color:root.controller.selectedId===row.modelData.id ? Theme.raised : "transparent";border.color:root.controller.selectedId===row.modelData.id ? Theme.brass : "transparent"}
                        Image {id:icon;x:12;anchors.verticalCenter:parent.verticalCenter;width:26;height:26;source:row.modelData.icon || "";fillMode:Image.PreserveAspectFit}
                        Glyph {x:15;anchors.verticalCenter:parent.verticalCenter;symbol:"windows";visible:icon.status!==Image.Ready}
                        Column {
                            x:52;y:12;width:parent.width-64;spacing:4
                            Text {width:parent.width;text:row.modelData.appName;textFormat:Text.PlainText;elide:Text.ElideRight;color:Theme.ink;font.pixelSize:13}
                            Text {width:parent.width;text:row.modelData.title;textFormat:Text.PlainText;elide:Text.ElideRight;color:Theme.muted;font.pixelSize:11}
                            Text {width:parent.width;text:"Workspace "+row.modelData.workspaceLabel+(row.modelData.monitor ? " · "+row.modelData.monitor : "");textFormat:Text.PlainText;elide:Text.ElideRight;color:Theme.brass;font.pixelSize:10}
                        }
                        MouseArea {anchors.fill:parent;onClicked:{controller.choose(row.modelData.id);controller.commit();}}
                    }
                }
                ColumnLayout {
                    visible:frame.width>=730;Layout.minimumWidth:340;Layout.preferredWidth:340;Layout.maximumWidth:340;Layout.fillHeight:true;spacing:13
                    Rectangle {
                        Layout.fillWidth:true;Layout.fillHeight:true;color:Theme.background;border.color:Theme.line;clip:true
                        Column {
                            anchors.centerIn:parent;spacing:14;visible:!capture.item || !capture.item.hasContent
                            Glyph {anchors.horizontalCenter:parent.horizontalCenter;width:48;height:48;symbol:"windows"}
                            Text {anchors.horizontalCenter:parent.horizontalCenter;text:controller.selected ? controller.selected.appName : "";textFormat:Text.PlainText;color:Theme.muted;font.pixelSize:13}
                        }
                        Loader {id:capture;anchors.fill:parent;anchors.margins:10;active:root.visible && root.previewComponent!==null;sourceComponent:root.previewComponent}
                    }
                    Text {Layout.fillWidth:true;text:controller.selected ? controller.selected.title : "";textFormat:Text.PlainText;wrapMode:Text.WordWrap;maximumLineCount:2;elide:Text.ElideRight;color:Theme.ink;font.family:Theme.displayFont;font.pixelSize:21}
                    Text {Layout.fillWidth:true;text:controller.selected ? "Workspace "+controller.selected.workspaceLabel+(controller.selected.monitor ? " · "+controller.selected.monitor : "") : "";textFormat:Text.PlainText;color:Theme.brass;font.pixelSize:11}
                }
            }
            Text {Layout.fillWidth:true;text:frame.width<600 ? "Tab / Shift+Tab · Select\nRelease Alt / Enter · Open     Esc · Cancel" : "Tab / Shift+Tab · Select      Release Alt / Enter · Open      Esc · Cancel";wrapMode:Text.WordWrap;color:Theme.brass;font.pixelSize:10}
        }
    }
}
