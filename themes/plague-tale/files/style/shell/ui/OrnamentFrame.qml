import QtQuick
Rectangle {
    color: Theme.background
    border.color: Theme.line
    border.width: 1
    Image { anchors.left: parent.left; anchors.top: parent.top; width:Theme.ornamentSize; height:width; source:Theme.cornerTopLeft }
    Image { anchors.right: parent.right; anchors.top: parent.top; width:Theme.ornamentSize; height:width; source:Theme.cornerTopRight }
    Image { anchors.left: parent.left; anchors.bottom: parent.bottom; width:Theme.ornamentSize; height:width; source:Theme.cornerBottomLeft }
    Image { anchors.right: parent.right; anchors.bottom: parent.bottom; width:Theme.ornamentSize; height:width; source:Theme.cornerBottomRight }
}
