import QtQuick
import "../ui"
import QtQuick.Controls
import QtQuick.Layouts
// Shared window layout for every theme. Blur, shadows and animations are not offered:
// they stay off for NVIDIA + Hyprland stability.
ColumnLayout {
    id:root
    required property var model
    readonly property bool own:model.draft.layout.themeOwn
    spacing:14
    Text {font.family:Theme.bodyFont;text:"WINDOW LAYOUT · ALL THEMES";color:Theme.brass;font.pixelSize:Theme.fontSize(11);font.letterSpacing:1.2}
    RowLayout {
        Layout.fillWidth:true;spacing:22
        ColumnLayout {
            Layout.fillWidth:true;spacing:12;enabled:!root.own && root.model.active!==null;opacity:enabled ? 1 : .5
            Repeater {
                model:[{key:"gapsIn",label:"Gap between windows",to:20},{key:"gapsOut",label:"Gap to screen edge",to:40},{key:"border",label:"Border width",to:6},{key:"rounding",label:"Corner radius",to:20}]
                PreferenceSlider {
                    required property var modelData
                    objectName:"layout-"+modelData.key;Layout.fillWidth:true;label:modelData.label;unit:" px";from:0;to:modelData.to
                    value:root.model.layoutValue(modelData.key)
                    onChosen:value=>root.model.setLayout(modelData.key,value)
                }
            }
        }
        // Sketch of the screen with two tiled windows at the chosen values.
        Rectangle {
            Layout.preferredWidth:250;Layout.preferredHeight:156;color:Theme.inputSurface;border.color:Theme.line
            Item {
                id:screen;anchors.fill:parent;anchors.margins:1
                readonly property real k:.67
                Repeater {
                    model:2
                    Rectangle {
                        required property int index
                        readonly property real o:root.model.layoutValue("gapsOut")*screen.k
                        readonly property real g:root.model.layoutValue("gapsIn")*screen.k
                        x:index===0 ? o : (screen.width+g)/2
                        y:o;height:screen.height-2*o
                        width:(screen.width-g)/2-o
                        radius:root.model.layoutValue("rounding")*screen.k
                        color:Theme.raised;border.width:Math.max(1,root.model.layoutValue("border")*screen.k);border.color:index===0 ? Theme.brass : Theme.line
                    }
                }
            }
        }
    }
    RowLayout {
        Layout.fillWidth:true
        Text {font.family:Theme.bodyFont;text:"Use each theme's own layout";color:Theme.ink;font.pixelSize:Theme.fontSize(13);Layout.fillWidth:true}
        ActionButton {objectName:"layoutThemeOwn";text:root.own ? "On" : "Off";selected:root.own;enabled:root.model.active!==null;onClicked:root.model.setThemeOwn(!root.own)}
    }
    Text {font.family:Theme.bodyFont;Layout.fillWidth:true;wrapMode:Text.WordWrap;text:"Applies to the active theme now and to every theme you switch to later. Blur, shadows and window animations stay off for stability.";color:Theme.muted;font.pixelSize:Theme.fontSize(11)}
    Item {Layout.fillHeight:true}
}
