import QtQuick
import "../surfaces"
BarSurface {
    clockSize:17;workspaceRadius:3
    barBackground:Component {Item {
        Rectangle {anchors.fill:parent;color:Theme.background}
        Rectangle {anchors.bottom:parent.bottom;width:parent.width;height:1;color:Theme.brass}
        Canvas {
            anchors.fill:parent;antialiasing:false
            onWidthChanged:requestPaint()
            onHeightChanged:requestPaint()
            onPaint: {
                const c=getContext("2d");c.reset();const w=width,h=height-1;
                c.lineWidth=1;c.strokeStyle=Theme.brass;c.beginPath();
                c.moveTo(.5,0);c.lineTo(.5,12);c.lineTo(7,12);c.lineTo(7,22);c.lineTo(15,22);c.lineTo(15,32);c.lineTo(25,32);c.lineTo(25,h);
                c.moveTo(w-.5,0);c.lineTo(w-.5,12);c.lineTo(w-7,12);c.lineTo(w-7,22);c.lineTo(w-15,22);c.lineTo(w-15,32);c.lineTo(w-25,32);c.lineTo(w-25,h);c.stroke();
            }
        }
    }}
}
