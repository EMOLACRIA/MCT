import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
ColumnLayout {
    id:root
    required property string label
    required property real value
    property real from:0
    property real to:100
    property real step:1
    signal chosen(real value)
    RowLayout {
        Text { font.family:Theme.bodyFont;text:root.label;color:Theme.ink;font.pixelSize:Theme.fontSize(13);Layout.fillWidth:true}
        Text { font.family:Theme.bodyFont;text:Math.round(slider.value)+"%";color:Theme.brass;font.pixelSize:Theme.fontSize(12)}
    }
    Slider {
        id:slider;objectName:root.objectName+"Slider"
        Layout.fillWidth:true;from:root.from;to:root.to;stepSize:root.step;value:root.value
        Binding {target:slider;property:"value";value:root.value;when:!slider.pressed}
        onMoved:if(!pressed)root.chosen(value)
        onPressedChanged:if(!pressed)root.chosen(value)
        Accessible.name:root.label
        background:Rectangle {x:slider.leftPadding;y:slider.topPadding+slider.availableHeight/2-height/2;width:slider.availableWidth;height:3;color:Theme.line
            Rectangle {width:slider.visualPosition*parent.width;height:3;color:Theme.brass}
        }
        handle:Rectangle {x:slider.leftPadding+slider.visualPosition*(slider.availableWidth-width);y:slider.topPadding+slider.availableHeight/2-height/2;width:12;height:12;radius:6;color:slider.pressed ? Theme.ink : Theme.brass}
    }
}
