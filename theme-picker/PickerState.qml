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
    readonly property var selected: {
        for (let i = 0; i < themes.length; ++i)
            if (themes[i].id === selectedId) return themes[i];
        return null;
    }
    readonly property bool blocked: busy || !ready || pending || stateError !== ""
    readonly property bool isActive: selected !== null && activeTheme !== null
                                    && selected.id === activeTheme.id && selected.version === activeTheme.version
    readonly property bool canCheck: !blocked && selected !== null && selected.valid && !isActive
    readonly property bool canApply: canCheck && checkedId === selectedId
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
    function run(next) {
        if (busy) return;
        if (next === "check" && !canCheck) return;
        if (next === "apply" && !canApply) return;
        if (next === "rollback") {
            if (blocked || !canRollback) return;
            if (!rollbackArmed) {rollbackArmed = true; return;}
        }
        rollbackArmed = false; busy = true; action = next; failed = false;
        message = next === "catalog" ? "Loading themes…" : next === "check" ? "Checking compatibility…"
                    : next === "apply" ? "Switching desktop…" : "Restoring previous desktop…";
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
            activeTheme = reply.catalog.active || null;
            canRollback = !!reply.catalog.canRollback;
            pending = !!reply.catalog.pending;
            stateError = reply.catalog.stateError || "";
            ready = true;
            let found = false;
            for (let i = 0; i < themes.length; ++i) if (themes[i].id === selectedId) found = true;
            if (!found) selectedId = activeTheme && themes.some(t => t.id === activeTheme.id)
                                    ? activeTheme.id : themes.length ? themes[0].id : "";
        }
        checkedId = reply.ok && action === "check" ? selectedId : "";
        message = reply.message || ""; failed = !reply.ok; busy = false; action = "";
    }
    function fail(text) {
        busy = false; failed = true; message = text; checkedId = ""; action = ""; rollbackArmed = false;
    }
}
