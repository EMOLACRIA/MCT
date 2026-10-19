import QtQuick
import "../ui"
import "../behavior"
import QtQuick.Controls
import QtQuick.Layouts
PowerController {
    id:root
    ColumnLayout {
        anchors.fill:parent; spacing:18
        PanelHeader {title:uiState.confirmation ? "Confirm" : "Session";symbol:"power";onClosed:uiState.close()}
        Flickable {
            id:powerScroll; objectName:"powerScroll"
            visible:uiState.confirmation===""; Layout.fillWidth:true; Layout.fillHeight:true; clip:true
            contentHeight:Math.max(height,powerActions.implicitHeight); boundsBehavior:Flickable.StopAtBounds
            function revealSelection() {
                const button=powerRepeater.itemAt(root.selectedIndex);
                if(!button)return;
                contentY=Math.max(0,Math.min(button.y,Math.max(contentY,button.y+button.height-height)));
            }
            ScrollBar.vertical:ScrollBar {}
            Connections {target:root;function onSelectedIndexChanged() {powerScroll.revealSelection();}}
            ColumnLayout {
                id:powerActions; width:powerScroll.width; height:Math.max(powerScroll.height,implicitHeight); spacing:6
                Repeater {
                    id:powerRepeater
                    model:root.actions
                    delegate: AbstractButton {
                        id:powerButton; objectName:"sessionAction-"+modelData.code; required property var modelData; required property int index
                        Layout.fillWidth:true; Layout.fillHeight:true; Layout.minimumHeight:implicitHeight
                        implicitHeight:Math.max(58,contentItem.implicitHeight+24); hoverEnabled:true; activeFocusOnTab:true
                        onActiveFocusChanged:if(activeFocus) {root.selectedIndex=index;powerScroll.revealSelection();}
                        Accessible.name:modelData.name
                        background:Rectangle { color:powerButton.hovered || powerButton.activeFocus || root.selectedIndex===powerButton.index ? Theme.raised : "transparent"; border.color:root.selectedIndex===powerButton.index ? Theme.line : "transparent" }
                        contentItem:RowLayout {
                            anchors.fill:parent; anchors.margins:12; spacing:17
                            Glyph { symbol:powerButton.modelData.symbol; width:24; height:24 }
                            ColumnLayout {
                                Layout.fillWidth:true; spacing:4
                                Text { font.family:Theme.bodyFont; Layout.fillWidth:true; text:powerButton.modelData.name; elide:Text.ElideRight; color:Theme.ink; font.pixelSize:Theme.fontSize(15)}
                                Text { font.family:Theme.bodyFont; Layout.fillWidth:true; text:powerButton.modelData.detail; elide:Text.ElideRight; color:Theme.muted; font.pixelSize:Theme.fontSize(11)}
                            }
                        }
                        onClicked:root.choose(modelData.code)
                    }
                }
            }
        }
        ColumnLayout {
            visible:uiState.confirmation!==""; Layout.fillWidth:true; Layout.fillHeight:true; spacing:18
            Text { Layout.fillWidth:true; wrapMode:Text.WordWrap; text:uiState.confirmation==="logout" ? "Log out of this session?" : uiState.confirmation==="restart" ? "Restart the computer?" : "Power off the computer?"; color:Theme.ink; font.family:Theme.displayFont; font.pixelSize:Theme.fontSize(23)}
            Text { font.family:Theme.bodyFont; text:"Save your work before continuing."; color:Theme.muted; font.pixelSize:Theme.fontSize(12)}
            Item { Layout.fillHeight:true }
            RowLayout {
                Layout.alignment:Qt.AlignRight; spacing:12
                ActionButton { objectName:"cancelPower"; text:"Cancel"; onClicked:uiState.confirmation="" }
                ActionButton { objectName:"confirmPower"; symbol:"power"; text:"Confirm"; destructive:true; onClicked:root.confirm() }
            }
        }
        Text { font.family:Theme.bodyFont; text:"Esc Close"; color:Theme.brass; font.pixelSize:Theme.fontSize(10)}
    }
}
