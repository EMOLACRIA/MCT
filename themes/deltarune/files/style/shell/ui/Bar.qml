import QtQuick
import "../surfaces"
BarSurface {
    clockSize:17;workspaceRadius:0
    barBackground:Component {Item {
        Rectangle {anchors.fill:parent;color:Theme.background}
        Canvas {
            anchors.fill:parent;antialiasing:true
            onWidthChanged:requestPaint()
            onHeightChanged:requestPaint()
            onPaint: {
                const c=getContext("2d");c.reset();
                const w=width,h=height-1;
                c.strokeStyle=Theme.line;c.lineWidth=1;
                c.beginPath();c.moveTo(1,1);c.lineTo(14,h);c.lineTo(w*.31,h);
                c.lineTo(w*.32,h-10);c.lineTo(w*.45,h-10);c.stroke();
                c.beginPath();c.moveTo(w*.55,h-10);c.lineTo(w*.75,h-10);
                c.lineTo(w*.76,h);c.lineTo(w-14,h);c.lineTo(w-1,1);c.stroke();
                c.strokeStyle=Theme.brass;
                c.beginPath();c.moveTo(7,6);c.lineTo(29,6);c.lineTo(38,14);
                c.lineTo(38,h-9);c.lineTo(46,h);c.stroke();
                c.beginPath();c.moveTo(w*.31,h);c.lineTo(w*.32,h-16);
                c.lineTo(w*.33,h-16);c.lineTo(w*.335,h-21);c.lineTo(w*.36,h-21);c.stroke();
                c.beginPath();c.moveTo(w*.75,h-10);c.lineTo(w*.765,h-10);
                c.lineTo(w*.77,h-3);c.lineTo(w*.78,h-3);c.stroke();
            }
        }
    }}
}
