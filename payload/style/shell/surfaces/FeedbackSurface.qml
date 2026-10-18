import QtQuick
import "../ui"
import "../behavior"
import QtQuick.Controls
FeedbackController {
    id:root
    property real iconTop:18
    property real titleTop:19
    property real percentTop:24
    property real sliderTop:52
    property real sliderHeight:30
    property real trackHeight:3
    property real handleRadius:6
    OrnamentFrame {anchors.fill:parent}
    implicitWidth:SurfaceLayout.osdWidth; implicitHeight:SurfaceLayout.osdHeight
    HoverHandler { id:hover }
    held:root.visible && (hover.hovered || slider.pressed)
    ActionButton {
        x:14; y:root.iconTop; width:40; height:40; padding:10
        symbol:uiState.feedbackKind==="brightness" ? "sun" : uiState.feedbackKind==="microphone" ? "mic" : uiState.feedbackMuted ? "mute" : "audio"
        enabled:uiState.feedbackKind!=="brightness"
        onClicked:root.toggleMute()
    }
    Text { x:64; y:root.titleTop; color:Theme.ink; font.family:Theme.displayFont; font.pixelSize:Theme.fontSize(20); text:uiState.feedbackKind==="brightness" ? "Brightness" : uiState.feedbackKind==="microphone" ? "Microphone" : "Volume" }
    Text { font.family:Theme.bodyFont; anchors.right:parent.right; anchors.rightMargin:24; y:root.percentTop; color:uiState.feedbackMuted ? Theme.danger : Theme.brass; font.pixelSize:Theme.fontSize(12); text:uiState.feedbackMuted ? "MUTED" : Math.round(slider.value)+"%" }
    Slider {
        id:slider; objectName:"feedbackSlider"
        x:64; y:root.sliderTop; width:parent.width-88; height:root.sliderHeight
        from:uiState.feedbackKind==="brightness" ? 1 : 0; to:100; stepSize:1; hoverEnabled:true
        value:uiState.feedbackLevel
        Binding { target:slider; property:"value"; value:root.uiState.feedbackLevel; when:!slider.pressed }
        onMoved:root.move(slider.value)
        onPressedChanged:if(!pressed)root.release(slider.value)
        background:Rectangle {
            x:slider.leftPadding; y:slider.topPadding+slider.availableHeight/2-height/2
            width:slider.availableWidth; height:root.trackHeight; color:Theme.line
            Rectangle { width:slider.visualPosition*parent.width; height:root.trackHeight; color:root.uiState.feedbackMuted ? Theme.muted : Theme.brass }
        }
        handle:Item {
            x:slider.leftPadding+slider.visualPosition*(slider.availableWidth-width)
            y:slider.topPadding+slider.availableHeight/2-height/2
            width:16; height:24
            Rectangle { anchors.centerIn:parent; width:26; height:26; radius:root.handleRadius===0 ? 0 : 13; color:Theme.brass; opacity:slider.hovered || slider.pressed ? .16 : 0; Behavior on opacity {NumberAnimation {duration:Theme.duration(Theme.quickMotion)}} }
            Rectangle { anchors.centerIn:parent; width:slider.pressed ? 12 : 8; height:slider.pressed ? 12 : 8; radius:root.handleRadius; color:slider.hovered || slider.pressed ? Theme.ink : Theme.brass; border.color:Theme.brass }
        }
        Accessible.name:root.uiState.feedbackKind
    }
}
