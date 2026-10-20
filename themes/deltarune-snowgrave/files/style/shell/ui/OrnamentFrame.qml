import QtQuick
Rectangle {
    id:root
    color:"transparent"
    property color fillColor:Theme.background
    property color frameColor:Theme.line
    onFillColorChanged:outline.requestPaint()
    onFrameColorChanged:outline.requestPaint()
    Canvas {
        id:outline;anchors.fill:parent;antialiasing:true
        onWidthChanged:requestPaint()
        onHeightChanged:requestPaint()
        onPaint: {
            const c=getContext("2d");c.reset();
            const w=width-1,h=height-1,r=9;
            c.beginPath();c.moveTo(r,.5);c.lineTo(w-r,.5);c.quadraticCurveTo(w,.5,w,r);
            c.lineTo(w,h-r);c.quadraticCurveTo(w,h,w-r,h);c.lineTo(r,h);
            c.quadraticCurveTo(.5,h,.5,h-r);c.lineTo(.5,r);c.quadraticCurveTo(.5,.5,r,.5);
            c.closePath();c.fillStyle=root.fillColor;c.fill();
            c.strokeStyle=root.frameColor;c.lineWidth=1;c.stroke();
            function branch(points) {
                c.beginPath();c.moveTo(points[0][0],points[0][1]);
                for(let i=1;i<points.length;i++)c.lineTo(points[i][0],points[i][1]);
                c.stroke();
            }
            function leaf(x,y,direction) {
                c.beginPath();c.moveTo(x,y);c.quadraticCurveTo(x+direction*8,y-7,x+direction*10,y-2);
                c.quadraticCurveTo(x+direction*7,y+4,x,y);c.fill();
            }
            c.strokeStyle=Theme.brass;
            // Frosted twigs around opposite corners; the centre stays quiet.
            branch([[2,48],[9,36],[12,23],[24,14],[35,10],[47,2]]);
            branch([[12,23],[5,14],[6,4]]);branch([[24,14],[25,4]]);
            branch([[9,36],[20,36],[27,28]]);
            branch([[w-2,h-48],[w-10,h-34],[w-12,h-22],[w-25,h-14],[w-38,h-10],[w-48,h-2]]);
            branch([[w-12,h-22],[w-4,h-15]]);branch([[w-25,h-14],[w-24,h-3]]);
            c.fillStyle=Theme.brass;
            leaf(7,18,1);leaf(w-12,h-35,-1);
            c.fillStyle=Theme.brass;leaf(20,36,1);leaf(w-38,h-10,-1);
        }
    }
}
