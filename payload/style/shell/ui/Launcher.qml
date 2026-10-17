import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
Item {
    id: root
    required property var backend
    required property var uiState
    readonly property var entries: {
        const terms=uiState.search.trim().toLocaleLowerCase().split(/\s+/).filter(t=>t.length);
        return backend.applications.filter(a=>terms.every(t=>(a.name+" "+a.comment).toLocaleLowerCase().indexOf(t)>=0));
    }
    function activate() { searchField.forceActiveFocus(); }
    function openSelected() { if(appList.currentIndex>=0 && entries[appList.currentIndex]) { backend.launchApplication(entries[appList.currentIndex].id); uiState.close(); } }
    ColumnLayout {
        anchors.fill:parent; spacing:18
        RowLayout {
            Glyph { symbol:"search"; width:25; height:25 }
            Text { text:"Search"; color:Theme.ink; font.family:Theme.displayFont; font.pixelSize:26; Layout.fillWidth:true }
            ActionButton { symbol:"close"; width:36; height:36; padding:8; onClicked:uiState.close() }
        }
        TextField {
            id:searchField; objectName:"applicationSearch"; Layout.fillWidth:true; implicitHeight:48
            text:uiState.search; onTextChanged:if(uiState.search!==text)uiState.search=text
            placeholderText:"Type to search applications…"; placeholderTextColor:Theme.muted
            color:Theme.ink; selectionColor:Theme.line; font.pixelSize:15; leftPadding:14
            background:Rectangle { color:"#242620"; border.width:1; border.color:searchField.activeFocus ? Theme.brass : Theme.line }
            Keys.onDownPressed: { appList.currentIndex=Math.min(appList.count-1,appList.currentIndex+1); appList.positionViewAtIndex(appList.currentIndex,ListView.Contain); }
            Keys.onUpPressed: { appList.currentIndex=Math.max(0,appList.currentIndex-1); appList.positionViewAtIndex(appList.currentIndex,ListView.Contain); }
            Keys.onReturnPressed:root.openSelected()
            Keys.onEnterPressed:root.openSelected()
        }
        ListView {
            id:appList; objectName:"applicationList"; Layout.fillHeight:true; Layout.fillWidth:true
            clip:true; model:root.entries; currentIndex:count ? 0 : -1; spacing:5
            onCountChanged:currentIndex=count ? 0 : -1
            ScrollBar.vertical:ScrollBar {}
            delegate: Item {
                id:appRow; required property var modelData; required property int index
                width:appList.width; height:60
                Rectangle { anchors.fill:parent; color:appRow.index===appList.currentIndex ? Theme.raised : "transparent"; border.width:1; border.color:appRow.index===appList.currentIndex ? Theme.line : "transparent" }
                Image { id:appIcon; x:14; anchors.verticalCenter:parent.verticalCenter; width:27; height:27; source:appRow.modelData.icon; fillMode:Image.PreserveAspectFit }
                Glyph { x:18; anchors.verticalCenter:parent.verticalCenter; visible:appIcon.status!==Image.Ready; symbol:"tree" }
                Column {
                    x:57; anchors.verticalCenter:parent.verticalCenter; width:parent.width-78; spacing:5
                    Text { width:parent.width; text:appRow.modelData.name; textFormat:Text.PlainText; elide:Text.ElideRight; color:Theme.ink; font.pixelSize:14 }
                    Text { width:parent.width; text:appRow.modelData.comment; textFormat:Text.PlainText; elide:Text.ElideRight; color:Theme.muted; font.pixelSize:11; visible:text.length>0 }
                }
                MouseArea { anchors.fill:parent; hoverEnabled:true; onEntered:appList.currentIndex=appRow.index; onClicked: {appList.currentIndex=appRow.index;root.openSelected();} }
            }
            Text { anchors.centerIn:parent; visible:appList.count===0; text:"No matching applications"; color:Theme.muted; font.pixelSize:14 }
        }
        RowLayout {
            Text { text:root.entries.length + " results"; color:Theme.muted; font.pixelSize:10; Layout.fillWidth:true }
            Text { text:"↑ ↓ Select    Enter Open    Esc Close"; color:Theme.brass; font.pixelSize:10 }
        }
    }
}
