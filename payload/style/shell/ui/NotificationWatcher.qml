import QtQuick
Item {
    id:root
    visible:false
    required property var notification
    signal updated()
    // One Notify replacement can change several properties in the same event.
    // Refresh once after that group instead of creating duplicate cards/timers.
    Timer { id:refresh; interval:0; onTriggered:if(root.notification)root.updated() }
    Connections {
        target:root.notification
        function onSummaryChanged() {refresh.restart();}
        function onBodyChanged() {refresh.restart();}
        function onAppNameChanged() {refresh.restart();}
        function onActionsChanged() {refresh.restart();}
        function onExpireTimeoutChanged() {refresh.restart();}
        function onTransientChanged() {refresh.restart();}
        function onClosed() {refresh.stop();root.destroy();}
    }
}
