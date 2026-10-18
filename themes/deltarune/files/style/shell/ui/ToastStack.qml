import QtQuick
Column {
    id:root;objectName:"toastStack"
    required property var backend
    spacing:SurfaceLayout.toastSpacing
    Repeater {
        model:root.backend.toasts
        delegate:Toast {
            required property var modelData
            width:root.width;height:implicitHeight;note:modelData;backend:root.backend
        }
    }
}
