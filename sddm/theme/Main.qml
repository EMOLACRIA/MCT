import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: root
    width: 1600
    height: 1000
    color: "#191a18"
    property bool busy: false
    property string failure: ""
    property string powerAction: ""
    property date now: new Date()

    function login() {
        if (busy || username.text.trim() === "" || sessions.currentIndex < 0)
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
        color: "#181a18"
        opacity: 0.12
    }
    Timer {
        interval: 1000; running: true; repeat: true
        onTriggered: root.now = new Date()
    }
    Column {
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.rightMargin: parent.width * 0.065
        anchors.topMargin: parent.height * 0.06
        spacing: 8
        Text {
            anchors.right: parent.right
            text: Qt.formatDateTime(root.now, "HH:mm")
            color: "#e5dcc6"
            font.family: "serif"
            font.pixelSize: 42
        }
        Text {
            anchors.right: parent.right
            text: Qt.formatDateTime(root.now, "dddd, d MMMM")
            color: "#aaa89b"
            font.pixelSize: 12
        }
    }

    component Field: TextField {
        implicitHeight: 42
        color: "#d8d3c5"
        placeholderTextColor: "#888b7d"
        font.pixelSize: 14
        leftPadding: 12
        rightPadding: 12
        selectionColor: "#77715e"
        selectedTextColor: "#ffffff"
        background: Rectangle {
            color: "#252620"
            border.width: 1
            border.color: parent.activeFocus ? "#b5a37c" : "#55564c"
        }
    }
    component ActionButton: Button {
        id: actionButton
        implicitHeight: 40
        font.pixelSize: 13
        contentItem: Text {
            text: actionButton.text
            color: actionButton.enabled ? "#d8d3c5" : "#777a70"
            font: actionButton.font
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
        background: Rectangle {
            color: actionButton.down ? "#484334" : actionButton.hovered ? "#35342c" : "#252620"
            border.width: 1
            border.color: actionButton.activeFocus ? "#d8d3c5" : "#77715e"
        }
    }

    Rectangle {
        id: card
        width: Math.min(380, parent.width - 48)
        height: form.implicitHeight + 64
        anchors.right: parent.right
        anchors.rightMargin: Math.max(24, parent.width * 0.065)
        anchors.verticalCenter: parent.verticalCenter
        color: "#ee191a18"
        border.width: 1
        border.color: "#77715e"
        Image { anchors.left: parent.left; anchors.top: parent.top; width: 20; height: 20; source: "tl.svg" }
        Image { anchors.right: parent.right; anchors.top: parent.top; width: 20; height: 20; source: "tr.svg" }
        Image { anchors.left: parent.left; anchors.bottom: parent.bottom; width: 20; height: 20; source: "bl.svg" }
        Image { anchors.right: parent.right; anchors.bottom: parent.bottom; width: 20; height: 20; source: "br.svg" }
        ColumnLayout {
            id: form
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.margins: 32
            spacing: 12
            Text {
                text: "Welcome back"
                color: "#e5dcc6"
                font.family: "serif"
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
                enabled: !root.busy
                Accessible.name: "Session"
                contentItem: Text {
                    text: sessions.displayText
                    color: "#aaa89b"
                    font.pixelSize: 12
                    verticalAlignment: Text.AlignVCenter
                    leftPadding: 12
                    rightPadding: 28
                    elide: Text.ElideRight
                }
                indicator: Text {
                    x: sessions.width - 24
                    y: (sessions.height - height) / 2
                    text: "⌄"
                    color: "#b5a37c"
                }
                background: Rectangle {
                    color: "#252620"
                    border.color: sessions.activeFocus ? "#b5a37c" : "#55564c"
                }
                delegate: ItemDelegate {
                    width: sessions.width
                    highlighted: sessions.highlightedIndex === index
                    contentItem: Text { text: model.name; color: "#d8d3c5"; font.pixelSize: 12 }
                    background: Rectangle { color: parent.highlighted ? "#35342c" : "#191a18" }
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
                    background: Rectangle { color: "#191a18"; border.color: "#77715e" }
                }
            }
            ActionButton {
                objectName: "signIn"
                Layout.fillWidth: true
                text: root.busy ? "Signing in…" : "Sign in"
                enabled: !root.busy && username.text.trim().length > 0 && sessions.count > 0
                onClicked: root.login()
            }
            Text {
                visible: root.failure.length > 0
                text: root.failure
                color: "#ce9582"
                font.pixelSize: 12
                wrapMode: Text.WordWrap
                Layout.fillWidth: true
            }
            Rectangle { Layout.fillWidth: true; height: 1; color: "#45473e"; Layout.topMargin: 8 }
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
    Popup {
        id: confirm
        objectName: "powerConfirmation"
        anchors.centerIn: parent
        width: Math.min(360, root.width - 48)
        modal: true
        focus: true
        padding: 24
        closePolicy: Popup.CloseOnEscape
        background: Rectangle { color: "#191a18"; border.color: "#b5a37c" }
        contentItem: ColumnLayout {
            spacing: 18
            Text {
                text: root.powerAction === "restart" ? "Restart the computer?" : "Power off the computer?"
                color: "#d8d3c5"
                font.family: "serif"
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
