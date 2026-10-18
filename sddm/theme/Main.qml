import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: root
    width: 1600
    height: 1000
    color: root.skin.c191a18
    readonly property LoginSkin skin:LoginSkin {}
    property bool busy: false
    property string failure: ""
    property string powerAction: ""
    property date now: new Date()
    readonly property bool compact: height < 700

    component StyledText:Text {font.family:root.skin.bodyFont}
    function reveal(item) {
        if (!item.activeFocus) return;
        let ancestor = item.parent;
        while (ancestor && ancestor !== form) ancestor = ancestor.parent;
        if (!ancestor) return;
        const top = item.mapToItem(form, 0, 0).y;
        formScroll.contentY = Math.max(0, Math.min(formScroll.contentHeight - formScroll.height,
            Math.max(top + item.height - formScroll.height, Math.min(top, formScroll.contentY))));
    }

    function login() {
        if (busy || username.text.trim() === "" || sessions.currentIndex < 0 || sessions.currentIndex >= sessions.count)
            return;
        failure = "";
        busy = true;
        sddm.login(username.text.trim(), password.text, sessions.currentIndex);
    }

    Image {
        anchors.fill: parent
        source: "wallpaper.png"
        fillMode: Image.PreserveAspectCrop
        asynchronous: true
    }
    Rectangle {
        anchors.fill: parent
        color: root.skin.c181a18
        opacity: 0.12
    }
    Timer {
        interval: 1000; running: true; repeat: true
        onTriggered: root.now = new Date()
    }
    Rectangle {
        visible:root.skin.clockPlate
        x:clock.x-14;y:clock.y-10;width:clock.width+28;height:clock.height+20
        color:root.skin.cee191a18;border.color:root.skin.c77715e
    }
    Column {
        id: clock
        objectName: "loginClock"
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.rightMargin: parent.width * 0.065
        anchors.topMargin: root.compact ? 16 : parent.height * 0.06
        spacing: root.compact ? 4 : 8
        StyledText {
            anchors.right: parent.right
            text: Qt.formatDateTime(root.now, "HH:mm")
            color: root.skin.ce5dcc6
            font.family: root.skin.displayFont
            font.pixelSize: root.compact ? 32 : 42
        }
        StyledText {
            anchors.right: parent.right
            text: Qt.formatDateTime(root.now, "dddd, d MMMM")
            color: root.skin.caaa89b
            font.pixelSize: 12
        }
    }

    component Field: TextField {
        font.family:root.skin.bodyFont
        onActiveFocusChanged: root.reveal(this)
        implicitHeight: 42
        color: root.skin.cd8d3c5
        placeholderTextColor: root.skin.c888b7d
        font.pixelSize: 14
        leftPadding: 12
        rightPadding: 12
        selectionColor: root.skin.c77715e
        selectedTextColor: root.skin.cffffff
        background: Rectangle {
            color: root.skin.c252620
            border.width: 1
            border.color: parent.activeFocus ? root.skin.cb5a37c : root.skin.c55564c
        }
    }
    component ActionButton: Button {
        font.family:root.skin.bodyFont
        id: actionButton
        onActiveFocusChanged: root.reveal(this)
        implicitHeight: 40
        font.pixelSize: 13
        contentItem: StyledText {
            text: actionButton.text
            color: actionButton.enabled ? root.skin.cd8d3c5 : root.skin.c777a70
            font: actionButton.font
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
        background: Rectangle {
            color: actionButton.down ? root.skin.c484334 : actionButton.hovered ? root.skin.c35342c : root.skin.c252620
            border.width: 1
            border.color: actionButton.activeFocus ? root.skin.cd8d3c5 : root.skin.c77715e
        }
    }

    Rectangle {
        id: card
        objectName: "loginCard"
        width: Math.min(380, parent.width - 48)
        readonly property int inset: root.compact ? 24 : 32
        height: Math.min(form.implicitHeight + inset * 2, root.height - clock.y - clock.height - 40)
        anchors.right: root.skin.formOnLeft ? undefined : parent.right
        anchors.left: root.skin.formOnLeft ? parent.left : undefined
        anchors.leftMargin: Math.max(24, parent.width * 0.065)
        anchors.rightMargin: Math.max(24, parent.width * 0.065)
        y: Math.max(clock.y + clock.height + 16, (root.height - height) / 2)
        color: root.skin.cee191a18
        border.width: 1
        border.color: root.skin.c77715e
        Image { anchors.left: parent.left; anchors.top: parent.top; width: root.skin.cornerSize; height: root.skin.cornerSize; source: "tl.svg" }
        Image { anchors.right: parent.right; anchors.top: parent.top; width: root.skin.cornerSize; height: root.skin.cornerSize; source: "tr.svg" }
        Image { anchors.left: parent.left; anchors.bottom: parent.bottom; width: root.skin.cornerSize; height: root.skin.cornerSize; source: "bl.svg" }
        Image { anchors.right: parent.right; anchors.bottom: parent.bottom; width: root.skin.cornerSize; height: root.skin.cornerSize; source: "br.svg" }
        Flickable {
            id: formScroll
            objectName: "loginScroll"
            anchors.fill: parent
            anchors.margins: card.inset
            clip: true
            contentWidth: width
            contentHeight: form.implicitHeight
            boundsBehavior: Flickable.StopAtBounds
            interactive: contentHeight > height
            ScrollIndicator.vertical: ScrollIndicator { }
            ColumnLayout {
                id: form
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                spacing: 12
                StyledText {
                    text: "Welcome back"
                    color: root.skin.ce5dcc6
                    font.family: root.skin.displayFont
                    font.pixelSize: 26
                    Layout.bottomMargin: 8
                }
                Field {
                    id: username
                    objectName: "username"
                    Layout.fillWidth: true
                    placeholderText: "Username"
                    text: userModel.lastUser
                    enabled: !root.busy
                    onAccepted: password.forceActiveFocus()
                    Accessible.name: "Username"
                }
                Field {
                    id: password
                    objectName: "password"
                    Layout.fillWidth: true
                    placeholderText: "Password"
                    echoMode: TextInput.Password
                    enabled: !root.busy
                    onAccepted: root.login()
                    Accessible.name: "Password"
                }
                ComboBox {
                    id: sessions
                    objectName: "sessions"
                    Layout.fillWidth: true
                    implicitHeight: 40
                    model: sessionModel
                    textRole: "name"
                    currentIndex: sessionModel.lastIndex >= 0 ? sessionModel.lastIndex : 0
                    enabled: !root.busy && count > 0
                    onActiveFocusChanged: root.reveal(this)
                    Accessible.name: "Session"
                    contentItem: StyledText {
                        text: sessions.count > 0 ? sessions.displayText : "No sessions available"
                        color: root.skin.caaa89b
                        font.pixelSize: 12
                        verticalAlignment: Text.AlignVCenter
                        leftPadding: 12
                        rightPadding: 28
                        elide: Text.ElideRight
                    }
                    indicator: StyledText {
                        x: sessions.width - 24
                        y: (sessions.height - height) / 2
                        text: "⌄"
                        color: root.skin.cb5a37c
                    }
                    background: Rectangle {
                        color: root.skin.c252620
                        border.color: sessions.activeFocus ? root.skin.cb5a37c : root.skin.c55564c
                    }
                    delegate: ItemDelegate {
                        width: sessions.width
                        highlighted: sessions.highlightedIndex === index
                        contentItem: StyledText { text: model.name; color: root.skin.cd8d3c5; font.pixelSize: 12 }
                        background: Rectangle { color: parent.highlighted ? root.skin.c35342c : root.skin.c191a18 }
                    }
                    popup: Popup {
                        y: sessions.height + 4
                        width: sessions.width
                        implicitHeight: Math.min(contentItem.implicitHeight + 8, 240)
                        padding: 4
                        contentItem: ListView {
                            clip: true
                            implicitHeight: contentHeight
                            model: sessions.popup.visible ? sessions.delegateModel : null
                            currentIndex: sessions.highlightedIndex
                            ScrollIndicator.vertical: ScrollIndicator { }
                        }
                        background: Rectangle { color: root.skin.c191a18; border.color: root.skin.c77715e }
                    }
                }
                ActionButton {
                    objectName: "signIn"
                    Layout.fillWidth: true
                    text: root.busy ? "Signing in…" : "Sign in"
                    enabled: !root.busy && username.text.trim().length > 0 && sessions.count > 0
                    onClicked: root.login()
                }
                StyledText {
                    visible: root.failure.length > 0
                    text: root.failure
                    color: root.skin.cce9582
                    font.pixelSize: 12
                    wrapMode: Text.WordWrap
                    Layout.fillWidth: true
                }
                Rectangle { Layout.fillWidth: true; height: 1; color: root.skin.c45473e; Layout.topMargin: 8 }
                RowLayout {
                    Layout.fillWidth: true
                    spacing: 12
                    ActionButton {
                        objectName: "restart"
                        Layout.fillWidth: true
                        text: "Restart"
                        visible: sddm.canReboot
                        enabled: !root.busy
                        onClicked: { root.powerAction = "restart"; confirm.open(); }
                    }
                    ActionButton {
                        objectName: "powerOff"
                        Layout.fillWidth: true
                        text: "Power off"
                        visible: sddm.canPowerOff
                        enabled: !root.busy
                        onClicked: { root.powerAction = "poweroff"; confirm.open(); }
                    }
                }
            }
        }
    }
    Popup {
        id: confirm
        objectName: "powerConfirmation"
        anchors.centerIn: parent
        width: Math.min(360, root.width - 48)
        modal: true
        focus: true
        padding: 24
        closePolicy: Popup.CloseOnEscape
        background: Rectangle { color: root.skin.c191a18; border.color: root.skin.cb5a37c }
        contentItem: ColumnLayout {
            spacing: 18
            StyledText {
                text: root.powerAction === "restart" ? "Restart the computer?" : "Power off the computer?"
                color: root.skin.cd8d3c5
                font.family: root.skin.displayFont
                font.pixelSize: 18
                Layout.fillWidth: true
                wrapMode: Text.WordWrap
            }
            RowLayout {
                Layout.fillWidth: true
                ActionButton { id: cancelButton; Layout.fillWidth: true; text: "Cancel"; onClicked: confirm.close() }
                ActionButton {
                    Layout.fillWidth: true
                    text: "Confirm"
                    onClicked: {
                        confirm.close();
                        if (root.powerAction === "restart") sddm.reboot();
                        else sddm.powerOff();
                    }
                }
            }
        }
        onOpened: cancelButton.forceActiveFocus()
    }
    Connections {
        target: sddm
        function onLoginFailed() {
            root.busy = false;
            root.failure = "Sign in failed. Please try again.";
            password.text = "";
            password.forceActiveFocus();
        }
        function onLoginSucceeded() { password.text = ""; }
    }
    Component.onCompleted: {
        if (username.text.length > 0) password.forceActiveFocus();
        else username.forceActiveFocus();
    }
}
