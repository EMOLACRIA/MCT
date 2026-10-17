import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
OrnamentFrame {
    id: root
    required property var backend
    required property var uiState
    property string screenToken: ""
    property var nativeWindow: null
    implicitHeight: 48
    Row {
        id:leftGroup
        anchors.left:parent.left; anchors.leftMargin:14; anchors.verticalCenter:parent.verticalCenter; spacing:root.width<1100 ? 3 : 7
        ActionButton { width:34; height:34; padding:7; symbol:"search"; onClicked:uiState.toggle("launcher",root.screenToken); ToolTip.visible:hovered; ToolTip.text:"Applications · Super+R" }
        Rectangle { width:1; height:22; color:Theme.line; anchors.verticalCenter:parent.verticalCenter }
        Repeater {
            model:backend.workspaces
            delegate: AbstractButton {
                id: workspaceButton
                required property var modelData
                width:root.width<800 ? 20 : 28; height:32; hoverEnabled:true; activeFocusOnTab:true
                readonly property bool chosen: backend.workspaceActive(modelData.id,root.screenToken)
                Accessible.name:"Workspace " + modelData.id
                background: Rectangle { color:workspaceButton.chosen ? "#35362d" : workspaceButton.hovered ? Theme.raised : "transparent"; border.color:workspaceButton.chosen ? Theme.line : "transparent" }
                contentItem: Item {
                    Text { anchors.centerIn:parent; anchors.verticalCenterOffset:-2; text:workspaceButton.modelData.id; color:workspaceButton.chosen ? Theme.ink : workspaceButton.modelData.count ? Theme.brass : Theme.muted; font.pixelSize:Theme.fontSize(12)}
                    Rectangle { anchors.bottom:parent.bottom; anchors.bottomMargin:2; anchors.horizontalCenter:parent.horizontalCenter; width:workspaceButton.chosen ? 14 : 3; height:workspaceButton.chosen ? 2 : 3; radius:1; visible:workspaceButton.chosen || workspaceButton.modelData.count > 0; color:Theme.brass }
                }
                onClicked:backend.activateWorkspace(modelData.id)
                ToolTip.visible:hovered; ToolTip.text: modelData.count + " windows"
            }
        }
    }
    Column {
        anchors.centerIn:parent; spacing:1
        Text { anchors.horizontalCenter:parent.horizontalCenter; text:backend.clock; color:Theme.ink; font.family:Theme.displayFont; font.pixelSize:Theme.fontSize(22)}
        Text { objectName:"barDate";anchors.horizontalCenter:parent.horizontalCenter; visible:Theme.preferences.barShowDate; text:root.width<1100 ? backend.date.split("·").slice(-1).join("·").trim() : backend.date; color:Theme.brass; font.pixelSize:Theme.fontSize(9); font.letterSpacing:1.2 }
    }
    Row {
        anchors.right:parent.right; anchors.rightMargin:14; anchors.verticalCenter:parent.verticalCenter; spacing:5
        Repeater {
            model:Theme.preferences.barShowTray ? backend.trayItems : []
            delegate: Item {
                id: trayIcon
                required property var modelData
                required property int index
                width:24; height:32
                Image { anchors.centerIn:parent; width:17; height:17; source:trayIcon.modelData.icon; fillMode:Image.PreserveAspectFit }
                MouseArea {
                    anchors.fill:parent; acceptedButtons:Qt.LeftButton|Qt.RightButton|Qt.MiddleButton; hoverEnabled:true
                    onClicked:mouse=> { const p=trayIcon.mapToItem(root,0,trayIcon.height); backend.trayClick(trayIcon.index,mouse.button,root.nativeWindow,p.x,p.y); }
                    onWheel:wheel=>backend.trayScroll(trayIcon.index,wheel.angleDelta.y)
                    ToolTip.visible:containsMouse; ToolTip.text:trayIcon.modelData.title
                }
            }
        }
        ActionButton { width:32; height:34; padding:7; symbol:"hardware"; onClicked:uiState.toggle("hardware",root.screenToken); ToolTip.visible:hovered; ToolTip.text:"Hardware · Super+T" }
        ActionButton { width:32; height:34; padding:7; symbol:"music"; onClicked:uiState.toggle("media",root.screenToken); ToolTip.visible:hovered; ToolTip.text:"Media" }
        ActionButton { width:32; height:34; padding:7; symbol:"bell"; selected:backend.unread > 0; onClicked: {backend.markRead();uiState.toggle("notifications",root.screenToken);} ToolTip.visible:hovered; ToolTip.text:"Notifications · Super+B" }
        ActionButton { height:34; padding:7; symbol:backend.muted ? "mute" : "audio"; text:root.width>1050 ? backend.volume + "%" : ""; onClicked:uiState.toggle("controls",root.screenToken); ToolTip.visible:hovered; ToolTip.text:"Sound and brightness" }
        ActionButton { width:32; height:34; padding:7; symbol:"network"; onClicked:uiState.toggle("controls",root.screenToken); ToolTip.visible:hovered; ToolTip.text:backend.network }
        ActionButton { height:34; padding:7; symbol:"battery"; iconLevel:backend.battery; iconCharging:backend.batteryCharging; iconColor:backend.battery>=0 && backend.battery<=15 && !backend.batteryCharging ? Theme.danger : Theme.brass; text:root.width>1050 && backend.battery >= 0 ? backend.battery + "%" : ""; onClicked:uiState.toggle("controls",root.screenToken); ToolTip.visible:hovered; ToolTip.text:backend.batteryText }
        Rectangle { width:1; height:22; color:Theme.line; anchors.verticalCenter:parent.verticalCenter }
        ActionButton { width:34; height:34; padding:7; symbol:"power"; onClicked:uiState.toggle("power",root.screenToken); ToolTip.visible:hovered; ToolTip.text:"Session · Super+M" }
    }
}
