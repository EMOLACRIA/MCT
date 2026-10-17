import QtQuick
import Quickshell
import "ui"
PopupWindow {
    id:root
    property var hint:null
    visible:hint!==null && hint.shown
    color:"transparent";grabFocus:false
    // Never intercept a click or hover, even if the compositor adjusts placement.
    mask:Region {width:0;height:0}
    anchor.item:hint ? hint.target : null
    anchor.rect.x:0
    anchor.rect.y:hint && hint.target ? hint.target.height+8 : 0
    anchor.rect.width:hint && hint.target ? Math.max(1,hint.target.width) : 1
    anchor.rect.height:1
    anchor.edges:Edges.Top
    anchor.gravity:Edges.Bottom
    anchor.adjustment:PopupAdjustment.SlideX
    implicitWidth:bubble.implicitWidth;implicitHeight:bubble.implicitHeight
    HintBubble {id:bubble;anchors.fill:parent;text:root.hint ? root.hint.text : ""}
}
