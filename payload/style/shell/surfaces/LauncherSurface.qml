import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../ui"
import "../behavior"
LauncherController {
    id:root
    property int rowSpacing:18
    property int applicationRowHeight:60
    onFocusRequested:searchField.forceActiveFocus()
    ColumnLayout {
        anchors.fill:parent; spacing:root.rowSpacing
        PanelHeader {title:"Search";symbol:"search";onClosed:uiState.close()}
        TextField {
            id:searchField; objectName:"applicationSearch"; Layout.fillWidth:true; implicitHeight:48
            text:uiState.search; onTextChanged:if(uiState.search!==text)uiState.search=text
            placeholderText:"Search apps or calculate…"; placeholderTextColor:Theme.muted
            color:Theme.ink; selectionColor:Theme.line; font.family:Theme.bodyFont; font.pixelSize:Theme.fontSize(15); leftPadding:14
            background:Rectangle { color:Theme.inputSurface; border.width:1; border.color:searchField.activeFocus ? Theme.brass : Theme.line }
            Keys.onDownPressed:root.moveSelection(1)
            Keys.onUpPressed:root.moveSelection(-1)
            Keys.onReturnPressed:event=> {if(event.modifiers & Qt.ControlModifier)root.copyResult();else root.openSelected();}
            Keys.onEnterPressed:event=> {if(event.modifiers & Qt.ControlModifier)root.copyResult();else root.openSelected();}
        }
        Text { font.family:Theme.bodyFont;
            objectName:"calculationMessage";Layout.fillWidth:true
            visible:root.calculation.state==="incomplete" || root.calculation.state==="error"
            text:root.calculation.message;wrapMode:Text.WordWrap;font.pixelSize:Theme.fontSize(12)
            color:root.calculation.state==="error" ? Theme.danger : Theme.muted
        }
        ListView {
            id:appList; objectName:"applicationList"; Layout.fillHeight:true; Layout.fillWidth:true
            clip:true; model:root.entries; currentIndex:root.selectedIndex; spacing:5
            onCurrentIndexChanged:if(currentIndex>=0)positionViewAtIndex(currentIndex,ListView.Contain)
            ScrollBar.vertical:ScrollBar {}
            delegate: Item {
                id:appRow; required property var modelData; required property int index
                readonly property bool result:modelData.kind==="calculation"
                objectName:result ? "calculationRow" : "applicationRow"
                width:appList.width; height:result ? 112 : root.applicationRowHeight
                Rectangle { anchors.fill:parent; color:appRow.index===appList.currentIndex ? Theme.raised : "transparent"; border.width:1; border.color:appRow.index===appList.currentIndex ? appRow.result ? Theme.brass : Theme.line : "transparent" }
                Image { id:appIcon; x:14; anchors.verticalCenter:parent.verticalCenter; width:27; height:27; visible:!appRow.result; source:appRow.modelData.icon || ""; fillMode:Image.PreserveAspectFit }
                Glyph { x:18; anchors.verticalCenter:parent.verticalCenter; visible:appRow.result || appIcon.status!==Image.Ready; symbol:appRow.result ? "calculator" : Theme.applicationSymbol(appRow.modelData.name) }
                Column {
                    x:57; anchors.verticalCenter:parent.verticalCenter; width:Math.max(0,parent.width-(appRow.result ? 165 : 78)); spacing:5
                    Text { font.family:Theme.bodyFont; visible:appRow.result;width:parent.width;text:"Calculation";color:Theme.brass;font.pixelSize:Theme.fontSize(11)}
                    Text { font.family:Theme.bodyFont; objectName:appRow.result ? "calculationValue" : "applicationName";width:parent.width;text:appRow.modelData.name;textFormat:Text.PlainText;elide:Text.ElideRight;color:Theme.ink;font.pixelSize:Theme.fontSize(appRow.result ? 29 : 14)}
                    Text { font.family:Theme.bodyFont;
                        width:parent.width;text:appRow.result ? root.uiState.search.indexOf("%")>=0 ? "% divides by 100" : "Enter to copy result" : appRow.modelData.comment || ""
                        textFormat:Text.PlainText;elide:Text.ElideRight;color:Theme.muted;font.pixelSize:Theme.fontSize(11);visible:text.length>0
                    }
                }
                MouseArea { anchors.fill:parent; hoverEnabled:true; onEntered:root.selectedIndex=appRow.index; onClicked: {root.selectedIndex=appRow.index;root.openSelected();} }
                ActionButton {
                    objectName:"copyCalculation";visible:appRow.result;text:root.copiedText===root.calculation.text && root.copiedText!=="" ? "Copied" : "Copy"
                    anchors.right:parent.right;anchors.rightMargin:12;anchors.verticalCenter:parent.verticalCenter
                    implicitWidth:84;onClicked:root.copyResult()
                }
            }
            Text { font.family:Theme.bodyFont; anchors.centerIn:parent; visible:appList.count===0 && root.calculation.state==="none"; text:"No matching applications"; color:Theme.muted; font.pixelSize:Theme.fontSize(14)}
        }
        RowLayout {
            Text { font.family:Theme.bodyFont; text:root.entries.length+(root.entries.length===1 ? " result" : " results");color:Theme.muted;font.pixelSize:Theme.fontSize(10);Layout.fillWidth:true }
            Text { font.family:Theme.bodyFont;
                text:root.calculation.state==="ready" ? "↑ ↓ Select    Enter Copy / Open\nCtrl+Enter Copy result    Esc Close" : "↑ ↓ Select    Enter Open    Esc Close"
                color:Theme.brass;font.pixelSize:Theme.fontSize(10)
            }
        }
    }
}
