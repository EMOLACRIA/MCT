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
            const w=width-1,h=height-1,n=12;
            // A continuous silhouette with quiet branch-like breaks at its edges.
            c.beginPath();c.moveTo(n,.5);c.lineTo(w-22,.5);
            c.lineTo(w-22,5);c.lineTo(w-9,5);c.lineTo(w,14);
            c.lineTo(w,h-n);c.lineTo(w-n,h);c.lineTo(9,h);
            c.lineTo(.5,h-9);c.lineTo(.5,n);c.closePath();
            c.fillStyle=root.fillColor;c.fill();c.strokeStyle=root.frameColor;c.lineWidth=1;c.stroke();
            function branch(points) {
                c.beginPath();c.moveTo(points[0][0],points[0][1]);
                for(let i=1;i<points.length;i++)c.lineTo(points[i][0],points[i][1]);
                c.stroke();
            }
            c.strokeStyle=Theme.brass;
            branch([[w-38,1],[w-31,8],[w-20,10],[w-15,18],[w-7,21],[w,34]]);
            branch([[w-20,10],[w-18,1]]);
            branch([[w-7,21],[w-2,17],[w-2,8]]);
            branch([[1,h-30],[8,h-22],[9,h-14],[20,h-10],[24,h-1]]);
            branch([[9,h-14],[2,h-11]]);
            branch([[20,h-10],[28,h-13],[35,h-7]]);
        }
    }
}
