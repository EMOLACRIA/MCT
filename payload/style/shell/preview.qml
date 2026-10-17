//@ pragma UseQApplication
import QtQuick
import Quickshell
FloatingWindow {
    visible:true
    title:"Desktop preview"
    implicitWidth:1280
    implicitHeight:800
    PreviewScene { anchors.fill:parent }
}
