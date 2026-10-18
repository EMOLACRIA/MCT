import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
Item {
    id:root;objectName:"settingsPanel"
    required property var backend
    required property var uiState
    readonly property var preferences:backend.preferences
    property bool resetPending:false
    function activate() {root.forceActiveFocus();backend.reloadPreferences();}
    ColumnLayout {
        anchors.fill:parent;spacing:16
        PanelHeader {
            title:"Preferences";titleSize:27;symbol:"settings";onClosed:uiState.close()
            extraAction:Component {ActionButton {objectName:"returnToControls";text:"Controls";onClicked:uiState.toggle("controls",uiState.screenName)}}
        }
        Text { font.family:Theme.bodyFont;Layout.fillWidth:true;text:backend.previewMode ? "Preview · changes stay in this window" : "Changes are saved automatically";color:Theme.muted;font.pixelSize:Theme.fontSize(11)}
        Flickable {
            id:scroll;objectName:"settingsScroll"
            Layout.fillWidth:true;Layout.fillHeight:true;clip:true;contentHeight:details.implicitHeight;boundsBehavior:Flickable.StopAtBounds
            ScrollBar.vertical:ScrollBar {}
            ColumnLayout {
                id:details;width:scroll.width-14;spacing:15
                enabled:root.preferences.ready && !root.preferences.saving
                Text { font.family:Theme.bodyFont;text:"APPEARANCE";color:Theme.brass;font.pixelSize:Theme.fontSize(11);font.letterSpacing:1.2}
                PreferenceSlider {objectName:"fontScale";Layout.fillWidth:true;label:"Shell text size";from:90;to:120;step:5;value:root.preferences.values.fontScale*100;onChosen:value=>root.preferences.request("fontScale",value/100)}
                PreferenceSlider {objectName:"surfaceOpacity";Layout.fillWidth:true;label:"Surface opacity";from:75;to:100;value:root.preferences.values.surfaceOpacity*100;onChosen:value=>root.preferences.request("surfaceOpacity",value/100)}
                Repeater {
                    model:[{key:"reduceMotion",label:"Reduce motion"},{key:"barFloating",label:"Floating bar"},{key:"barShowDate",label:"Show date"},{key:"barShowTray",label:"Show system tray"},{key:"centerPanels",label:"Center side panels"}]
                    delegate:RowLayout {
                        required property var modelData
                        Layout.fillWidth:true
                        Text { font.family:Theme.bodyFont;text:modelData.label;color:Theme.ink;font.pixelSize:Theme.fontSize(13);Layout.fillWidth:true;wrapMode:Text.WordWrap}
                        ActionButton {objectName:modelData.key+"Toggle";text:root.preferences.values[modelData.key] ? "On" : "Off";selected:root.preferences.values[modelData.key];onClicked:root.preferences.request(modelData.key,!root.preferences.values[modelData.key])}
                    }
                }
                Text { font.family:Theme.bodyFont;text:"Volume and brightness position";color:Theme.ink;font.pixelSize:Theme.fontSize(13)}
                PreferenceChoice {objectName:"osdPositionChoice";Layout.fillWidth:true;choices:[{id:"bottom",name:"Bottom"},{id:"top",name:"Top"}];selection:root.preferences.values.osdPosition;onChosen:id=>root.preferences.request("osdPosition",id)}
                Rectangle {Layout.fillWidth:true;height:1;color:Theme.line}
                Text { font.family:Theme.bodyFont;text:"APPLICATIONS";color:Theme.brass;font.pixelSize:Theme.fontSize(11);font.letterSpacing:1.2}
                Text { font.family:Theme.bodyFont;text:"Terminal · Super+Q and terminal applications";color:Theme.ink;font.pixelSize:Theme.fontSize(13);Layout.fillWidth:true;wrapMode:Text.WordWrap}
                PreferenceChoice {objectName:"terminalChoice";Layout.fillWidth:true;choices:root.preferences.terminals.filter(t=>t.available);selection:root.preferences.values.terminal;onChosen:id=>root.preferences.request("terminal",id)}
                Text { font.family:Theme.bodyFont;text:"File manager · Super+E";color:Theme.ink;font.pixelSize:Theme.fontSize(13)}
                PreferenceChoice {objectName:"fileManagerChoice";Layout.fillWidth:true;choices:backend.fileManagerChoices;selection:root.preferences.values.fileManager;onChosen:id=>root.preferences.request("fileManager",id)}
                Text { font.family:Theme.bodyFont;text:"Existing custom shortcuts keep their commands.";color:Theme.muted;font.pixelSize:Theme.fontSize(11);Layout.fillWidth:true;wrapMode:Text.WordWrap}
                Rectangle {Layout.fillWidth:true;height:1;color:Theme.line}
                Text { font.family:Theme.bodyFont;text:"DIAGNOSTICS";color:Theme.brass;font.pixelSize:Theme.fontSize(11);font.letterSpacing:1.2}
                RowLayout {
                    ActionButton {objectName:"diagnosePreferences";text:"Refresh diagnostics";onClicked:backend.diagnosePreferences()}
                    ActionButton {text:"Reload preferences";onClicked:backend.reloadPreferences()}
                }
                Text { font.family:Theme.bodyFont;Layout.fillWidth:true;text:root.preferences.path;textFormat:Text.PlainText;wrapMode:Text.WrapAnywhere;color:Theme.muted;font.pixelSize:Theme.fontSize(11)}
                Text { font.family:Theme.bodyFont;Layout.fillWidth:true;visible:text!=="";text:root.preferences.diagnostics;textFormat:Text.PlainText;wrapMode:Text.WrapAnywhere;color:Theme.ink;font.pixelSize:Theme.fontSize(11)}
                Rectangle {Layout.fillWidth:true;height:1;color:Theme.line}
                Text { font.family:Theme.bodyFont;Layout.fillWidth:true;visible:root.resetPending;text:"Reset these preferences? The previous file will be retained.";wrapMode:Text.WordWrap;color:Theme.ink;font.pixelSize:Theme.fontSize(12)}
                RowLayout {
                    ActionButton {objectName:"resetPreferences";text:root.resetPending ? "Confirm reset" : "Reset preferences";destructive:root.resetPending;onClicked: {if(root.resetPending){root.preferences.reset();root.resetPending=false;}else root.resetPending=true;}}
                    ActionButton {visible:root.resetPending;text:"Cancel";onClicked:root.resetPending=false}
                }
            }
        }
        Text { font.family:Theme.bodyFont;objectName:"preferenceStatus";Layout.fillWidth:true;visible:text!=="";text:root.preferences.error || (root.preferences.saving ? "Saving…" : root.preferences.notice);textFormat:Text.PlainText;wrapMode:Text.WordWrap;color:root.preferences.error ? Theme.danger : Theme.brass;font.pixelSize:Theme.fontSize(12)}
    }
}
