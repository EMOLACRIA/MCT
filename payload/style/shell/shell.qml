//@ pragma UseQApplication
import QtQuick
import Quickshell
import Quickshell.Io
import Quickshell.Wayland
import Quickshell.Hyprland
import "ui"

ShellRoot {
    id:root
    LiveContext { id:services; hardwareMonitoring:shellState.activePanel==="hardware" || Theme.partyStripEnabled }
    Binding {target:Theme;property:"preferences";value:services.preferences.values}
    UiState { id:shellState;onActivePanelChanged:if(activePanel!=="")switcher.cancel() }
    WindowSwitcherState {
        id:switcher;windows:services.windows;activeWindowId:services.activeWindowId
        onCommitted:windowId=>services.activateWindow(windowId)
    }
    function cycleWindows(direction) {
        shellState.close();
        if(!switcher.active)services.refreshWindows();
        switcher.begin(direction,root.focusedScreen ? root.focusedScreen.name : "");
    }
    GlobalShortcut {appid:"desktop-style";name:"window-next";description:"Next window";onPressed:root.cycleWindows(1)}
    GlobalShortcut {appid:"desktop-style";name:"window-previous";description:"Previous window";onPressed:root.cycleWindows(-1)}
    GlobalShortcut {appid:"desktop-style";name:"window-accept";description:"Accept selected window";onPressed:switcher.commit();onReleased:switcher.commit()}
    readonly property var focusedScreen:Quickshell.screens.find(s=>s.name===services.focusedScreenName) || Quickshell.screens[0] || null
    readonly property var panelScreen:Quickshell.screens.find(s=>s.name===shellState.screenName) || focusedScreen
    readonly property var switcherScreen:Quickshell.screens.find(s=>s.name===switcher.screenName) || null
    onSwitcherScreenChanged:if(switcher.active && !switcherScreen)switcher.cancel()
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
            margins {top:Theme.preferences.barFloating ? SurfaceLayout.barTopMargin : 0;left:Theme.preferences.barFloating ? SurfaceLayout.barSideMargin : 0;right:Theme.preferences.barFloating ? SurfaceLayout.barSideMargin : 0}
            implicitHeight:SurfaceLayout.barHeight; exclusiveZone:Theme.preferences.barFloating ? SurfaceLayout.floatingBarReservedHeight : SurfaceLayout.barHeight; color:"transparent"
            WlrLayershell.layer:WlrLayer.Top
            WlrLayershell.namespace:"desktop-bar"
            Bar { anchors.fill:parent; backend:services; uiState:shellState; screenToken:barWindow.modelData.name; nativeWindow:barWindow;hintPopup:nativeHint }
        }
    }
    Component {id:nativeHint;HintPopup {}}
    Variants {
        model:Theme.partyStripEnabled ? Quickshell.screens : []
        PanelWindow {
            id:partyWindow
            required property var modelData
            screen:modelData
            anchors {bottom:true}
            margins {bottom:8}
            implicitWidth:Math.min(660,Math.max(250,modelData.width-32))
            implicitHeight:64
            exclusiveZone:80
            color:"transparent"
            WlrLayershell.layer:WlrLayer.Top
            WlrLayershell.namespace:"desktop-party"
            PartyStrip {anchors.fill:parent;backend:services;uiState:shellState;screenToken:partyWindow.modelData.name}
        }
    }
    PanelWindow {
        visible:switcher.active && root.switcherScreen!==null
        screen:root.switcherScreen;anchors {top:true;bottom:true;left:true;right:true}
        color:"transparent";exclusionMode:ExclusionMode.Ignore
        WlrLayershell.layer:WlrLayer.Overlay
        WlrLayershell.keyboardFocus:WlrKeyboardFocus.Exclusive
        WlrLayershell.namespace:"desktop-window-switcher"
        WindowSwitcher {anchors.fill:parent;controller:switcher;previewComponent:windowCaptureView}
    }
    Component {
        id:windowCaptureView
        Item {
            property alias hasContent:stream.hasContent
            ScreencopyView {
                id:stream
                anchors.centerIn:parent
                width:sourceSize.width>0 && sourceSize.height>0 ? Math.min(parent.width,parent.height*sourceSize.width/sourceSize.height) : parent.width
                height:sourceSize.width>0 && sourceSize.height>0 ? Math.min(parent.height,parent.width*sourceSize.height/sourceSize.width) : parent.height
                captureSource:switcher.active ? services.windowCapture(switcher.selectedId) : null
                live:false;paintCursor:false
            }
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
        screen:root.focusedScreen
        anchors {top:Theme.preferences.osdPosition==="top";bottom:Theme.preferences.osdPosition!=="top"}
        margins {top:SurfaceLayout.osdEdgeMargin;bottom:SurfaceLayout.osdEdgeMargin}
        implicitWidth:SurfaceLayout.osdWidth; implicitHeight:SurfaceLayout.osdHeight; color:"transparent"
        exclusionMode:ExclusionMode.Ignore; focusable:false
        WlrLayershell.layer:WlrLayer.Overlay
        WlrLayershell.namespace:"desktop-feedback"
        Feedback { anchors.fill:parent; uiState:shellState; backend:services }
    }
    PanelWindow {
        visible:services.toasts.length>0 && shellState.activePanel==="" && root.focusedScreen!==null
        screen:root.focusedScreen
        anchors {top:true;right:true}
        margins {top:SurfaceLayout.toastTop;right:SurfaceLayout.toastSideMargin}
        implicitWidth:SurfaceLayout.toastWidth; implicitHeight:toastColumn.implicitHeight; color:"transparent"
        exclusionMode:ExclusionMode.Ignore; focusable:false
        WlrLayershell.layer:WlrLayer.Overlay
        WlrLayershell.namespace:"desktop-notifications"
        ToastStack {id:toastColumn;width:parent.width;backend:services}
    }
}
