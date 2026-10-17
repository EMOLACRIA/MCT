import QtQuick
import QtQuick.Controls
import "ui"
Item {
    id:root
    objectName:"previewScene"
    width:1600; height:1000
    property alias uiState:shellState
    property alias backend:demo
    Image { anchors.fill:parent; source:Theme.wallpaper; fillMode:Image.PreserveAspectCrop }
    DemoContext { id:demo }
    Binding {target:Theme;property:"preferences";value:demo.preferences.values}
    UiState { id:shellState; objectName:"uiState";onActivePanelChanged:if(activePanel!=="")switcher.cancel() }
    WindowSwitcherState {id:switcher;objectName:"windowSwitcherState";windows:demo.windows;activeWindowId:demo.activeWindowId;onCommitted:windowId=>demo.activateWindow(windowId)}
    function cycleWindows(direction) {shellState.close();switcher.begin(direction,"preview");}
    Connections { target:demo; function onFeedbackRequested(kind,level,muted) {shellState.showFeedback(kind,level,muted);} }
    Bar { x:Theme.preferences.barFloating ? SurfaceLayout.barSideMargin : 0; y:Theme.preferences.barFloating ? SurfaceLayout.barTopMargin : 0; width:parent.width-2*x; height:SurfaceLayout.barHeight; backend:demo; uiState:shellState; screenToken:"preview" }
    ToastStack {
        backend:demo;visible:demo.toasts.length>0 && shellState.activePanel===""
        x:parent.width-width-SurfaceLayout.toastSideMargin;y:SurfaceLayout.toastTop;width:SurfaceLayout.toastWidth
    }
    Overlay { anchors.fill:parent; backend:demo; uiState:shellState }
    WindowSwitcher {anchors.fill:parent;controller:switcher}
    Feedback { anchors.horizontalCenter:parent.horizontalCenter; y:Theme.preferences.osdPosition==="top" ? SurfaceLayout.osdEdgeMargin : parent.height-height-SurfaceLayout.osdEdgeMargin; width:SurfaceLayout.osdWidth; height:SurfaceLayout.osdHeight; backend:demo; uiState:shellState; visible:shellState.feedbackVisible }
    Rectangle {
        anchors.horizontalCenter:parent.horizontalCenter; anchors.bottom:parent.bottom; anchors.bottomMargin:18
        width:status.implicitWidth+28; height:30; color:Theme.previewStatusSurface; border.color:Theme.line
        Text { font.family:Theme.bodyFont; id:status; anchors.centerIn:parent; text:demo.lastAction || "Preview · changes stay in this window"; color:Theme.muted; font.pixelSize:Theme.fontSize(11) }
    }
    Shortcut { sequence:"Meta+R"; onActivated:shellState.toggle("launcher","preview") }
    Shortcut { sequence:"Alt+Tab";enabled:!switcher.active;onActivated:root.cycleWindows(1) }
    Shortcut { sequence:"Alt+Shift+Tab";enabled:!switcher.active;onActivated:root.cycleWindows(-1) }
    Shortcut { sequence:"Meta+M"; onActivated:shellState.toggle("power","preview") }
    Shortcut { sequence:"Meta+T"; onActivated:shellState.toggle("hardware","preview") }
    Shortcut { sequence:"Meta+B"; onActivated:shellState.toggle("notifications","preview") }
    Shortcut { sequence:"Escape"; onActivated:{switcher.cancel();shellState.close();} }
}
