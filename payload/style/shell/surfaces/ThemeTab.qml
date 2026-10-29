import QtQuick
import "../ui"
import QtQuick.Controls
import QtQuick.Layouts
// Overrides for the active theme only: wallpaper, the lock/Fastfetch line and colours.
// The approved package never changes; "Reset theme" returns to it.
ColumnLayout {
    id:root
    required property var model
    property string editing:""
    spacing:10

    // Renders the line for Fastfetch in this theme's own display font, then applies.
    function apply() {
        const m=model;
        if(!m.canApply)return;
        const needs=!m.ephemeral && m.entry.quote && m.quoteImagePath!=="";
        if(!needs) {m.apply(false);return;}
        quoteRender.lines=m.entry.quote;quoteRender.color="#"+m.color("accent").slice(-6);
        Qt.callLater(()=>quoteRender.grabToImage(result=>m.apply(result.saveToFile(m.quoteImagePath)),Qt.size(1536,1280)));
    }
    function luminance(c) {const f=v=>v<=.03928 ? v/12.92 : Math.pow((v+.055)/1.055,2.4);return .2126*f(c.r)+.7152*f(c.g)+.0722*f(c.b);}
    function contrast(a,b) {const x=luminance(a),y=luminance(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05);}
    readonly property real textContrast:contrast(Qt.color(model.color("text")),Qt.color(model.color("surface")))

    // Text fields keep what is typed; refresh them when the draft is replaced (discard, reset, reload).
    Connections {
        target:root.model
        function onDraftChanged() {
            if(!first.activeFocus && !second.activeFocus) {first.text=root.model.quoteLines[0] || "";second.text=root.model.quoteLines[1] || "";}
            if(root.editing!=="" && !hexField.activeFocus)hexField.text="#"+root.model.color(root.editing).slice(-6).toUpperCase();
        }
    }
    onEditingChanged:if(editing!=="")hexField.text="#"+model.color(editing).slice(-6).toUpperCase()
    component Section: Text {font.family:Theme.bodyFont;color:Theme.brass;font.pixelSize:Theme.fontSize(11);font.letterSpacing:1.2}
    component Field: TextField {
        Layout.fillWidth:true;implicitHeight:38;font.family:Theme.bodyFont;font.pixelSize:Theme.fontSize(13);color:Theme.ink
        leftPadding:10;placeholderTextColor:Theme.muted
        background:Rectangle {color:Theme.inputSurface;border.color:parent.activeFocus ? Theme.brass : Theme.line}
    }
    component Swatch: Item {
        id:sw
        required property string role
        readonly property color value:root.model.color(role)
        readonly property bool changed:root.model.isChanged(role)
        Layout.fillWidth:true;implicitHeight:34
        Row {
            spacing:8
            Rectangle {width:30;height:30;color:sw.value;border.width:root.editing===sw.role ? 2 : 1;border.color:root.editing===sw.role ? Theme.ink : Theme.line
                Rectangle {visible:sw.changed;width:8;height:8;radius:4;color:Theme.brass;anchors.right:parent.right;anchors.top:parent.top;anchors.margins:-3}}
            Column {
                Text {font.family:Theme.bodyFont;text:root.model.roleLabels[sw.role];color:Theme.ink;font.pixelSize:Theme.fontSize(12)}
                Text {font.family:"monospace";text:"#"+root.model.color(sw.role).slice(-6).toUpperCase()+(sw.value.a<.995 ? " · "+Math.round(sw.value.a*100)+"%" : "");color:Theme.muted;font.pixelSize:Theme.fontSize(10)}
            }
        }
        MouseArea {objectName:"swatch-"+sw.role;anchors.fill:parent;cursorShape:Qt.PointingHandCursor;onClicked:root.editing=root.editing===sw.role ? "" : sw.role}
    }

    // Off-screen render target for the Fastfetch image (1536×1280, transparent).
    Item {
        width:0;height:0;clip:true
        Item {
            id:quoteRender;objectName:"quoteRender"
            width:1536;height:1280
            property var lines:[]
            property color color:Theme.brass
            TextMetrics {id:widest;font.family:Theme.displayFont;font.pixelSize:190
                text:quoteRender.lines.reduce((a,b)=>a.length>=b.length ? a : b,"")}
            readonly property real size:Math.min(190,190*1400/Math.max(1,widest.advanceWidth))
            Column {
                anchors.centerIn:parent
                Repeater {model:quoteRender.lines
                    Text {required property string modelData;anchors.horizontalCenter:parent.horizontalCenter;text:modelData;textFormat:Text.PlainText;color:quoteRender.color;font.family:Theme.displayFont;font.pixelSize:quoteRender.size}}
            }
        }
    }

    Flickable {
        objectName:"themeScroll"
        Layout.fillWidth:true;Layout.fillHeight:true;clip:true;contentHeight:body.implicitHeight;boundsBehavior:Flickable.StopAtBounds
        ScrollBar.vertical:ScrollBar {}
        ColumnLayout {
            id:body;width:parent.width-14;spacing:10
            enabled:root.model.ready && !root.model.busy && root.model.active!==null
            Section {text:"WALLPAPER"}
            RowLayout {
                spacing:16
                Rectangle {
                    Layout.preferredWidth:176;Layout.preferredHeight:99;color:Theme.inputSurface;border.color:Theme.line
                    Image {
                        id:thumb;anchors.fill:parent;anchors.margins:1;fillMode:Image.PreserveAspectCrop;asynchronous:true;cache:false
                        readonly property bool custom:!!(root.model.entry.wallpaper && root.model.customWallpaper!=="")
                        readonly property string file:custom ? root.model.customWallpaper : root.model.wallpaper
                        source:file==="" ? "" : "file://"+file+"#"+root.model.wallpaperRevision
                        sourceSize.width:352
                    }
                }
                ColumnLayout {
                    spacing:8;Layout.fillWidth:true
                    Text {font.family:Theme.bodyFont;text:thumb.custom ? "Your image" : "Theme wallpaper";color:Theme.ink;font.pixelSize:Theme.fontSize(13)}
                    Row {spacing:6
                        ActionButton {objectName:"pickWallpaper";text:"Choose image…";onClicked:root.model.pick()}
                        ActionButton {objectName:"defaultWallpaper";text:"Use theme default";enabled:!!root.model.entry.wallpaper;onClicked:root.model.setWallpaper(false,false)}
                    }
                    RowLayout {
                        Layout.fillWidth:true;spacing:6
                        Field {id:pathField;objectName:"wallpaperPath";placeholderText:"or paste a PNG/JPEG path";onAccepted:root.model.importWallpaper(text)}
                        ActionButton {text:"Use";enabled:pathField.text!=="";onClicked:root.model.importWallpaper(pathField.text)}
                    }
                    Row {spacing:6;visible:!!root.model.entry.wallpaper
                        ActionButton {objectName:"wallpaperDesktop";text:"Desktop";selected:!!root.model.entry.wallpaper && root.model.entry.wallpaper.desktop
                            onClicked:root.model.setWallpaper(!root.model.entry.wallpaper.desktop,root.model.entry.wallpaper.lock)}
                        ActionButton {objectName:"wallpaperLock";text:"Lock screen";selected:!!root.model.entry.wallpaper && root.model.entry.wallpaper.lock
                            onClicked:root.model.setWallpaper(root.model.entry.wallpaper.desktop,!root.model.entry.wallpaper.lock)}
                    }
                    Text {font.family:Theme.bodyFont;Layout.fillWidth:true;wrapMode:Text.WordWrap;color:Theme.muted;font.pixelSize:Theme.fontSize(11)
                        text:"The image is copied into your MCT settings. Sign-in screen keeps the theme wallpaper for now."}
                }
            }
            Rectangle {Layout.fillWidth:true;height:1;color:Theme.line}
            Section {text:root.model.lockQuote ? "LINE · LOCK SCREEN AND FASTFETCH" : "LINE · FASTFETCH"}
            RowLayout {
                spacing:16;Layout.fillWidth:true
                ColumnLayout {
                    Layout.preferredWidth:270;Layout.maximumWidth:270;spacing:6
                    Field {id:first;objectName:"quoteFirst";maximumLength:root.model.quoteMax;text:root.model.quoteLines[0] || ""
                        onTextEdited:root.model.setQuote(text,second.text)}
                    Field {id:second;objectName:"quoteSecond";maximumLength:root.model.quoteMax;text:root.model.quoteLines[1] || ""
                        onTextEdited:root.model.setQuote(first.text,text)}
                    Text {font.family:Theme.bodyFont;text:root.model.quoteProblem || "Two rows, up to "+root.model.quoteMax+" characters each";color:root.model.quoteProblem ? Theme.danger : Theme.muted;font.pixelSize:Theme.fontSize(11);Layout.fillWidth:true;wrapMode:Text.WordWrap}
                }
                Rectangle {
                    Layout.fillWidth:true;Layout.preferredHeight:84;color:Theme.inputSurface;border.color:Theme.line;clip:true
                    Column {anchors.centerIn:parent
                        Repeater {model:root.model.quoteLines
                            Text {required property string modelData;anchors.horizontalCenter:parent.horizontalCenter;text:modelData;textFormat:Text.PlainText;color:root.model.color("accent");font.family:Theme.displayFont;font.pixelSize:Theme.fontSize(21)}}
                    }
                }
            }
            Rectangle {Layout.fillWidth:true;height:1;color:Theme.line}
            RowLayout {
                Layout.fillWidth:true
                Section {text:"COLOURS";Layout.fillWidth:true}
                Text {font.family:Theme.bodyFont;text:"Text on surface "+root.textContrast.toFixed(1)+":1"+(root.textContrast<4.5 ? " · low contrast" : " · readable")
                    color:root.textContrast<4.5 ? Theme.danger : Theme.muted;font.pixelSize:Theme.fontSize(11)}
            }
            GridLayout {
                Layout.fillWidth:true;columns:4;rowSpacing:10;columnSpacing:10
                Repeater {model:root.model.roles;Swatch {required property string modelData;role:modelData}}
            }
            // Editor for the selected colour: hex, plus opacity where the role allows it.
            RowLayout {
                visible:root.editing!=="";Layout.fillWidth:true;spacing:8
                readonly property string current:root.editing==="" ? String(Theme.ink) : root.model.color(root.editing)
                readonly property bool alpha:root.model.alphaRoles.indexOf(root.editing)>=0
                Text {font.family:Theme.bodyFont;text:root.editing==="" ? "" : root.model.roleLabels[root.editing];color:Theme.ink;font.pixelSize:Theme.fontSize(12);Layout.preferredWidth:76}
                Field {
                    id:hexField;objectName:"colorHex";Layout.preferredWidth:112;Layout.fillWidth:false;font.family:"monospace"
                    text:"#"+parent.current.slice(-6).toUpperCase();maximumLength:7
                    validator:RegularExpressionValidator {regularExpression:/#?[0-9A-Fa-f]{0,6}/}
                    onTextEdited:if(/^#?[0-9A-Fa-f]{6}$/.test(text))root.model.setColor(root.editing,(parent.alpha && parent.current.length===9 ? "#"+parent.current.slice(1,3) : "#")+text.replace("#","").toLowerCase())
                }
                PreferenceSlider {
                    visible:parent.alpha;Layout.fillWidth:true;label:"Opacity";from:10;to:100
                    value:parent.current.length===9 ? Math.round(parseInt(parent.current.slice(1,3),16)/2.55) : 100
                    onChosen:value=> {const a=("0"+Math.round(value*2.55).toString(16)).slice(-2);root.model.setColor(root.editing,(value>=100 ? "#" : "#"+a)+parent.current.slice(-6));}
                }
                Item {Layout.fillWidth:!parent.alpha}
                ActionButton {text:"Reset";enabled:root.model.isChanged(root.editing);onClicked:root.model.setColor(root.editing,"")}
            }
            Text {font.family:Theme.bodyFont;Layout.fillWidth:true;wrapMode:Text.WordWrap;color:Theme.muted;font.pixelSize:Theme.fontSize(11)
                text:"All colours change the desktop shell. The accent also reaches window borders, Kitty, the lock screen, Fastfetch, Dolphin and Spotify. Dolphin text always stays white."}
            RowLayout {
                ActionButton {objectName:"resetThemeConfig";text:"Reset theme";enabled:root.model.changeCount>0 && root.model.entry && Object.keys(root.model.entry).length>0;onClicked: {root.editing="";root.model.resetTheme();}}
                Text {font.family:Theme.bodyFont;text:"Returns this theme to its approved look (after Apply).";color:Theme.muted;font.pixelSize:Theme.fontSize(11)}
            }
            Text {font.family:Theme.bodyFont;Layout.fillWidth:true;wrapMode:Text.WordWrap;visible:text!=="";color:root.model.lastApply && !root.model.lastApply.ok ? Theme.danger : Theme.muted;font.pixelSize:Theme.fontSize(11)
                text:root.model.lastApply ? "Last apply "+root.model.lastApply.time+": "+root.model.lastApply.message : ""}
        }
    }
}
