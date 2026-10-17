import QtQuick
Canvas {
    id: root
    property string symbol: "search"
    property color ink: Theme.brass
    property real level: 100
    property bool charging: false
    onLevelChanged: requestPaint()
    onChargingChanged: requestPaint()
    implicitWidth: 20; implicitHeight: 20
    onSymbolChanged: requestPaint()
    onInkChanged: requestPaint()
    onWidthChanged: requestPaint()
    onHeightChanged: requestPaint()
    onPaint: {
        const c = getContext("2d"); c.reset();
        c.scale(width/24, height/24); c.strokeStyle = ink;
        c.lineWidth = 1.45; c.lineCap = "round"; c.lineJoin = "round";
        function line(x,y,a,b) { c.beginPath(); c.moveTo(x,y); c.lineTo(a,b); c.stroke(); }
        function arc(x,y,r,a,b) { c.beginPath(); c.arc(x,y,r,a,b); c.stroke(); }
        if (symbol === "search") { arc(10,10,6,0,Math.PI*2); line(15,15,21,21); }
        else if (symbol === "power") { arc(12,13,8,-Math.PI*.32,Math.PI*1.32); line(12,2,12,12); }
        else if (symbol === "audio" || symbol === "mute") {
            c.beginPath(); c.moveTo(3,9); c.lineTo(7,9); c.lineTo(12,5); c.lineTo(12,19); c.lineTo(7,15); c.lineTo(3,15); c.closePath(); c.stroke();
            if (symbol === "mute") { line(16,9,21,15); line(21,9,16,15); }
            else { arc(13,12,5,-.9,.9); arc(13,12,9,-.9,.9); }
        } else if (symbol === "mic") {
            c.strokeRect(9,3,6,12); arc(12,12,7,0,Math.PI); line(12,19,12,22); line(8,22,16,22);
        } else if (symbol === "sun") {
            arc(12,12,4,0,Math.PI*2);
            for(let i=0;i<8;i++) { const a=i*Math.PI/4; line(12+7*Math.cos(a),12+7*Math.sin(a),12+10*Math.cos(a),12+10*Math.sin(a)); }
        } else if (symbol === "bell") {
            c.beginPath(); c.moveTo(5,17); c.lineTo(7,14); c.lineTo(7,9); c.arc(12,9,5,Math.PI,0); c.lineTo(17,14); c.lineTo(19,17); c.closePath(); c.stroke(); arc(12,19,2,0,Math.PI);
        } else if (symbol === "lock") { c.strokeRect(5,11,14,10); arc(12,10,5,Math.PI,Math.PI*2); line(12,15,12,18); }
        else if (symbol === "moon") { c.beginPath(); c.arc(12,12,9,.5,Math.PI*1.75); c.bezierCurveTo(8,14,8,8,12,3); c.stroke(); }
        else if (symbol === "close") { line(6,6,18,18); line(18,6,6,18); }
        else if (symbol === "play") { c.beginPath(); c.moveTo(8,5); c.lineTo(19,12); c.lineTo(8,19); c.closePath(); c.stroke(); }
        else if (symbol === "pause") { line(8,5,8,19); line(16,5,16,19); }
        else if (symbol === "previous" || symbol === "next") {
            const n = symbol === "next"; c.save(); if(n) {c.translate(24,0); c.scale(-1,1);}
            line(5,5,5,19); c.beginPath(); c.moveTo(18,5); c.lineTo(8,12); c.lineTo(18,19); c.closePath(); c.stroke(); c.restore();
        } else if (symbol === "restart") { arc(12,12,8,.1,Math.PI*1.8); line(19,4,19,10); line(19,10,13,8); }
        else if (symbol === "logout") { line(4,3,4,21); line(4,3,11,3); line(4,21,11,21); line(9,12,21,12); line(16,7,21,12); line(16,17,21,12); }
        else if (symbol === "battery") {
            c.strokeRect(2,7,18,10); line(22,10,22,14);
            if(charging) {c.beginPath();c.moveTo(12,8);c.lineTo(8,12);c.lineTo(13,12);c.lineTo(10,16);c.stroke();}
            else if(level>=0) {c.fillStyle=ink;c.fillRect(4,9,14*Math.max(0,Math.min(100,level))/100,6);}
            else {line(9,10,13,14);line(13,10,9,14);}
        }
        else if (symbol === "hardware") { c.strokeRect(6,6,12,12);c.strokeRect(9,9,6,6);for(let n=8;n<=16;n+=4) {line(n,2,n,5);line(n,19,n,22);line(2,n,5,n);line(19,n,22,n);} }
        else if (symbol === "network") { arc(12,19,14,Math.PI*1.24,Math.PI*1.76); arc(12,19,9,Math.PI*1.24,Math.PI*1.76); arc(12,19,4,Math.PI*1.24,Math.PI*1.76); arc(12,20,1,0,Math.PI*2); }
        else if (symbol === "music") { line(9,5,9,18); line(9,5,19,3); line(19,3,19,16); arc(6,18,3,0,Math.PI*2); arc(16,16,3,0,Math.PI*2); }
        else if (symbol === "tree") {
            arc(12,12,10,0,Math.PI*2); line(12,19,12,10); line(12,13,6,8); line(12,13,18,8); line(12,11,9,5); line(12,11,15,5); line(12,19,7,21); line(12,19,17,21);
        } else { arc(12,12,7,0,Math.PI*2); }
    }
}
