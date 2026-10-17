import QtQuick
import QtQuick.Controls
OrnamentFrame {
    id:root
    required property var uiState
    required property var backend
    implicitWidth:370; implicitHeight:100
    HoverHandler { id:hover }
    Binding { target:root.uiState; property:"feedbackHeld"; value:root.visible && (hover.hovered || slider.pressed) }
    ActionButton {
        x:14; y:18; width:40; height:40; padding:10
        symbol:uiState.feedbackKind==="brightness" ? "sun" : uiState.feedbackKind==="microphone" ? "mic" : uiState.feedbackMuted ? "mute" : "audio"
        enabled:uiState.feedbackKind!=="brightness"
        onClicked:uiState.feedbackKind==="microphone" ? backend.toggleMicrophone() : backend.toggleMute()
    }
    Text { x:64; y:19; color:Theme.ink; font.family:Theme.displayFont; font.pixelSize:Theme.fontSize(20); text:uiState.feedbackKind==="brightness" ? "Brightness" : uiState.feedbackKind==="microphone" ? "Microphone" : "Volume" }
    Text { anchors.right:parent.right; anchors.rightMargin:24; y:24; color:uiState.feedbackMuted ? Theme.danger : Theme.brass; font.pixelSize:Theme.fontSize(12); text:uiState.feedbackMuted ? "MUTED" : Math.round(slider.value)+"%" }
    function commit() {
        const v=Math.round(slider.value);
        if(uiState.feedbackKind==="brightness")backend.setBrightness(v);
        else if(uiState.feedbackKind==="microphone")backend.setMicrophoneVolume(v);
        else backend.setVolume(v);
    }
    Timer { id:throttle; interval:90; onTriggered:root.commit() }
    Slider {
        id:slider; objectName:"feedbackSlider"
        x:64; y:52; width:parent.width-88; height:30
        from:uiState.feedbackKind==="brightness" ? 1 : 0; to:100; stepSize:1; hoverEnabled:true
        value:uiState.feedbackLevel
        Binding { target:slider; property:"value"; value:root.uiState.feedbackLevel; when:!slider.pressed }
        onMoved: { if(!throttle.running)throttle.start(); }
        onPressedChanged:if(!pressed) {throttle.stop();root.commit();}
        background:Rectangle {
            x:slider.leftPadding; y:slider.topPadding+slider.availableHeight/2-height/2
            width:slider.availableWidth; height:3; color:Theme.line
            Rectangle { width:slider.visualPosition*parent.width; height:3; color:root.uiState.feedbackMuted ? Theme.muted : Theme.brass }
        }
        handle:Item {
            x:slider.leftPadding+slider.visualPosition*(slider.availableWidth-width)
            y:slider.topPadding+slider.availableHeight/2-height/2
            width:16; height:24
            Rectangle { anchors.centerIn:parent; width:26; height:26; radius:13; color:Theme.brass; opacity:slider.hovered || slider.pressed ? .16 : 0; Behavior on opacity {NumberAnimation {duration:Theme.duration(110)}} }
            Rectangle { anchors.centerIn:parent; width:slider.pressed ? 12 : 8; height:slider.pressed ? 12 : 8; radius:6; color:slider.hovered || slider.pressed ? Theme.ink : Theme.brass; border.color:Theme.brass }
        }
        Accessible.name:root.uiState.feedbackKind
    }
}
