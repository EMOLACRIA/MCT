import QtQuick
Item {
    id:root
    required property var uiState
    required property var backend
    property bool held:false
    property real draft:0
    Binding {target:root.uiState;property:"feedbackHeld";value:root.held}
    function toggleMute() {
        if(uiState.feedbackKind==="microphone")backend.toggleMicrophone();
        else if(uiState.feedbackKind!=="brightness")backend.toggleMute();
    }
    function commit(value) {
        const v=Math.round(value);
        if(uiState.feedbackKind==="brightness")backend.setBrightness(v);
        else if(uiState.feedbackKind==="microphone")backend.setMicrophoneVolume(v);
        else backend.setVolume(v);
    }
    function move(value) {draft=value;if(!throttle.running)throttle.start();}
    function release(value) {throttle.stop();commit(value);}
    Timer {id:throttle;interval:90;onTriggered:root.commit(root.draft)}
}
