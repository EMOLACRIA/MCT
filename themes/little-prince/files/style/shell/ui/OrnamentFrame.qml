import QtQuick
// Cut paper: an amber and a rose sheet stacked behind the panel, each hand-cut a
// little differently. The panel itself is translucent, so the sheets are erased
// under it and only their edges show. Static; repaints only on resize.
Item {
    id:root
    property color fillColor:Theme.background
    property color frameColor:Theme.line
    onFillColorChanged:paper.requestPaint()
    Canvas {
        id:paper
        x:-10;y:-10;width:root.width+22;height:root.height+22
        antialiasing:true
        onWidthChanged:requestPaint()
        onHeightChanged:requestPaint()
        function sheet(c,ox,oy,w,h,seed,r) {
            function wob(i) {return Math.sin(i*0.37+seed)*0.9+Math.sin(i*0.11+seed*2.3)*0.7;}
            const step=10;let i=0;
            c.beginPath();c.moveTo(ox+r,oy+wob(i++));
            for(let x=r+step;x<w-r;x+=step)c.lineTo(ox+x,oy+wob(i++));
            c.quadraticCurveTo(ox+w,oy,ox+w+wob(i++),oy+r);
            for(let y=r+step;y<h-r;y+=step)c.lineTo(ox+w+wob(i++),oy+y);
            c.quadraticCurveTo(ox+w,oy+h,ox+w-r,oy+h+wob(i++));
            for(let x=w-r-step;x>r;x-=step)c.lineTo(ox+x,oy+h+wob(i++));
            c.quadraticCurveTo(ox,oy+h,ox+wob(i++),oy+h-r);
            for(let y=h-r-step;y>r;y-=step)c.lineTo(ox+wob(i++),oy+y);
            c.quadraticCurveTo(ox,oy,ox+r,oy);
            c.closePath();
        }
        onPaint: {
            const c=getContext("2d");c.reset();
            const w=root.width,h=root.height;
            sheet(c,10+7,10+8,w,h,4.1,9);c.fillStyle=Theme.offsetInk;c.fill();
            sheet(c,10+3,10+4,w,h,1.7,9);c.fillStyle=Theme.paperLayer;c.fill();
            c.globalCompositeOperation="destination-out";
            sheet(c,10,10,w,h,0.3,9);c.fillStyle="#000000";c.fill();
            c.globalCompositeOperation="source-over";
            sheet(c,10,10,w,h,0.3,9);c.fillStyle=root.fillColor;c.fill();
        }
    }
}
