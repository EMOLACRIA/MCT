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
    // Rail entries are family heads; variants (deltarune-*) appear under their head.
    readonly property var railThemes: themes.filter(t => (t.family || t.id) === t.id)
    function familyOf(id) {
        for (let i = 0; i < themes.length; ++i)
            if (themes[i].id === id) return themes[i].family || id;
        return id;
    }
    function familyMembers(head) {
        const members = themes.filter(t => (t.family || t.id) === head);
        return members.filter(t => t.id === head).concat(members.filter(t => t.id !== head));
    }
    readonly property string selectedFamily: familyOf(selectedId)
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
        // Left/right: between rail entries; a family is entered at its head.
        const rail = railThemes;
        if (busy || !rail.length) return;
        let index = 0;
        for (let i = 0; i < rail.length; ++i) if (rail[i].id === selectedFamily) index = i;
        choose(rail[(index + delta + rail.length) % rail.length].id);
    }
    function step(delta) {
        // Up/down: within the selected family (head first, then variants).
        const members = familyMembers(selectedFamily);
        if (busy || members.length < 2) return;
        let index = 0;
        for (let i = 0; i < members.length; ++i) if (members[i].id === selectedId) index = i;
        choose(members[Math.max(0, Math.min(members.length - 1, index + delta))].id);
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
