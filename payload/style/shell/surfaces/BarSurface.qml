import QtQuick
import "../ui"
import QtQuick.Controls
import QtQuick.Layouts
Item {
    property Component barBackground:Component {OrnamentFrame {}}
    property real workspaceRadius:1
    property int clockSize:22
    Loader {anchors.fill:parent;sourceComponent:root.barBackground}
    id: root
    required property var backend
    required property var uiState
    property string screenToken: ""
    property var nativeWindow: null
    property Component hintPopup:null
    implicitHeight:SurfaceLayout.barHeight
    Row {
        id:leftGroup
        anchors.left:parent.left; anchors.leftMargin:14; anchors.verticalCenter:parent.verticalCenter; spacing:root.width<800 ? 2 : root.width<1100 ? 3 : 7
        ActionButton { width:34; height:34; padding:7; symbol:"search"; onClicked:uiState.toggle("launcher",root.screenToken); hintPopup:root.hintPopup; hint:"Applications · Super+R" }
        Rectangle { width:1; height:22; color:Theme.line; anchors.verticalCenter:parent.verticalCenter }
        Repeater {
            model:backend.workspaces
            delegate: AbstractButton {
                id: workspaceButton
                required property var modelData
                width:root.width<800 ? 18 : 28; height:32; hoverEnabled:true; activeFocusOnTab:true
                readonly property bool chosen: backend.workspaceActive(modelData.id,root.screenToken)
                Accessible.name:"Workspace " + modelData.id
                background: Rectangle { color:workspaceButton.chosen ? Theme.activeWorkspaceSurface : workspaceButton.hovered ? Theme.raised : "transparent"; border.color:workspaceButton.chosen ? Theme.line : "transparent" }
                contentItem: Item {
                    Text { font.family:Theme.bodyFont; anchors.centerIn:parent; anchors.verticalCenterOffset:-2; text:workspaceButton.modelData.id; color:workspaceButton.chosen ? Theme.ink : workspaceButton.modelData.count ? Theme.brass : Theme.muted; font.pixelSize:Theme.fontSize(12)}
                    Rectangle { anchors.bottom:parent.bottom; anchors.bottomMargin:2; anchors.horizontalCenter:parent.horizontalCenter; width:workspaceButton.chosen ? 14 : 3; height:workspaceButton.chosen ? 2 : 3; radius:root.workspaceRadius; visible:workspaceButton.chosen || workspaceButton.modelData.count > 0; color:Theme.brass }
                }
                onClicked:backend.activateWorkspace(modelData.id)
                SurfaceHint {active:workspaceButton.visible && workspaceButton.hovered && !workspaceButton.pressed;text:workspaceButton.modelData.count+" windows";target:workspaceButton;popupComponent:root.hintPopup}
            }
        }
    }
    Column {
        id:clockGroup; objectName:"barClock"
        // Keep the clock centered; a long date yields space to tray navigation.
        readonly property real trayReserve:Theme.preferences.barShowTray ? Math.min(56,Math.max(0,backend.trayItems.length*29-5)) : 0
        readonly property real maximumWidth:Math.max(clockTime.implicitWidth,Math.min(root.width-2*(leftGroup.x+leftGroup.width+12),2*(rightGroup.x-root.width/2-trayReserve-16)))
        anchors.centerIn:parent; spacing:1
        Text { id:clockTime; anchors.horizontalCenter:parent.horizontalCenter; text:backend.clock; color:Theme.ink; font.family:Theme.displayFont; font.pixelSize:Theme.fontSize(root.clockSize)}
        Text { font.family:Theme.bodyFont; objectName:"barDate";anchors.horizontalCenter:parent.horizontalCenter; width:Math.min(implicitWidth,clockGroup.maximumWidth); horizontalAlignment:Text.AlignHCenter; elide:Text.ElideRight; visible:Theme.preferences.barShowDate; text:root.width<1100 ? backend.date.split("·").slice(-1).join("·").trim() : backend.date; color:Theme.brass; font.pixelSize:Theme.fontSize(9); font.letterSpacing:1.2 }
    }
    Row {
        id:rightGroup; objectName:"barActions"
        anchors.right:parent.right; anchors.rightMargin:14; anchors.verticalCenter:parent.verticalCenter; spacing:root.width<800 ? 2 : 5
        ActionButton { width:32; height:34; padding:7; symbol:"hardware"; onClicked:uiState.toggle("hardware",root.screenToken); hintPopup:root.hintPopup; hint:"Hardware · Super+T" }
        ActionButton { width:32; height:34; padding:7; symbol:"music"; onClicked:uiState.toggle("media",root.screenToken); hintPopup:root.hintPopup; hint:"Media" }
        ActionButton { width:32; height:34; padding:7; symbol:"bell"; selected:backend.unread > 0; onClicked: {backend.markRead();uiState.toggle("notifications",root.screenToken);} hintPopup:root.hintPopup;hint:"Notifications · Super+B" }
        ActionButton { width:text ? implicitWidth : 32; height:34; padding:7; symbol:backend.muted ? "mute" : "audio"; text:root.width>1050 ? backend.volume + "%" : ""; onClicked:uiState.toggle("controls",root.screenToken); hintPopup:root.hintPopup; hint:"Sound and brightness" }
        ActionButton { width:32; height:34; padding:7; symbol:"network"; onClicked:uiState.toggle("controls",root.screenToken); hintPopup:root.hintPopup; hint:backend.network }
        ActionButton { width:text ? implicitWidth : 32; height:34; padding:7; symbol:"battery"; iconLevel:backend.battery; iconCharging:backend.batteryCharging; iconColor:backend.battery>=0 && backend.battery<=15 && !backend.batteryCharging ? Theme.danger : Theme.brass; text:root.width>1050 && backend.battery >= 0 ? backend.battery + "%" : ""; onClicked:uiState.toggle("controls",root.screenToken); hintPopup:root.hintPopup; hint:backend.batteryText }
        Rectangle { width:1; height:22; color:Theme.line; anchors.verticalCenter:parent.verticalCenter }
        ActionButton { width:34; height:34; padding:7; symbol:"power"; onClicked:uiState.toggle("power",root.screenToken); hintPopup:root.hintPopup; hint:"Session · Super+M" }
    }
    Item {
        id:tray; objectName:"barTray"
        readonly property real availableWidth:Math.max(0,rightGroup.x-(clockGroup.x+clockGroup.width)-16)
        readonly property real naturalWidth:Math.max(0,trayRow.width)
        readonly property bool overflowing:naturalWidth>availableWidth
        anchors.right:rightGroup.left; anchors.rightMargin:8; anchors.verticalCenter:parent.verticalCenter
        width:Theme.preferences.barShowTray ? Math.min(availableWidth,naturalWidth+(overflowing ? 32 : 0)) : 0
        height:32; visible:width>=24
        AbstractButton {
            objectName:"trayPrevious"; width:16; height:32; visible:tray.overflowing; enabled:trayViewport.contentX>0
            opacity:enabled ? 1 : .35
            Accessible.name:"Previous tray icons"
            background:Rectangle {color:parent.hovered || parent.activeFocus ? Theme.raised : "transparent"}
            contentItem:Glyph { symbol:"previous"; width:12; height:16 }
            onClicked:trayViewport.step(-1)
        }
        Flickable {
            id:trayViewport; objectName:"trayViewport"
            x:tray.overflowing ? 16 : 0; width:Math.max(0,tray.width-2*x); height:32
            contentWidth:trayRow.width; contentHeight:32; clip:true; interactive:false
            function clamp() {contentX=Math.max(0,Math.min(contentX,Math.max(0,contentWidth-width)));}
            function step(direction) {contentX+=direction*29;clamp();}
            onWidthChanged:clamp()
            onContentWidthChanged:clamp()
            Row {
                id:trayRow; spacing:5
                Repeater {
                    model:Theme.preferences.barShowTray ? backend.trayItems : []
                    delegate: Item {
                        id:trayIcon; objectName:"trayIcon-"+index
                        required property var modelData
                        required property int index
                        width:24; height:32
                        Image { anchors.centerIn:parent; width:17; height:17; source:trayIcon.modelData.icon; fillMode:Image.PreserveAspectFit }
                        MouseArea {
                            anchors.fill:parent; acceptedButtons:Qt.LeftButton|Qt.RightButton|Qt.MiddleButton; hoverEnabled:true
                            onClicked:mouse=> {const p=trayIcon.mapToItem(root,0,trayIcon.height);backend.trayClick(trayIcon.index,mouse.button,root.nativeWindow,p.x,p.y);}
                            onWheel:wheel=>backend.trayScroll(trayIcon.index,wheel.angleDelta.y)
                            SurfaceHint {active:parent.visible && parent.containsMouse && !parent.pressed;text:trayIcon.modelData.title;target:trayIcon;popupComponent:root.hintPopup}
                        }
                    }
                }
            }
        }
        AbstractButton {
            objectName:"trayNext"; anchors.right:parent.right; width:16; height:32; visible:tray.overflowing
            enabled:trayViewport.contentX<trayViewport.contentWidth-trayViewport.width
            opacity:enabled ? 1 : .35
            Accessible.name:"Next tray icons"
            background:Rectangle {color:parent.hovered || parent.activeFocus ? Theme.raised : "transparent"}
            contentItem:Glyph { symbol:"next"; width:12; height:16 }
            onClicked:trayViewport.step(1)
        }
    }
}
