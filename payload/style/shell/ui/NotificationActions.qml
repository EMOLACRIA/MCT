import QtQuick
import QtQuick.Controls
Flow {
    id:root
    required property var actions
    required property var notificationKey
    required property var backend
    spacing:6
    Repeater {
        model:root.actions
        delegate:ActionButton {
            required property var modelData;objectName:"notificationAction-"+modelData.id
            width:Math.min(implicitWidth,root.width);height:32;text:modelData.text
            onClicked:root.backend.notificationAction(root.notificationKey,modelData.id)
            hint:text
        }
    }
}
