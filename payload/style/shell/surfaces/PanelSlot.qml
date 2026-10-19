import QtQuick
Loader {
    id:root
    required property string panel
    required property var uiState
    property bool visited:false
    readonly property bool current:uiState.activePanel===panel
    active:visited
    visible:current
    signal shown()
    function sync() {
        if(current) {visited=true;activateContent.restart();}
        else activateContent.stop();
    }
    onCurrentChanged:sync()
    Component.onCompleted:sync()
    onLoaded:if(current)activateContent.restart()
    Timer {
        id:activateContent;interval:0
        onTriggered:if(root.current && root.item) {
            root.shown();if(root.item.activate)root.item.activate();
        }
    }
}
