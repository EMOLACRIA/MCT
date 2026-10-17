import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
Item {
    id:root
    required property var backend
    required property var uiState
    property int selectedIndex:0
    readonly property var actions: [
        {code:"lock",name:"Lock",symbol:"lock",detail:"Keep your session running"},
        {code:"suspend",name:"Suspend",symbol:"moon",detail:"Put the computer to sleep"},
        {code:"logout",name:"Log out",symbol:"logout",detail:"Return to the sign-in screen"},
        {code:"restart",name:"Restart",symbol:"restart",detail:"Restart the computer"},
        {code:"poweroff",name:"Power off",symbol:"power",detail:"Shut down the computer"}
    ]
    function activate() { root.forceActiveFocus(); selectedIndex=0; }
    function choose(code) { if(["logout","restart","poweroff"].indexOf(code)>=0)uiState.confirmation=code; else {backend.sessionAction(code);uiState.close();} }
    function confirm() { const code=uiState.confirmation;uiState.close();backend.sessionAction(code); }
    Keys.onUpPressed:selectedIndex=Math.max(0,selectedIndex-1)
    Keys.onDownPressed:selectedIndex=Math.min(4,selectedIndex+1)
    Keys.onReturnPressed:if(!uiState.confirmation)choose(actions[selectedIndex].code)
    Keys.onEnterPressed:if(!uiState.confirmation)choose(actions[selectedIndex].code)
    ColumnLayout {
        anchors.fill:parent; spacing:18
        RowLayout {
            Glyph { symbol:"power"; width:25; height:25 }
            Text { text:uiState.confirmation ? "Confirm" : "Session"; color:Theme.ink; font.family:Theme.displayFont; font.pixelSize:Theme.fontSize(26); Layout.fillWidth:true }
            ActionButton { symbol:"close"; width:36; height:36; padding:8; onClicked:uiState.close() }
        }
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
                                Text { Layout.fillWidth:true; text:powerButton.modelData.name; elide:Text.ElideRight; color:Theme.ink; font.pixelSize:Theme.fontSize(15)}
                                Text { Layout.fillWidth:true; text:powerButton.modelData.detail; elide:Text.ElideRight; color:Theme.muted; font.pixelSize:Theme.fontSize(11)}
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
            Text { text:"Save your work before continuing."; color:Theme.muted; font.pixelSize:Theme.fontSize(12)}
            Item { Layout.fillHeight:true }
            RowLayout {
                Layout.alignment:Qt.AlignRight; spacing:12
                ActionButton { objectName:"cancelPower"; text:"Cancel"; onClicked:uiState.confirmation="" }
                ActionButton { objectName:"confirmPower"; symbol:"power"; text:"Confirm"; destructive:true; onClicked:root.confirm() }
            }
        }
        Text { text:"Esc Close"; color:Theme.brass; font.pixelSize:Theme.fontSize(10)}
    }
}
