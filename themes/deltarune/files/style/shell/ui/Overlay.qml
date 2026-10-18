import QtQuick
FocusScope {
    id:root
    required property var backend
    required property var uiState
    visible:uiState.activePanel!==""
    focus:visible
    Keys.onEscapePressed:uiState.close()
    Rectangle { anchors.fill:parent; color:Theme.panelScrim }
    MouseArea { anchors.fill:parent; onClicked:uiState.close() }
    OrnamentFrame {
        id:frame; objectName:"activePanelFrame"
        readonly property bool centered:SurfaceLayout.panelCentered(uiState.activePanel,Theme.preferences.centerPanels)
        width:SurfaceLayout.panelWidth(uiState.activePanel,root.width)
        height:SurfaceLayout.panelHeight(uiState.activePanel,root.height,uiState.confirmation,Theme.fontScale)
        x:centered ? (root.width-width)/2 : uiState.activePanel==="controls" ? root.width-width-SurfaceLayout.panelSideMargin : SurfaceLayout.panelSideMargin
        y:centered ? (root.height-height)/2 : SurfaceLayout.panelTop
        MouseArea { anchors.fill:parent }
        Loader {
            id:content; anchors.fill:parent; anchors.margins:SurfaceLayout.panelPadding
            sourceComponent:uiState.activePanel==="launcher" ? launcher : uiState.activePanel==="power" ? power : uiState.activePanel==="controls" ? controls : uiState.activePanel==="notifications" ? notifications : uiState.activePanel==="media" ? media : uiState.activePanel==="hardware" ? hardware : uiState.activePanel==="settings" ? settings : null
            onLoaded: {appear.restart();activateContent.restart();}
            Timer {id:activateContent;interval:0;onTriggered:if(content.item && content.item.activate)content.item.activate()}
        }
        NumberAnimation { id:appear; target:frame; property:"opacity"; from:0; to:1; duration:Theme.duration(Theme.panelEnterMotion); easing.type:Easing.OutQuad }
    }
    Component { id:launcher; Launcher { backend:root.backend; uiState:root.uiState } }
    Component { id:power; Power { backend:root.backend; uiState:root.uiState } }
    Component { id:controls; Controls { backend:root.backend; uiState:root.uiState } }
    Component { id:notifications; Notifications { backend:root.backend; uiState:root.uiState } }
    Component { id:hardware; Hardware { backend:root.backend; uiState:root.uiState } }
    Component { id:settings; Settings { backend:root.backend; uiState:root.uiState } }
    Component { id:media; Media { backend:root.backend; uiState:root.uiState } }
}
