import QtQuick
QtObject {
    id: root
    property var themes: []
    property var activeTheme: null
    property string selectedId: ""
    property string checkedId: ""
    property bool busy: false
    property bool ready: false
    property bool canRollback: false
    property bool pending: false
    property string stateError: ""
    property string message: ""
    property bool failed: false
    property string action: ""
    property bool rollbackArmed: false
    property bool reduceMotion: false
    property real fontScale: 1
    property string monoFontSource: ""
    signal applied()
    readonly property var selected: {
        for (let i = 0; i < themes.length; ++i)
            if (themes[i].id === selectedId) return themes[i];
        return null;
    }
    readonly property bool blocked: busy || !ready || pending || stateError !== ""
    readonly property bool isActive: selected !== null && activeTheme !== null
                                    && selected.id === activeTheme.id && selected.version === activeTheme.version
    readonly property bool canCheck: !blocked && selected !== null && selected.valid && !isActive
    readonly property bool canApply: canCheck
    signal requested(string action, string theme)

    function choose(id) {
        if (busy || selectedId === id) return;
        selectedId = id; checkedId = ""; message = ""; failed = false; rollbackArmed = false;
    }
    function navigate(delta) {
        if (busy || !themes.length) return;
        let index = 0;
        for (let i = 0; i < themes.length; ++i) if (themes[i].id === selectedId) index = i;
        choose(themes[(index + delta + themes.length) % themes.length].id);
    }
    function activate(id) {
        if (blocked) return;
        choose(id);
        if (canApply) run("apply");
    }
    function run(next) {
        if (busy) return;
        if (next === "check" && !canCheck) return;
        if (next === "apply" && !canApply) return;
        if (next === "rollback") {
            if (blocked || !canRollback) return;
            if (!rollbackArmed) {rollbackArmed = true; return;}
        }
        rollbackArmed = false; busy = true; action = next; failed = false;
        message = next === "catalog" ? "" : next === "check" ? "Checking compatibility…"
                    : next === "apply" ? "Checking & switching…" : "Restoring previous desktop…";
        if (next === "check" || next === "catalog") checkedId = "";
        requested(next, next === "apply" || next === "check" ? selectedId : "");
    }
    function accept(reply) {
        if (!reply || typeof reply.ok !== "boolean" || reply.action !== action
            || ((action === "check" || action === "apply") && reply.theme !== selectedId)) {
            fail("The theme helper returned an invalid response. Refresh to read the current state."); return;
        }
        if (reply.catalog) {
            themes = reply.catalog.themes || [];
            for (let i = 0; i < themes.length; ++i)
                if (themes[i].fontSource) monoFontSource = themes[i].fontSource;
            activeTheme = reply.catalog.active || null;
            canRollback = !!reply.catalog.canRollback;
            pending = !!reply.catalog.pending;
            stateError = reply.catalog.stateError || "";
            reduceMotion = !!reply.catalog.reduceMotion;
            fontScale = reply.catalog.fontScale || 1;
            ready = true;
            let found = false;
            for (let i = 0; i < themes.length; ++i) if (themes[i].id === selectedId) found = true;
            if (!found) selectedId = activeTheme && themes.some(t => t.id === activeTheme.id)
                                    ? activeTheme.id : themes.length ? themes[0].id : "";
        }
        checkedId = reply.ok && action === "check" ? selectedId : "";
        const switched = reply.ok && (action === "apply" || action === "rollback");
        message = switched ? "Ready." : reply.message || "";
        failed = !reply.ok; busy = false; action = "";
        if (switched) applied();
    }
    function fail(text) {
        busy = false; failed = true; message = text; checkedId = ""; action = ""; rollbackArmed = false;
    }
}
