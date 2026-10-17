import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../logic/Calculator.js" as Calculator
Item {
    id: root
    objectName:"launcher"
    required property var backend
    required property var uiState
    readonly property var calculation:Calculator.calculate(uiState.search)
    property string copiedText:""
    onCalculationChanged: {copiedText="";copyFeedback.stop();}
    readonly property var applications: {
        const terms=uiState.search.trim().toLocaleLowerCase().split(/\s+/).filter(t=>t.length);
        return backend.applications.filter(a=>terms.every(t=>(a.name+" "+a.comment).toLocaleLowerCase().indexOf(t)>=0));
    }
    readonly property var entries: {
        const apps=applications.map(a=>({kind:"application",id:a.id,name:a.name,comment:a.comment,icon:a.icon}));
        return calculation.state==="ready" ? [{kind:"calculation",name:calculation.text}].concat(apps) : apps;
    }
    function activate() { searchField.forceActiveFocus(); }
    function copyResult() {
        if(calculation.state!=="ready")return;
        backend.copyText(calculation.text);copiedText=calculation.text;copyFeedback.restart();activate();
    }
    function openSelected() {
        const entry=entries[appList.currentIndex];if(!entry)return;
        if(entry.kind==="calculation")copyResult();
        else {backend.launchApplication(entry.id);uiState.close();}
    }
    function moveSelection(direction) {
        if(!appList.count)return;
        appList.currentIndex=Math.max(0,Math.min(appList.count-1,appList.currentIndex+direction));
        appList.positionViewAtIndex(appList.currentIndex,ListView.Contain);
    }
    Timer {id:copyFeedback;interval:1600;onTriggered:root.copiedText=""}
    ColumnLayout {
        anchors.fill:parent; spacing:18
        RowLayout {
            Glyph { symbol:"search"; width:25; height:25 }
            Text { text:"Search"; color:Theme.ink; font.family:Theme.displayFont; font.pixelSize:Theme.fontSize(26); Layout.fillWidth:true }
            ActionButton { symbol:"close"; width:36; height:36; padding:8; onClicked:uiState.close() }
        }
        TextField {
            id:searchField; objectName:"applicationSearch"; Layout.fillWidth:true; implicitHeight:48
            text:uiState.search; onTextChanged:if(uiState.search!==text)uiState.search=text
            placeholderText:"Search apps or calculate…"; placeholderTextColor:Theme.muted
            color:Theme.ink; selectionColor:Theme.line; font.pixelSize:Theme.fontSize(15); leftPadding:14
            background:Rectangle { color:"#242620"; border.width:1; border.color:searchField.activeFocus ? Theme.brass : Theme.line }
            Keys.onDownPressed:root.moveSelection(1)
            Keys.onUpPressed:root.moveSelection(-1)
            Keys.onReturnPressed:event=> {if(event.modifiers & Qt.ControlModifier)root.copyResult();else root.openSelected();}
            Keys.onEnterPressed:event=> {if(event.modifiers & Qt.ControlModifier)root.copyResult();else root.openSelected();}
        }
        Text {
            objectName:"calculationMessage";Layout.fillWidth:true
            visible:root.calculation.state==="incomplete" || root.calculation.state==="error"
            text:root.calculation.message;wrapMode:Text.WordWrap;font.pixelSize:Theme.fontSize(12)
            color:root.calculation.state==="error" ? Theme.danger : Theme.muted
        }
        ListView {
            id:appList; objectName:"applicationList"; Layout.fillHeight:true; Layout.fillWidth:true
            clip:true; model:root.entries; currentIndex:count ? 0 : -1; spacing:5
            onModelChanged:currentIndex=root.entries.length ? 0 : -1
            onCountChanged:currentIndex=count ? 0 : -1
            ScrollBar.vertical:ScrollBar {}
            delegate: Item {
                id:appRow; required property var modelData; required property int index
                readonly property bool result:modelData.kind==="calculation"
                objectName:result ? "calculationRow" : "applicationRow"
                width:appList.width; height:result ? 112 : 60
                Rectangle { anchors.fill:parent; color:appRow.index===appList.currentIndex ? Theme.raised : "transparent"; border.width:1; border.color:appRow.index===appList.currentIndex ? appRow.result ? Theme.brass : Theme.line : "transparent" }
                Image { id:appIcon; x:14; anchors.verticalCenter:parent.verticalCenter; width:27; height:27; visible:!appRow.result; source:appRow.modelData.icon || ""; fillMode:Image.PreserveAspectFit }
                Glyph { x:18; anchors.verticalCenter:parent.verticalCenter; visible:appRow.result || appIcon.status!==Image.Ready; symbol:appRow.result ? "calculator" : "tree" }
                Column {
                    x:57; anchors.verticalCenter:parent.verticalCenter; width:Math.max(0,parent.width-(appRow.result ? 165 : 78)); spacing:5
                    Text { visible:appRow.result;width:parent.width;text:"Calculation";color:Theme.brass;font.pixelSize:Theme.fontSize(11)}
                    Text { objectName:appRow.result ? "calculationValue" : "applicationName";width:parent.width;text:appRow.modelData.name;textFormat:Text.PlainText;elide:Text.ElideRight;color:Theme.ink;font.pixelSize:Theme.fontSize(appRow.result ? 29 : 14)}
                    Text {
                        width:parent.width;text:appRow.result ? root.uiState.search.indexOf("%")>=0 ? "% divides by 100" : "Enter to copy result" : appRow.modelData.comment || ""
                        textFormat:Text.PlainText;elide:Text.ElideRight;color:Theme.muted;font.pixelSize:Theme.fontSize(11);visible:text.length>0
                    }
                }
                MouseArea { anchors.fill:parent; hoverEnabled:true; onEntered:appList.currentIndex=appRow.index; onClicked: {appList.currentIndex=appRow.index;root.openSelected();} }
                ActionButton {
                    objectName:"copyCalculation";visible:appRow.result;text:root.copiedText===root.calculation.text && root.copiedText!=="" ? "Copied" : "Copy"
                    anchors.right:parent.right;anchors.rightMargin:12;anchors.verticalCenter:parent.verticalCenter
                    implicitWidth:84;onClicked:root.copyResult()
                }
            }
            Text { anchors.centerIn:parent; visible:appList.count===0 && root.calculation.state==="none"; text:"No matching applications"; color:Theme.muted; font.pixelSize:Theme.fontSize(14)}
        }
        RowLayout {
            Text { text:root.entries.length+(root.entries.length===1 ? " result" : " results");color:Theme.muted;font.pixelSize:Theme.fontSize(10);Layout.fillWidth:true }
            Text {
                text:root.calculation.state==="ready" ? "↑ ↓ Select    Enter Copy / Open\nCtrl+Enter Copy result    Esc Close" : "↑ ↓ Select    Enter Open    Esc Close"
                color:Theme.brass;font.pixelSize:Theme.fontSize(10)
            }
        }
    }
}
