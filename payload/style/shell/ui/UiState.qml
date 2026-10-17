import QtQuick
Item {
    id: root
    visible: false
    property string activePanel: ""
    property string screenName: ""
    property string confirmation: ""
    property string search: ""
    property bool feedbackHeld: false
    onFeedbackHeldChanged: { if(feedbackHeld)hideFeedback.stop();else if(feedbackVisible)hideFeedback.restart(); }
    property bool feedbackVisible: false
    property string feedbackKind: "volume"
    property int feedbackLevel: 0
    property bool feedbackMuted: false
    readonly property var panels: ["launcher","power","controls","notifications","media","hardware"]
    function toggle(panel, screen) {
        if (panels.indexOf(panel) < 0) return;
        const same = activePanel === panel;
        close();
        if (!same) { screenName = screen || ""; activePanel = panel; }
    }
    function close() { activePanel = ""; confirmation = ""; search = ""; }
    function showFeedback(kind, level, muted) {
        feedbackKind = kind; feedbackLevel = Math.max(0,Math.min(100,level));
        feedbackMuted = muted; feedbackVisible = true; if(!feedbackHeld)hideFeedback.restart();
    }
    Timer { id: hideFeedback; interval: 1400; onTriggered: root.feedbackVisible = false }
}
