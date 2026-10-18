import QtQuick
import QtQuick.Window
FocusScope {
    id:root
    objectName:"windowSwitcher"
    required property var controller
    property Component previewComponent:null
    visible:controller.active
    focus:visible
    property bool hadWindowFocus:false
    readonly property bool windowActive:Window.window ? Window.window.active : false
    onWindowActiveChanged: {
        if(windowActive)hadWindowFocus=true;
        else if(hadWindowFocus && controller.active)controller.cancel();
    }
    onVisibleChanged: {
        hadWindowFocus=visible && windowActive;
        if(visible)Qt.callLater(()=>{if(root.visible)root.forceActiveFocus();});
    }
    Keys.onPressed:event=> {
        if(event.key===Qt.Key_Tab || event.key===Qt.Key_Backtab) {controller.step(event.key===Qt.Key_Backtab || (event.modifiers & Qt.ShiftModifier) ? -1 : 1);event.accepted=true;}
        else if(event.key===Qt.Key_Left || event.key===Qt.Key_Up) {controller.step(-1);event.accepted=true;}
        else if(event.key===Qt.Key_Right || event.key===Qt.Key_Down) {controller.step(1);event.accepted=true;}
        else if(event.key===Qt.Key_Return || event.key===Qt.Key_Enter) {controller.commit();event.accepted=true;}
        else if(event.key===Qt.Key_Escape) {controller.cancel();event.accepted=true;}
    }
    Keys.onReleased:event=> {if(event.key===Qt.Key_Alt && !event.isAutoRepeat) {controller.commit();event.accepted=true;}}
}
