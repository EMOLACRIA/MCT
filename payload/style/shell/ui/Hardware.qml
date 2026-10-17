import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
Item {
    id:root
    required property var backend
    required property var uiState
    readonly property var metrics:backend.hardware
    function activate() {root.forceActiveFocus();}
    function shown(value,suffix) {return value===undefined || value===null ? "—" : value+suffix;}
    ColumnLayout {
        anchors.fill:parent; spacing:18
        RowLayout {
            Glyph {symbol:"hardware"; Layout.preferredWidth:26; Layout.preferredHeight:26}
            Text {text:"Hardware"; color:Theme.ink; font.family:Theme.displayFont; font.pixelSize:28; Layout.fillWidth:true}
            Text {text:backend.previewMode ? "DEMO" : "LIVE · 2s"; color:Theme.brass; font.pixelSize:10; font.letterSpacing:1.5}
            ActionButton {symbol:"close"; Layout.preferredWidth:36; Layout.preferredHeight:36; padding:8; onClicked:uiState.close()}
        }
        Text {Layout.fillWidth:true; text:root.metrics.cpuName || "Reading sensors…"; textFormat:Text.PlainText; color:Theme.muted; font.pixelSize:12; elide:Text.ElideRight}
        RowLayout {
            Layout.fillWidth:true; spacing:12
            Repeater {
                model:[{label:"CPU LOAD",value:root.shown(root.metrics.cpuUsage,"%"),level:root.metrics.cpuUsage || 0},{label:"CPU TEMP",value:root.shown(root.metrics.cpuTemp,"°C"),level:root.metrics.cpuTemp || 0},{label:"MEMORY",value:root.shown(root.metrics.memoryUsed," GiB"),level:root.metrics.memoryPercent || 0}]
                delegate:Rectangle {
                    required property var modelData
                    Layout.fillWidth:true; Layout.preferredHeight:110
                    color:Theme.raised; border.color:Theme.line
                    Text {x:16;y:16;text:modelData.label;color:Theme.brass;font.pixelSize:9;font.letterSpacing:1.3}
                    Text {x:16;y:38;text:modelData.value;color:Theme.ink;font.family:Theme.displayFont;font.pixelSize:30}
                    Rectangle {x:16;y:88;width:parent.width-32;height:2;color:Theme.line;Rectangle {height:2;width:parent.width*Math.min(100,modelData.level)/100;color:modelData.label==="CPU TEMP" && modelData.level>=90 ? Theme.danger : Theme.brass}}
                }
            }
        }
        Flickable {
            Layout.fillWidth:true; Layout.fillHeight:true; clip:true; contentHeight:details.implicitHeight; boundsBehavior:Flickable.StopAtBounds
            ScrollBar.vertical:ScrollBar {}
            ColumnLayout {
                id:details; width:parent.width; spacing:12
                Text {text:"GRAPHICS"; color:Theme.brass; font.pixelSize:10; font.letterSpacing:1.4}
                Repeater {model:root.metrics.gpus || []; delegate:ColumnLayout {required property var modelData;Layout.fillWidth:true;spacing:4
                    Text {text:modelData.name;textFormat:Text.PlainText;color:Theme.ink;font.pixelSize:13;Layout.fillWidth:true;elide:Text.ElideRight}
                    Text {text:modelData.state;textFormat:Text.PlainText;color:Theme.muted;font.pixelSize:12;Layout.fillWidth:true;wrapMode:Text.WordWrap}
                }}
                Text {visible:!(root.metrics.gpus || []).length;text:"GPU information unavailable";color:Theme.muted;font.pixelSize:12}
                Rectangle {Layout.fillWidth:true;height:1;color:Theme.line}
                RowLayout {Layout.fillWidth:true
                    Text {text:"Memory";color:Theme.muted;font.pixelSize:12;Layout.fillWidth:true}
                    Text {text:root.shown(root.metrics.memoryUsed,"")+" / "+root.shown(root.metrics.memoryTotal," GiB");color:Theme.ink;font.pixelSize:12}
                }
                RowLayout {Layout.fillWidth:true
                    Text {text:"Home filesystem";color:Theme.muted;font.pixelSize:12;Layout.fillWidth:true}
                    Text {text:root.shown(root.metrics.diskUsed,"")+" / "+root.shown(root.metrics.diskTotal," GiB");color:Theme.ink;font.pixelSize:12}
                }
                RowLayout {Layout.fillWidth:true
                    Text {text:"Uptime";color:Theme.muted;font.pixelSize:12;Layout.fillWidth:true}
                    Text {text:root.shown(root.metrics.uptime," hours");color:Theme.ink;font.pixelSize:12}
                }
                Rectangle {Layout.fillWidth:true;height:1;color:Theme.line}
                Text {text:"SENSORS";color:Theme.brass;font.pixelSize:10;font.letterSpacing:1.4}
                Repeater {
                    model:(root.metrics.temperatures || []).concat(root.metrics.fans || [])
                    delegate:RowLayout {
                        required property var modelData
                        Layout.fillWidth:true
                        Text {text:modelData.name;textFormat:Text.PlainText;color:Theme.muted;font.pixelSize:12;Layout.fillWidth:true;elide:Text.ElideRight}
                        Text {text:modelData.value+" "+modelData.unit;color:modelData.unit==="°C" && modelData.value>=90 ? Theme.danger : Theme.ink;font.pixelSize:12}
                    }
                }
                Text {visible:!(root.metrics.temperatures || []).length;text:"No readable temperature sensors";color:Theme.muted;font.pixelSize:12}
                Text {visible:!!root.metrics.error;text:root.metrics.error || "";color:Theme.danger;font.pixelSize:12;Layout.fillWidth:true;wrapMode:Text.WordWrap;textFormat:Text.PlainText}
            }
        }
        Text {text:"Sleeping graphics cards stay asleep.";color:Theme.muted;font.pixelSize:10}
    }
}
