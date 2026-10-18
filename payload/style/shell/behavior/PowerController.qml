import QtQuick
Item {
    id:root
    required property var backend
    required property var uiState
    property int selectedIndex:0
    readonly property var actions: [
        {code:"lock",name:"Lock",symbol:"lock",detail:"Keep your session running"},
        {code:"suspend",name:"Suspend",symbol:"moon",detail:"Put the computer to sleep"},
        {code:"logout",name:"Log out",symbol:"logout",detail:"Return to the sign-in screen"},
        {code:"restart",name:"Restart",symbol:"restart",detail:"Restart the computer"},
        {code:"poweroff",name:"Power off",symbol:"power",detail:"Shut down the computer"}
    ]
    function activate() { root.forceActiveFocus(); selectedIndex=0; }
    function choose(code) { if(["logout","restart","poweroff"].indexOf(code)>=0)uiState.confirmation=code; else {backend.sessionAction(code);uiState.close();} }
    function confirm() { const code=uiState.confirmation;uiState.close();backend.sessionAction(code); }
    Keys.onUpPressed:selectedIndex=Math.max(0,selectedIndex-1)
    Keys.onDownPressed:selectedIndex=Math.min(4,selectedIndex+1)
    Keys.onReturnPressed:if(!uiState.confirmation)choose(actions[selectedIndex].code)
    Keys.onEnterPressed:if(!uiState.confirmation)choose(actions[selectedIndex].code)
}
