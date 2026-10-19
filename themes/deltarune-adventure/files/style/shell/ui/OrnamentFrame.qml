import QtQuick
Rectangle {
    id:root
    color:"transparent"
    property color fillColor:Theme.background
    property color frameColor:Theme.line
    onFillColorChanged:outline.requestPaint()
    onFrameColorChanged:outline.requestPaint()
    Canvas {
        id:outline;anchors.fill:parent;antialiasing:false
        onWidthChanged:requestPaint()
        onHeightChanged:requestPaint()
        onPaint: {
            const c=getContext("2d");c.reset();
            const w=width-1,h=height-1;
            // Stepped roof eaves, inset corners and a sunlit ridge.
            c.beginPath();c.moveTo(24,.5);c.lineTo(w-24,.5);
            c.lineTo(w-24,6.5);c.lineTo(w-13,6.5);c.lineTo(w-13,16.5);c.lineTo(w,16.5);
            c.lineTo(w,h-16);c.lineTo(w-10,h-16);c.lineTo(w-10,h-6);c.lineTo(w-24,h-6);c.lineTo(w-24,h);
            c.lineTo(24,h);c.lineTo(24,h-6);c.lineTo(10,h-6);c.lineTo(10,h-16);c.lineTo(.5,h-16);
            c.lineTo(.5,16.5);c.lineTo(13,16.5);c.lineTo(13,6.5);c.lineTo(24,6.5);c.closePath();
            c.fillStyle=root.fillColor;c.fill();c.strokeStyle=root.frameColor;c.lineWidth=1;c.stroke();
            c.strokeStyle=Theme.brass;c.beginPath();c.moveTo(25,1);c.lineTo(w-25,1);c.stroke();
            c.strokeStyle=Theme.danger;c.beginPath();c.moveTo(25,h-1);c.lineTo(w-25,h-1);c.stroke();
        }
    }
}
