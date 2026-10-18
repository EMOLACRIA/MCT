import QtQuick
import QtQuick.Controls
OrnamentFrame {
    id:root
    objectName:"partyStrip"
    required property var backend
    required property var uiState
    property string screenToken:""
    readonly property var cpu:backend.hardware || ({})
    readonly property var cells:[
        {name:"SYSTEM",portrait:Theme.kris,ink:Theme.brass,panel:"hardware",
         value:typeof cpu.cpuTemp==="number" && isFinite(cpu.cpuTemp) ? Math.round(cpu.cpuTemp)+"°C" : "TEMP —",
         level:typeof cpu.cpuUsage==="number" ? cpu.cpuUsage : 0},
        {name:"AUDIO",portrait:Theme.susie,ink:Theme.partyPink,panel:"controls",
         value:!backend.audioAvailable ? "OFFLINE" : backend.muted ? "MUTED" : backend.volume+"%",
         level:backend.audioAvailable && !backend.muted ? backend.volume : 0},
        {name:"POWER",portrait:Theme.ralsei,ink:Theme.partyGreen,panel:"controls",
         value:backend.battery<0 ? "AC" : backend.battery+"%"+(backend.batteryCharging ? " +" : ""),
         level:backend.battery<0 ? 0 : backend.battery}
    ]
    Row {
        anchors.fill:parent;anchors.margins:8
        Repeater {
            model:root.cells
            delegate:AbstractButton {
                id:cell
                required property var modelData
                required property int index
                objectName:"partyCell-"+index
                width:(root.width-16)/3;height:root.height-16
                hoverEnabled:true;activeFocusOnTab:true
                Accessible.name:modelData.name+" "+modelData.value
                background:Rectangle {color:cell.hovered || cell.activeFocus ? Theme.raised : "transparent"}
                contentItem:Item {
                    Image {x:4;anchors.verticalCenter:parent.verticalCenter;width:32;height:32;smooth:false;fillMode:Image.PreserveAspectFit;source:cell.modelData.portrait;visible:cell.width>=150}
                    Column {
                        x:cell.width>=150 ? 48 : 7;y:3;width:parent.width-x-10;spacing:4
                        Text {width:parent.width;text:cell.modelData.name;color:cell.modelData.ink;font.family:Theme.bodyFont;font.pixelSize:Theme.fontSize(11);elide:Text.ElideRight}
                        Text {objectName:"partyValue-"+cell.index;width:parent.width;text:cell.modelData.value;color:Theme.ink;font.family:Theme.bodyFont;font.pixelSize:Theme.fontSize(11);elide:Text.ElideRight}
                        Rectangle {width:parent.width;height:3;color:Theme.line
                            Rectangle {width:parent.width*Math.max(0,Math.min(100,cell.modelData.level))/100;height:3;color:cell.modelData.ink}
                        }
                    }
                    Rectangle {visible:cell.index>0;width:1;height:parent.height;x:0;color:cell.modelData.ink;opacity:.6}
                }
                onClicked:root.uiState.toggle(modelData.panel,root.screenToken)
            }
        }
    }
}
