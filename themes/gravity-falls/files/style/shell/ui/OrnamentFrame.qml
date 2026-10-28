import QtQuick
// A journal page: plain panel with two strips of paper tape on opposite corners.
Item {
    id:root
    property color fillColor:Theme.background
    property color frameColor:Theme.line
    Rectangle {anchors.fill:parent;radius:4;color:root.fillColor;border.width:1;border.color:root.frameColor}
    Image {x:-14;y:-14;width:Theme.ornamentSize;height:width;source:Theme.cornerTopLeft;sourceSize:Qt.size(width*2,height*2)}
    Image {x:parent.width-width+14;y:parent.height-height+14;width:Theme.ornamentSize;height:width;source:Theme.cornerBottomRight;sourceSize:Qt.size(width*2,height*2)}
}
