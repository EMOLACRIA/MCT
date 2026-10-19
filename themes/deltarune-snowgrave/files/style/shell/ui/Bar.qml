import QtQuick
import "../surfaces"
BarSurface {
    clockSize:17;workspaceRadius:1
    barBackground:Component {Item {
        Rectangle {anchors.fill:parent;color:Theme.background}
        Rectangle {anchors.bottom:parent.bottom;width:parent.width;height:1;color:Theme.line}
        Canvas {
            anchors.fill:parent;antialiasing:true
            onWidthChanged:requestPaint()
            onHeightChanged:requestPaint()
            onPaint: {
                const c=getContext("2d");c.reset();
                const w=width,h=height-1;
                c.lineWidth=1;c.strokeStyle=Theme.brass;
                c.beginPath();c.moveTo(2,h-27);c.lineTo(12,h-19);c.lineTo(15,h-8);c.lineTo(28,h);
                c.moveTo(12,h-19);c.lineTo(23,h-24);c.lineTo(31,h-21);
                c.moveTo(w-2,h-25);c.lineTo(w-15,h-17);c.lineTo(w-19,h-7);c.lineTo(w-33,h);
                c.moveTo(w-15,h-17);c.lineTo(w-27,h-22);c.stroke();
                c.fillStyle=Theme.danger;
                c.beginPath();c.moveTo(23,h-24);c.lineTo(30,h-30);c.lineTo(32,h-21);c.closePath();c.fill();
                c.beginPath();c.moveTo(w-27,h-22);c.lineTo(w-35,h-28);c.lineTo(w-35,h-19);c.closePath();c.fill();
            }
        }
    }}
}
