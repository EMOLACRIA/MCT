import QtQuick
Rectangle {
    id:root
    color:"transparent"
    property color fillColor:Theme.background
    property color frameColor:Theme.brass
    onFillColorChanged:outline.requestPaint()
    onFrameColorChanged:outline.requestPaint()
    Canvas {
        id:outline;anchors.fill:parent;antialiasing:false
        onWidthChanged:requestPaint()
        onHeightChanged:requestPaint()
        onPaint: {
            const c=getContext("2d");c.reset();
            const w=width-1,h=height-1,n=10;
            c.beginPath();c.moveTo(n,.5);c.lineTo(w-n,.5);c.lineTo(w,n);
            c.lineTo(w,h-n);c.lineTo(w-n,h);c.lineTo(.5,h);c.lineTo(.5,n);c.closePath();
            c.fillStyle=root.fillColor;c.fill();c.strokeStyle=root.frameColor;c.lineWidth=1;c.stroke();
            c.fillStyle=root.frameColor;c.fillRect(12,5,18,2);c.fillRect(w-16,h-7,8,2);
        }
    }
}
