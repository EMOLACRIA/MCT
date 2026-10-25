import QtQuick
import "../surfaces"
BarSurface {
    clockSize:17;workspaceRadius:5
    barBackground:Component {Item {
        Rectangle {anchors.fill:parent;color:Theme.background}
        Rectangle {anchors.bottom:parent.bottom;width:parent.width;height:1;color:Theme.line}
        Canvas {
            anchors.fill:parent;antialiasing:true
            onWidthChanged:requestPaint()
            onHeightChanged:requestPaint()
            onPaint: {
                const c=getContext("2d");c.reset();const w=width,h=height;
                function star(x,y,s) {const q=s*.16;c.beginPath();c.moveTo(x,y-s);c.quadraticCurveTo(x+q,y-q,x+s,y);c.quadraticCurveTo(x+q,y+q,x,y+s);c.quadraticCurveTo(x-q,y+q,x-s,y);c.quadraticCurveTo(x-q,y-q,x,y-s);c.closePath();c.fill();}
                c.fillStyle=Theme.ink;star(8,h-8,6);star(w-8,h-8,6);
                c.strokeStyle=Theme.brass;c.lineWidth=1;c.beginPath();c.moveTo(18,h-1);c.lineTo(70,h-1);c.moveTo(w-18,h-1);c.lineTo(w-70,h-1);c.stroke();
            }
        }
    }}
}
