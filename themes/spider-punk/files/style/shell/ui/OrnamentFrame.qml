import QtQuick
// Torn paper panel, printed with a second (cyan) ink layer slightly out of register.
// Static: repaints only when the panel size or colour changes.
Item {
    id:root
    property color fillColor:Theme.background
    property color frameColor:Theme.line
    onFillColorChanged:paper.requestPaint()
    Canvas {
        id:paper
        x:-8;y:-8;width:root.width+16;height:root.height+16
        antialiasing:true
        onWidthChanged:requestPaint()
        onHeightChanged:requestPaint()
        function tear(c,ox,oy,w,h,seed) {
            // deterministic jagged outline: the same panel size tears the same way
            function j(i) {const v=Math.sin(i*12.9898+seed*78.233)*43758.5453;return (v-Math.floor(v))*3.2-1.6;}
            const step=7;let i=0;
            c.beginPath();c.moveTo(ox,oy+j(i++));
            for(let x=step;x<w;x+=step)c.lineTo(ox+x,oy+j(i++));
            c.lineTo(ox+w+j(i++),oy);
            for(let y=step;y<h;y+=step)c.lineTo(ox+w+j(i++),oy+y);
            c.lineTo(ox+w,oy+h+j(i++));
            for(let x=w-step;x>0;x-=step)c.lineTo(ox+x,oy+h+j(i++));
            c.lineTo(ox+j(i++),oy+h);
            for(let y=h-step;y>0;y-=step)c.lineTo(ox+j(i++),oy+y);
            c.closePath();
        }
        onPaint: {
            const c=getContext("2d");c.reset();
            const w=root.width,h=root.height;
            tear(c,8+5,8+5,w,h,7);c.fillStyle=Theme.offsetInk;c.fill();
            tear(c,8,8,w,h,3);c.fillStyle=root.fillColor;c.fill();
        }
    }
}
