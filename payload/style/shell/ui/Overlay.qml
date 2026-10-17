import QtQuick
FocusScope {
    id:root
    required property var backend
    required property var uiState
    visible:uiState.activePanel!==""
    focus:visible
    Keys.onEscapePressed:uiState.close()
    Rectangle { anchors.fill:parent; color:"#55000000" }
    MouseArea { anchors.fill:parent; onClicked:uiState.close() }
    OrnamentFrame {
        id:frame; objectName:"activePanelFrame"
        readonly property bool centered:uiState.activePanel==="launcher" || uiState.activePanel==="power" || uiState.activePanel==="hardware"
        width:Math.max(250,Math.min(root.width-48,uiState.activePanel==="hardware" ? 650 : uiState.activePanel==="launcher" ? 620 : uiState.activePanel==="power" ? 550 : uiState.activePanel==="notifications" ? 460 : 420))
        height:Math.max(210,Math.min(root.height-100,uiState.activePanel==="hardware" ? 660 : uiState.activePanel==="launcher" ? 580 : uiState.activePanel==="power" ? uiState.confirmation ? 260 : 465 : uiState.activePanel==="notifications" ? 650 : uiState.activePanel==="controls" ? 610 : 520))
        x:centered ? (root.width-width)/2 : root.width-width-16
        y:centered ? (root.height-height)/2 : 74
        MouseArea { anchors.fill:parent }
        Loader {
            id:content; anchors.fill:parent; anchors.margins:24
            sourceComponent:uiState.activePanel==="launcher" ? launcher : uiState.activePanel==="power" ? power : uiState.activePanel==="controls" ? controls : uiState.activePanel==="notifications" ? notifications : uiState.activePanel==="media" ? media : uiState.activePanel==="hardware" ? hardware : null
            onLoaded: {appear.restart();activateContent.restart();}
            Timer {id:activateContent;interval:0;onTriggered:if(content.item && content.item.activate)content.item.activate()}
        }
        NumberAnimation { id:appear; target:frame; property:"opacity"; from:0; to:1; duration:140; easing.type:Easing.OutQuad }
    }
    Component { id:launcher; Launcher { backend:root.backend; uiState:root.uiState } }
    Component { id:power; Power { backend:root.backend; uiState:root.uiState } }
    Component { id:controls; Controls { backend:root.backend; uiState:root.uiState } }
    Component { id:notifications; Notifications { backend:root.backend; uiState:root.uiState } }
    Component { id:hardware; Hardware { backend:root.backend; uiState:root.uiState } }
    Component { id:media; Media { backend:root.backend; uiState:root.uiState } }
}
