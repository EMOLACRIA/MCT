import QtQuick
import "../surfaces"
// Translucent strip with two thin cut-paper edges underneath (amber, rose).
BarSurface {
    clockSize:19;workspaceRadius:2
    barBackground:Component {Item {
        Rectangle {anchors.fill:parent;color:Theme.background}
        Rectangle {anchors.bottom:parent.bottom;anchors.bottomMargin:-3;width:parent.width;height:3;color:Theme.paperLayer}
        Rectangle {anchors.bottom:parent.bottom;anchors.bottomMargin:-6;width:parent.width;height:3;color:Theme.offsetInk}
    }}
}
