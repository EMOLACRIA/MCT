import QtQuick
import "../ui"
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
        x:centered ? (root.width-width)/2 : SurfaceLayout.panelSide(uiState.activePanel)==="left" ? SurfaceLayout.panelSideMargin : root.width-width-SurfaceLayout.panelSideMargin
        y:centered ? (root.height-height)/2 : SurfaceLayout.panelTop
        MouseArea { anchors.fill:parent }
        PanelSlot {anchors.fill:parent;anchors.margins:SurfaceLayout.panelPadding;panel:"launcher";uiState:root.uiState;sourceComponent:launcher;onShown:appear.restart()}
        PanelSlot {anchors.fill:parent;anchors.margins:SurfaceLayout.panelPadding;panel:"power";uiState:root.uiState;sourceComponent:power;onShown:appear.restart()}
        PanelSlot {anchors.fill:parent;anchors.margins:SurfaceLayout.panelPadding;panel:"controls";uiState:root.uiState;sourceComponent:controls;onShown:appear.restart()}
        PanelSlot {anchors.fill:parent;anchors.margins:SurfaceLayout.panelPadding;panel:"notifications";uiState:root.uiState;sourceComponent:notifications;onShown:appear.restart()}
        PanelSlot {anchors.fill:parent;anchors.margins:SurfaceLayout.panelPadding;panel:"media";uiState:root.uiState;sourceComponent:media;onShown:appear.restart()}
        PanelSlot {anchors.fill:parent;anchors.margins:SurfaceLayout.panelPadding;panel:"hardware";uiState:root.uiState;sourceComponent:hardware;onShown:appear.restart()}
        PanelSlot {anchors.fill:parent;anchors.margins:SurfaceLayout.panelPadding;panel:"settings";uiState:root.uiState;sourceComponent:settings;onShown:appear.restart()}
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
