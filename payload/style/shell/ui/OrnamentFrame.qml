import QtQuick
Rectangle {
    color: Theme.background
    border.color: Theme.line
    border.width: 1
    Image { anchors.left: parent.left; anchors.top: parent.top; width: 20; height: 20; source: "../assets/tl.svg" }
    Image { anchors.right: parent.right; anchors.top: parent.top; width: 20; height: 20; source: "../assets/tr.svg" }
    Image { anchors.left: parent.left; anchors.bottom: parent.bottom; width: 20; height: 20; source: "../assets/bl.svg" }
    Image { anchors.right: parent.right; anchors.bottom: parent.bottom; width: 20; height: 20; source: "../assets/br.svg" }
}
