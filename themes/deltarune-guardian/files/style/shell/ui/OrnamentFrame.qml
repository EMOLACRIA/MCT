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
            const w=width-1,h=height-1,r=10;
            c.beginPath();c.moveTo(r,.5);c.lineTo(w-r,.5);c.quadraticCurveTo(w,.5,w,r);
            c.lineTo(w,h-r);c.quadraticCurveTo(w,h,w-r,h);c.lineTo(r,h);
            c.quadraticCurveTo(.5,h,.5,h-r);c.lineTo(.5,r);c.quadraticCurveTo(.5,.5,r,.5);
            c.closePath();c.fillStyle=root.fillColor;c.fill();
            c.strokeStyle=root.frameColor;c.lineWidth=1;c.stroke();
            // Quiet radial light, with asymmetric four-point stars like the reference.
            function star(x,y,size) {
                const q=size*.18;
                c.beginPath();c.moveTo(x,y-size);c.quadraticCurveTo(x+q,y-q,x+size,y);
                c.quadraticCurveTo(x+q,y+q,x,y+size);c.quadraticCurveTo(x-q,y+q,x-size,y);
                c.quadraticCurveTo(x-q,y-q,x,y-size);c.closePath();c.fill();
            }
            c.fillStyle=Theme.ink;star(11,11,10);star(w-11,h-11,8);
            c.strokeStyle=Theme.brass;c.beginPath();c.moveTo(27,.5);c.lineTo(Math.min(110,w-25),.5);
            c.moveTo(w-27,h);c.lineTo(Math.max(w-110,25),h);c.stroke();
        }
    }
}
