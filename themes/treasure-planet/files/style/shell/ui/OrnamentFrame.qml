import QtQuick
// Navigation plate: double rule, riveted silver corner brackets and a compass
// tick at the middle of each edge. Static; repaints only on resize.
Item {
    id:root
    property color fillColor:Theme.background
    property color frameColor:Theme.line
    onFillColorChanged:plate.requestPaint()
    Rectangle {anchors.fill:parent;radius:3;color:root.fillColor}
    Canvas {
        id:plate
        anchors.fill:parent;anchors.margins:-3
        antialiasing:true
        onWidthChanged:requestPaint()
        onHeightChanged:requestPaint()
        onPaint: {
            const c=getContext("2d");c.reset();
            const w=width,h=height,o=3;
            c.strokeStyle=Theme.brassDark;c.lineWidth=1;
            c.strokeRect(o+.5,o+.5,w-2*o-1,h-2*o-1);
            c.strokeStyle=Theme.line;c.strokeRect(o+5.5,o+5.5,w-2*o-11,h-2*o-11);
            c.strokeStyle=Theme.frame;c.lineWidth=2;
            const L=22;
            for(const [x,y,dx,dy] of [[o,o,1,1],[w-o,o,-1,1],[o,h-o,1,-1],[w-o,h-o,-1,-1]]) {
                c.beginPath();c.moveTo(x+dx*L,y+dy*1);c.lineTo(x+dx*1,y+dy*1);c.lineTo(x+dx*1,y+dy*L);c.stroke();
                c.beginPath();c.arc(x+dx*7,y+dy*7,2.2,0,Math.PI*2);c.fillStyle=Theme.frame;c.fill();
            }
            c.lineWidth=1.5;
            for(const [x,y,dx,dy] of [[w/2,o,0,1],[w/2,h-o,0,-1],[o,h/2,1,0],[w-o,h/2,-1,0]]) {
                c.beginPath();c.moveTo(x,y);c.lineTo(x+dx*9,y+dy*9);c.stroke();
            }
        }
    }
}
