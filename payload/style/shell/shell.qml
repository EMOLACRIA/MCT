//@ pragma UseQApplication
import QtQuick
import Quickshell
import Quickshell.Io
import Quickshell.Wayland
import "ui"

ShellRoot {
    id:root
    LiveContext { id:services; hardwareMonitoring:shellState.activePanel==="hardware" }
    UiState { id:shellState }
    readonly property var focusedScreen:Quickshell.screens.find(s=>s.name===services.focusedScreenName) || Quickshell.screens[0] || null
    readonly property var panelScreen:Quickshell.screens.find(s=>s.name===shellState.screenName) || focusedScreen
    Connections { target:services; function onFeedbackRequested(kind,level,muted) {shellState.showFeedback(kind,level,muted);} }
    IpcHandler {
        target:"desktop"
        function ping():string {return services.ready ? "ready" : "starting";}
        function pid():int {return Quickshell.processId;}
        function toggle(panel:string):void {shellState.toggle(panel,services.focusedScreenName);}
        function mediaInfo():string {return JSON.stringify({title:services.mediaTitle,artist:services.mediaArtist,art:services.mediaArt,playing:services.mediaPlaying});}
        function mediaControl(action:string):void {services.mediaCommand(action);}
        function close():void {shellState.close();}
        function error(message:string):void {services.lastError=message;if(shellState.activePanel!=="controls")shellState.toggle("controls",services.focusedScreenName);}
    }
    IpcHandler {
        target:"feedback"
        function ping():string {return "ready";}
        function present(kind:string,level:int,muted:bool):void {shellState.showFeedback(kind,level,muted);}
    }
    Variants {
        model:Quickshell.screens
        PanelWindow {
            id:barWindow
            required property var modelData
            screen:modelData
            anchors {top:true;left:true;right:true}
            margins {top:10;left:16;right:16}
            implicitHeight:48; exclusiveZone:60; color:"transparent"
            WlrLayershell.layer:WlrLayer.Top
            WlrLayershell.namespace:"desktop-bar"
            Bar { anchors.fill:parent; backend:services; uiState:shellState; screenToken:barWindow.modelData.name; nativeWindow:barWindow }
        }
    }
    PanelWindow {
        visible:shellState.activePanel!=="" && root.panelScreen!==null
        screen:root.panelScreen; anchors {top:true;bottom:true;left:true;right:true}
        color:"transparent"; exclusionMode:ExclusionMode.Ignore; focusable:true
        WlrLayershell.layer:WlrLayer.Overlay
        WlrLayershell.namespace:"desktop-panels"
        Overlay { anchors.fill:parent; backend:services; uiState:shellState }
    }
    PanelWindow {
        visible:shellState.feedbackVisible && root.focusedScreen!==null
        screen:root.focusedScreen; anchors.bottom:true; margins.bottom:80
        implicitWidth:370; implicitHeight:100; color:"transparent"
        exclusionMode:ExclusionMode.Ignore; focusable:false
        WlrLayershell.layer:WlrLayer.Overlay
        WlrLayershell.namespace:"desktop-feedback"
        Feedback { anchors.fill:parent; uiState:shellState; backend:services }
    }
    PanelWindow {
        visible:services.toasts.length>0 && shellState.activePanel==="" && root.focusedScreen!==null
        screen:root.focusedScreen
        anchors {top:true;right:true}
        margins {top:76;right:16}
        implicitWidth:390; implicitHeight:toastColumn.implicitHeight; color:"transparent"
        exclusionMode:ExclusionMode.Ignore; focusable:false
        WlrLayershell.layer:WlrLayer.Overlay
        WlrLayershell.namespace:"desktop-notifications"
        Column {
            id:toastColumn; width:parent.width; spacing:10
            Repeater { model:services.toasts; delegate:Toast { required property var modelData; width:toastColumn.width; height:implicitHeight; note:modelData; backend:services } }
        }
    }
}
