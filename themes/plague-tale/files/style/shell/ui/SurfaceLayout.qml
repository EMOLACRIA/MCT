pragma Singleton
import QtQuick
QtObject {
    // Logical pixels, shared by native windows and the offscreen preview.
    readonly property int barHeight:48
    readonly property int barTopMargin:10
    readonly property int barSideMargin:16
    readonly property int floatingBarReservedHeight:60
    readonly property int panelPadding:24
    readonly property int panelSideMargin:16
    readonly property int panelTop:74
    readonly property int panelWidthMargin:48
    readonly property int panelHeightMargin:100
    readonly property int panelMinimumWidth:250
    readonly property int panelMinimumHeight:210
    readonly property var panels:({
        launcher:{width:620,height:580,centered:true},
        power:{width:550,height:465,confirmationHeight:280,centered:true},
        controls:{width:420,height:610,centered:false},
        notifications:{width:460,height:650,centered:false},
        media:{width:420,height:520,centered:false},
        hardware:{width:650,height:660,centered:true},
        settings:{width:720,height:740,centered:true}
    })
    function panelSpec(name) {return panels[name] || panels.media;}
    function panelCentered(name,centerSidePanels) {return centerSidePanels || panelSpec(name).centered;}
    function panelWidth(name,availableWidth) {
        return Math.max(panelMinimumWidth,Math.min(availableWidth-panelWidthMargin,panelSpec(name).width));
    }
    function panelHeight(name,availableHeight,confirmation,fontScale) {
        const spec=panelSpec(name);
        const preferred=name==="power" ? Math.round((confirmation ? spec.confirmationHeight : spec.height)*fontScale) : spec.height;
        return Math.max(panelMinimumHeight,Math.min(availableHeight-panelHeightMargin,preferred));
    }
    readonly property int osdWidth:370
    readonly property int osdHeight:100
    readonly property int osdEdgeMargin:80
    readonly property int toastWidth:390
    readonly property int toastTop:76
    readonly property int toastSideMargin:16
    readonly property int toastSpacing:10
    readonly property int switcherWidth:960
    readonly property int switcherHeight:590
    readonly property int switcherMinimumWidth:200
    readonly property int switcherMinimumHeight:180
    readonly property int switcherWidthMargin:40
    readonly property int switcherHeightMargin:80
}
