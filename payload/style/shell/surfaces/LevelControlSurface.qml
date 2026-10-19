import QtQuick
import "../ui"
import QtQuick.Controls
import QtQuick.Layouts
ColumnLayout {
    id:root
    property real handleRadius:6
    property string label: ""
    property string symbol:"audio"
    property int level:0
    property bool available:true
    signal commit(int percent)
    RowLayout {
        Glyph { symbol:root.symbol }
        Text { font.family:Theme.bodyFont; text:root.label; color:Theme.ink; font.pixelSize:Theme.fontSize(13); Layout.fillWidth:true }
        Text { font.family:Theme.bodyFont; text:root.available ? Math.round(slider.value)+"%" : "Unavailable"; color:Theme.brass; font.pixelSize:Theme.fontSize(12)}
    }
    Slider {
        id:slider; Layout.fillWidth:true; from:0; to:100; stepSize:1
        enabled:root.available; value:root.level
        onPressedChanged:if(!pressed && activeFocus)root.commit(Math.round(value))
        onMoved:if(!pressed)root.commit(Math.round(value))
        background:Rectangle { x:slider.leftPadding; y:slider.topPadding+slider.availableHeight/2-height/2; width:slider.availableWidth; height:3; color:Theme.line; Rectangle { width:slider.visualPosition*parent.width; height:3; color:Theme.brass } }
        handle:Rectangle { x:slider.leftPadding+slider.visualPosition*(slider.availableWidth-width); y:slider.topPadding+slider.availableHeight/2-height/2; width:12; height:12; radius:root.handleRadius; color:Theme.ink; border.width:1; border.color:Theme.brass }
    }
}
