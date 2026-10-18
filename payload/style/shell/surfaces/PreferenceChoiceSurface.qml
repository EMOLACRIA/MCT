import QtQuick
import "../ui"
import QtQuick.Controls
ComboBox {
    id:control
    required property var choices
    required property string selection
    signal chosen(string id)
    onVisibleChanged:if(!visible)popup.close()
    model:choices;textRole:"name";valueRole:"id"
    currentIndex:choices.findIndex(c=>c.id===selection)
    displayText:currentIndex<0 ? selection : currentText
    implicitHeight:44;font.family:Theme.bodyFont;font.pixelSize:Theme.fontSize(13)
    onActivated:index=> {if(choices[index])chosen(choices[index].id);}
    contentItem:Text {text:control.displayText;leftPadding:12;rightPadding:30;verticalAlignment:Text.AlignVCenter;elide:Text.ElideRight;color:Theme.ink;font:control.font}
    indicator:Glyph {symbol:"chevron";x:control.width-width-10;anchors.verticalCenter:parent.verticalCenter;width:18;height:18}
    background:Rectangle {color:Theme.raised;border.color:control.activeFocus ? Theme.brass : Theme.line}
    delegate:ItemDelegate {
        required property var modelData
        required property int index
        width:control.width;height:42
        contentItem:Text {text:modelData.name;elide:Text.ElideRight;color:Theme.ink;font:control.font;verticalAlignment:Text.AlignVCenter}
        background:Rectangle {color:control.highlightedIndex===index ? Theme.raised : Theme.background}
    }
    popup:Popup {
        y:control.height;width:control.width;padding:4
        implicitHeight:Math.min(230,list.contentHeight+8)
        background:Rectangle {color:Theme.background;border.color:Theme.line}
        contentItem:ListView {id:list;clip:true;implicitHeight:contentHeight;model:control.popup.visible ? control.delegateModel : null;currentIndex:control.highlightedIndex;ScrollBar.vertical:ScrollBar {}}
    }
}
