import QtQuick
import QtQuick.Controls
import QtQuick.Window
Item {
    id:root;objectName:"surfaceHint"
    property bool active:false
    property string text:""
    property Item target:parent
    property Component popupComponent:null
    property bool ready:false
    readonly property bool shown:active && visible && ready && target!==null && text!==""
    function restart() {
        ready=false;wake.stop();
        if(active && visible && target && text!=="")wake.start();
    }
    onActiveChanged:restart()
    onVisibleChanged:restart()
    onTextChanged:restart()
    onTargetChanged:restart()
    Timer {id:wake;interval:600;onTriggered:root.ready=true}
    Loader {
        objectName:"hintNativeLoader"
        active:root.shown && root.popupComponent!==null
        sourceComponent:root.popupComponent
        onLoaded:item.hint=root
    }
    ToolTip {
        id:fallback;objectName:"hintFallback"
        parent:root.target
        visible:root.shown && root.popupComponent===null
        // Full-window preview/panels use Qt; the 48px native bar uses PopupWindow.
        readonly property point origin:root.shown && parent ? parent.mapToItem(null,0,0) : Qt.point(0,0)
        x:parent ? (parent.width-width)/2 : 0
        y:parent && parent.Window.window && origin.y+parent.height+8+height<=parent.Window.window.height ? parent.height+8 : -height-8
        focus:false;modal:false;enabled:false;closePolicy:Popup.NoAutoClose
        padding:0
        enter:Transition {}
        exit:Transition {}
        background:null
        contentItem:HintBubble {text:root.text}
    }
}
