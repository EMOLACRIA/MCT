import QtQuick
import "../ui"
import QtQuick.Controls
import QtQuick.Layouts
Item {
    id:root;objectName:"settingsPanel"
    required property var backend
    required property var uiState
    readonly property var preferences:backend.preferences
    readonly property var themeConfig:backend.themeConfig
    property bool resetPending:false
    // 0 shell preferences (saved instantly) · 1 shared window layout · 2 active theme.
    property int tab:0
    function activate() {resetPending=false;root.forceActiveFocus();backend.reloadPreferences();themeConfig.reload();}
    ColumnLayout {
        anchors.fill:parent;spacing:16
        PanelHeader {
            title:"Preferences";titleSize:27;symbol:"settings";onClosed:uiState.close()
            extraAction:Component {ActionButton {objectName:"returnToControls";text:"Controls";onClicked:uiState.toggle("controls",uiState.screenName)}}
        }
        Text { font.family:Theme.bodyFont;Layout.fillWidth:true;text:backend.previewMode ? "Preview · changes stay in this window" : root.tab===0 ? "Changes are saved automatically" : "Changes wait for Apply; theme.sh rollback undoes an applied change";color:Theme.muted;font.pixelSize:Theme.fontSize(11)}
        Row {
            spacing:6
            Repeater {
                model:["Shell","Layout",root.themeConfig.active ? root.themeConfig.active.name : "Theme"]
                ActionButton {required property int index;required property string modelData;objectName:"settingsTab"+index;text:modelData;selected:root.tab===index;onClicked:root.tab=index}
            }
        }
        Rectangle {Layout.fillWidth:true;height:1;color:Theme.line}
        LayoutTab {visible:root.tab===1;Layout.fillWidth:true;Layout.fillHeight:true;model:root.themeConfig}
        ThemeTab {id:themeTab;visible:root.tab===2;Layout.fillWidth:true;Layout.fillHeight:true;model:root.themeConfig}
        ColumnLayout {
            visible:root.tab!==0;Layout.fillWidth:true;spacing:8
            Rectangle {Layout.fillWidth:true;height:1;color:Theme.line}
            RowLayout {
                Layout.fillWidth:true;spacing:8
                Text {
                    objectName:"themeConfigSummary";Layout.fillWidth:true;wrapMode:Text.WordWrap;font.family:Theme.bodyFont;font.pixelSize:Theme.fontSize(12)
                    readonly property var m:root.themeConfig
                    color:m.error ? Theme.danger : Theme.muted
                    text:m.error ? m.error : m.busy ? "Working…" : m.notice!=="" ? m.notice
                         : m.active===null ? "Choose a theme with Super+G first."
                         : m.dirty ? m.changeCount+" changes from defaults · not applied yet"
                         : m.applied===false ? "Saved settings are not applied" : m.changeCount+" changes from defaults · applied"
                }
                ActionButton {objectName:"discardThemeConfig";text:"Discard";visible:root.themeConfig.dirty;onClicked:root.themeConfig.discard()}
                ActionButton {objectName:"applyThemeConfig";text:"Apply";selected:root.themeConfig.canApply;enabled:root.themeConfig.canApply;onClicked:themeTab.apply()}
            }
        }
        Flickable {
            id:scroll;objectName:"settingsScroll";visible:root.tab===0
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
        Text { font.family:Theme.bodyFont;objectName:"preferenceStatus";Layout.fillWidth:true;visible:root.tab===0 && text!=="";text:root.preferences.error || (root.preferences.saving ? "Saving…" : root.preferences.notice);textFormat:Text.PlainText;wrapMode:Text.WordWrap;color:root.preferences.error ? Theme.danger : Theme.brass;font.pixelSize:Theme.fontSize(12)}
    }
}
