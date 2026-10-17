import QtQuick
import QtQuick.Controls
import "ui"
Item {
    id:root
    objectName:"previewScene"
    width:1600; height:1000
    property alias uiState:shellState
    property alias backend:demo
    Image { anchors.fill:parent; source:"assets/wallpaper.png"; fillMode:Image.PreserveAspectCrop }
    DemoContext { id:demo }
    UiState { id:shellState; objectName:"uiState" }
    Connections { target:demo; function onFeedbackRequested(kind,level,muted) {shellState.showFeedback(kind,level,muted);} }
    Bar { x:16; y:10; width:parent.width-32; height:48; backend:demo; uiState:shellState; screenToken:"preview" }
    Overlay { anchors.fill:parent; backend:demo; uiState:shellState }
    Feedback { anchors.horizontalCenter:parent.horizontalCenter; anchors.bottom:parent.bottom; anchors.bottomMargin:80; width:370; height:100; backend:demo; uiState:shellState; visible:shellState.feedbackVisible }
    Rectangle {
        anchors.horizontalCenter:parent.horizontalCenter; anchors.bottom:parent.bottom; anchors.bottomMargin:18
        width:status.implicitWidth+28; height:30; color:"#e6191a18"; border.color:Theme.line
        Text { id:status; anchors.centerIn:parent; text:demo.lastAction || "Preview · changes stay in this window"; color:Theme.muted; font.pixelSize:11 }
    }
    Shortcut { sequence:"Meta+R"; onActivated:shellState.toggle("launcher","preview") }
    Shortcut { sequence:"Meta+M"; onActivated:shellState.toggle("power","preview") }
    Shortcut { sequence:"Meta+T"; onActivated:shellState.toggle("hardware","preview") }
    Shortcut { sequence:"Meta+B"; onActivated:shellState.toggle("notifications","preview") }
    Shortcut { sequence:"Escape"; onActivated:shellState.close() }
}
